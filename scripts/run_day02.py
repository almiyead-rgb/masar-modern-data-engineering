"""Run authored native Day 2 labs after a successful Day 1 Bronze workspace."""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.runtime import inspect_environment, require_environment, start_spark, EnvironmentUnavailable
from masar.workspace import completed_bronze_workspace, workspace_path, write_json
from masar.silver import run_staging_lab, run_incremental_lab


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--part',choices=['staging','silver','all'],default='all')
    args=parser.parse_args()
    spark=None
    work=None
    try:
        require_environment()
        work=completed_bronze_workspace(ROOT)
        spark=start_spark(work)
        result={}
        if args.part in ('staging','all'):
            result['staging']=run_staging_lab(spark,ROOT/'data/masar-small-v1',work)
        if args.part in ('silver','all'):
            result['silver']=run_incremental_lab(spark,ROOT/'data/masar-small-v1',work)
        print(json.dumps(result,indent=2))
        return 0
    except EnvironmentUnavailable as exc:
        print(json.dumps({'status':'BLOCKED_DEPENDENCIES','error':str(exc),
                          'environment':inspect_environment(),'engine_executed':False},indent=2))
        return 2
    except Exception as exc:
        result={'status':'FAILED','error_type':type(exc).__name__,'message':str(exc),
                'engine_started':spark is not None,'complete_lab_success':False}
        if work is not None:
            write_json(workspace_path(work,'reports/day02_failure.json'),result)
        print(json.dumps(result,indent=2))
        return 1
    finally:
        if spark is not None:
            spark.stop()

if __name__=='__main__':
    raise SystemExit(main())
