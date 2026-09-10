"""Continue the same cumulative workspace, or integrate from fresh sources."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.runtime import EnvironmentUnavailable,require_environment,start_spark,inspect_environment
from masar.workspace import completed_bronze_workspace,write_json,workspace_path
from masar.pipeline import dependency_preflight,run_pipeline
from masar.serving import run_recovery_exercise,run_serving_lab


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--part',choices=['gold','serve','all','integration'],default='all')
    parser.add_argument('--preflight',action='store_true')
    args=parser.parse_args();spark=None;work=None;code=0
    try:
        if args.preflight:
            result=dependency_preflight() if args.part=='integration' else inspect_environment()
            print(json.dumps(result,ensure_ascii=False,indent=2));return 2 if result['issues'] else 0
        if args.part=='integration':
            print(json.dumps(run_pipeline(ROOT),ensure_ascii=False,indent=2));return 0
        require_environment();work=completed_bronze_workspace(ROOT);spark=start_spark(work)
        result={}
        if args.part in {'gold','all'}:result['gold_recovery']=run_recovery_exercise(spark,ROOT/'data/masar-small-v1',work)
        if args.part in {'serve','all'}:result['serving']=run_serving_lab(spark,ROOT/'data/masar-small-v1',work)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except EnvironmentUnavailable as exc:
        print(json.dumps({'scope':'DAY05_NATIVE_ATTEMPT','status':'BLOCKED_DEPENDENCIES','engine_executed':False,
            'message':str(exc),'environment':inspect_environment()},ensure_ascii=False,indent=2));code=2
    except Exception as exc:
        result={'scope':'DAY05_NATIVE_ATTEMPT','status':'FAILED','engine_started':spark is not None,
            'complete_lab_success':False,'error_type':type(exc).__name__,'message':str(exc)}
        if work is not None:write_json(workspace_path(work,'reports/day05_failure_latest.json'),result)
        print(json.dumps(result,ensure_ascii=False,indent=2));code=1
    finally:
        if spark is not None:
            try:spark.stop()
            except Exception as exc:
                print(json.dumps({'status':'SPARK_STOP_FAILED','message':str(exc)}));code=1
    return code
if __name__=='__main__':raise SystemExit(main())
