"""Required image-build smoke: actual fixed-source Delta write/read; no broker needed.

This check prefetches the same Delta/Kafka JARs used by the notebooks. It does not
certify Kafka transport, dbt, GX, performance, the eight labs, or a teaching release.
"""
from pathlib import Path
import argparse
import csv
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.runtime import inspect_environment, require_environment, start_spark, EnvironmentUnavailable
from masar.workspace import new_workspace, workspace_path, require_fixed_dataset, rows_digest, write_json, digest_file
from masar.workbench import utc_now

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    work = new_workspace(ROOT, 'storage_smoke')
    report_path = args.report or workspace_path(work, 'reports/storage_smoke.json')
    if report_path.exists():
        raise FileExistsError('Do not overwrite an earlier smoke report')
    report = {'scope': 'BUILD_TIME_NATIVE_STORAGE_SMOKE', 'status': 'STARTED',
        'started_at_utc': utc_now(), 'engine_executed': False, 'checks': {},
        'environment': inspect_environment(), 'full_course_verified': False,
        'does_not_verify': ['Kafka broker/transport', 'GX', 'dbt', 'all eight labs', 'teaching release']}
    spark = None
    try:
        require_environment()
        source = ROOT / 'data/masar-small-v1'
        require_fixed_dataset(source)
        with (source / 'trips.csv').open(newline='', encoding='utf-8') as handle:
            expected = list(csv.DictReader(handle))
        spark = start_spark(work, kafka=True)
        frame = spark.read.option('header', True).option('inferSchema', False).option('mode', 'FAILFAST').csv(str(source / 'trips.csv'))
        target = workspace_path(work, 'mini_lakehouse/bronze/storage_smoke')
        frame.write.format('delta').mode('errorifexists').save(str(target))
        back = spark.read.format('delta').load(str(target))
        actual = [r.asDict() for r in back.collect()]
        from delta.tables import DeltaTable
        version = DeltaTable.forPath(spark, str(target)).history(1).first()['version']
        # Resolve the Kafka provider class without pretending a broker ran.
        loader = spark._jvm.java.lang.Thread.currentThread().getContextClassLoader()
        loader.loadClass('org.apache.spark.sql.kafka010.KafkaSourceProvider')
        files = sorted(target.rglob('*.parquet')) + sorted((target / '_delta_log').glob('*.json'))
        checks = {'rows_match_source': actual and rows_digest(actual) == rows_digest(expected),
            'source_keys_unique': len({r['trip_id'] for r in actual}) == len(expected),
            'initial_delta_version_zero': int(version) == 0,
            'actual_delta_and_parquet_files': bool(list(target.rglob('*.parquet'))) and bool(list((target/'_delta_log').glob('*.json'))),
            'kafka_provider_class_loaded': True}
        if not all(value is True for value in checks.values()):
            raise AssertionError('Native storage smoke failed: ' + str(checks))
        report.update(status='PASSED_NATIVE_STORAGE_SMOKE', engine_executed=True, checks=checks,
            source_rows=len(expected), observed_rows=len(actual), business_digest=rows_digest(actual),
            delta_version=int(version), spark_version=spark.version,
            file_evidence=[{'path': str(p), 'sha256': digest_file(p)} for p in files])
    except EnvironmentUnavailable as exc:
        report.update(status='BLOCKED_DEPENDENCIES', error=str(exc))
    except Exception as exc:
        report.update(status='FAILED', engine_started=spark is not None,
                      error_type=type(exc).__name__, error=str(exc))
    finally:
        if spark is not None:
            try:
                spark.stop()
            except Exception as exc:
                report.update(status='FAILED_SHUTDOWN', error=str(exc))
        report['finished_at_utc'] = utc_now()
        write_json(report_path, report)
    print(json.dumps({'status': report['status'], 'report': str(report_path),
        'engine_executed': report['engine_executed'], 'full_course_verified': False}, indent=2))
    return 0 if report['status'] == 'PASSED_NATIVE_STORAGE_SMOKE' else (2 if report['status']=='BLOCKED_DEPENDENCIES' else 1)

if __name__ == '__main__':
    raise SystemExit(main())
