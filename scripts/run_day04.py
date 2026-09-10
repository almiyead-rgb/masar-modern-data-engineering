"""Bounded native Day 4 runner. Missing prerequisites fail before any writes."""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.runtime import EnvironmentUnavailable,inspect_environment,require_environment,start_spark
from masar.streaming import stream_preflight,run_stream_lab
from masar.quality_gate import quality_preflight,run_quality_lab
from masar.workspace import completed_bronze_workspace,workspace_path,write_json


def preflight(part:str) -> dict:
    engine=inspect_environment()
    streaming=stream_preflight() if part in {'streaming','all'} else None
    quality=quality_preflight() if part in {'quality','all'} else None
    issues=engine['issues']+([] if streaming is None else streaming['issues'])+([] if quality is None else quality['issues'])
    return {'scope':'DAY04_PREFLIGHT_ONLY','engine_executed':False,'kafka_executed':False,'gx_executed':False,
            'engine':engine,'streaming':streaming,'quality':quality,'issues':issues,
            'status':'BLOCKED_DEPENDENCIES' if issues else 'PREFLIGHT_PASSED_ENGINE_NOT_TESTED'}


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--part',choices=['streaming','quality','all'],default='all')
    parser.add_argument('--preflight',action='store_true')
    args=parser.parse_args()
    spark=None;work=None;exit_code=0
    try:
        readiness=preflight(args.part)
        if args.preflight:
            print(json.dumps(readiness,indent=2))
            return 2 if readiness['issues'] else 0
        if readiness['issues']: raise EnvironmentUnavailable('; '.join(readiness['issues']))
        require_environment()
        work=completed_bronze_workspace(ROOT)
        spark=start_spark(work,kafka=args.part in {'streaming','all'})
        results={}
        if args.part in {'streaming','all'}: results['streaming']=run_stream_lab(spark,ROOT/'data/masar-small-v1',work)
        if args.part in {'quality','all'}: results['quality']=run_quality_lab(spark,ROOT/'data/masar-small-v1',work)
        print(json.dumps(results,ensure_ascii=False,indent=2))
    except EnvironmentUnavailable as exc:
        print(json.dumps({'scope':'DAY04_NATIVE_ATTEMPT','status':'BLOCKED_DEPENDENCIES',
            'engine_executed':False,'kafka_executed':False,'gx_executed':False,'error':str(exc),
            'preflight':preflight(args.part)},ensure_ascii=False,indent=2))
        exit_code=2
    except Exception as exc:
        result={'status':'FAILED','engine_started':spark is not None,'complete_lab_success':False,
                'error_type':type(exc).__name__,'message':str(exc)}
        if work is not None: write_json(workspace_path(work,'reports/day04_failure.json'),result)
        print(json.dumps(result,ensure_ascii=False,indent=2));exit_code=1
    finally:
        if spark is not None:
            try:spark.stop()
            except Exception as exc:
                print(json.dumps({'status':'SPARK_STOP_FAILED','message':str(exc)}));exit_code=1
    return exit_code

if __name__=='__main__':raise SystemExit(main())
