from pathlib import Path
from copy import deepcopy
from decimal import Decimal
import json,random,tempfile,unittest,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.serving_reference import (day05_reference,tables_from_trusted,validate_tables,availability_index,
    FEATURE_INPUTS,validate_feature_inputs,TABLE_COLUMNS,independent_sql_check)
from masar.delta_reference import day03_reference
from masar.trust_reference import events_from_source,GPS_FILES
from masar.workspace import rows_digest,new_workspace
from masar.pipeline import execute_steps
from masar.serving import require_report,QUALITY_CHECKS,STREAM_CHECKS
from masar.submission import audit_submission,REPORTS
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'data/masar-small-v1'

class ServingReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref=day05_reference(SOURCE);cls.tables=cls.ref['tables']
        cls.trips=day03_reference(SOURCE)['expected_corrected_rows']
        cls.events=[r for name in GPS_FILES for r in events_from_source(SOURCE,name)]
    def mutated(self,fn):
        t=deepcopy(self.tables);fn(t)
        with self.assertRaises((ValueError,KeyError)):validate_tables(t)
    def test_all_checks_pass(self):self.assertTrue(all(self.ref['checks'].values()))
    def test_reference_does_not_claim_engine(self):self.assertIs(self.ref['engine_executed'],False)
    def test_exact_eight_products(self):self.assertEqual(len(self.tables),8)
    def test_counts_at_different_grains(self):
        self.assertEqual(self.ref['row_counts'],{'gold.zone_hourly_demand':75,'gold.driver_daily':18,
        'bi.dim_zone':3,'bi.dim_driver':6,'bi.dim_date':3,'bi.fact_trips':75,'ai.zone_hourly_features':3,'ai.zone_hourly_labels':3})
    def test_money_reconciles(self):self.assertEqual(sum(Decimal(r['fare_sar']) for r in self.tables['bi.fact_trips']),Decimal('1880.60'))
    def test_duration_units(self):self.assertEqual(self.ref['reconciliation']['duration_seconds'],95400)
    def test_city_breakdown(self):self.assertEqual([r['fare_minor'] for r in self.ref['reconciliation']['zone_totals']],[67040,62520,58500])
    def test_no_fare_fanout(self):self.assertEqual(len(self.tables['bi.fact_trips']),75);self.assertEqual(sum(r['gps_event_count'] for r in self.tables['bi.fact_trips']),217)
    def test_late_trips_not_lost(self):
        rows=[r for r in self.tables['bi.fact_trips'] if r['trip_id'].startswith('SYN_LATE')]
        self.assertEqual(len(rows),3);self.assertTrue(all(r['gps_event_count']==0 and r['date_key']==20260601 for r in rows))
    def test_city_proxy_is_explicit(self):self.assertEqual({r['zone_resolution'] for r in self.tables['bi.dim_zone']},{'city_proxy'})
    def test_features_count_past_completed(self):self.assertEqual([r['completed_trips_24h'] for r in self.tables['ai.zone_hourly_features']],[8,8,8])
    def test_feature_durations(self):self.assertEqual([r['avg_duration_seconds_24h'] for r in self.tables['ai.zone_hourly_features']],['1470.00','1350.00','1230.00'])
    def test_labels_unknown(self):self.assertTrue(all(r['target_trip_count'] is None for r in self.tables['ai.zone_hourly_labels']))
    def test_replay_keeps_earliest_availability(self):self.assertEqual(availability_index(SOURCE)[('SYN_T0002',1)],'2026-06-04T03:00:00Z')
    def test_correction_has_later_revision_availability(self):self.assertEqual(availability_index(SOURCE)[('SYN_T0001',2)],'2026-06-04T03:03:00Z')
    def test_early_cutoff_does_not_see_later_deliveries(self):
        t=tables_from_trusted(self.trips,self.events,SOURCE,as_of='2026-06-02T03:05:00Z')
        self.assertTrue(all(r['history_available'] is False and r['avg_duration_seconds_24h'] is None for r in t['ai.zone_hourly_features']))
    def test_naive_cutoff_rejected(self):
        with self.assertRaises(ValueError):tables_from_trusted(self.trips,self.events,SOURCE,as_of='2026-06-04T03:05:00')
    def test_replayed_events_do_not_multiply_outputs(self):
        t=tables_from_trusted(self.trips,self.events*2,SOURCE)
        self.assertEqual(t,self.tables)
    def test_shuffled_order_same_content(self):
        t=deepcopy(self.trips);e=deepcopy(self.events);random.Random(17).shuffle(t);random.Random(8).shuffle(e)
        self.assertEqual(tables_from_trusted(t,e,SOURCE),self.tables)
    def test_duplicate_trip_rejected(self):
        with self.assertRaises(ValueError):tables_from_trusted(self.trips+[self.trips[0]],self.events,SOURCE)
    def test_orphan_event_rejected(self):
        e=deepcopy(self.events);e[0]['trip_id']='SYN_MISSING'
        with self.assertRaises(ValueError):tables_from_trusted(self.trips,e,SOURCE)
    def test_conflicting_event_payload_rejected(self):
        e=deepcopy(self.events);e.append(deepcopy(e[0]));e[-1]['city']='Other'
        with self.assertRaises(ValueError):tables_from_trusted(self.trips,e,SOURCE)
    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):tables_from_trusted([],self.events,SOURCE)
    def test_unbounded_input_rejected(self):
        with self.assertRaises(ValueError):tables_from_trusted(self.trips,self.events*3,SOURCE)
    def test_feature_allowlist(self):validate_feature_inputs(FEATURE_INPUTS)
    def test_feature_label_injection_rejected(self):
        with self.assertRaises(ValueError):validate_feature_inputs([*FEATURE_INPUTS,'target_trip_count'])
    def test_feature_duplicate_rejected(self):
        with self.assertRaises(ValueError):validate_feature_inputs([*FEATURE_INPUTS,FEATURE_INPUTS[0]])
    def test_feature_missing_column_rejected(self):
        with self.assertRaises(ValueError):validate_feature_inputs(FEATURE_INPUTS[:-1])
    def test_missing_table_rejected(self):self.mutated(lambda t:t.pop('bi.dim_zone'))
    def test_missing_column_rejected(self):self.mutated(lambda t:t['bi.fact_trips'][0].pop('date_key'))
    def test_duplicate_fact_rejected(self):self.mutated(lambda t:t['bi.fact_trips'].append(deepcopy(t['bi.fact_trips'][0])))
    def test_orphan_dimension_key_rejected(self):self.mutated(lambda t:t['bi.fact_trips'][0].update(zone_key='Z_UNKNOWN'))
    def test_duplicate_dimension_rejected(self):self.mutated(lambda t:t['bi.dim_zone'].append(deepcopy(t['bi.dim_zone'][0])))
    def test_wrong_gold_total_rejected(self):self.mutated(lambda t:t['gold.driver_daily'][0].update(total_fare_sar='0.00'))
    def test_negative_events_rejected(self):self.mutated(lambda t:t['bi.fact_trips'][0].update(gps_event_count=-1))
    def test_invented_label_zero_rejected(self):self.mutated(lambda t:t['ai.zone_hourly_labels'][0].update(target_trip_count=0))
    def test_false_observed_label_rejected(self):self.mutated(lambda t:t['ai.zone_hourly_labels'][0].update(label_status='OBSERVED'))
    def test_misaligned_label_horizon_rejected(self):self.mutated(lambda t:t['ai.zone_hourly_labels'][0].update(prediction_hour_utc='2026-06-05T00:00:00Z'))
    def test_future_availability_rejected(self):self.mutated(lambda t:t['ai.zone_hourly_features'][0].update(max_source_available_at_utc='2026-06-04T03:06:00Z'))
    def test_bad_history_flag_rejected(self):self.mutated(lambda t:t['ai.zone_hourly_features'][0].update(history_available=False))
    def test_bad_history_window_rejected(self):self.mutated(lambda t:t['ai.zone_hourly_features'][0].update(history_window_start_utc='2026-06-04T00:00:00Z'))
    def test_misassigned_group_fares_rejected_even_when_total_same(self):
        def swap(t):
            rows=t['gold.driver_daily'];rows[0]['total_fare_sar'],rows[1]['total_fare_sar']=rows[1]['total_fare_sar'],rows[0]['total_fare_sar']
        self.mutated(swap)
    def test_wrong_local_day_rejected(self):self.mutated(lambda t:t['bi.fact_trips'][0].update(date_key=20260602))
    def test_wrong_local_hour_rejected(self):self.mutated(lambda t:t['gold.zone_hourly_demand'][0].update(hour_local='2026-06-01T00:00:00+03:00'))
    def test_mislabeled_city_proxy_rejected(self):self.mutated(lambda t:t['bi.dim_zone'][0].update(city='Riyadh'))
    def test_hashes_are_order_independent(self):
        self.assertEqual(rows_digest(list(reversed(self.tables['bi.fact_trips']))),self.ref['content_digests']['bi.fact_trips'])
    def test_sql_is_labelled_independent_not_spark(self):self.assertIn('NOT_SPARK',independent_sql_check(self.tables)['scope'])

class NativeBoundaryTests(unittest.TestCase):
    def test_empty_native_report_rejected(self):
        with self.assertRaises(ValueError):require_report({},'DAY04_NATIVE_QUALITY',QUALITY_CHECKS,'gx_executed')
    def test_reference_report_rejected_as_native(self):
        with self.assertRaises(ValueError):require_report(day05_reference(SOURCE),'DAY04_NATIVE_QUALITY',QUALITY_CHECKS,'gx_executed')
    def test_nonboolean_native_truth_rejected(self):
        report={'scope':'DAY04_NATIVE_QUALITY','engine_executed':1}
        with self.assertRaises(ValueError):require_report(report,'DAY04_NATIVE_QUALITY',QUALITY_CHECKS)
    def test_required_report_names_match_existing_writers(self):
        self.assertIn('reports/day02_staging_latest.json',REPORTS)
        self.assertEqual(REPORTS['reports/day02_silver.json'],'DAY02_SILVER_ENGINE')
        self.assertIn('reports/day03_maintenance_latest.json',REPORTS)
    def test_generic_dag_stops_at_failure(self):
        calls=[]
        def first():calls.append('a');return {'engine_executed':True,'scope':'UNIT_TEST_STUB_NOT_ENGINE','checks':{'unit_stub_only':True}}
        def fail():calls.append('b');raise RuntimeError('test fault')
        def last():calls.append('c');return {'engine_executed':True,'scope':'UNIT_TEST_STUB_NOT_ENGINE','checks':{'unit_stub_only':True}}
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'journal.json'
            with self.assertRaises(RuntimeError):execute_steps([('a',first),('b',fail),('c',last)],p)
            r=json.loads(p.read_text());self.assertEqual(r['status'],'FAILED');self.assertEqual(r['blocked_stages'],['c'])
        self.assertEqual(calls,['a','b'])
    def test_generic_dag_rejects_helper_result(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):execute_steps([('a',lambda:{'engine_executed':False})],Path(d)/'journal.json')
    def test_duplicate_stage_names_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):execute_steps([('a',lambda:{}),('a',lambda:{})],Path(d)/'j.json')
    def test_empty_dag_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):execute_steps([],Path(d)/'j.json')
    def test_empty_submission_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            result=audit_submission(Path(d),Path(d))
            self.assertEqual(result['status'],'BLOCKED');self.assertIs(result['grade_awarded'],False)
            self.assertIs(result['publication_approved'],False)
    def test_invalid_repository_url_cannot_pass_inventory(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'submission.json').write_text(json.dumps({'participant_name':'Learner','repository_url':'https://github.com.evil.example/user/repo'}))
            self.assertTrue(any('GitHub' in x for x in audit_submission(p,p)['issues']))

    def test_native_json_array_report_rejected(self):
        with self.assertRaises(ValueError):require_report([], 'DAY04_NATIVE_QUALITY', QUALITY_CHECKS)
    def test_json_array_submission_metadata_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'submission.json').write_text('[]')
            self.assertEqual(audit_submission(p,p)['status'],'BLOCKED')
    def test_json_array_evidence_is_inventory_error(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'course.json').write_text('{}');work=new_workspace(p,'inventory');(work/'reports').mkdir()
            (work/'reports/bronze.json').write_text('[]')
            self.assertTrue(any('bronze.json' in x for x in audit_submission(p,work)['issues']))
