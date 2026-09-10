"""Day 2 standard-library semantics, including negative tests; not engine tests."""
import copy
import json
import random
import sys
import unittest
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.silver_reference import (normalize_city,parse_timestamp,parse_measure,drivers_index,
    normalize_trip,conformed_rows,merge_insert_only,reference_result,read_csv)
from masar.workspace import digest_file, rows_digest

class SilverReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=ROOT/'data/masar-small-v1'
        cls.base=read_csv(cls.source,'trips.csv')
        cls.driver_rows=read_csv(cls.source,'drivers.csv')
        cls.drivers=drivers_index(cls.driver_rows)
        cls.report=reference_result(cls.source)
    def test_city_normalization(self):self.assertEqual(normalize_city(' rIYaDh '),'Riyadh')
    def test_unknown_city_not_guessed(self):self.assertIsNone(normalize_city('unknown'))
    def test_null_city_not_stringified(self):self.assertIsNone(normalize_city(None))
    def test_timestamp_offset_applied_once(self):self.assertEqual(parse_timestamp('2026-06-01T06:00:00+03:00').hour,3)
    def test_naive_timestamp_rejected(self):self.assertIsNone(parse_timestamp('2026-06-01T06:00:00'))
    def test_invalid_calendar_rejected(self):self.assertIsNone(parse_timestamp('2026-02-30T06:00:00+03:00'))
    def test_invalid_timestamp_rejected(self):self.assertIsNone(parse_timestamp('not-a-timestamp'))
    def test_utc_z_accepted(self):self.assertEqual(parse_timestamp('2026-06-01T03:00:00Z').hour,3)
    def test_fare_exact_decimal(self):self.assertEqual(parse_measure('19.25'),Decimal('19.25'))
    def test_fare_zero_allowed(self):self.assertEqual(parse_measure('0.00'),Decimal('0.00'))
    def test_distance_zero_rejected(self):self.assertIsNone(parse_measure('0',positive=True))
    def test_negative_fare_rejected(self):self.assertIsNone(parse_measure('-5.00'))
    def test_excess_precision_not_rounded(self):self.assertIsNone(parse_measure('19.251'))
    def test_decimal_overflow_rejected(self):self.assertIsNone(parse_measure('10000000000.00'))
    def test_non_finite_and_scientific_rejected(self):
        for value in ['NaN','Infinity','-Infinity','1e2','',None]:
            with self.subTest(value=value):self.assertIsNone(parse_measure(value))
    def test_dimension_duplicate_rejected(self):
        with self.assertRaises(ValueError):drivers_index(self.driver_rows+[self.driver_rows[0]])
    def test_empty_driver_dimension_rejected(self):
        with self.assertRaises(ValueError):drivers_index([])
    def test_driver_rating_invalid_rejected(self):
        for value in ['6','NaN','4.35']:
            with self.subTest(value=value),self.assertRaises(ValueError):
                drivers_index([{**self.driver_rows[0],'driver_rating':value}])
    def test_local_date_differs_from_utc_date_at_boundary(self):
        row={**self.base[0],'start_ts':'2026-06-02T00:30:00+03:00','end_ts':'2026-06-02T00:45:00+03:00'}
        result,errors=normalize_trip(row,self.drivers)
        self.assertFalse(errors);self.assertEqual(result['trip_date_local'],'2026-06-02')
        self.assertEqual(result['start_utc'],'2026-06-01T21:30:00Z')
    def test_midnight_crossing_duration(self):
        row=read_csv(self.source,'late_trips.csv')[0];result,errors=normalize_trip(row,self.drivers)
        self.assertFalse(errors);self.assertEqual(result['duration_seconds'],780)
        self.assertEqual(result['trip_date_local'],'2026-06-01')
    def test_missing_required_column_rejected(self):
        row=dict(self.base[0]);del row['fare_sar']
        with self.assertRaises(ValueError):normalize_trip(row,self.drivers)
    def test_invalid_revision_rejected(self):
        for value in [0,-1,True,'1']:
            with self.subTest(value=value),self.assertRaises(ValueError):normalize_trip(self.base[0],self.drivers,value)
    def test_equal_start_and_end_rejected(self):
        row={**self.base[0],'end_ts':self.base[0]['start_ts']}
        self.assertIn('INVALID_DURATION',normalize_trip(row,self.drivers)[1])
    def test_unknown_driver_not_silently_dropped(self):
        row={**self.base[0],'driver_id':'SYN_D999'}
        self.assertIn('UNKNOWN_DRIVER',normalize_trip(row,self.drivers)[1])
    def test_duplicate_receipts_reduce_to_72(self):
        rows,bad=conformed_rows(self.base*2,self.drivers);self.assertEqual(len(rows),72);self.assertFalse(bad)
    def test_same_revision_conflict_rejected(self):
        with self.assertRaises(ValueError):conformed_rows(self.base+[{**self.base[0],'fare_sar':'999.00'}],self.drivers)
    def test_shuffled_input_is_deterministic(self):
        rows=list(self.base*2);random.Random(7).shuffle(rows)
        self.assertEqual(conformed_rows(rows,self.drivers),conformed_rows(self.base*2,self.drivers))
    def test_rerun_and_redelivery_do_not_change_content(self):
        stages=self.report['stages'];self.assertEqual(stages[0]['digest'],stages[1]['digest'])
        self.assertEqual(len({s['digest'] for s in stages[2:]}),1)
    def test_late_trips_and_fare_reconciliation(self):
        self.assertEqual(self.report['final_fare_sar'],'1875.60')
        self.assertEqual(self.report['late_added_fare_sar'],'81.00')
        self.assertEqual(len(self.report['expected_silver_rows']),75)
    def test_late_trips_affect_old_business_date(self):self.assertEqual(self.report['dates_after'],{'2026-06-01':27,'2026-06-02':24,'2026-06-03':24})
    def test_raw_gps_join_changes_grain(self):self.assertEqual(self.report['join_demo']['raw_gps_join_rows'],216)
    def test_quality_fixture_has_seven_distinct_failures(self):
        cases=self.report['quality_examples'];self.assertEqual(len(cases),7)
        self.assertTrue(all(len(c['reasons'])==1 for c in cases))
        self.assertEqual(len({c['reasons'][0] for c in cases}),7)
    def test_target_duplicate_keys_rejected(self):
        row=self.report['expected_silver_rows'][0]
        with self.assertRaises(ValueError):merge_insert_only([row,row],[])
    def test_source_duplicate_keys_rejected_before_merge(self):
        row=self.report['expected_silver_rows'][0]
        with self.assertRaises(ValueError):merge_insert_only([],[row,row])
    def test_correction_not_silently_overwritten(self):
        row=self.report['expected_silver_rows'][0]
        with self.assertRaises(ValueError):merge_insert_only([row],[{**row,'fare_sar':'999.00'}])
    def test_input_objects_are_not_modified(self):
        before=copy.deepcopy(self.base);conformed_rows(self.base,self.drivers);self.assertEqual(before,self.base)
    def test_source_bytes_not_modified(self):
        before={p.name:digest_file(p) for p in self.source.iterdir() if p.is_file()}
        reference_result(self.source)
        self.assertEqual(before,{p.name:digest_file(p) for p in self.source.iterdir() if p.is_file()})
    def test_helper_never_claims_engine_or_dbt(self):
        self.assertFalse(self.report['engine_executed']);self.assertFalse(self.report['dbt_executed'])
    def test_non_source_filename_rejected(self):
        with self.assertRaises(ValueError):read_csv(self.source,'../../secrets.csv')
    def test_all_reference_checks_true(self):self.assertTrue(all(v is True for v in self.report['checks'].values()))

if __name__=='__main__':unittest.main()
