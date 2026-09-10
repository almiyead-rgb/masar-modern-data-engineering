"""Native Lab 04: revision-aware corrections and isolated Delta maintenance.

AUTHORED, ENGINE NOT EXECUTED in the course build environment.
Requires the actual completed Day 2 Delta workspace. No Python/CSV fallback.
Only the authorized correction changes trusted Silver; every destructive probe
and schema/maintenance exercise uses a new independently written Delta copy.
This is a single-writer teaching flow, not a concurrent ingestion protocol.
"""
from __future__ import annotations
import csv
import json
import re
import uuid
from pathlib import Path
from masar.delta_reference import day03_reference, schema_fixture
from masar.silver_reference import BUSINESS_FIELDS, TRIP_FIELDS, reference_result
from masar.silver import (
    _city, _number, _timestamp, _utc_session, canonical_rows, delta_artifacts, stage_frames,
)
from masar.workspace import (
    DATASET_MANIFEST_SHA256, digest_file, require_fixed_dataset,
    rows_digest, workspace_path, write_json,
)


def _table_path(path: Path) -> str:
    value = str(Path(path).resolve())
    if '`' in value or any(ord(c) < 32 for c in value):
        raise ValueError('Unsafe SQL path')
    return 'delta.`' + value + '`'


def vacuum_dry_run_sql(work: Path, target: Path, retention_hours: int = 168) -> str:
    """Only generate a dry run on a registered workspace's sandbox descendant."""
    if type(retention_hours) is not int or retention_hours < 168:
        raise ValueError('Keep at least 168 hours; do not disable the retention safeguard')
    # Validate the original target before resolving: symlinks must not be hidden.
    work_abs = Path(work).resolve()
    target_abs = Path(target).absolute()
    try:
        relative = target_abs.relative_to(work_abs)
    except ValueError as exc:
        raise ValueError('Maintenance target is outside this workspace') from exc
    checked = workspace_path(work, relative.as_posix())
    if len(relative.parts) < 3 or relative.parts[:2] != ('sandbox', 'day03'):
        raise ValueError('Maintenance is restricted to sandbox/day03 copies')
    return f'VACUUM {_table_path(checked)} RETAIN {retention_hours} HOURS DRY RUN'


def _history(spark, path: Path) -> list[dict]:
    from delta.tables import DeltaTable
    rows = DeltaTable.forPath(spark, str(path)).history().collect()
    return json.loads(json.dumps([r.asDict(recursive=True) for r in rows], default=str))


def _state(spark, path: Path) -> dict:
    from delta.tables import DeltaTable
    frame = spark.read.format('delta').load(str(path))
    rows = canonical_rows(frame)
    return {'rows': len(rows), 'business_digest': rows_digest(rows),
            'version': int(DeltaTable.forPath(spark, str(path)).history(1).select('version').first()[0]),
            'schema': [(f.name, f.dataType.simpleString()) for f in frame.schema]}


def _new_copy(spark, work: Path, frame, label: str) -> Path:
    if not re.fullmatch(r'[a-z][a-z0-9_]{1,30}', label):
        raise ValueError('Unsafe sandbox label')
    target = workspace_path(work, 'sandbox/day03/' + label + '_' + uuid.uuid4().hex)
    frame.write.format('delta').mode('errorifexists').save(str(target))
    if canonical_rows(spark.read.format('delta').load(str(target))) != canonical_rows(frame):
        raise AssertionError('Independent sandbox copy does not match its input')
    return target


def _incoming(spark, source: Path, work: Path, filename: str, revision: int, *, land: bool = False):
    """Type the actual source using Spark, preserving source-file provenance."""
    from pyspark.sql import functions as F, types as T
    require_fixed_dataset(source)
    if filename not in {'correction.csv', 'schema_change.csv', 'quality_cases.csv'}:
        raise ValueError('Unsupported Day 3 source')
    if type(revision) is not int or revision < 1:
        raise ValueError('Revision must be a positive integer')
    path = Path(source) / filename
    with path.open(encoding='utf-8', newline='') as handle:
        header = next(csv.reader(handle))
    wanted = list(TRIP_FIELDS) + (['surcharge_sar'] if filename == 'schema_change.csv' else [])
    if header != wanted:
        raise ValueError('Unexpected source schema')
    schema = T.StructType([T.StructField(name, T.StringType(), True) for name in header])
    raw = (spark.read.schema(schema).option('header', True).option('enforceSchema', False)
           .option('mode', 'FAILFAST').csv(str(path)))
    receipt = (raw.withColumn('_source_file', F.lit(filename))
               .withColumn('_source_sha256', F.lit(digest_file(path)))
               .withColumn('_source_revision', F.lit(revision)))
    if land:
        target = workspace_path(work, 'mini_lakehouse/bronze/day03_corrections/' + uuid.uuid4().hex)
        receipt.withColumn('_ingested_at', F.current_timestamp()).write.format('delta').mode('errorifexists').save(str(target))
    trips = raw.select(F.trim('trip_id').alias('trip_id'), F.trim('driver_id').alias('driver_id'),
        _city(F.col('city')).alias('city'), _timestamp(F.col('start_ts')).alias('start_utc'),
        _timestamp(F.col('end_ts')).alias('end_utc'), _number(F.col('fare_sar')).alias('fare_sar'),
        _number(F.col('distance_km')).alias('distance_km'),
        *([_number(F.col('surcharge_sar')).alias('surcharge_sar')] if filename == 'schema_change.csv' else []))
    trips = (trips.withColumn('duration_seconds', F.col('end_utc').cast('long') - F.col('start_utc').cast('long'))
             .withColumn('trip_date_local', F.to_date(F.from_utc_timestamp('start_utc', 'Asia/Riyadh')))
             .withColumn('source_revision', F.lit(revision)))
    drivers = stage_frames(spark, work, base_snapshot=True)['stg_drivers']
    joined = trips.join(drivers, 'driver_id', 'left')
    if joined.count() != trips.count():
        raise AssertionError('Driver join multiplied correction rows')
    joined = (joined.withColumn('_source_file', F.lit(filename))
              .withColumn('_source_sha256', F.lit(digest_file(path)))
              .withColumn('_payload_hash', F.sha2(F.to_json(F.struct(*[F.col(n) for n in BUSINESS_FIELDS])), 256)))
    extras = ['surcharge_sar'] if filename == 'schema_change.csv' else []
    return joined.select(*BUSINESS_FIELDS, '_source_file', '_source_sha256', '_payload_hash', *extras)


def revision_merge_delta(spark, target: Path, incoming) -> dict:
    """Native MERGE; duplicate keys and same-revision conflicts fail explicitly."""
    from pyspark.sql import functions as F
    from delta.tables import DeltaTable
    current = spark.read.format('delta').load(str(target))
    if set(current.columns) != set(incoming.columns):
        raise ValueError('Explicit matching schemas are required before correction MERGE')
    for label, frame in [('target', current), ('source', incoming)]:
        if (frame.where(F.col('trip_id').isNull() | (F.trim('trip_id') == '')
                        | F.col('source_revision').isNull() | (F.col('source_revision') < 1)
                        | F.col('_payload_hash').isNull()).limit(1).count()
                or frame.groupBy('trip_id').count().where('count != 1').limit(1).count()):
            raise ValueError(label + ': keys/revisions/payload hashes must be valid and unique')
    overlap = current.alias('t').join(incoming.alias('s'), 'trip_id', 'inner')
    conflict = ((F.col('t.source_revision') == F.col('s.source_revision'))
                & ~F.col('t._payload_hash').eqNullSafe(F.col('s._payload_hash')))
    if overlap.where(conflict).limit(1).count():
        raise ValueError('Same-revision conflict; no correction was committed')
    (DeltaTable.forPath(spark, str(target)).alias('t')
     .merge(incoming.alias('s'), 't.trip_id = s.trip_id')
     .whenMatchedUpdateAll(condition='s.source_revision > t.source_revision')
     .whenNotMatchedInsertAll().execute())
    return _state(spark, target)


def _expected_write_rejection(spark, target: Path, action, kind: str) -> dict:
    """A random exception is not a successful negative test."""
    tokens = {'constraint': ('delta_violate_constraint', 'check constraint', 'invariantviolation'),
              'schema': ('schema mismatch', 'delta_schema_mismatch')}
    if kind not in tokens:
        raise ValueError('Unknown rejection class')
    before = _state(spark, target)
    try:
        action()
    except Exception as exc:
        text = (type(exc).__name__ + ': ' + str(exc)).lower()
        if not any(token in text for token in tokens[kind]):
            raise RuntimeError('Unexpected failure, not the intended ' + kind + ' rejection') from exc
        observed = {'kind': kind, 'exception_type': type(exc).__name__, 'message_excerpt': str(exc)[:500]}
    else:
        raise AssertionError('The invalid write unexpectedly succeeded')
    after = _state(spark, target)
    if before != after:
        raise AssertionError('A rejected write changed committed contents, version, or schema')
    return {**observed, 'before': before, 'after': after, 'committed_table_unchanged': True}


def _completed_day02(spark, source: Path, work: Path):
    require_fixed_dataset(source)
    _utc_session(spark)
    report = json.loads(workspace_path(work, 'reports/day02_silver.json').read_text())
    if (report.get('scope') != 'DAY02_SILVER_ENGINE' or report.get('engine_executed') is not True
            or report.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256
            or not report.get('checks') or not all(v is True for v in report['checks'].values())):
        raise ValueError('Actual verified Day 2 Silver is required')
    return workspace_path(work, 'mini_lakehouse/silver/trips')


def run_transactions_lab(spark, source: Path, work: Path) -> dict:
    """Lab 4a: correct trusted Silver; test constraints only on an isolated copy."""
    from pyspark.sql import functions as F
    target = _completed_day02(spark, source, work)
    expected = day03_reference(source)
    report_path = workspace_path(work, 'reports/day03_transactions.json')
    if report_path.exists():
        prior = json.loads(report_path.read_text())
        if (prior.get('scope') != 'DAY03_TRANSACTIONS_ENGINE' or prior.get('engine_executed') is not True
                or not prior.get('checks') or not all(v is True for v in prior['checks'].values())
                or canonical_rows(spark.read.format('delta').load(str(target))) != expected['expected_corrected_rows']):
            raise ValueError('Existing Day 3 report/state cannot be reused; preserve it for diagnosis')
        delta_artifacts(work, target)
        return {**prior, 'rerun_status': 'CURRENT_READBACK_RECHECKED_NO_HISTORICAL_RETEST'}
    before_rows = reference_result(source)['expected_silver_rows']
    if canonical_rows(spark.read.format('delta').load(str(target))) != before_rows:
        raise ValueError('Expected untouched Day 2 Silver. Preserve partial/later work; use a clean full pipeline run.')
    before = _state(spark, target)
    original = spark.read.format('delta').option('versionAsOf', before['version']).load(str(target))
    incoming = _incoming(spark, source, work, 'correction.csv', 2, land=True)
    if canonical_rows(incoming) != [expected['corrected_trip_after']]:
        raise AssertionError('Native correction differs from independent source calculation')
    after = revision_merge_delta(spark, target, incoming)
    if canonical_rows(spark.read.format('delta').load(str(target))) != expected['expected_corrected_rows']:
        raise AssertionError('Corrected Silver differs from the independent expectation')
    replay = revision_merge_delta(spark, target, incoming)
    stale = revision_merge_delta(spark, target, original)
    if not after['business_digest'] == replay['business_digest'] == stale['business_digest'] == expected['after']['digest']:
        raise AssertionError('Replay or stale redelivery changed the corrected business values')
    # An expected application-policy error is distinguished from engine constraints.
    conflict = incoming.withColumn('fare_sar', F.lit('24.00').cast('decimal(12,2)'))
    conflict = conflict.withColumn('_payload_hash', F.sha2(F.to_json(F.struct(*[F.col(n) for n in BUSINESS_FIELDS])), 256))
    conflict_before = _state(spark, target)
    try:
        revision_merge_delta(spark, target, conflict)
    except ValueError as exc:
        if 'Same-revision conflict' not in str(exc):
            raise
    else:
        raise AssertionError('A same-revision conflict was not rejected')
    if _state(spark, target) != conflict_before:
        raise AssertionError('Conflict precheck changed the target')
    past_rows = canonical_rows(spark.read.format('delta').option('versionAsOf', before['version']).load(str(target)))
    if past_rows != before_rows:
        raise AssertionError('The actual earlier Delta version is not preserved')
    trusted = spark.read.format('delta').load(str(target))
    sandbox = _new_copy(spark, work, trusted, 'constraints')
    spark.sql(f'ALTER TABLE {_table_path(sandbox)} ADD CONSTRAINT fare_nonnegative CHECK (fare_sar IS NOT NULL AND fare_sar >= 0)')
    spark.sql(f"ALTER TABLE {_table_path(sandbox)} ADD CONSTRAINT trip_id_present CHECK (trip_id IS NOT NULL AND length(trim(trip_id)) > 0)")
    bad = _incoming(spark, source, work, 'quality_cases.csv', 1).where("trip_id = 'SYN_BAD002'")
    good = trusted.where("trip_id = 'SYN_T0002'").withColumn('trip_id', F.lit('SYN_VALID_PROBE'))
    # Recompute the test probe's hash; both probes are transient, not source edits.
    good = good.withColumn('_payload_hash', F.sha2(F.to_json(F.struct(*[F.col(n) for n in BUSINESS_FIELDS])), 256))
    mixed = good.unionByName(bad)
    if mixed.count() != 2 or bad.count() != 1:
        raise AssertionError('Expected one valid and one negative-fare write probe')
    rejection = _expected_write_rejection(spark, sandbox,
        lambda: mixed.write.format('delta').mode('append').save(str(sandbox)), 'constraint')
    report = {'scope': 'DAY03_TRANSACTIONS_ENGINE', 'engine_executed': True,
        'run_id': uuid.uuid4().hex, 'spark_version': spark.version,
        'dataset_manifest_sha256': DATASET_MANIFEST_SHA256,
        'before': before, 'after_correction': after, 'after_replay': replay, 'after_stale_replay': stale,
        'past_version_read': before['version'], 'history': _history(spark, target),
        'constraint_probe': rejection, 'expected_final_fare_sar': expected['after']['fare_sar'],
        'artifacts': {'silver': delta_artifacts(work, target), 'constraints_copy': delta_artifacts(work, sandbox)},
        'checks': {'native_correction_matches_source_expectation': True, 'business_rows_stay_75': True,
                   'replay_and_stale_delivery_preserve_values': True, 'same_revision_conflict_rejected': True,
                   'actual_prior_version_read': True, 'mixed_valid_invalid_batch_rejected_atomically': True},
        'not_proven': ['concurrent writer stress', 'multi-table ACID', 'crash durability stress', 'cloud deployment']}
    write_json(report_path, report)
    return report


def run_maintenance_lab(spark, source: Path, work: Path) -> dict:
    """Lab 4b: approved schema evolution, compact, delete/restore and VACUUM dry run."""
    from pyspark.sql import functions as F
    from delta.tables import DeltaTable
    target = _completed_day02(spark, source, work)
    expected = day03_reference(source)
    prior = json.loads(workspace_path(work, 'reports/day03_transactions.json').read_text())
    if prior.get('scope') != 'DAY03_TRANSACTIONS_ENGINE' or prior.get('engine_executed') is not True or not prior.get('checks') or not all(v is True for v in prior['checks'].values()):
        raise ValueError('Complete native Lab 4a first')
    if spark.conf.get('spark.databricks.delta.schema.autoMerge.enabled', 'false').lower() != 'false':
        raise ValueError('Disable global auto-merge; this exercise approves one specific write')
    trusted = spark.read.format('delta').load(str(target))
    if canonical_rows(trusted) != expected['expected_corrected_rows']:
        raise ValueError('Trusted Silver no longer matches the completed correction')
    untouched = _state(spark, target)
    fixture = schema_fixture(source)
    # Omit one existing row from a NEW sandbox, then append its extended shape once.
    # This demonstrates schema evolution without teaching duplicate primary keys.
    extended = _incoming(spark, source, work, 'schema_change.csv', 1)
    if canonical_rows(extended) != [fixture['business_row']]:
        raise AssertionError('Schema fixture changed business fields')
    evolution = _new_copy(spark, work, trusted.where(F.col('trip_id') != fixture['trip_id']), 'schema')
    rejected = _expected_write_rejection(spark, evolution,
        lambda: extended.write.format('delta').mode('append').save(str(evolution)), 'schema')
    extended.write.format('delta').option('mergeSchema', 'true').mode('append').save(str(evolution))
    evolved = spark.read.format('delta').load(str(evolution))
    if (canonical_rows(evolved) != expected['expected_corrected_rows'] or evolved.count() != 75
            or evolved.where(F.col('surcharge_sar').isNull()).count() != 74
            or evolved.where(F.col('surcharge_sar') == F.lit('2.00').cast('decimal(12,2)')).count() != 1
            or evolved.groupBy('trip_id').count().where('count != 1').count()):
        raise AssertionError('Schema evolution did not preserve grain and business values')
    compact = _new_copy(spark, work, trusted.repartition(4), 'compact')
    dt = DeltaTable.forPath(spark, str(compact))
    detail_before = dt.detail().select('numFiles', 'sizeInBytes').first().asDict()
    optimization = [r.asDict(recursive=True) for r in dt.optimize().executeCompaction().collect()]
    detail_after = dt.detail().select('numFiles', 'sizeInBytes').first().asDict()
    if canonical_rows(spark.read.format('delta').load(str(compact))) != expected['expected_corrected_rows']:
        raise AssertionError('Compaction changed business contents')
    recovery = _new_copy(spark, work, trusted, 'recovery')
    recovery_before = _state(spark, recovery)
    rd = DeltaTable.forPath(spark, str(recovery))
    rd.delete("trip_id = 'SYN_T0001'")
    deleted = _state(spark, recovery)
    if deleted['rows'] != 74:
        raise AssertionError('DELETE should remove exactly the selected trip in the copy')
    old = spark.read.format('delta').option('versionAsOf', recovery_before['version']).load(str(recovery))
    if canonical_rows(old) != expected['expected_corrected_rows']:
        raise AssertionError('Pre-delete version is unavailable')
    rd.restoreToVersion(recovery_before['version']).collect()
    restored = _state(spark, recovery)
    if restored['business_digest'] != recovery_before['business_digest'] or restored['version'] <= deleted['version']:
        raise AssertionError('RESTORE must create a later commit with the original business content')
    before_dryrun = _state(spark, recovery)
    candidates = [r.asDict(recursive=True) for r in spark.sql(vacuum_dry_run_sql(work, recovery)).collect()]
    if _state(spark, recovery) != before_dryrun or _state(spark, target) != untouched:
        raise AssertionError('Read-only dry run or sandbox operations changed committed/trusted contents')
    report = {'scope': 'DAY03_MAINTENANCE_ENGINE', 'engine_executed': True,
        'run_id': uuid.uuid4().hex, 'spark_version': spark.version,
        'dataset_manifest_sha256': DATASET_MANIFEST_SHA256, 'schema_rejection': rejected,
        'evolved_rows': 75, 'surcharge_null_rows': 74, 'surcharge_nonnull_rows': 1,
        'optimize': {'before': detail_before, 'after': detail_after, 'metrics': optimization,
                     'speedup_claimed': False},
        'recovery': {'before': recovery_before, 'after_delete': deleted, 'after_restore': restored,
                     'history': _history(spark, recovery)},
        'vacuum': {'dry_run_only': True, 'retention_hours': 168, 'candidates': candidates,
                   'files_deleted_by_vacuum': 0},
        'trusted_silver': untouched,
        'artifacts': {name: delta_artifacts(work, path) for name, path in
                       [('schema_copy', evolution), ('compact_copy', compact), ('recovery_copy', recovery)]},
        'checks': {'unexpected_column_rejected': True, 'approved_evolution_preserves_business_values': True,
                   'compaction_preserves_values': True, 'delete_affects_copy_only': True,
                   'restore_creates_new_commit': True, 'vacuum_is_non_destructive_dry_run': True,
                   'trusted_silver_unchanged': True},
        'not_proven': ['actual expired-file vacuum deletion', 'performance gain', 'concurrent writer stress']}
    report = json.loads(json.dumps(report, default=str))
    write_json(workspace_path(work, 'reports/day03_maintenance_' + report['run_id'] + '.json'), report)
    write_json(workspace_path(work, 'reports/day03_maintenance_latest.json'), report)
    return report
