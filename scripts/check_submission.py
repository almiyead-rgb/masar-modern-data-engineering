"""Inspect a learner's accumulated submission; never award a grade."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.submission import audit_submission

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--submission',required=True,type=Path)
    parser.add_argument('--workspace',required=True,type=Path)
    args=parser.parse_args()
    result=audit_submission(args.submission,args.workspace)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='NEEDS_REVIEW' else 2
if __name__=='__main__':raise SystemExit(main())
