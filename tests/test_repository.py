"""Learner packaging tests; they do not substitute for native notebook execution."""
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
import nbformat
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('repository_checker',ROOT/'scripts/check_repository.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)/'repo'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('.git','outputs','evidence','__pycache__','.venv'))
    def tearDown(self):
        self.temp.cleanup()
    def mutate_config(self,name,value):
        path=self.root/'course.json';cfg=json.loads(path.read_text());cfg[name]=value
        path.write_text(json.dumps(cfg))
    def test_clean_layout(self):
        self.assertTrue(checker.inspect(self.root)['passed'])
    def test_wrong_duration_rejected(self):
        self.mutate_config('hours_total',25)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_extra_project_rejected(self):
        self.mutate_config('extra_final_project',True)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_required_distinction_rejected(self):
        self.mutate_config('distinction_required',True)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_paid_service_rejected(self):
        self.mutate_config('paid_services_required',True)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_private_material_rejected(self):
        (self.root/'INSTRUCTOR_PACKAGE.md').write_text('private')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_duplicate_entry_rejected(self):
        (self.root/'MASAR_STUDENT.ipynb').write_text('{}')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_missing_daily_notebook_rejected(self):
        (self.root/'day03/STUDENT.ipynb').unlink()
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_missing_lab_walkthrough_rejected(self):
        (self.root/'day04/labs/lab06/WALKTHROUGH.md').unlink()
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_broken_markdown_link_rejected(self):
        path=self.root/'README.md';path.write_text(path.read_text()+'\n<a href="missing.md">missing</a>')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_broken_notebook_link_rejected(self):
        path=self.root/'day02/STUDENT.ipynb';nb=nbformat.read(path,4)
        nb.cells.append(nbformat.v4.new_markdown_cell('<a href="missing.ipynb">missing</a>'))
        nbformat.write(nb,path)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_changed_data_rejected(self):
        (self.root/'data/masar-small-v1/trips.csv').write_text('changed')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_payload_and_manifest_rewrite_rejected(self):
        p=self.root/'data/masar-small-v1/trips.csv';p.write_bytes(p.read_bytes()+b'\n')
        m=p.parent/'manifest.json';value=json.loads(m.read_text())
        for rec in value['files']:
            if rec['path']=='trips.csv':
                rec['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();rec['bytes']=p.stat().st_size
        m.write_text(json.dumps(value))
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_wrong_notebook_registry_rejected(self):
        self.mutate_config('learner_notebooks',['missing.ipynb'])
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_publication_flag_cannot_replace_execution(self):
        (self.root/'docs/verification.json').unlink(missing_ok=True)
        cfg=json.loads((self.root/'course.json').read_text())
        self.assertEqual(checker.release_issues(self.root,{**cfg,'published':True}),
                         checker.release_issues(self.root,{**cfg,'published':False}))
        self.assertTrue(checker.release_issues(self.root,cfg))
    def test_incomplete_course_record_rejected(self):
        p=self.root/'docs/verification.json';p.write_text(json.dumps({'status':'PASSED','independent_course_runs':1}))
        self.assertTrue(checker.release_issues(self.root,{}))
    def test_code_digest_detects_cell_change(self):
        nb=nbformat.read(self.root/'day01/STUDENT.ipynb',4);before=checker.code_digest(nb)
        next(c for c in nb.cells if c.cell_type=='code').source+='\nprint("changed")'
        self.assertNotEqual(before,checker.code_digest(nb))
    def test_code_digest_excludes_machine_timing_outputs(self):
        nb=nbformat.read(self.root/'day01/STUDENT.ipynb',4);before=checker.code_digest(nb)
        cell=next(c for c in nb.cells if c.cell_type=='code')
        cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text='a different duration')]
        self.assertEqual(before,checker.code_digest(nb))


if __name__=='__main__':
    unittest.main()
