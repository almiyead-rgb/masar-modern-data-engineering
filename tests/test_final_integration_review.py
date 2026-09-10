"""Adversarial helper tests. Synthetic records below are NOT engine results."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.native_contracts import STAGES, validate_stage_result, verify_artifact_records, read_stage_report
from masar.pipeline import execute_steps
from masar.release_evidence import (engine_evidence_issues, dbt_evidence_issues,
    implementation_digest, seal_inventory, inventory_files, _safe_path, _record)
from masar.workspace import DATASET_MANIFEST_SHA256, new_workspace, write_json, digest_file
from masar.submission import audit_submission
spec = importlib.util.spec_from_file_location('final_checker', ROOT / 'scripts/check_repository.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def stub(stage='lab03a_staging'):
    """A contract test fixture only; no artifact is emitted as native proof."""
    return {'scope': STAGES[stage][1], 'engine_executed': True,
            'dataset_manifest_sha256': DATASET_MANIFEST_SHA256,
            'checks': {key: True for key in STAGES[stage][2]}}


class NativeContractReviewTests(unittest.TestCase):
    def test_ten_stages_still_eight_labs(self):
        self.assertEqual(len(STAGES), 10)
        self.assertEqual(len(json.loads((ROOT/'course.json').read_text())['labs']), 8)
    def test_complete_shape_is_not_execution(self):
        self.assertIsNone(validate_stage_result('lab03a_staging', stub()))
    def test_failed_status_rejected(self):
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging', {**stub(), 'status':'FAILED'})
    def test_missing_checks_rejected(self):
        x=stub();del x['checks']
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',x)
    def test_null_checks_rejected(self):
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',{**stub(),'checks':None})
    def test_empty_checks_rejected(self):
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',{**stub(),'checks':{}})
    def test_false_check_rejected(self):
        x=stub();x['checks'][next(iter(x['checks']))]=False
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',x)
    def test_integer_one_is_not_true(self):
        x=stub();x['checks'][next(iter(x['checks']))]=1
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',x)
    def test_incomplete_required_checks_rejected(self):
        x=stub();x['checks'].pop(next(iter(x['checks'])))
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',x)
    def test_wrong_scope_rejected(self):
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',{**stub(),'scope':'OTHER'})
    def test_wrong_dataset_rejected(self):
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',{**stub(),'dataset_manifest_sha256':'0'*64})
    def test_partial_success_rejected(self):
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',{**stub(),'complete_lab_success':False})
    def test_helper_cannot_pass(self):
        with self.assertRaises(ValueError):validate_stage_result('lab03a_staging',{**stub(),'engine_executed':False})
    def test_kafka_flag_required(self):
        with self.assertRaises(ValueError):validate_stage_result('lab05_streaming',stub('lab05_streaming'))
    def test_gx_flag_required(self):
        with self.assertRaises(ValueError):validate_stage_result('lab06_quality',stub('lab06_quality'))
    def test_downstream_not_called_on_reported_failure(self):
        calls=[]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'journal.json'
            with self.assertRaises(ValueError):
                execute_steps([('lab03a_staging',lambda:{**stub(),'status':'FAILED'}),
                    ('next',lambda:calls.append('unsafe'))],p)
            state=json.loads(p.read_text())
        self.assertEqual(calls,[]);self.assertEqual(state['status'],'FAILED')
        self.assertEqual(state['blocked_stages'],['next'])
    def test_generic_stub_empty_scope_rejected(self):
        with self.assertRaises(ValueError):validate_stage_result('test_only',{'engine_executed':True,'checks':{'ok':True}})
    def test_result_must_be_object(self):
        with self.assertRaises(ValueError):validate_stage_result('test_only',[])


class FileEvidenceReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        (self.root/'course.json').write_text('{}');self.work=new_workspace(self.root,'review')
    def tearDown(self):self.temp.cleanup()
    def record(self,relative='mini_lakehouse/table/part.parquet'):
        p=self.work/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'TEST_ONLY_NOT_PARQUET')
        return {'path':relative,'sha256':digest_file(p)}
    def test_hash_matching_fixture_checks_integrity_only(self):
        self.assertEqual(verify_artifact_records(self.work,{'test_only':[self.record()]}),1)
    def test_missing_native_file_rejected(self):
        x=self.record();(self.work/x['path']).unlink()
        with self.assertRaises(ValueError):verify_artifact_records(self.work,x)
    def test_changed_native_file_rejected(self):
        x=self.record();(self.work/x['path']).write_bytes(b'changed')
        with self.assertRaises(ValueError):verify_artifact_records(self.work,x)
    def test_zero_length_native_file_rejected(self):
        x=self.record();p=self.work/x['path'];p.write_bytes(b'');x['sha256']=digest_file(p)
        with self.assertRaises(ValueError):verify_artifact_records(self.work,x)
    def test_traversal_rejected(self):
        with self.assertRaises(ValueError):verify_artifact_records(self.work,{'path':'../escape','sha256':'0'*64})
    def test_symlink_rejected(self):
        x=self.record();(self.work/'shortcut').symlink_to(self.work/x['path'])
        with self.assertRaises(ValueError):verify_artifact_records(self.work,{'path':'shortcut','sha256':x['sha256']})
    def test_receipt_flag_without_files_rejected(self):
        p=self.work/STAGES['lab03a_staging'][0];p.parent.mkdir();write_json(p,stub())
        with self.assertRaises(ValueError):read_stage_report(self.work,'lab03a_staging')
    def test_inventory_matches_then_detects_change(self):
        x=self.record();seal_inventory(self.work)
        inv=json.loads((self.work/'reports/integration_inventory.json').read_text())
        self.assertEqual(inv['files'],inventory_files(self.work))
        (self.work/x['path']).write_bytes(b'changed')
        self.assertNotEqual(inv['files'],inventory_files(self.work))
    def test_inventory_detects_extra_output(self):
        self.record();seal_inventory(self.work)
        inv=json.loads((self.work/'reports/integration_inventory.json').read_text())
        self.record('mini_lakehouse/unreviewed.parquet')
        self.assertNotEqual(inv['files'],inventory_files(self.work))
    def test_missing_dbt_is_separate_blocker(self):self.assertTrue(dbt_evidence_issues(self.root))
    def test_dbt_empty_results_rejected(self):
        e=self.root/'evidence';e.mkdir()
        write_json(e/'run_results.json',{'metadata':{'invocation_id':'fixture'},'results':[]})
        write_json(e/'manifest.json',{'metadata':{'invocation_id':'fixture'},'nodes':{}})
        write_json(e/'dbt_validation.json',{'scope':'DBT_EXECUTION_EVIDENCE','status':'PASSED','dbt_executed':True,'adapter':'spark',
          'run_results':{'path':'evidence/run_results.json','sha256':digest_file(e/'run_results.json')},
          'manifest':{'path':'evidence/manifest.json','sha256':digest_file(e/'manifest.json')}})
        self.assertTrue(dbt_evidence_issues(self.root))
    def test_malformed_engine_list_does_not_crash(self):
        e=self.root/'evidence';e.mkdir();(e/'engine_validation.json').write_text('[]')
        self.assertTrue(engine_evidence_issues(self.root))
    def test_malformed_engine_json_does_not_crash(self):
        e=self.root/'evidence';e.mkdir();(e/'engine_validation.json').write_text('{')
        self.assertTrue(engine_evidence_issues(self.root))
    def test_bare_distinct_ids_are_not_evidence(self):
        e=self.root/'evidence';e.mkdir()
        write_json(e/'engine_validation.json',{'status':'PASSED','all_eight_labs_verified':True,
          'runs':[{'run_id':'fake-one'},{'run_id':'fake-two'}]})
        self.assertTrue(engine_evidence_issues(self.root))
    def test_even_correct_scope_needs_artifacts(self):
        e=self.root/'evidence';e.mkdir()
        write_json(e/'engine_validation.json',{'scope':'TWO_NATIVE_RUNS_FILE_BACKED','status':'PASSED',
          'all_eight_labs_verified':True,'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
          'runs':[{'run_id':'1'*32},{'run_id':'2'*32}]})
        self.assertTrue(engine_evidence_issues(self.root))
    def test_verified_flags_do_not_replace_evidence(self):
        cfg=deepcopy(json.loads((ROOT/'course.json').read_text()))
        for x in cfg['labs']:x['status']='VERIFIED'
        cfg['notebook_execution_status']='VERIFIED'
        cfg['published_days']=[1,2,3,4,5]
        for k in ('day02_dbt_status','day04_kafka_status','day04_gx_status'):cfg[k]='VERIFIED'
        self.assertTrue(checker.release_issues(self.root,cfg))
    def test_evidence_absolute_path_rejected(self):
        with self.assertRaises(ValueError):_safe_path(self.root,'/tmp/not-course')
    def test_evidence_backslash_rejected(self):
        with self.assertRaises(ValueError):_safe_path(self.root,'..\\outside')
    def test_evidence_descriptor_requires_hash(self):
        with self.assertRaises(ValueError):_record(self.root,{'path':'anything'})
    def test_runtime_hash_changes_with_code(self):
        (self.root/'src').mkdir();p=self.root/'src/test_only.py';p.write_text('x=1')
        before=implementation_digest(self.root);p.write_text('x=2')
        self.assertNotEqual(before,implementation_digest(self.root))
    def test_runtime_hash_ignores_build_status(self):
        before=implementation_digest(self.root);(self.root/'course.json').write_text('{"published":true}')
        self.assertEqual(before,implementation_digest(self.root))
    def test_submission_cannot_accept_flag_only(self):
        p=self.work/STAGES['lab03a_staging'][0];p.parent.mkdir()
        write_json(p,{'scope':'DAY02_STAGING_ENGINE','engine_executed':True})
        result=audit_submission(self.root,self.work)
        self.assertTrue(any('day02_staging_latest.json' in s for s in result['issues']))
