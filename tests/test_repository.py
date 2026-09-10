from pathlib import Path
import importlib.util, json, shutil, tempfile, unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('repository_checker', ROOT/'scripts/check_repository.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
class RepositoryTests(unittest.TestCase):
    def copy(self,d):
        dest=Path(d)/'repo'
        shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('.git','outputs','__pycache__'))
        return dest
    def test_clean_repository(self):self.assertTrue(checker.inspect(ROOT)['passed'])
    def test_wrong_duration_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'course.json';v=json.loads(p.read_text());v['hours_total']=25;p.write_text(json.dumps(v))
            self.assertFalse(checker.inspect(root)['passed'])
    def test_required_distinction_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'course.json';v=json.loads(p.read_text());v['distinction_required']=True;p.write_text(json.dumps(v))
            self.assertFalse(checker.inspect(root)['passed'])
    def test_broken_link_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'README.md';p.write_text(p.read_text()+'\n<a href="missing.md">Missing</a>')
            self.assertFalse(checker.inspect(root)['passed'])
    def test_private_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);(root/'INSTRUCTOR_PACKAGE.md').write_text('Private')
            self.assertFalse(checker.inspect(root)['passed'])
    def test_unexecuted_notebook_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'notebooks/day01/01_source_inspection.ipynb';n=json.loads(p.read_text())
            next(c for c in n['cells'] if c['cell_type']=='code')['execution_count']=None;p.write_text(json.dumps(n))
            self.assertFalse(checker.inspect(root)['passed'])
    def test_changed_data_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);(root/'data/masar-small-v1/trips.csv').write_text('changed')
            self.assertFalse(checker.inspect(root)['passed'])

class DraftAndReleaseTests(unittest.TestCase):
    def copy(self,d):
        dest=Path(d)/'repo'
        shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('.git','outputs','__pycache__'))
        return dest
    def test_engine_drafts_visible_as_warnings(self):
        r=checker.inspect(ROOT)
        expected = sum(n.get('execution_status') == 'ENGINE_NOT_EXECUTED' for n in json.loads((ROOT/'course.json').read_text())['notebooks'])
        self.assertEqual(len(r['warnings']), expected)
        self.assertTrue(all('NOT EXECUTED' in w for w in r['warnings']))
    def test_draft_cannot_contain_fake_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'notebooks/day01/03_bronze_delta.ipynb';n=json.loads(p.read_text())
            next(c for c in n['cells'] if c['cell_type']=='code')['outputs']=[{'output_type':'stream','name':'stdout','text':['fake success']}]
            p.write_text(json.dumps(n));self.assertFalse(checker.inspect(root)['passed'])
    def test_missing_notebook_notice_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'notebooks/day01/03_bronze_delta.ipynb';n=json.loads(p.read_text())
            for c in n['cells']:
                if c['cell_type']=='markdown':c['source']=''.join(c['source']).replace('ENGINE_NOT_EXECUTED','')
            p.write_text(json.dumps(n));self.assertFalse(checker.inspect(root)['passed'])
    def test_notebook_link_is_checked(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'notebooks/day01/03_bronze_delta.ipynb';n=json.loads(p.read_text())
            next(c for c in n['cells'] if c['cell_type']=='markdown')['source'] += ['<a href="missing.ipynb">bad</a>']
            p.write_text(json.dumps(n));self.assertFalse(checker.inspect(root)['passed'])
    def test_registry_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'notebooks/day01/03_bronze_delta.ipynb';n=json.loads(p.read_text());n['metadata']['masar']['engine_verified']=True
            p.write_text(json.dumps(n));self.assertFalse(checker.inspect(root)['passed'])
    def test_published_flag_does_not_change_teaching_readiness(self):
        cfg=json.loads((ROOT/'course.json').read_text())
        a=checker.release_issues(ROOT,{**cfg,'published':False})
        b=checker.release_issues(ROOT,{**cfg,'published':True})
        self.assertEqual(a,b);self.assertTrue(a)
    def test_all_statuses_verified_without_evidence_still_rejected(self):
        cfg=json.loads((ROOT/'course.json').read_text())
        for l in cfg['labs']:l['status']='VERIFIED'
        for n in cfg['notebooks']:
            if n['kind']=='engine':n['execution_status']='VERIFIED'
        self.assertTrue(any('no independent' in issue for issue in checker.release_issues(ROOT,cfg)))
    def test_manifest_and_payload_rewrite_rejected(self):
        import hashlib
        with tempfile.TemporaryDirectory() as d:
            root=self.copy(d);p=root/'data/masar-small-v1/trips.csv';p.write_bytes(p.read_bytes()+b'\n')
            m=root/'data/masar-small-v1/manifest.json';v=json.loads(m.read_text())
            for rec in v['files']:
                if rec['path']=='trips.csv':rec['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();rec['bytes']=p.stat().st_size
            m.write_text(json.dumps(v));self.assertFalse(checker.inspect(root)['passed'])
