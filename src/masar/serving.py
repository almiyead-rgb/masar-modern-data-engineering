"""Native Labs 07/08. Read pinned Delta inputs; publish only validated releases.

No fallback engine, no driver-side reference rows used to populate Gold tables.
Small lookup metadata is allowed; trusted facts/events always come from Delta.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import re
import uuid
from masar.workspace import (workspace_path,write_json,digest_file,rows_digest,
    require_fixed_dataset,DATASET_MANIFEST_SHA256)
from masar.serving_reference import (AS_OF,ZONE_KEYS,TABLE_COLUMNS,TABLE_KEYS,FEATURE_INPUTS,
    availability_index,tables_from_trusted,validate_tables)

QUALITY_CHECKS = {'trusted_and_rechecked_pass_gx','mixed_candidate_fails_gx','native_mixed_counts',
    'native_reasons_match_reference','failed_candidate_not_promoted','quarantine_delta_readback',
    'approved_readback_same_business_contents','source_silver_untouched','data_docs_exist_for_all_three_cases'}
STREAM_CHECKS = {'phase_transport_counts','phase_event_counts','transport_keys_always_unique',
    'restart_same_query_identity','restart_new_execution_ids','checkpoint_same_for_all_phases',
    'actual_checkpoint_files_present','producer_consumer_offsets_reconcile','source_json_text_preserved',
    'event_content_matches_source','unique_events_delta_readback','all_events_link_to_trusted_trips','late_event_retained'}


class InjectedFailure(RuntimeError):
    """Deliberate classroom fault. Must not create or move a committed release."""


def require_report(report: dict, scope: str, checks: set[str], extra_flag: str | None = None) -> None:
    if not isinstance(report,dict) or not isinstance(report.get('checks'),dict):
        raise ValueError('Native prerequisite must be a report object with named checks')
    if (report.get('scope') != scope or report.get('engine_executed') is not True
        or report.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256
        or not re.fullmatch(r'[0-9a-f]{32}',report.get('run_id',''))
        or set(report.get('checks',{})) != checks
        or not all(value is True for value in report['checks'].values())
        or (extra_flag and report.get(extra_flag) is not True)):
        raise ValueError('Missing, incomplete or wrong-scope native prerequisite: '+scope)


def _snapshot(spark, work: Path, relative: str, limit: int):
    from delta.tables import DeltaTable
    from masar.silver import delta_artifacts
    path = workspace_path(work,relative)
    delta_artifacts(work,path)
    version = int(DeltaTable.forPath(spark,str(path)).history(1).first()['version'])
    frame = spark.read.format('delta').option('versionAsOf',version).load(str(path))
    count = frame.limit(limit+1).count()
    if not 1 <= count <= limit: raise ValueError('Unbounded or empty classroom snapshot')
    return frame, {'path':relative,'version':version,'row_count':count}


def load_validated_inputs(spark, source: Path, work: Path):
    from masar.silver import canonical_rows
    from masar.trust_reference import unique_events, day04_reference
    require_fixed_dataset(source)
    if spark.conf.get('spark.sql.session.timeZone') != 'UTC': raise ValueError('UTC Spark session required')
    quality = json.loads(workspace_path(work,'reports/day04_quality_latest.json').read_text(encoding='utf-8'))
    stream = json.loads(workspace_path(work,'reports/day04_stream_latest.json').read_text(encoding='utf-8'))
    require_report(quality,'DAY04_NATIVE_QUALITY',QUALITY_CHECKS,'gx_executed')
    require_report(stream,'DAY04_NATIVE_STREAMING',STREAM_CHECKS,'kafka_executed')
    # Read the quality-approved copy, never the intentionally contaminated candidate.
    trusted, tmeta = _snapshot(spark,work,quality['approved_table'],500)
    events, emeta = _snapshot(spark,work,stream['event_table'],500)
    trips = canonical_rows(trusted)
    observed_events = [r.asDict(recursive=True) for r in events.collect()]
    expected = day04_reference(source)
    if (rows_digest(trips) != quality['approved_business_digest']
        or rows_digest(trips) != expected['trusted_business_digest']
        or len(observed_events) != 217
        or rows_digest(unique_events(observed_events)) != expected['unique_events_digest']):
        raise ValueError('Actual pinned inputs disagree with validated fixture contents')
    return trusted, events, {'trips':tmeta,'events':emeta,
        'quality_report_sha256':digest_file(workspace_path(work,'reports/day04_quality_latest.json')),
        'stream_report_sha256':digest_file(workspace_path(work,'reports/day04_stream_latest.json'))}


def build_frames(spark,trusted,events,source:Path):
    """All fact shaping and aggregation below runs in Spark, not in the oracle."""
    from pyspark.sql import functions as F,types as T
    zones = spark.createDataFrame([(key,city,'city_proxy') for city,key in sorted(ZONE_KEYS.items())],
        'zone_key string, city string, zone_resolution string')
    x = trusted.join(F.broadcast(zones),'city','inner')
    by_event = events.groupBy('trip_id').agg(F.count('*').alias('gps_event_count'))
    facts = x.join(by_event,'trip_id','left').select('trip_id',F.col('driver_id').alias('driver_key'),'zone_key',
        F.date_format('trip_date_local','yyyyMMdd').cast('int').alias('date_key'),'start_utc',
        'fare_sar','distance_km','duration_seconds',F.coalesce('gps_event_count',F.lit(0)).cast('long').alias('gps_event_count'))
    hourly = x.withColumn('hour_utc',F.date_trunc('hour','start_utc')).groupBy('zone_key','hour_utc').agg(
        F.count('*').alias('trip_count'),F.sum('fare_sar').cast('decimal(20,2)').alias('total_fare_sar'),
        F.sum('duration_seconds').alias('total_duration_seconds'))
    # UTC remains the canonical instant; local clock text is only a presentation field.
    hourly = hourly.withColumn('hour_local',F.concat(
        F.date_format(F.from_utc_timestamp('hour_utc','Asia/Riyadh'),"yyyy-MM-dd'T'HH:mm:ss"),F.lit('+03:00')))
    daily = x.groupBy(F.col('driver_id').alias('driver_key'),'trip_date_local').agg(
        F.count('*').alias('trip_count'),F.sum('fare_sar').cast('decimal(20,2)').alias('total_fare_sar'),
        F.sum('duration_seconds').alias('total_duration_seconds'))
    drivers = trusted.select(F.col('driver_id').alias('driver_key'),'driver_id','vehicle_type').distinct()
    dates = trusted.select(F.col('trip_date_local').alias('date_local')).distinct().select(
        F.date_format('date_local','yyyyMMdd').cast('int').alias('date_key'),'date_local',
        F.year('date_local').alias('year'),F.month('date_local').alias('month'),F.dayofmonth('date_local').alias('day'))
    # This lookup is delivery metadata from the unchanged schedule, not feature values.
    availability = spark.createDataFrame([(trip,rev,ts) for (trip,rev),ts in availability_index(source).items()],
        'trip_id string, source_revision int, source_available_at_utc string')
    history = x.join(F.broadcast(availability),['trip_id','source_revision'],'left').withColumn(
        'source_available_at_utc',F.to_timestamp('source_available_at_utc'))
    if history.where(F.col('source_available_at_utc').isNull()).count():
        raise ValueError('Every source revision needs availability metadata')
    cutoff = F.to_timestamp(F.lit(AS_OF))
    start = cutoff-F.expr('INTERVAL 24 HOURS')
    target = F.date_trunc('hour',cutoff)+F.expr('INTERVAL 1 HOUR')
    history = history.where((F.col('source_available_at_utc')<=cutoff)&(F.col('end_utc')<cutoff)&(F.col('end_utc')>=start))
    aggregated = history.groupBy('zone_key').agg(F.count('*').alias('completed_trips_24h'),
        F.round(F.avg('duration_seconds'),2).cast('decimal(20,2)').alias('avg_duration_seconds_24h'),
        F.max('source_available_at_utc').alias('max_source_available_at_utc'))
    features = zones.select('zone_key').join(aggregated,'zone_key','left').withColumn(
        'completed_trips_24h',F.coalesce('completed_trips_24h',F.lit(0)).cast('long')).withColumn(
        'history_available',F.col('completed_trips_24h')>0).withColumn('as_of_utc',cutoff).withColumn(
        'prediction_hour_utc',target).withColumn('history_window_start_utc',start)
    # The dataset contains no target-hour coverage: unknown must stay NULL.
    labels = zones.select('zone_key').withColumn('prediction_hour_utc',target).withColumn(
        'target_trip_count',F.lit(None).cast('long')).withColumn('label_status',F.lit('UNOBSERVED')).withColumn(
        'label_available_at_utc',F.lit(None).cast('timestamp'))
    frames = dict(zip(TABLE_COLUMNS,[hourly,daily,zones,drivers,dates,facts,features,labels]))
    return {name:df.select(*TABLE_COLUMNS[name]) for name,df in frames.items()}


def canonical_table(frame,name: str) -> list[dict]:
    from pyspark.sql import functions as F,types as T
    if name not in TABLE_COLUMNS or set(frame.columns)!=set(TABLE_COLUMNS[name]):
        raise ValueError('Unexpected native serving schema')
    if frame.limit(501).count()>500: raise ValueError('Bounded readback exceeded')
    selected=[]
    for field in frame.schema:
        column=F.col(field.name)
        if isinstance(field.dataType,T.TimestampType): column=F.date_format(column,"yyyy-MM-dd'T'HH:mm:ss'Z'")
        elif isinstance(field.dataType,(T.DateType,T.DecimalType)): column=column.cast('string')
        selected.append(column.alias(field.name))
    return [row.asDict() for row in frame.select(*selected).orderBy(*TABLE_KEYS[name]).collect()]


def _gold_latest(work:Path) -> bytes | None:
    p=workspace_path(work,'reports/day05_gold_latest.json')
    return p.read_bytes() if p.is_file() else None


def run_gold_lab(spark,source:Path,work:Path,*,fail_after:int|None=None) -> dict:
    from masar.silver import canonical_rows,delta_artifacts
    if fail_after is not None and (type(fail_after) is not int or not 1<=fail_after<=len(TABLE_COLUMNS)):
        raise ValueError('Failure injection must be a table position from 1 to 8')
    trusted,events,inputs=load_validated_inputs(spark,source,work)
    expected=tables_from_trusted(canonical_rows(trusted),[r.asDict(recursive=True) for r in events.collect()],source)
    frames=build_frames(spark,trusted,events,source)
    release_id=uuid.uuid4().hex
    root=f'mini_lakehouse/serving_releases/{release_id}'
    manifest_path=workspace_path(work,root+'/release.json')
    before=_gold_latest(work)
    tables={};readback={}
    try:
        for i,(name,frame) in enumerate(frames.items(),1):
            target=workspace_path(work,root+'/'+name.replace('.','/'))
            frame.write.format('delta').mode('errorifexists').save(str(target))
            observed,meta=_snapshot(spark,work,target.relative_to(work).as_posix(),500)
            readback[name]=canonical_table(observed,name)
            if readback[name]!=expected[name]: raise AssertionError('Spark result differs from independent reference: '+name)
            tables[name]={**meta,'content_sha256':rows_digest(readback[name]),'artifacts':delta_artifacts(work,target)}
            if i==fail_after: raise InjectedFailure('Deliberate failure after table '+str(i))
        checks=validate_tables(readback)
        result={'scope':'DAY05_NATIVE_GOLD','engine_executed':True,'run_id':release_id,
            'spark_version':spark.version,'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
            'as_of_utc':AS_OF,'inputs':inputs,'tables':tables,'checks':checks,
            'transaction_boundary':'Each Delta table commits independently; this manifest gates this local consumer only.',
            'not_proven':['global multi-table atomicity','concurrent publisher safety','production-scale performance','dbt execution']}
        write_json(manifest_path,result)
        write_json(workspace_path(work,'reports/day05_gold_latest.json'),{
            'run_id':release_id,'manifest':manifest_path.relative_to(work).as_posix(),'manifest_sha256':digest_file(manifest_path)})
        return result
    except Exception as exc:
        write_json(workspace_path(work,f'reports/day05_failures/{release_id}.json'),{
            'scope':'DAY05_GOLD_FAILURE','engine_started':True,'complete_lab_success':False,
            'run_id':release_id,'error_type':type(exc).__name__,'message':str(exc),
            'tables_written':list(tables),'committed_release_exists':manifest_path.exists(),
            'previous_pointer_preserved':before==_gold_latest(work)})
        raise


def read_release(spark,work:Path) -> tuple[dict,dict]:
    pointer=json.loads(workspace_path(work,'reports/day05_gold_latest.json').read_text(encoding='utf-8'))
    manifest=workspace_path(work,pointer['manifest'])
    if digest_file(manifest)!=pointer.get('manifest_sha256'): raise ValueError('Release manifest changed')
    report=json.loads(manifest.read_text(encoding='utf-8'))
    if (report.get('scope')!='DAY05_NATIVE_GOLD' or report.get('engine_executed') is not True
        or report.get('run_id')!=pointer.get('run_id') or report.get('dataset_manifest_sha256')!=DATASET_MANIFEST_SHA256
        or set(report.get('tables',{}))!=set(TABLE_COLUMNS)):
        raise ValueError('Release identity or table set invalid')
    tables={}
    for name,meta in report['tables'].items():
        path=workspace_path(work,meta['path'])
        from masar.silver import delta_artifacts
        delta_artifacts(work,path)
        version=meta.get('version')
        if type(version) is not int or version<0: raise ValueError('Invalid pinned table version')
        frame=spark.read.format('delta').option('versionAsOf',version).load(str(path))
        tables[name]=canonical_table(frame,name)
        if rows_digest(tables[name])!=meta['content_sha256'] or len(tables[name])!=meta['row_count']:
            raise ValueError('Actual table differs from release contents: '+name)
    expected_checks=validate_tables(tables)
    if report.get('checks')!=expected_checks: raise ValueError('Release checks incomplete or altered')
    return report,tables


def run_serving_lab(spark,source:Path,work:Path) -> dict:
    require_fixed_dataset(source)
    release,tables=read_release(spark,work)
    export_id=uuid.uuid4().hex
    prefix=f'reports/serving/{export_id}'
    files={}
    for name,rows in tables.items():
        path=workspace_path(work,prefix+'/'+name.replace('.','_')+'.csv')
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('x',encoding='utf-8',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=TABLE_COLUMNS[name],lineterminator='\n')
            writer.writeheader();writer.writerows(rows)
        with path.open(encoding='utf-8',newline='') as handle:
            loaded=list(csv.DictReader(handle))
        rendered=[{k:('' if r[k] is None else str(r[k])) for k in TABLE_COLUMNS[name]} for r in rows]
        if loaded!=rendered: raise AssertionError('CSV readback mismatch')
        files[name]={'path':path.relative_to(work).as_posix(),'sha256':digest_file(path),'rows':len(rows)}
    # A real SQL consumer over the pinned native fact table, not the CSV oracle.
    fact_meta=release['tables']['bi.fact_trips']
    fact=spark.read.format('delta').option('versionAsOf',fact_meta['version']).load(str(workspace_path(work,fact_meta['path'])))
    fact.createOrReplaceTempView('masar_day05_fact')
    query_path = Path(source).resolve().parents[1] / 'day05/sql/bi_zone_summary.sql'
    bi=spark.sql(query_path.read_text(encoding='utf-8'))
    bi_summary=[{'zone_key':r.zone_key,'trip_count':r.trip_count,'total_fare_sar':str(r.total_fare_sar)} for r in bi.collect()]
    from decimal import Decimal
    if sum(x['trip_count'] for x in bi_summary)!=75 or sum(Decimal(x['total_fare_sar']) for x in bi_summary)!=Decimal('1880.60'):
        raise AssertionError('Native BI consumer does not reconcile')
    checks=validate_tables(tables)
    result={'scope':'DAY05_NATIVE_SERVING','engine_executed':True,'run_id':export_id,
        'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,'source_release_id':release['run_id'],
        'exports':files,'bi_summary':bi_summary,'feature_inputs':list(FEATURE_INPUTS),
        'label_status':'UNOBSERVED_NOT_ZERO','checks':checks,'csv_null_representation':'empty field',
        'not_proven':['model training or accuracy','Power BI connector execution','public deployment','full course approval']}
    write_json(workspace_path(work,prefix+'/serving.json'),result)
    write_json(workspace_path(work,'reports/day05_serving_latest.json'),result)
    return result


def run_recovery_exercise(spark,source:Path,work:Path) -> dict:
    first=run_gold_lab(spark,source,work)
    before=_gold_latest(work)
    try:
        run_gold_lab(spark,source,work,fail_after=1)
    except InjectedFailure:
        pass
    else:
        raise AssertionError('Expected failure was not triggered')
    if _gold_latest(work)!=before: raise AssertionError('Failed build changed committed release')
    # Read the former good release even though the failed candidate's files remain.
    read_release(spark,work)
    second=run_gold_lab(spark,source,work)
    equal=all(first['tables'][k]['content_sha256']==second['tables'][k]['content_sha256'] for k in TABLE_COLUMNS)
    if not equal or first['run_id']==second['run_id']: raise AssertionError('Independent release builds disagree')
    result={'scope':'DAY05_NATIVE_RECOVERY','engine_executed':True,'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
        'run_ids':[first['run_id'],second['run_id']],'checks':{'injected_failure_observed':True,
        'previous_release_preserved':True,'rebuild_has_new_identity':True,'content_equal':equal},
        'limits':'Same Spark session; this is not the independent fresh-environment final validation.'}
    write_json(workspace_path(work,'reports/day05_recovery.json'),result)
    return result
