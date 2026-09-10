"""Native Spark/Delta implementation of Lab 03; engine execution is pending.

Small single-writer teaching pipeline. It reads actual Day 1 Delta tables and
never falls back to CSV transformations or a mock engine. Day 2 is insert-only;
correction precedence, concurrency and production recovery belong to later work.
"""
from __future__ import annotations
import csv
import json
import re
import uuid
from pathlib import Path
from masar.silver_reference import BUSINESS_FIELDS, TIME_RE, NUMBER_RE, reference_result
from masar.workspace import (workspace_path, require_fixed_dataset, digest_file,
                             write_json, rows_digest, DATASET_MANIFEST_SHA256)


def _utc_session(spark) -> None:
    if spark.conf.get('spark.sql.session.timeZone') != 'UTC':
        raise ValueError('Use UTC session timezone; derive the business date in Asia/Riyadh')
    spark.conf.set('spark.sql.timestampType', 'TIMESTAMP_LTZ')


def _city(column):
    from pyspark.sql import functions as F
    return F.create_map(F.lit('riyadh'), F.lit('Riyadh'), F.lit('jeddah'),
                        F.lit('Jeddah'), F.lit('dammam'), F.lit('Dammam'))[F.lower(F.trim(column))]


def _timestamp(column):
    from pyspark.sql import functions as F
    return F.when(F.trim(column).rlike(TIME_RE),
                  F.try_to_timestamp(F.trim(column), F.lit("yyyy-MM-dd'T'HH:mm:ssXXX")))


def _number(name: str):
    # SQL TRY_CAST is available in Spark 3.5; Column.try_cast is a Spark 4 API.
    # Only these fixed identifiers are accepted; no user SQL is interpolated.
    if name not in {"fare_sar", "distance_km"}:
        raise ValueError("Unsupported numeric source field")
    from pyspark.sql import functions as F
    return F.when(F.trim(F.col(name)).rlike(NUMBER_RE),
                  F.expr(f"try_cast(trim(`{name}`) as decimal(12,2))"))


def stage_frames(spark, work: Path, *, base_snapshot: bool = False) -> dict:
    """In-memory staging; Bronze strings/raw JSON remain untouched on disk."""
    from pyspark.sql import functions as F, types as T
    from delta.tables import DeltaTable
    _utc_session(spark)
    raw = {}
    for feed in ('trips', 'drivers', 'gps_events'):
        path = workspace_path(work, 'mini_lakehouse/bronze/' + feed)
        if not DeltaTable.isDeltaTable(spark, str(path)):
            raise FileNotFoundError('Run Day 1 Bronze successfully first: ' + feed)
        reader = spark.read.format('delta')
        if base_snapshot:
            reader = reader.option('versionAsOf', 1 if feed == 'trips' else 0)
        raw[feed] = reader.load(str(path))
    # Do not silently include later correction/quality scenarios in Day 2.
    if raw['trips'].where(~F.col('_source_file').isin('trips.csv','late_trips.csv')
                          | F.col('_source_file').isNull()).limit(1).count():
        raise ValueError('Day 2 supports base and late trips only; preserve later-day tables')
    trips = raw['trips'].select(
        F.trim('trip_id').alias('trip_id'), F.trim('driver_id').alias('driver_id'),
        _city(F.col('city')).alias('city'), _timestamp(F.col('start_ts')).alias('start_utc'),
        _timestamp(F.col('end_ts')).alias('end_utc'), _number('fare_sar').alias('fare_sar'),
        _number('distance_km').alias('distance_km'),
        F.col('city').alias('raw_city'), '_source_file', '_source_sha256', '_batch_id', '_ingested_at')
    trips = (trips.withColumn('duration_seconds',F.col('end_utc').cast('long')-F.col('start_utc').cast('long'))
             .withColumn('trip_date_local', F.to_date(F.from_utc_timestamp('start_utc','Asia/Riyadh')))
             .withColumn('source_revision', F.lit(1)))
    drivers = raw['drivers'].select(F.trim('driver_id').alias('driver_id'),
        F.lower(F.trim('vehicle_type')).alias('vehicle_type'),
        F.when(F.trim('driver_rating').rlike(r'^[0-9](\.[0-9])?$'),
               F.expr('try_cast(trim(driver_rating) as decimal(3,1))')).alias('driver_rating'))
    gps_schema = T.StructType([
        T.StructField('event_id',T.StringType()), T.StructField('trip_id',T.StringType()),
        T.StructField('city',T.StringType()), T.StructField('event_ts',T.StringType()),
        T.StructField('synthetic',T.BooleanType()),
        T.StructField('location',T.StructType([T.StructField('lat',T.DoubleType()),T.StructField('lon',T.DoubleType())]))])
    gps = raw['gps_events'].withColumn('e', F.from_json('raw_json',gps_schema)).select(
        F.col('e.event_id').alias('event_id'), F.col('e.trip_id').alias('trip_id'),
        _city(F.col('e.city')).alias('city'), _timestamp(F.col('e.event_ts')).alias('event_utc'),
        F.col('e.location.lat').alias('latitude'), F.col('e.location.lon').alias('longitude'),
        F.col('e.synthetic').alias('synthetic'), '_source_file', '_batch_id')
    return {'stg_trips':trips, 'stg_drivers':drivers, 'stg_gps':gps}


def validate_staging(frames: dict) -> dict:
    from pyspark.sql import functions as F
    trips, drivers, gps = (frames[n] for n in ('stg_trips','stg_drivers','stg_gps'))
    d_bad = (F.col('driver_id').isNull() | (F.col('driver_id')=='') | F.col('vehicle_type').isNull()
             | ~F.col('vehicle_type').isin('sedan','suv') | F.col('driver_rating').isNull()
             | ~F.col('driver_rating').between(0,5))
    if drivers.where(d_bad).limit(1).count() or drivers.groupBy('driver_id').count().where('count != 1').limit(1).count():
        raise ValueError('Invalid or duplicate driver dimension; joining would be unsafe')
    t_bad = (F.col('trip_id').isNull() | (F.col('trip_id')=='') | F.col('city').isNull()
             | F.col('start_utc').isNull() | F.col('end_utc').isNull()
             | F.col('fare_sar').isNull() | (F.col('fare_sar')<0)
             | F.col('distance_km').isNull() | (F.col('distance_km')<=0)
             | F.col('duration_seconds').isNull() | (F.col('duration_seconds')<=0))
    if trips.where(t_bad).limit(1).count():
        raise ValueError('Invalid trip values detected; no invalid rows were silently dropped')
    if trips.join(drivers.select('driver_id'),'driver_id','left_anti').limit(1).count():
        raise ValueError('Unknown driver; stop before the enrichment join')
    g_bad = (F.col('event_id').isNull() | (F.col('event_id')=='') | F.col('event_utc').isNull()
             | F.col('city').isNull() | F.col('latitude').isNull() | F.col('longitude').isNull()
             | F.isnan('latitude') | F.isnan('longitude') | ~F.col('latitude').between(-90,90)
             | ~F.col('longitude').between(-180,180) | F.col('synthetic').isNull() | ~F.col('synthetic'))
    if gps.where(g_bad).limit(1).count() or gps.groupBy('event_id').count().where('count != 1').limit(1).count():
        raise ValueError('GPS base staging invalid; streaming replay is a later lab')
    if gps.join(trips.select('trip_id').distinct(),'trip_id','left_anti').limit(1).count():
        raise ValueError('GPS references an unknown trip')
    return {name: frame.count() for name,frame in frames.items()}


def silver_candidates(frames: dict):
    """Validate first, detect conflicts, then select one stable receipt per key."""
    from pyspark.sql import functions as F, Window
    validate_staging(frames)
    joined = frames['stg_trips'].join(frames['stg_drivers'],'driver_id','left')
    if joined.count() != frames['stg_trips'].count():
        raise AssertionError('Driver join changed the trip receipt grain')
    payload = F.to_json(F.struct(*[F.col(name) for name in BUSINESS_FIELDS]))
    staged = joined.withColumn('_payload_hash',F.sha2(payload,256))
    if staged.groupBy('trip_id','source_revision').agg(F.countDistinct('_payload_hash').alias('variants')).where('variants > 1').limit(1).count():
        raise ValueError('Conflicting same-revision records require explicit correction handling')
    order = Window.partitionBy('trip_id').orderBy(F.col('source_revision').desc(),
        F.col('_source_file').asc(),F.col('_source_sha256').asc(),F.col('_batch_id').asc())
    return (staged.withColumn('_choice',F.row_number().over(order)).where('_choice = 1')
            .select(*BUSINESS_FIELDS,'_source_file','_source_sha256','_payload_hash'))


def canonical_rows(frame) -> list[dict]:
    from pyspark.sql import functions as F
    frame = frame.select(*[F.col(name) for name in BUSINESS_FIELDS])
    for name in ('start_utc','end_utc'):
        frame = frame.withColumn(name,F.date_format(name,"yyyy-MM-dd'T'HH:mm:ss'Z'"))
    for name in ('fare_sar','distance_km','driver_rating','trip_date_local'):
        frame = frame.withColumn(name,F.col(name).cast('string'))
    return [r.asDict() for r in frame.orderBy('trip_id').collect()]


def delta_artifacts(work: Path, target: Path) -> dict:
    commits = sorted((target/'_delta_log').glob('[0-9]'*20+'.json'))
    data = sorted(target.rglob('*.parquet'))
    if not commits or not data or any(p.stat().st_size == 0 for p in commits+data):
        raise AssertionError('Actual Delta transactions and data files are required')
    return {'commits':[{'path':p.relative_to(work).as_posix(),'sha256':digest_file(p)} for p in commits],
            'data_files':[{'path':p.relative_to(work).as_posix(),'sha256':digest_file(p)} for p in data]}


def run_staging_lab(spark, source: Path, work: Path) -> dict:
    require_fixed_dataset(source)
    frames = stage_frames(spark,work,base_snapshot=True)
    counts = validate_staging(frames)
    if counts != {'stg_trips':144,'stg_drivers':6,'stg_gps':216}:
        raise AssertionError('Unexpected Day 1 snapshot counts')
    candidates = silver_candidates(frames)
    expected = reference_result(source)['expected_silver_rows']
    expected = [row for row in expected if not row['trip_id'].startswith('SYN_LATE')]
    if canonical_rows(candidates) != expected:
        raise AssertionError('Native staging does not match independent source expectations')
    run = uuid.uuid4().hex
    artifacts = {}
    for name,frame in frames.items():
        target = workspace_path(work,'mini_lakehouse/staging/day02_'+run+'/'+name)
        frame.write.format('delta').mode('errorifexists').save(str(target))
        reread = spark.read.format('delta').load(str(target))
        if reread.count() != counts[name] or reread.schema != frame.schema:
            # Delta may relax nullability; check physical data types, not inferred null flags.
            if reread.count() != counts[name] or [(f.name,f.dataType) for f in reread.schema] != [(f.name,f.dataType) for f in frame.schema]:
                raise AssertionError('Staging Delta readback mismatch')
        artifacts[name] = delta_artifacts(work,target)
    report={'scope':'DAY02_STAGING_ENGINE','engine_executed':True,'run_id':run,
            'spark_version':spark.version,'counts':counts,'unique_base_trips':len(expected),
            'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,'artifacts':artifacts,
            'checks':{'counts_verified':True,'typed_values_match_source_oracle':True,
                      'drivers_unique_and_join_safe':True,'gps_valid':True,'delta_readback':True}}
    write_json(workspace_path(work,'reports/day02_staging_'+run+'.json'),report)
    write_json(workspace_path(work,'reports/day02_staging_latest.json'),report)
    return report


def ingest_late(spark, source: Path, work: Path, batch_id: str) -> dict:
    """A same-id retry is a checked no-op; a new id is intentional redelivery.

    Single writer only: this check+append is not a concurrent transaction protocol.
    """
    from pyspark.sql import functions as F, types as T
    require_fixed_dataset(source)
    if not re.fullmatch(r'late_[A-Za-z0-9_]{1,30}',batch_id):
        raise ValueError('Use a safe late_ batch identifier')
    target = workspace_path(work,'mini_lakehouse/bronze/trips')
    current = spark.read.format('delta').load(str(target))
    path = Path(source)/'late_trips.csv'
    with path.open(encoding='utf-8',newline='') as f:
        header = next(csv.reader(f))
    schema = T.StructType([T.StructField(n,T.StringType(),True) for n in header])
    raw = (spark.read.schema(schema).option('header',True).option('enforceSchema',False)
           .option('mode','FAILFAST').csv(str(path)))
    old = current.where(F.col('_batch_id')==batch_id)
    if old.limit(1).count():
        old_rows = [r.asDict() for r in old.select(*header).collect()]
        raw_rows = [r.asDict() for r in raw.collect()]
        if rows_digest(old_rows) != rows_digest(raw_rows) or old.where(
            (F.col('_source_file')!='late_trips.csv') | (F.col('_source_sha256')!=digest_file(path))
            | F.col('_source_file').isNull() | F.col('_source_sha256').isNull()).count():
            raise ValueError('A batch id exists with different payload or metadata')
        return {'batch_id':batch_id,'appended_rows':0,'bronze_receipts':current.count(),'status':'CHECKED_NOOP'}
    if raw.count()!=3:
        raise AssertionError('The approved late batch must contain three rows')
    enriched=(raw.withColumn('_source_file',F.lit('late_trips.csv'))
        .withColumn('_source_sha256',F.lit(digest_file(path))).withColumn('_batch_id',F.lit(batch_id))
        .withColumn('_ingested_at',F.current_timestamp()))
    enriched.write.format('delta').mode('append').save(str(target))
    return {'batch_id':batch_id,'appended_rows':3,'bronze_receipts':spark.read.format('delta').load(str(target)).count(),'status':'APPENDED'}


def merge_silver(spark, work: Path, candidates) -> dict:
    from pyspark.sql import functions as F
    from delta.tables import DeltaTable
    target=workspace_path(work,'mini_lakehouse/silver/trips')
    if candidates.groupBy('trip_id').count().where('count != 1').limit(1).count() or candidates.where(F.col('trip_id').isNull() | (F.col('trip_id')=='')).count():
        raise ValueError('Deduplicate and validate the merge source first')
    if DeltaTable.isDeltaTable(spark,str(target)):
        existing = spark.read.format('delta').load(str(target))
        if set(existing.columns)!=set(candidates.columns):
            raise ValueError('Unexpected existing Silver schema; preserve it and diagnose')
        if existing.where(F.col('trip_id').isNull() | (F.col('trip_id')=='')).limit(1).count() or existing.groupBy('trip_id').count().where('count != 1').limit(1).count():
            raise ValueError('Existing Silver keys are not unique')
        overlap=existing.alias('t').join(candidates.alias('s'),'trip_id','inner')
        if overlap.where(~F.col('t._payload_hash').eqNullSafe(F.col('s._payload_hash'))).limit(1).count():
            raise ValueError('Day 2 does not overwrite corrections; use the Day 3 revision policy')
        (DeltaTable.forPath(spark,str(target)).alias('t').merge(candidates.alias('s'),'t.trip_id = s.trip_id')
         .whenNotMatchedInsertAll().execute())
    else:
        if target.exists():
            raise ValueError('Existing target is not Delta; nothing was overwritten')
        candidates.write.format('delta').mode('errorifexists').save(str(target))
    result=spark.read.format('delta').load(str(target))
    rows=canonical_rows(result)
    return {'silver_rows':len(rows),'digest':rows_digest(rows),
            'version':int(DeltaTable.forPath(spark,str(target)).history(1).select('version').first()[0])}


def run_incremental_lab(spark, source: Path, work: Path) -> dict:
    """Run five explicit scenarios, or verify a completed Day 2 rerun read-only."""
    require_fixed_dataset(source)
    stage_report=workspace_path(work,'reports/day02_staging_latest.json')
    if not stage_report.is_file():
        raise FileNotFoundError('Complete the native Lab 3a staging notebook first')
    stage=json.loads(stage_report.read_text())
    if stage.get('engine_executed') is not True or stage.get('scope')!='DAY02_STAGING_ENGINE' or stage.get('dataset_manifest_sha256')!=DATASET_MANIFEST_SHA256:
        raise ValueError('The staging report is not valid')
    expected=reference_result(source)
    prior=workspace_path(work,'reports/day02_silver.json')
    target=workspace_path(work,'mini_lakehouse/silver/trips')
    if prior.exists():
        rows=canonical_rows(spark.read.format('delta').load(str(target)))
        if rows!=expected['expected_silver_rows']:
            raise ValueError('Silver changed since Day 2; do not rerun an earlier-day lab over later work')
        result=json.loads(prior.read_text())
        if result.get('scope')!='DAY02_SILVER_ENGINE' or result.get('engine_executed') is not True or not result.get('checks') or not all(v is True for v in result['checks'].values()):
            raise ValueError('Prior report is incomplete')
        return {**result,'rerun_status':'READBACK_RECHECKED_EXISTING_RESULTS'}
    bronze=workspace_path(work,'mini_lakehouse/bronze/trips')
    if spark.read.format('delta').load(str(bronze)).count()!=144:
        raise ValueError('An earlier partial Day 2 attempt exists. Preserve it; use a new full Day 1 run for a clean replay.')
    observations=[]
    for index,step in enumerate(expected['stages']):
        if index==2: ingest_late(spark,source,work,'late_003')
        elif index==3: ingest_late(spark,source,work,'late_003')
        elif index==4: ingest_late(spark,source,work,'late_replay_004')
        frames=stage_frames(spark,work)
        outcome=merge_silver(spark,work,silver_candidates(frames))
        outcome.update(stage=step['stage'],bronze_receipts=frames['stg_trips'].count())
        for key in ('bronze_receipts','silver_rows','digest'):
            if outcome[key]!=step[key]:
                raise AssertionError(f'Native/reference mismatch at {step["stage"]}: {key}')
        observations.append(outcome)
    rows=canonical_rows(spark.read.format('delta').load(str(target)))
    if rows!=expected['expected_silver_rows']:
        raise AssertionError('Final Silver content mismatch')
    report={'scope':'DAY02_SILVER_ENGINE','engine_executed':True,'dbt_executed':False,
            'run_id':uuid.uuid4().hex,'spark_version':spark.version,
            'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,'stages':observations,
            'artifacts':delta_artifacts(work,target),'final_fare_sar':expected['final_fare_sar'],
            'checks':{'all_scenarios_match_independent_oracle':True,'business_keys_unique':True,
                      'replay_preserves_business_content':True,'late_rows_retained':True,
                      'actual_delta_files':True},'single_writer_teaching_scope':True}
    write_json(prior,report)
    write_json(workspace_path(work,'reports/day02_expected_vs_actual.json'),
               {'scope':'ACTUAL_DELTA_READBACK','engine_executed':True,'rows':rows})
    return report
