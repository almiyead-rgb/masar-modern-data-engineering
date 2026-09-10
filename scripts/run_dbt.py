"""Run the Lab 03 dbt component in one shared local Spark process.
No installation, remote creation, publishing, or fallback execution occurs here.
"""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.dbt_lab import inspect_dbt_environment, run_dbt_lab


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preflight',action='store_true',help='Inspect dependencies only; never an engine proof')
    parser.add_argument('--include-correction',action='store_true',help='Later-day runtime QA with the existing correction fixture')
    parser.add_argument('--reprocess-all',action='store_true',help='Review all ingestion history while preserving revision precedence')
    args=parser.parse_args()
    if args.preflight:
        report=inspect_dbt_environment()
        print(json.dumps(report,indent=2))
        return 2 if report['issues'] else 0
    report,path=run_dbt_lab(ROOT,include_correction=args.include_correction,reprocess_all=args.reprocess_all)
    print(json.dumps({'status':report['status'],'engine_executed':report['engine_executed'],
        'dbt_executed':report['dbt_executed'],'attempt_report':str(path.relative_to(ROOT)),
        'phases_completed':len(report['phases']),'error':report.get('error')},indent=2))
    return 0 if report['status']=='PASSED_DBT_NATIVE' else (2 if report['status']=='BLOCKED_DEPENDENCIES' else 1)

if __name__=='__main__':
    raise SystemExit(main())
