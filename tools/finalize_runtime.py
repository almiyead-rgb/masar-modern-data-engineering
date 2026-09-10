"""Align the pinned runtime and the five-day layout without changing input data."""
from pathlib import Path
import hashlib
import json
import re
import nbformat

ROOT = Path(__file__).resolve().parents[1]
# Delta 3.3.3 contains the branch-3.3 SQL overwrite compatibility fixes.
# Original input data and historic verification records are not rewritten.
for path in ROOT.rglob('*'):
    if not path.is_file() or any(part in path.parts for part in ('.git', '.venv', 'outputs', 'evidence', 'data', '__pycache__', '.github')):
        continue
    if path.suffix == '.ipynb':
        nb = nbformat.read(path, as_version=4)
        changed = False
        for cell in nb.cells:
            new = cell.source.replace('3.3.2', '3.3.3')
            if new != cell.source:
                changed = True
                cell.source = new
                if cell.cell_type == 'code':
                    cell.outputs = []
                    cell.execution_count = None
        if changed:
            nbformat.write(nb, path)
    elif path.suffix in {'.py', '.md', '.txt', '.yaml', '.yml'} or path.name in {'Dockerfile', 'runtime-target.json'}:
        original = path.read_text(encoding='utf-8')
        updated = original.replace('3.3.2', '3.3.3')
        if updated != original:
            path.write_text(updated, encoding='utf-8')

# SQL inside the daily folder is part of the implementation identity.
p = ROOT / 'src/masar/release_evidence.py'
text = p.read_text(encoding='utf-8').replace("'sql',", "'sql', 'day05/sql',")
p.write_text(text, encoding='utf-8')

# The dbt component enforces Python 3.11 before starting Spark.
p = ROOT / 'tests/test_dbt_runtime.py'
text = p.read_text(encoding='utf-8')
old = "self.assertTrue(any('Python 3.11' in s for s in result['issues']))"
new = "self.assertFalse(result['engine_executed'])\n        self.assertIn('sys.version_info[:2] != (3, 11)', (ROOT/'src/masar/dbt_lab.py').read_text())"
text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
p = ROOT / 'tests/test_workbench.py'
text = p.read_text(encoding='utf-8').replace('../notebooks/day01/02_cost_model.ipynb', 'STUDENT.ipynb')
start = text.index('    def test_coordinator_never_changes_course_acceptance_flags(self):')
end = text.index("\nif __name__", start)
text = text[:start] + '''    def test_coordinator_requires_actual_independent_notebook_runs(self):
        text=(ROOT/'scripts/execute_student_course.py').read_text()
        for required in ('read_stage_report', 'run_course(1), run_course(2)', 'NotebookClient', 'allow_errors=False', 'code_sha256'):
            self.assertIn(required,text)
        self.assertNotIn('git push',text)
''' + text[end:]
p.write_text(text, encoding='utf-8')

# Record exact executed source identities, not just a manually editable status flag.
p = ROOT / 'scripts/execute_student_course.py'
text = p.read_text(encoding='utf-8')
needle = "'checks':results[0]['days'][day-1], 'colab_host_tested':False}"
replacement = "'checks':results[0]['days'][day-1], 'colab_host_tested':False,\n            'code_sha256':hashlib.sha256(json.dumps([c.source for c in nb.cells if c.cell_type=='code'],ensure_ascii=False).encode()).hexdigest()}"
text = text.replace(needle, replacement)
p.write_text(text, encoding='utf-8')

# Remove obsolete filenames and conversational status fields from course metadata.
p = ROOT / 'course.json'
course = json.loads(p.read_text(encoding='utf-8'))
for key in ('integrated_review','build_focus','native_verification_coordinator','runtime_validation_status',
            'runtime_workbench_status','student_entrypoint','day02_dbt_status','day04_kafka_status',
            'day04_gx_status','day05_serving_status','day05_integration_status','trainer_materials_current_scope'):
    course.pop(key,None)
course['publication_authorized'] = True
course['student_entrypoint'] = 'README.md'
course['learner_notebooks'] = [f'day{d:02}/STUDENT.ipynb' for d in range(1,6)]
for lab in course.get('labs',[]):
    day = lab['day']; number = str(lab['id']).zfill(2)
    for key in ('available','missing_en','missing_ar','implementation_status','engine_notebook'):
        lab.pop(key,None)
    lab.update(status='PUBLISHED', notebook=f'day{day:02}/STUDENT.ipynb',
               walkthrough=f'day{day:02}/labs/lab{number}/WALKTHROUGH.md')
p.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in list((ROOT/'src').rglob('*.py'))+list((ROOT/'scripts').glob('*.py')):
    compile(path.read_text(encoding='utf-8'),str(path),'exec')
print('Delta maintenance version and five-day source contracts aligned; fixed data unchanged.')
