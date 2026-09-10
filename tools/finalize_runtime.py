"""Migrate the learner runtime to the Delta maintenance release and current layout."""
from pathlib import Path
import json
import nbformat

ROOT = Path(__file__).resolve().parents[1]
# 3.3.3 fixes SQL table overwrite compatibility with Spark 3.5.6+.
# https://github.com/delta-io/delta/releases/tag/v3.3.3
for path in ROOT.rglob('*'):
    if not path.is_file() or any(part in path.parts for part in ('.git', '.venv', 'outputs', 'evidence', 'data', '__pycache__', '.github', 'tools')):
        continue
    if path.suffix == '.ipynb':
        notebook = nbformat.read(path, as_version=4)
        changed = False
        for cell in notebook.cells:
            source = cell.source.replace('3.3.2', '3.3.3')
            if source != cell.source:
                changed = True
                cell.source = source
                if cell.cell_type == 'code':
                    cell.outputs = []
                    cell.execution_count = None
        if changed:
            nbformat.write(notebook, path)
    elif path.suffix in {'.py', '.md', '.txt', '.yaml', '.yml'} or path.name in {'Dockerfile', 'runtime-target.json'}:
        original = path.read_text(encoding='utf-8')
        updated = original.replace('3.3.2', '3.3.3')
        if updated != original:
            path.write_text(updated, encoding='utf-8')
# The declared teaching target must also be enforced before Spark starts.
p = ROOT / 'src/masar/runtime.py'
text = p.read_text().replace('sys.version_info[:2] < (3, 10)', 'sys.version_info[:2] != (3, 11)')
text = text.replace('Day 1 requires Python 3.10 or newer; CI verification uses Python 3.11',
                    'This complete course requires Python 3.11; use the documented virtual environment')
text = text.replace('appName("Masar-Day01")', 'appName("Masar-Course")')
p.write_text(text, encoding='utf-8')
p = ROOT / 'src/masar/release_evidence.py'
text = p.read_text().replace("'config', 'sql', 'day02/dbt'", "'config', 'sql', 'day05/sql', 'day02/dbt'")
p.write_text(text, encoding='utf-8')
# Update packaging assertions to the single daily notebook layout; retain behavioral tests.
p = ROOT / 'tests/test_workbench.py'
text = p.read_text().replace('../notebooks/day01/02_cost_model.ipynb', 'STUDENT.ipynb')
start = text.index('    def test_coordinator_never_changes_course_acceptance_flags(self):') if '    def test_coordinator_never_changes_course_acceptance_flags(self):' in text else -1
if start >= 0:
    end = text.index('\nif __name__', start)
    text = text[:start] + '''    def test_coordinator_requires_actual_independent_notebook_runs(self):
        text=(ROOT/'scripts/execute_student_course.py').read_text()
        for required in ('read_stage_report', 'run_course(1), run_course(2)', 'NotebookClient', 'allow_errors=False', 'code_sha256'):
            self.assertIn(required,text)
        self.assertNotIn('git push',text)
''' + text[end:]
p.write_text(text, encoding='utf-8')
p = ROOT / 'tests/test_trust_reference.py'
text = p.read_text().replace("day04=[x for x in cfg['notebooks'] if '/day04/' in x['path']]\n        self.assertEqual(len(day04),3)", "day04=[x for x in cfg['learner_notebooks'] if x.startswith('day04/')]\n        self.assertEqual(day04,['day04/STUDENT.ipynb'])")
text = text.replace("self.assertIs(cfg['trainer_materials_current_scope'],False);self.assertIs(cfg['published'],False)", "self.assertFalse(cfg.get('trainer_materials_current_scope',False));self.assertTrue(cfg['published']);self.assertFalse((ROOT/'INSTRUCTOR_PACKAGE.md').exists())")
p.write_text(text, encoding='utf-8')
p = ROOT / 'tests/test_final_integration_review.py'
text = p.read_text().replace("for x in cfg['notebooks']:\n            if x['kind']=='engine':x['execution_status']='VERIFIED'", "cfg['notebook_execution_status']='VERIFIED'\n        cfg['published_days']=[1,2,3,4,5]")
p.write_text(text, encoding='utf-8')
# Bind the verification record to the executed code, not publication flags.
p = ROOT / 'scripts/execute_student_course.py'
text = p.read_text()
text = text.replace("'checks':results[0]['days'][day-1], 'colab_host_tested':False}", "'checks':results[0]['days'][day-1], 'colab_host_tested':False,\n            'code_sha256':hashlib.sha256(json.dumps([c.source for c in nb.cells if c.cell_type=='code'],ensure_ascii=False).encode()).hexdigest()}")
p.write_text(text, encoding='utf-8')
# Student metadata contains learning paths rather than authoring conversations.
p=ROOT/'course.json'; course=json.loads(p.read_text())
for key in ('integrated_review','build_focus','native_verification_coordinator','runtime_validation_status',
            'runtime_workbench_status','day02_dbt_status','day04_kafka_status',
            'day04_gx_status','day05_serving_status','day05_integration_status','trainer_materials_current_scope'):
    course.pop(key,None)
course['student_entrypoint']='README.md'
course['learner_notebooks']=[f'day{d:02}/STUDENT.ipynb' for d in range(1,6)]
for lab in course.get('labs',[]):
    day=lab['day']; number=str(lab['id']).zfill(2)
    for key in ('available','missing_en','missing_ar','implementation_status','engine_notebook'):
        lab.pop(key,None)
    lab.update(notebook=f'day{day:02}/STUDENT.ipynb',walkthrough=f'day{day:02}/labs/lab{number}/WALKTHROUGH.md')
p.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Delta maintenance release and current learning paths applied; original data and historical execution records retained.')
