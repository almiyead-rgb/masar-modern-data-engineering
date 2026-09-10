"""Actual dbt-spark session runner for Lab 03, with isolated Delta tables.

No CSV/SQLite/reference-only fallback is permitted.
Every dbt command runs serially in the same process as the real Spark session.
The final report remains separate from full-course teaching acceptance.
"""
from __future__ import annotations

from contextlib import contextmanager, redirect_stdout, redirect_stderr, nullcontext
from masar.dbt_catalog import structured_spark_catalog
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
from typing import Iterator

from masar.runtime import inspect_environment, start_spark, EnvironmentUnavailable, PINNED
from masar.workspace import (new_workspace, workspace_path, require_fixed_dataset,
    write_json, digest_file, rows_digest, completed_bronze_workspace,
    DATASET_MANIFEST_SHA256, MARKER)

DBT_PINS = {'dbt-core': '1.9.8', 'dbt-spark': '1.9.1'}
PROJECT = 'masar_day02_design'
MODEL_NAMES = {'stg_trips', 'stg_drivers', 'stg_gps', 'int_trip_candidates',
               'silver_trips', 'mart_city_daily'}
PREMERGE_TEST_NAMES = {'assert_stage_contract', 'assert_no_same_revision_conflicts',
    'assert_driver_relationship', 'assert_ingestion_contract', 'assert_dimension_and_gps_contract'}
ALL_TEST_NAMES = PREMERGE_TEST_NAMES | {'assert_mart_reconciliation', 'assert_mart_key'}
SOURCE_NAMES = {'trips', 'drivers', 'gps_events'}


def inspect_dbt_environment() -> dict:
    report = inspect_environment()
    report['scope'] = 'DBT_DEPENDENCY_PREFLIGHT_ONLY'
    report['dbt_executed'] = False
    for name, version in DBT_PINS.items():
        try:
            actual = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            actual = None
        report['packages'][name] = {'required': version, 'observed': actual}
        if actual != version:
            report['issues'].append(f'{name}: required {version}, observed {actual}')
    report['status'] = ('BLOCKED_DEPENDENCIES' if report['issues']
                        else 'DEPENDENCIES_PRESENT_ENGINE_NOT_TESTED')
    return report


def identifier(value: str) -> str:
    """Only generated safe catalog names are interpolated into SQL."""
    if not isinstance(value, str) or not re.fullmatch(r'[a-z][a-z0-9_]{0,62}', value):
        raise ValueError('Invalid SQL identifier')
    return value


def sql_path(path: Path) -> str:
    text = str(Path(path).resolve())
    if any(char in text for char in "'\\\n\r\x00"):
        raise ValueError('The workspace path contains an unsupported SQL-literal character')
    return "'" + text + "'"


@contextmanager
def process_environment(values: dict[str, str]) -> Iterator[None]:
    """Restore every setting, including previously absent variables."""
    previous = {name: os.environ.get(name) for name in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def _json_file(path: Path) -> dict:
    if not path.is_file() or path.is_symlink() or path.stat().st_size == 0:
        raise ValueError('Missing, empty, or symlinked dbt artifact: ' + path.name)
    content = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(content, dict):
        raise ValueError('dbt artifact must contain an object')
    return content


def validate_dbt_artifacts(target: Path, *, models: set[str] | None = None,
                           tests: set[str] | None = None, freshness: bool = False) -> dict:
    """Validate saved native artifact shape and coverage, not just exit code.

    This verifier can be unit-tested with synthetic artifacts; that does NOT
    imply dbt ran. The native runner only calls it after a real successful invoke.
    """
    if not target.is_dir() or target.is_symlink():
        raise ValueError('Expected a real dbt target directory')
    name = 'sources.json' if freshness else 'run_results.json'
    result = _json_file(target / name)
    invocation = result.get('metadata', {}).get('invocation_id')
    if not isinstance(invocation, str) or not invocation.strip():
        raise ValueError('Missing dbt invocation identity')
    rows = result.get('results')
    if not isinstance(rows, list) or not rows:
        raise ValueError('No actual dbt result rows')
    ids = [r.get('unique_id') for r in rows if isinstance(r, dict)]
    if len(ids) != len(rows) or any(not isinstance(x, str) for x in ids) or len(set(ids)) != len(ids):
        raise ValueError('Invalid or duplicate dbt result identities')
    allowed = {'pass', 'warn'} if freshness else {'pass', 'success'}
    if any(r.get('status') not in allowed for r in rows):
        raise ValueError('A required dbt result is not successful')
    if freshness:
        required = {f'source.{PROJECT}.bronze.{n}' for n in SOURCE_NAMES}
        if set(ids) != required:
            raise ValueError('Freshness must cover all three Bronze sources')
        for row in rows:
            if row.get('max_loaded_at') is None or row.get('snapshotted_at') is None:
                raise ValueError('Freshness lacks an observed source timestamp')
    else:
        manifest = _json_file(target / 'manifest.json')
        if manifest.get('metadata', {}).get('invocation_id') != invocation:
            raise ValueError('Manifest/result invocation mismatch')
        nodes = manifest.get('nodes', {})
        if not isinstance(nodes, dict) or any(i not in nodes for i in ids):
            raise ValueError('Result nodes are not present in the matching manifest')
        for row in rows:
            kind = nodes[row['unique_id']].get('resource_type')
            if kind in {'model','test'} and row['status'] != ('success' if kind == 'model' else 'pass'):
                raise ValueError('dbt node kind/status mismatch')
        actual_models = {nodes[i].get('name') for i in ids if nodes[i].get('resource_type') == 'model'}
        actual_tests = {nodes[i].get('name') for i in ids if nodes[i].get('resource_type') == 'test'}
        if not (models or set()) <= actual_models or not (tests or set()) <= actual_tests:
            raise ValueError('Required dbt models/tests were skipped or not selected')
    paths = [name] if freshness else ['manifest.json', name]
    return {'invocation_id': invocation, 'results': len(rows),
            'warning_count': sum(r['status'] == 'warn' for r in rows),
            'artifacts': [{'name': n, 'sha256': digest_file(target / n)} for n in paths]}


def _copy_bronze(spark, source: Path, original: Path, work: Path) -> dict:
    from pyspark.sql import functions as F
    from delta.tables import DeltaTable
    from masar.bronze import verify_bronze
    for feed in ('trips', 'drivers', 'gps_events'):
        old = workspace_path(original, 'mini_lakehouse/bronze/' + feed)
        if not DeltaTable.isDeltaTable(spark, str(old)):
            raise ValueError('The input must be an actual Day 1 Delta table')
        # Explicit snapshots exclude later corrections/quality experiments.
        raw = (spark.read.format('delta').option('versionAsOf', 1 if feed == 'trips' else 0)
               .load(str(old)))
        new = workspace_path(work, 'mini_lakehouse/bronze/' + feed)
        raw.where(F.col('_batch_id') == 'base_001').write.format('delta').mode('errorifexists').save(str(new))
        if feed == 'trips':
            raw.where(F.col('_batch_id') == 'replay_002').write.format('delta').mode('append').save(str(new))
    # Check all payloads and metadata against fixed files after the actual copy.
    # _ingested_at is deliberately NOT reset to the copy time.
    return verify_bronze(spark, source, work)


def _append_trips(spark, source: Path, work: Path, filename: str, batch_id: str) -> None:
    from pyspark.sql import types as T, functions as F
    from masar.silver_reference import TRIP_FIELDS
    if filename not in {'late_trips.csv', 'trips.csv', 'correction.csv'}:
        raise ValueError('Unsupported dbt scenario file')
    identifier(batch_id)
    path = workspace_path(work, 'mini_lakehouse/bronze/trips')
    if spark.read.format('delta').load(str(path)).where(F.col('_batch_id') == batch_id).limit(1).count():
        raise ValueError('Batch already applied')
    schema = T.StructType([T.StructField(name, T.StringType(), True) for name in TRIP_FIELDS])
    raw = (spark.read.schema(schema).option('header', True).option('enforceSchema', False)
           .option('mode', 'FAILFAST').csv(str(source / filename)))
    expected = {'late_trips.csv': 3, 'trips.csv': 72, 'correction.csv': 1}[filename]
    if raw.count() != expected:
        raise ValueError('Scenario input count changed')
    (raw.withColumn('_source_file', F.lit(filename))
        .withColumn('_source_sha256', F.lit(digest_file(source / filename)))
        .withColumn('_batch_id', F.lit(batch_id))
        .withColumn('_ingested_at', F.current_timestamp())
        .write.format('delta').mode('append').save(str(path)))


def _invoke(project: Path, work: Path, phase: str, command: list[str], seen: set[str],
            *, models: set[str] | None = None, tests: set[str] | None = None,
            freshness: bool = False, docs: bool = False, reprocess_all: bool = False) -> dict:
    from dbt.cli.main import dbtRunner
    identifier(phase)
    folder = workspace_path(work, 'dbt/commands/' + phase)
    folder.mkdir(parents=True, exist_ok=False)
    target = folder / 'target'
    arguments = ['--no-use-colors', '--no-partial-parse', '--log-path', str(folder / 'logs'),
        *command, '--project-dir', str(project), '--profiles-dir', str(project / 'profiles'),
        '--target-path', str(target), '--vars', json.dumps({'reprocess_all': reprocess_all})]
    # Never use shell=True; all arguments and output paths are bounded.
    with (folder / 'console.log').open('w', encoding='utf-8') as log:
        with redirect_stdout(log), redirect_stderr(log), (structured_spark_catalog() if docs else nullcontext()):
            outcome = dbtRunner().invoke(arguments)
    if outcome.success is not True or outcome.exception is not None:
        raise RuntimeError('dbt command failed: ' + phase + '; inspect its saved console/dbt artifacts')
    if docs:
        catalog = _json_file(target / 'catalog.json')
        nodes = catalog.get('nodes', {})
        if not {f'model.{PROJECT}.{n}' for n in MODEL_NAMES} <= set(nodes):
            raise ValueError('Generated dbt catalog does not cover the required models')
        required_sources = {f'source.{PROJECT}.bronze.{n}' for n in SOURCE_NAMES}
        if not required_sources <= set(catalog.get('sources', {})):
            raise ValueError('Generated dbt catalog does not cover the three actual sources')
        checked = {'catalog_sha256': digest_file(target / 'catalog.json'),
                   'models_documented': len(nodes), 'sources_documented': len(catalog['sources']),
                   'metadata_method': 'native DESCRIBE TABLE EXTENDED'}
    else:
        checked = validate_dbt_artifacts(target, models=models, tests=tests, freshness=freshness)
        if checked['invocation_id'] in seen:
            raise ValueError('A stale dbt invocation was reused')
        seen.add(checked['invocation_id'])
    checked.update({'phase': phase, 'command': command,
                    'target': target.relative_to(work).as_posix()})
    return checked


def run_dbt_lab(root: Path, *, include_correction: bool = False,
                reprocess_all: bool = False) -> tuple[dict, Path]:
    """Create one immutable-attempt workspace and retain failure as well as success.

    Ordinary Lab 03: base -> rerun -> late -> late replay (75 trips).
    --include-correction only extends runtime QA using the existing Day 3 file.
    """
    root = Path(root).resolve()
    source = root / 'data/masar-small-v1'
    work = new_workspace(root, 'dbt_validation')
    target_report = workspace_path(work, 'reports/dbt_attempt.json')
    identity = json.loads((work / MARKER).read_text())['run_id']
    from masar.release_evidence import implementation_digest
    report = {'process_id': os.getpid(), 'implementation_sha256': implementation_digest(root),
              'scope': 'DBT_RUNTIME_ATTEMPT', 'status': 'STARTED', 'run_id': identity,
              'started_at': datetime.now(timezone.utc).isoformat(), 'engine_executed': False,
              'dbt_executed': False, 'dataset_manifest_sha256': DATASET_MANIFEST_SHA256,
              'complete_course_verified': False, 'commands': [], 'phases': [],
              'include_correction': include_correction, 'reprocess_all': reprocess_all,
              'environment': inspect_dbt_environment()}
    write_json(target_report, report)
    spark = None
    try:
        require_fixed_dataset(source)
        if report['environment']['issues']:
            raise EnvironmentUnavailable('; '.join(report['environment']['issues']))
        original = completed_bronze_workspace(root)
        input_report = _json_file(workspace_path(original, 'reports/bronze.json'))
        if input_report.get('spark_version') != PINNED['pyspark']:
            raise ValueError('Day 1 Bronze must be rebuilt in the unified runtime, not an earlier candidate')
        report['input_workspace'] = original.relative_to(root).as_posix()
        report['input_bronze_report_sha256'] = digest_file(workspace_path(original, 'reports/bronze.json'))
        spark = start_spark(work)
        spark.range(1).count()  # An action, not merely a session object.
        report['engine_executed'] = True
        report['source_copy'] = _copy_bronze(spark, source, original, work)
        # The project and its profile are copied, not modified in the source tree.
        project = workspace_path(work, 'dbt/project')
        shutil.copytree(root / 'day02/dbt', project,
                        ignore=shutil.ignore_patterns('target', 'logs', 'dbt_packages', '__pycache__'))
        bronze_schema = identifier('masar_bronze_' + identity[:16])
        target_schema = identifier('masar_dbt_' + identity[:16])
        for name in (bronze_schema, target_schema):
            location = workspace_path(work, 'dbt/catalog/' + name)
            spark.sql(f'CREATE DATABASE `{name}` LOCATION {sql_path(location)}')
        for feed in SOURCE_NAMES:
            location = workspace_path(work, 'mini_lakehouse/bronze/' + feed)
            spark.sql(f'CREATE TABLE `{bronze_schema}`.`{feed}` USING DELTA LOCATION {sql_path(location)}')
        from delta.tables import DeltaTable
        from masar.silver_reference import reference_result
        from masar.silver import canonical_rows, delta_artifacts
        expected = reference_result(source)['expected_silver_rows']
        phase_inputs = [('base', None), ('rerun', None), ('late', 'late_trips.csv'),
                        ('late_replay', 'late_trips.csv')]
        if include_correction:
            phase_inputs.extend([('correction', 'correction.csv'), ('correction_replay', 'correction.csv'),
                                 ('stale_replay', 'trips.csv')])
        seen = set()
        with process_environment({'MASAR_DBT_SCHEMA': target_schema,
                'MASAR_DBT_BRONZE_SCHEMA': bronze_schema, 'DBT_SEND_ANONYMOUS_USAGE_STATS': 'false',
                'DBT_PARTIAL_PARSE': 'false', 'DO_NOT_TRACK': '1'}):
            for name, filename in phase_inputs:
                if filename:
                    _append_trips(spark, source, work, filename, 'dbt_' + name)
                    spark.catalog.refreshTable(bronze_schema + '.trips')
                for suffix, cmd, models, tests, freshness in [
                    ('stage', ['run', '--select', 'path:models/staging'], {'stg_trips','stg_drivers','stg_gps'}, None, False),
                    ('gate', ['test', '--select', 'tag:premerge', '--indirect-selection', 'eager'], None, PREMERGE_TEST_NAMES, False),
                    ('freshness', ['source', 'freshness'], None, None, True),
                    ('build', ['build'], MODEL_NAMES, ALL_TEST_NAMES, False)]:
                    evidence = _invoke(project, work, name+'_'+suffix, cmd, seen, models=models,
                        tests=tests, freshness=freshness, reprocess_all=reprocess_all)
                    report['commands'].append(evidence)
                    report['dbt_executed'] = True
                    write_json(target_report, report)
                frame = spark.table(target_schema + '.silver_trips')
                rows = canonical_rows(frame)
                wanted = expected
                if name in {'base','rerun'}:
                    wanted = [r for r in expected if not r['trip_id'].startswith('SYN_LATE')]
                if name in {'correction','correction_replay','stale_replay'}:
                    from masar.delta_reference import day03_reference
                    wanted = day03_reference(source)['expected_corrected_rows']
                if rows != wanted:
                    raise AssertionError('Native dbt output differs from the independent fixed-source reference')
                actual_delta = spark.sql(f'DESCRIBE DETAIL `{target_schema}`.`silver_trips`').first().asDict()
                from urllib.parse import urlparse, unquote
                location = Path(unquote(urlparse(actual_delta['location']).path))
                if not location.resolve().is_relative_to(work):
                    raise ValueError('dbt created a Delta table outside its isolated workspace')
                artifacts = delta_artifacts(work, location)
                snapshot = workspace_path(work, 'reports/dbt_' + name + '_business_rows.json')
                write_json(snapshot, {'rows':rows, 'digest':rows_digest(rows)})
                # The SQL reconciliation test covers the mart; read it too.
                mart = [r.asDict() for r in spark.table(target_schema+'.mart_city_daily').orderBy('trip_date_local','city').collect()]
                fare = sum(r['total_fare_sar'] for r in mart)
                if sum(r['trip_count'] for r in mart) != len(rows):
                    raise AssertionError('Mart trip count changed')
                from decimal import Decimal
                if fare != sum(Decimal(r['fare_sar']) for r in rows):
                    raise AssertionError('Mart fare total changed')
                report['phases'].append({'phase':name,'rows':len(rows),'total_fare_sar':str(fare),
                    'business_digest':rows_digest(rows),'snapshot':snapshot.relative_to(work).as_posix(),
                    'snapshot_sha256':digest_file(snapshot),'delta_version':int(DeltaTable.forName(spark,target_schema+'.silver_trips').history(1).select('version').first()[0]),
                    'delta_artifacts':artifacts})
                write_json(target_report, report)
            report['commands'].append(_invoke(project, work, 'documentation', ['docs','generate'], seen, docs=True))
        report['status'] = 'PASSED_DBT_NATIVE'
    except EnvironmentUnavailable as exc:
        report.update(status='BLOCKED_DEPENDENCIES', error=str(exc))
    except Exception as exc:
        report.update(status='FAILED', error_type=type(exc).__name__, error=str(exc))
    finally:
        if spark is not None:
            try:
                spark.stop()
            except Exception as exc:
                report.update(status='FAILED', shutdown_error=str(exc))
        report['finished_at'] = datetime.now(timezone.utc).isoformat()
        write_json(target_report, report)
    return report, target_report
