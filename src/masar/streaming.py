"""Native Kafka -> Structured Streaming -> Delta Lab 05.

Requires actual services; no file-source fallback. Local, single-broker teaching
configuration only. A complete invocation gets its own topic and checkpoint;
restart tests within that invocation reuse the SAME checkpoint and target.
"""
from __future__ import annotations
import importlib.metadata
import json
import os
import re
import socket
import uuid
from collections import Counter
from pathlib import Path
from masar.runtime import EnvironmentUnavailable
from masar.workspace import (DATASET_MANIFEST_SHA256, workspace_path, write_json,
                             require_fixed_dataset, digest_file, rows_digest)
from masar.trust_reference import GPS_FILES, day04_reference, unique_events

KAFKA_CLIENT_VERSION = '2.2.15'
BOOTSTRAP = '127.0.0.1:9092'

def bootstrap_address() -> str:
    value = os.environ.get('MASAR_KAFKA_BOOTSTRAP', BOOTSTRAP)
    if value not in {'127.0.0.1:9092', 'kafka:29092'}:
        raise ValueError('Only the local host or the course Compose Kafka endpoint is allowed')
    return value

KAFKA_SPARK_PACKAGE = 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8'


def stream_preflight() -> dict:
    try:
        observed = importlib.metadata.version('kafka-python')
    except importlib.metadata.PackageNotFoundError:
        observed = None
    endpoint = bootstrap_address()
    host, port = endpoint.rsplit(':', 1)
    listening = False
    try:
        with socket.create_connection((host,int(port)), timeout=2): listening=True
    except OSError:
        pass
    issues = []
    if observed != KAFKA_CLIENT_VERSION: issues.append('kafka-python pinned version is not installed')
    if not listening: issues.append('Course Kafka endpoint ' + endpoint + ' is not listening')
    return {'scope':'LOCAL_DEPENDENCY_CHECK_ONLY','kafka_executed':False,
            'client_required':KAFKA_CLIENT_VERSION,'client_observed':observed,
            'bootstrap_servers':endpoint,'tcp_listening':listening,'issues':issues}


def validate_topic(topic: str) -> str:
    if not isinstance(topic,str) or not re.fullmatch(r'masar-day04-[0-9a-f]{32}',topic):
        raise ValueError('Only a newly allocated course topic is allowed')
    return topic


def create_topic(topic: str) -> None:
    validate_topic(topic)
    from kafka.admin import KafkaAdminClient, NewTopic
    admin = KafkaAdminClient(bootstrap_servers=bootstrap_address(), client_id='masar-admin',
                             request_timeout_ms=15000, api_version_auto_timeout_ms=8000)
    try:
        # No implicit reuse, delete, or offset reset of a previous learner topic.
        admin.create_topics([NewTopic(topic, num_partitions=2, replication_factor=1)],timeout_ms=15000)
    finally:
        admin.close()


def publish_fixture(source: Path, topic: str, filename: str, work: Path, run_id: str) -> dict:
    validate_topic(topic)
    if filename not in GPS_FILES or not re.fullmatch(r'[0-9a-f]{32}',run_id):
        raise ValueError('Invalid source or run identity')
    require_fixed_dataset(source)
    receipt = workspace_path(work,f'reports/day04/{run_id}/producer_{filename}.json')
    if receipt.exists():
        raise ValueError('A publish intent already exists; do not silently redeliver after a partial send')
    lines = (Path(source)/filename).read_text(encoding='utf-8').splitlines()
    # Durable intent before the first send: uncertain sends require diagnosis,
    # not a false success or automatic application-level retry.
    write_json(receipt, {'status':'INTENT_RECORDED','topic':topic,'file':filename,
                         'file_sha256':digest_file(Path(source)/filename),'sent_confirmed':0})
    from kafka import KafkaProducer
    producer = None
    acked = []
    try:
        producer = KafkaProducer(bootstrap_servers=bootstrap_address(),client_id='masar-'+run_id[:12],
            enable_idempotence=True,acks='all',retries=5,max_in_flight_requests_per_connection=1,
            request_timeout_ms=15000,delivery_timeout_ms=45000,max_block_ms=15000,
            api_version_auto_timeout_ms=8000)
        for line in lines:
            event=json.loads(line)
            # Preserve the exact source JSON text; use the trip as partition key.
            future=producer.send(topic,key=event['trip_id'].encode('utf-8'),value=line.encode('utf-8'),
                                 headers=[('source_file',filename.encode('utf-8'))])
            metadata=future.get(timeout=45)
            acked.append({'topic':metadata.topic,'partition':metadata.partition,'offset':metadata.offset})
        producer.flush(timeout=45)
    except Exception as exc:
        write_json(receipt,{'status':'FAILED_OR_PARTIAL_PUBLISH','file':filename,'topic':topic,
                           'sent_confirmed':len(acked),'acknowledgments':acked,
                           'error_type':type(exc).__name__,'message':str(exc)})
        raise
    finally:
        if producer is not None: producer.close(timeout=10)
    if len(acked)!=len(lines) or len({(a['topic'],a['partition'],a['offset']) for a in acked})!=len(lines):
        raise AssertionError('Publish receipts do not reconcile')
    result={'status':'ACKNOWLEDGED','file':filename,'topic':topic,
            'file_sha256':digest_file(Path(source)/filename),'sent_confirmed':len(acked),
            'acknowledgments':acked,'kafka_executed':True}
    write_json(receipt,result)
    return result


def consume_available(spark,work:Path,topic:str,run_id:str,phase:str) -> dict:
    validate_topic(topic)
    if phase not in {'base','restart','replay','late'} or not re.fullmatch(r'[0-9a-f]{32}',run_id):
        raise ValueError('Invalid phase or run identity')
    from pyspark.sql import functions as F
    target=workspace_path(work,'mini_lakehouse/bronze/gps_stream/'+run_id)
    checkpoint=workspace_path(work,'checkpoints/day04/gps_'+run_id)
    frame=(spark.readStream.format('kafka').option('kafka.bootstrap.servers',bootstrap_address())
        .option('subscribe',topic).option('startingOffsets','earliest')
        .option('includeHeaders','true').option('failOnDataLoss','true')
        .option('maxOffsetsPerTrigger',72).load())
    frame=frame.select('topic','partition','offset',
        F.col('timestamp').alias('broker_timestamp'),F.col('key').cast('string').alias('message_key'),
        F.col('value').cast('string').alias('raw_json'),'headers',F.current_timestamp().alias('ingested_at'))
    query=None
    try:
        query=(frame.writeStream.format('delta').outputMode('append')
            .option('checkpointLocation',str(checkpoint)).queryName('masar_gps_'+run_id)
            .trigger(availableNow=True).start(str(target)))
        if not query.awaitTermination(180):
            raise TimeoutError('Streaming phase exceeded bounded teaching run; progress must be inspected')
        if query.exception() is not None:
            raise RuntimeError(str(query.exception()))
        result={'phase':phase,'query_id':str(query.id),'query_run_id':str(query.runId),
                'checkpoint':checkpoint.relative_to(work).as_posix(),
                'target':target.relative_to(work).as_posix(),'progress':query.recentProgress}
        rows=spark.read.format('delta').load(str(target))
        result['transport_rows']=rows.count()
        if result['transport_rows']>500: raise ValueError('Unexpected unbounded classroom topic input')
        result['unique_transport_keys']=rows.select('topic','partition','offset').distinct().count()
        events=[json.loads(row['raw_json']) for row in rows.select('raw_json').collect()]
        result['unique_event_ids']=len(unique_events(events))
        result['business_event_digest']=rows_digest(unique_events(events))
        write_json(workspace_path(work,f'reports/day04/{run_id}/consumer_{phase}.json'),result)
        return result
    finally:
        if query is not None and query.isActive: query.stop()


def run_stream_lab(spark,source:Path,work:Path) -> dict:
    require_fixed_dataset(source)
    preflight=stream_preflight()
    if preflight['issues']: raise EnvironmentUnavailable('; '.join(preflight['issues']))
    from masar.delta_reference import day03_reference
    from masar.silver import canonical_rows,delta_artifacts
    from masar.quality_gate import completed_day03_table
    # Enforce the cumulative project: do not substitute regenerated CSV Silver.
    trusted=completed_day03_table(spark,source,work)
    if len(canonical_rows(trusted))!=75: raise AssertionError('Trusted Silver is not ready')
    expected=day04_reference(source)
    run_id=uuid.uuid4().hex
    topic='masar-day04-'+run_id
    create_topic(topic)
    phases=[];receipts=[]
    receipts.append(publish_fixture(source,topic,'gps.ndjson',work,run_id))
    phases.append(consume_available(spark,work,topic,run_id,'base'))
    # Reuse the same checkpoint without publishing any new message.
    phases.append(consume_available(spark,work,topic,run_id,'restart'))
    receipts.append(publish_fixture(source,topic,'gps_replay.ndjson',work,run_id))
    phases.append(consume_available(spark,work,topic,run_id,'replay'))
    receipts.append(publish_fixture(source,topic,'gps_late.ndjson',work,run_id))
    phases.append(consume_available(spark,work,topic,run_id,'late'))
    from pyspark.sql import functions as F,types as T
    raw_path=workspace_path(work,phases[-1]['target'])
    raw=spark.read.format('delta').load(str(raw_path))
    # Audit exact transport receipts, not just counts.
    actual_keys={(r.topic,r.partition,r.offset) for r in raw.select('topic','partition','offset').collect()}
    sent_keys={(r['topic'],r['partition'],r['offset']) for p in receipts for r in p['acknowledgments']}
    original_lines=[line for name in GPS_FILES for line in (Path(source)/name).read_text(encoding='utf-8').splitlines()]
    read_lines=[r.raw_json for r in raw.select('raw_json').collect()]
    schema=T.StructType([T.StructField('event_id',T.StringType()),T.StructField('trip_id',T.StringType()),
        T.StructField('event_ts',T.StringType()),T.StructField('city',T.StringType()),
        T.StructField('location',T.StructType([T.StructField('lat',T.DoubleType()),T.StructField('lon',T.DoubleType())])),
        T.StructField('synthetic',T.BooleanType())])
    events=raw.select(F.from_json('raw_json',schema).alias('e')).select('e.*')
    if events.where(F.col('event_id').isNull()).count(): raise AssertionError('Unparseable event')
    # unique_events already rejected same-key conflicting payloads above.
    events=events.dropDuplicates(['event_id'])
    event_path=workspace_path(work,'mini_lakehouse/silver/gps_events_day04/'+run_id)
    events.write.format('delta').mode('errorifexists').save(str(event_path))
    event_read=spark.read.format('delta').load(str(event_path))
    cp=workspace_path(work,phases[-1]['checkpoint'])
    checks={
        'phase_transport_counts': [x['transport_rows'] for x in phases]==[216,216,218,219],
        'phase_event_counts':[x['unique_event_ids'] for x in phases]==[216,216,216,217],
        'transport_keys_always_unique':all(x['transport_rows']==x['unique_transport_keys'] for x in phases),
        'restart_same_query_identity':len({x['query_id'] for x in phases})==1,
        'restart_new_execution_ids':len({x['query_run_id'] for x in phases})==4,
        'checkpoint_same_for_all_phases':len({x['checkpoint'] for x in phases})==1,
        'actual_checkpoint_files_present':(cp/'metadata').is_file() and bool(list((cp/'offsets').glob('[0-9]*'))) and bool(list((cp/'commits').glob('[0-9]*'))),
        'producer_consumer_offsets_reconcile':actual_keys==sent_keys and len(actual_keys)==219,
        'source_json_text_preserved':Counter(read_lines)==Counter(original_lines),
        'event_content_matches_source':phases[-1]['business_event_digest']==expected['unique_events_digest'],
        'unique_events_delta_readback':event_read.count()==event_read.select('event_id').distinct().count()==217,
        'all_events_link_to_trusted_trips':event_read.join(trusted.select('trip_id'),'trip_id','left_anti').count()==0,
        'late_event_retained':event_read.where("event_id = 'SYN_E_LATE001'").count()==1,
    }
    if not all(checks.values()): raise AssertionError(checks)
    result={'scope':'DAY04_NATIVE_STREAMING','engine_executed':True,'kafka_executed':True,
        'run_id':run_id,'topic':topic,'spark_version':spark.version,'phases':phases,
        'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
        'event_table':event_path.relative_to(work).as_posix(),'raw_table':raw_path.relative_to(work).as_posix(),
        'artifacts':{'raw':delta_artifacts(work,raw_path),'events':delta_artifacts(work,event_path)},
        'checks':checks,'not_proven':['crash recovery stress','broker failover','distributed deployment','watermark execution']}
    write_json(workspace_path(work,f'reports/day04/{run_id}/streaming.json'),result)
    write_json(workspace_path(work,'reports/day04_stream_latest.json'),result)
    return result
