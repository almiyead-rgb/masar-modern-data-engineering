"""Run native Lab 04 in the existing successfully completed Day 2 workspace."""
from pathlib import Path
import argparse
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.runtime import EnvironmentUnavailable, inspect_environment, require_environment, start_spark
from masar.workspace import completed_bronze_workspace, workspace_path, write_json
from masar.delta_lab import run_transactions_lab, run_maintenance_lab


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', choices=['transactions', 'maintenance', 'all'], default='all')
    args = parser.parse_args()
    spark, work = None, None
    exit_code = 0
    try:
        require_environment()
        work = completed_bronze_workspace(ROOT)
        spark = start_spark(work)
        result = {}
        if args.part in ('transactions', 'all'):
            result['transactions'] = run_transactions_lab(spark, ROOT / 'data/masar-small-v1', work)
        if args.part in ('maintenance', 'all'):
            result['maintenance'] = run_maintenance_lab(spark, ROOT / 'data/masar-small-v1', work)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except EnvironmentUnavailable as exc:
        print(json.dumps({'scope': 'DAY03_NATIVE_ATTEMPT', 'status': 'BLOCKED_DEPENDENCIES',
            'engine_executed': False, 'error': str(exc), 'environment': inspect_environment()}, indent=2))
        exit_code = 2
    except Exception as exc:
        result = {'status': 'FAILED', 'error_type': type(exc).__name__, 'message': str(exc),
                  'engine_started': spark is not None, 'complete_lab_success': False}
        if work is not None:
            write_json(workspace_path(work, 'reports/day03_failure.json'), result)
        print(json.dumps(result, indent=2))
        exit_code = 1
    finally:
        if spark is not None:
            try:
                spark.stop()
            except Exception as exc:
                print(json.dumps({'status': 'SPARK_STOP_FAILED', 'error': str(exc)}))
                exit_code = 1
    return exit_code

if __name__ == '__main__':
    raise SystemExit(main())
