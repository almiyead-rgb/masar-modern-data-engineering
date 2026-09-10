"""Local end-to-end QA: two fresh source copies, original engines and dbt, then notebooks.

No alternative engine, fabricated output, automatic VERIFIED flags, GitHub calls,
publication, deletion of learner data, or extra student assignment is permitted.
"""
from pathlib import Path
import json
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from masar.pipeline import dependency_preflight
from masar.dbt_lab import inspect_dbt_environment, validate_dbt_artifacts, MODEL_NAMES, ALL_TEST_NAMES
from masar.release_evidence import _native_run, INVENTORY
from masar.workbench import copy_source, run_logged, utc_now
from masar.workspace import write_json, digest_file, DATASET_MANIFEST_SHA256


def descriptor(root: Path, path: Path) -> dict:
    return {'path': path.relative_to(root).as_posix(), 'sha256': digest_file(path)}

def read_native_result(root: Path) -> dict:
    found = list((root/'outputs').glob('integration_*/reports/integration.json'))
    if len(found)!=1:
        raise ValueError('Exactly one completed native integration report is required per fresh copy')
    path=found[0]; report=json.loads(path.read_text()); work=path.parent.parent
    item={'workspace': work.relative_to(root).as_posix(), 'run_id':report.get('run_id'),
        'report':descriptor(root,path),'inventory':descriptor(root,work/INVENTORY)}
    return _native_run(root,item)

def read_dbt_result(root: Path) -> dict:
    found=list((root/'outputs').glob('dbt_validation_*/reports/dbt_attempt.json'))
    if len(found)!=1:
        raise ValueError('Exactly one actual dbt attempt is required')
    path=found[0];report=json.loads(path.read_text()); work=path.parent.parent
    expected=['base','rerun','late','late_replay','correction','correction_replay','stale_replay']
    if (report.get('status')!='PASSED_DBT_NATIVE' or report.get('engine_executed') is not True
        or report.get('dbt_executed') is not True or [p['phase'] for p in report.get('phases',[])]!=expected):
        raise ValueError('dbt scenarios have not all passed')
    expected_commands={name+'_'+suffix for name in expected for suffix in ['stage','gate','freshness','build']}|{'documentation'}
    if {c.get('phase') for c in report.get('commands',[])}!=expected_commands or len(report['commands'])!=len(expected_commands):
        raise ValueError('dbt command sequence is incomplete')
    invocations=set()
    for command in report['commands']:
        relative=Path(command['target'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe dbt target path')
        destination=work/relative
        if command['phase']=='documentation':
            if digest_file(destination/'catalog.json')!=command['catalog_sha256']:
                raise ValueError('dbt documentation changed')
            continue
        fresh=command['phase'].endswith('_freshness')
        full=command['phase'].endswith('_build')
        result=validate_dbt_artifacts(destination,models=MODEL_NAMES if full else None,
            tests=ALL_TEST_NAMES if full else None,freshness=fresh)
        if result['invocation_id'] in invocations or result['invocation_id']!=command['invocation_id'] or result['artifacts']!=command['artifacts']:
            raise ValueError('dbt command artifacts changed or reused an invocation')
        invocations.add(result['invocation_id'])
    # The native runner validates command artifacts. Recheck persisted business
    # snapshots too, rather than accepting only its final status string.
    from masar.workspace import rows_digest
    digests={}
    for phase in report['phases']:
        relative=Path(phase['snapshot'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe dbt snapshot path')
        snapshot=work/relative
        if snapshot.is_symlink() or digest_file(snapshot)!=phase['snapshot_sha256']:
            raise ValueError('dbt snapshot missing or changed')
        data=json.loads(snapshot.read_text())
        if rows_digest(data['rows'])!=phase['business_digest'] or data['digest']!=phase['business_digest']:
            raise ValueError('dbt business digest is inconsistent')
        digests[phase['phase']]=phase['business_digest']
    return {'run_id':report['run_id'],'process_id':report['process_id'],
        'business_digests':digests,'report':descriptor(root,path)}

def main() -> int:
    parent=ROOT/'outputs'
    if parent.is_symlink():
        raise ValueError('Outputs cannot be a symlink')
    parent.mkdir(exist_ok=True)
    audit=Path(tempfile.mkdtemp(prefix='native_acceptance_',dir=parent))
    report={'scope':'LOCAL_NATIVE_ACCEPTANCE_ATTEMPT','status':'STARTED',
        'started_at_utc':utc_now(),'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
        'runs':[], 'notebooks':None,'engine_executed':False,'dbt_executed':False,
        'teaching_approved':False,'published':False}
    target=audit/'acceptance.json'
    try:
        parts={'pipeline':dependency_preflight(),'dbt':inspect_dbt_environment()}
        report['preflight']=parts
        issues=[i for p in parts.values() for i in p['issues']]
        if issues:
            report.update(status='BLOCKED_DEPENDENCIES',issues=issues)
            return_code=2
        else:
            for number in (1,2):
                copy=audit/f'run_{number}'
                copy_source(ROOT,copy)
                record={'copy':copy.relative_to(ROOT).as_posix(),'commands':[],'status':'RUNNING'}
                report['runs'].append(record);write_json(target,report)
                for name,args in [('pipeline',['scripts/run_day05.py','--part','integration']),
                                  ('dbt',['scripts/run_dbt.py','--include-correction'])]:
                    outcome=run_logged([sys.executable,*args],cwd=copy,log=audit/f'run_{number}_{name}.log')
                    record['commands'].append(outcome);write_json(target,report)
                    if outcome['returncode']!=0:
                        raise RuntimeError(f'Run {number} {name} failed; see its preserved log')
                    if name=='pipeline':
                        record['native']=read_native_result(copy)
                        report['engine_executed']=True
                    else:
                        record['dbt']=read_dbt_result(copy)
                        report['dbt_executed']=True
                    write_json(target,report)
                record['status']='PASSED_NATIVE_AND_DBT'
                report['engine_executed']=report['dbt_executed']=True
                write_json(target,report)
            first,second=report['runs']
            for component,key in [('native','table_digests'),('dbt','business_digests')]:
                a,b=first[component],second[component]
                if a[key]!=b[key] or a['run_id']==b['run_id'] or a['process_id']==b['process_id']:
                    raise ValueError('Repeated native results differ or process identities are not independent')
            # Student notebooks must execute too, not just shared module functions.
            copy=audit/'notebook_copy';copy_source(ROOT,copy)
            write_json(copy/'.native-notebook-copy.json',{'purpose':'isolated native notebook execution'})
            result=run_logged([sys.executable,'scripts/execute_engine_notebooks.py'],cwd=copy,
                log=audit/'native_notebooks.log',timeout=10800)
            report['notebook_command']=result
            if result['returncode']!=0:
                raise RuntimeError('Native notebook execution failed; source notebooks remain unmodified')
            notebook_report=copy/'outputs/native_notebook_execution/summary.json'
            info=json.loads(notebook_report.read_text())
            if info.get('status')!='EXECUTED_PENDING_REVIEW' or len(info.get('notebooks',[]))!=10:
                raise ValueError('Ten executed native notebooks are required')
            report['notebooks']=descriptor(ROOT,notebook_report)
            report['status']='PASSED_RUNTIME_CHECKS_PENDING_RELEASE_REVIEW'
            return_code=0
    except Exception as exc:
        report.update(status='FAILED',error_type=type(exc).__name__,error=str(exc))
        return_code=1
    finally:
        report['finished_at_utc']=utc_now();write_json(target,report)
    print(json.dumps({'status':report['status'],'runs_completed':sum(r.get('status')=='PASSED_NATIVE_AND_DBT' for r in report['runs']),
        'report':target.relative_to(ROOT).as_posix(),'teaching_approved':False,'published':False},indent=2))
    return return_code

if __name__=='__main__':
    raise SystemExit(main())
