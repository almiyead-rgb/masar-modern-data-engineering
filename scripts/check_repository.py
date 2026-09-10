"""Check the learner layout and optional file-backed runtime evidence."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import nbformat
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))


def code_digest(nb):
    return hashlib.sha256(json.dumps([c.source for c in nb.cells if c.cell_type=='code'],ensure_ascii=False).encode()).hexdigest()


def release_issues(root:Path,cfg:dict)->list[str]:
    """Publishing flags never replace saved execution evidence."""
    path=root/'docs/verification.json'; problems=[]
    if not path.is_file():
        return ['No independent full-course notebook execution record']
    report=json.loads(path.read_text())
    if report.get('status')!='PASSED' or report.get('independent_course_runs')!=2 or report.get('notebook_executions')!=10:
        problems.append('Missing two complete five-day executions')
    if report.get('dataset_manifest_sha256')!='20a7e45bed2980b9394c10e8532da3b9f40f614366bb2df26a88610253e768e3':
        problems.append('Wrong dataset in execution evidence')
    for day in range(1,6):
        nb=nbformat.read(root/f'day{day:02}/STUDENT.ipynb',4)
        record_path=root/f'day{day:02}/verification.json'
        if not record_path.is_file():
            problems.append(f'Missing Day {day} evidence');continue
        record=json.loads(record_path.read_text())
        if record.get('status')!='PASSED' or record.get('independent_course_runs')!=2:
            problems.append(f'Day {day}: incomplete native evidence')
        if record.get('code_sha256')!=code_digest(nb):
            problems.append(f'Day {day}: source changed after execution')
        if any(c.cell_type=='code' and c.source.strip() and (c.execution_count is None or any(o.get('output_type')=='error' for o in c.get('outputs',[]))) for c in nb.cells):
            problems.append(f'Day {day}: missing execution or failed cell')
    return problems


def inspect(root:Path=ROOT)->dict:
    root=Path(root).resolve();problems=[]
    spec=importlib.util.spec_from_file_location('student_layout',ROOT/'scripts/check_student_course.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    try:
        layout=module.inspect(root);problems.extend(layout['errors'])
    except Exception as exc:
        layout={};problems.append(str(exc))
    cfg=json.loads((root/'course.json').read_text())
    checks={'days':5,'hours_total':30,'labs_total':8,'cumulative_labs_are_final_project':True,
            'extra_final_project':False,'distinction_required':False,'paid_services_required':False}
    for field,expected in checks.items():
        if cfg.get(field)!=expected:
            problems.append(f'Course contract changed: {field}')
    if cfg.get('learner_notebooks')!=[f'day{d:02}/STUDENT.ipynb' for d in range(1,6)]:
        problems.append('Daily notebook registry differs from learning path')
    for forbidden in ('INSTRUCTOR_PACKAGE.md','instructor_only','MASAR_STUDENT.ipynb','DAY01_STUDENT.ipynb'):
        if (root/forbidden).exists():
            problems.append('Private or duplicate learner entry: '+forbidden)
    return {'passed':not problems,'issues':problems,'warnings':[],**{k:v for k,v in layout.items() if k not in ('errors','status')}}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--release',action='store_true');args=parser.parse_args()
    result=inspect()
    if args.release:
        result['issues'].extend(release_issues(ROOT,json.loads((ROOT/'course.json').read_text())))
        result['passed']=not result['issues']
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['passed'] else 1)
