from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
import json
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.delta_reference import day03_reference, revision_merge, schema_fixture
from masar.silver_reference import reference_result
from masar.delta_lab import vacuum_dry_run_sql, _table_path, _expected_write_rejection
from masar.workspace import new_workspace, workspace_path, rows_digest
SOURCE=ROOT/'data/masar-small-v1'

class CorrectionValueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected=day03_reference(SOURCE)
        cls.before=reference_result(SOURCE)['expected_silver_rows']
        cls.after=cls.expected['expected_corrected_rows']
        cls.correction=[cls.expected['corrected_trip_after']]
    def test_reference_is_not_engine_evidence(self):
        self.assertIs(self.expected['engine_executed'],False)
        self.assertEqual(self.expected['scope'],'DAY03_REFERENCE_BUSINESS_VALUES_ONLY')
    def test_before_after_cardinality(self):self.assertEqual((self.expected['before']['rows'],self.expected['after']['rows']),(75,75))
    def test_total_before(self):self.assertEqual(self.expected['before']['fare_sar'],'1875.60')
    def test_total_after(self):self.assertEqual(self.expected['after']['fare_sar'],'1880.60')
    def test_independent_difference(self):
        self.assertEqual(sum(Decimal(r['fare_sar']) for r in self.after)-sum(Decimal(r['fare_sar']) for r in self.before),Decimal('5.00'))
    def test_one_changed_record(self):self.assertEqual([a['trip_id'] for a,b in zip(self.before,self.after) if a!=b],['SYN_T0001'])
    def test_old_fare(self):self.assertEqual(self.expected['corrected_trip_before']['fare_sar'],'18.00')
    def test_new_fare(self):self.assertEqual(self.expected['corrected_trip_after']['fare_sar'],'23.00')
    def test_replay_identical(self):self.assertEqual(revision_merge(self.after,self.correction)[0],self.after)
    def test_stale_delivery_ignored(self):self.assertEqual(revision_merge(self.after,self.before)[0],self.after)
    def test_only_one_stale_revision(self):self.assertEqual(self.expected['stale_ignored_count'],1)
    def test_input_lists_not_mutated(self):
        left,right=deepcopy(self.before),deepcopy(self.correction)
        revision_merge(left,right)
        self.assertEqual(left,self.before);self.assertEqual(right,self.correction)
    def test_return_rows_not_aliases(self):
        left,right=deepcopy(self.before),deepcopy(self.correction)
        result,_=revision_merge(left,right);result[0]['fare_sar']='999.00'
        self.assertEqual(left,self.before);self.assertEqual(right,self.correction)
    def test_order_independent(self):self.assertEqual(revision_merge(self.before[::-1],self.correction)[0],self.after)
    def test_same_revision_conflict_rejected(self):
        bad=deepcopy(self.correction);bad[0]['fare_sar']='24.00'
        with self.assertRaisesRegex(ValueError,'Same-revision conflict'):revision_merge(self.after,bad)
    def test_conflict_does_not_mutate_target(self):
        original=deepcopy(self.after);bad=deepcopy(self.correction);bad[0]['fare_sar']='24.00'
        with self.assertRaises(ValueError):revision_merge(original,bad)
        self.assertEqual(original,self.after)
    def test_duplicate_source_rejected(self):
        with self.assertRaises(ValueError):revision_merge(self.before,self.correction*2)
    def test_duplicate_target_rejected(self):
        with self.assertRaises(ValueError):revision_merge(self.before+[self.before[0]],self.correction)
    def test_revision_bool_zero_negative_text_rejected(self):
        for value in (True,False,0,-1,'2',None,2.0):
            with self.subTest(value=value):
                bad=deepcopy(self.correction);bad[0]['source_revision']=value
                with self.assertRaises(ValueError):revision_merge(self.before,bad)
    def test_empty_or_untrimmed_key_rejected(self):
        for key in ('',' ',' SYN_T0001',None,42):
            with self.subTest(key=key):
                bad=deepcopy(self.correction);bad[0]['trip_id']=key
                with self.assertRaises(ValueError):revision_merge(self.before,bad)
    def test_missing_field_rejected(self):
        bad=deepcopy(self.correction);del bad[0]['fare_sar']
        with self.assertRaises(ValueError):revision_merge(self.before,bad)
    def test_extra_field_rejected(self):
        bad=deepcopy(self.correction);bad[0]['unapproved']=True
        with self.assertRaises(ValueError):revision_merge(self.before,bad)
    def test_new_valid_key_inserted(self):
        incoming=deepcopy(self.correction);incoming[0]['trip_id']='SYN_TRANSIENT_TEST'
        result,actions=revision_merge(self.before,incoming)
        self.assertEqual(len(result),76);self.assertEqual(actions[0]['action'],'INSERT')
    def test_empty_source_no_change(self):self.assertEqual(revision_merge(self.before,[])[0],self.before)
    def test_correction_matches_frozen_digest(self):self.assertEqual(rows_digest(self.after),'1321d375742d806a1f0fef82be9e2862af04f5d18f3a976792a6b1d9aa1b4383')
    def test_schema_fixture(self):
        x=schema_fixture(SOURCE)
        self.assertEqual((x['trip_id'],x['extra_column'],x['value']),('SYN_T0002','surcharge_sar','2.00'))
    def test_only_correction_has_revision_two(self):self.assertEqual(sum(r['source_revision']==2 for r in self.after),1)
    def test_no_fake_table_versions_in_reference(self):self.assertFalse(any('table_version' in k or 'delta_version' in k for k in self.expected))

class SafetyHelpersTests(unittest.TestCase):
    def make(self,folder):
        root=Path(folder)/'course';root.mkdir();(root/'course.json').write_text('{}')
        work=new_workspace(root,'day03_test')
        target=workspace_path(work,'sandbox/day03/recovery_test')
        return work,target
    def test_dry_run_only(self):
        with tempfile.TemporaryDirectory() as d:
            w,p=self.make(d);sql=vacuum_dry_run_sql(w,p)
            self.assertTrue(sql.endswith('RETAIN 168 HOURS DRY RUN'))
    def test_larger_retention_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            w,p=self.make(d);self.assertIn('RETAIN 336 HOURS DRY RUN',vacuum_dry_run_sql(w,p,336))
    def test_unsafe_retention_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            w,p=self.make(d)
            for n in (0,1,167,-1,True,'168',168.0):
                with self.subTest(n=n):
                    with self.assertRaises(ValueError):vacuum_dry_run_sql(w,p,n)
    def test_trusted_table_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            w,p=self.make(d)
            with self.assertRaises(ValueError):vacuum_dry_run_sql(w,w/'mini_lakehouse/silver/trips')
    def test_outside_workspace_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            w,p=self.make(d)
            with self.assertRaises(ValueError):vacuum_dry_run_sql(w,Path(d)/'outside')
    def test_parent_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            w,p=self.make(d)
            with self.assertRaises(ValueError):vacuum_dry_run_sql(w,w/'sandbox/day03/../escape')
    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            w,p=self.make(d);other=w/'sandbox/day03/actual';other.mkdir(parents=True);p.symlink_to(other)
            with self.assertRaises(ValueError):vacuum_dry_run_sql(w,p)
    def test_backtick_in_sql_path_rejected(self):
        with self.assertRaises(ValueError):_table_path(Path('/tmp/bad`path'))
    def test_unknown_error_is_not_negative_test_success(self):
        def bad():raise FileNotFoundError('a dependency is missing')
        with patch('masar.delta_lab._state',return_value={'rows':75}):
            with self.assertRaisesRegex(RuntimeError,'Unexpected failure'):
                _expected_write_rejection(None,Path('/tmp/test'),bad,'constraint')
    def test_no_error_is_not_negative_test_success(self):
        with patch('masar.delta_lab._state',return_value={'rows':75}):
            with self.assertRaises(AssertionError):_expected_write_rejection(None,Path('/tmp/test'),lambda:None,'schema')
    def test_changed_state_after_error_rejected(self):
        def bad():raise RuntimeError('CHECK constraint was violated')
        with patch('masar.delta_lab._state',side_effect=[{'rows':75},{'rows':76}]):
            with self.assertRaises(AssertionError):_expected_write_rejection(None,Path('/tmp/test'),bad,'constraint')
    def test_mocked_rejection_classifier_not_engine_test(self):
        def bad():raise RuntimeError('A schema mismatch detected')
        with patch('masar.delta_lab._state',return_value={'rows':75}):
            r=_expected_write_rejection(None,Path('/tmp/test'),bad,'schema')
            self.assertIs(r['committed_table_unchanged'],True)
    def test_bad_rejection_kind_rejected(self):
        with self.assertRaises(ValueError):_expected_write_rejection(None,Path('/tmp/test'),lambda:None,'unknown')

if __name__=='__main__':unittest.main()
