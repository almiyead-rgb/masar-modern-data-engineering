from pathlib import Path
import json
from copy import deepcopy
from decimal import Decimal
import unittest
import sys
import tempfile
import inspect
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.trust_reference import (day04_reference,events_from_source,event_contract,unique_events,
    quality_probe_rows,row_quality_reasons,evaluate_quality,freshness,city_distribution,decimal_value)
from masar.delta_reference import day03_reference
from masar.silver_reference import drivers_index,read_csv,BUSINESS_FIELDS
from masar.streaming import validate_topic,publish_fixture,consume_available
from masar.workspace import new_workspace,workspace_path

class TrustReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=ROOT/'data/masar-small-v1'
        cls.rows=day03_reference(cls.source)['expected_corrected_rows']
        cls.drivers=set(drivers_index(read_csv(cls.source,'drivers.csv')))
        cls.events=events_from_source(cls.source,'gps.ndjson')
        cls.trip_ids={r['trip_id'] for r in cls.rows}
        cls.result=day04_reference(cls.source)
    def test_reference_is_explicitly_not_native(self):
        for key in ['engine_executed','kafka_executed','gx_executed']:self.assertIs(self.result[key],False)
    def test_expected_delivery_counts(self):self.assertEqual(self.result['deliveries'],{'base':216,'replay':2,'late':1,'total':219})
    def test_unique_count(self):self.assertEqual(self.result['distinct_events'],217)
    def test_all_reference_checks(self):self.assertTrue(all(self.result['checks'].values()))
    def test_reference_deterministic(self):self.assertEqual(day04_reference(self.source),self.result)
    def test_exact_events_replay(self):self.assertEqual(unique_events(self.events),unique_events(self.events*2))
    def test_event_order_does_not_change_result(self):self.assertEqual(unique_events(self.events),unique_events(list(reversed(self.events))))
    def test_conflicting_events_rejected(self):
        e=deepcopy(self.events[0]);e['location']['lat']+=0.1
        with self.assertRaisesRegex(ValueError,'Conflicting'):unique_events([self.events[0],e])
    def test_missing_event_id_rejected(self):
        with self.assertRaises(ValueError):unique_events([{'event_id':''}])
    def test_unknown_event_source_rejected(self):
        with self.assertRaises(ValueError):events_from_source(self.source,'../gps.ndjson')
    def test_event_contract_known_input(self):self.assertEqual(event_contract(self.events[0],self.trip_ids),[])
    def test_unknown_trip(self):
        r=deepcopy(self.events[0]);r['trip_id']='missing';self.assertIn('UNKNOWN_TRIP',event_contract(r,self.trip_ids))
    def test_non_synthetic_rejected(self):
        r=deepcopy(self.events[0]);r['synthetic']=False;self.assertIn('NON_SYNTHETIC_EVENT',event_contract(r,self.trip_ids))
    def test_integer_synthetic_is_not_true(self):
        r=deepcopy(self.events[0]);r['synthetic']=1;self.assertIn('NON_SYNTHETIC_EVENT',event_contract(r,self.trip_ids))
    def test_nan_coordinate(self):
        r=deepcopy(self.events[0]);r['location']['lat']=float('nan');self.assertIn('INVALID_LAT',event_contract(r,self.trip_ids))
    def test_out_of_range_coordinate(self):
        r=deepcopy(self.events[0]);r['location']['lon']=181;self.assertIn('INVALID_LON',event_contract(r,self.trip_ids))
    def test_bool_coordinate(self):
        r=deepcopy(self.events[0]);r['location']['lat']=True;self.assertIn('INVALID_LAT',event_contract(r,self.trip_ids))
    def test_wrong_location_schema(self):
        r=deepcopy(self.events[0]);r['location']={};self.assertIn('INVALID_LOCATION',event_contract(r,self.trip_ids))
    def test_missing_time_zone_rejected(self):
        r=deepcopy(self.events[0]);r['event_ts']='2026-06-01T06:00:00';self.assertIn('INVALID_EVENT_TIME',event_contract(r,self.trip_ids))
    def test_event_extra_column(self):
        r=deepcopy(self.events[0]);r['name']='a';self.assertEqual(event_contract(r,self.trip_ids),['EVENT_SCHEMA_MISMATCH'])
    def test_clean_passes(self):self.assertTrue(evaluate_quality(self.rows,self.drivers)['promote_allowed'])
    def test_mixed_seven_quarantine(self):
        r=evaluate_quality(self.rows+quality_probe_rows(self.source),self.drivers)
        self.assertEqual((r['input_rows'],r['accepted_rows'],r['rejected_rows']),(82,75,7));self.assertFalse(r['promote_allowed'])
    def test_seven_root_reasons(self):
        self.assertEqual(set(self.result['quality_mixed']['reason_counts']),{'MISSING_TRIP_ID','UNKNOWN_DRIVER','INVALID_CITY','INVALID_TIMESTAMP','INVALID_DURATION','INVALID_FARE','INVALID_DISTANCE'})
    def test_rejection_rate_denominator(self):self.assertAlmostEqual(self.result['quality_mixed']['rejection_rate'],7/82)
    def test_revalidation_no_fare_change(self):
        r=evaluate_quality(self.rows+quality_probe_rows(self.source),self.drivers)
        after=evaluate_quality(r['accepted'],self.drivers)
        self.assertTrue(after['promote_allowed']);self.assertEqual(sum(Decimal(x['fare_sar']) for x in after['accepted']),Decimal('1880.60'))
    def test_no_mutation(self):
        rows=deepcopy(self.rows);saved=deepcopy(rows);evaluate_quality(rows,self.drivers);self.assertEqual(rows,saved)
    def test_duplicate_is_quarantined_on_both_occurrences(self):
        r=evaluate_quality(self.rows+[self.rows[0]],self.drivers)
        self.assertEqual(sum('DUPLICATE_TRIP_ID' in q['reason_codes'] for q in r['quarantine']),2)
    def test_empty_batch_blocks(self):
        r=evaluate_quality([],self.drivers);self.assertFalse(r['promote_allowed']);self.assertIsNone(r['rejection_rate'])
    def test_incomplete_but_valid_batch_blocks(self):
        r=evaluate_quality(self.rows[:60],self.drivers);self.assertEqual(r['accepted_rows'],60);self.assertEqual(r['batch_blockers'],['VOLUME_MISMATCH'])
    def test_missing_column_schema_failure(self):
        rows=deepcopy(self.rows);del rows[0]['city'];r=evaluate_quality(rows,self.drivers);self.assertIn('SCHEMA_MISMATCH',r['batch_blockers'])
    def test_extra_column_schema_failure(self):
        r=deepcopy(self.rows[0]);r['phone']='do_not_add';self.assertEqual(row_quality_reasons(r,self.drivers),['BUSINESS_SCHEMA_MISMATCH'])
    def test_null_key(self):
        r=deepcopy(self.rows[0]);r['trip_id']=None;self.assertIn('MISSING_TRIP_ID',row_quality_reasons(r,self.drivers))
    def test_non_string_key(self):
        r=deepcopy(self.rows[0]);r['trip_id']=[];self.assertFalse(evaluate_quality([r],self.drivers,expected_rows=1)['promote_allowed'])
    def test_bad_driver_type(self):
        r=deepcopy(self.rows[0]);r['driver_id']=[];self.assertIn('UNKNOWN_DRIVER',row_quality_reasons(r,self.drivers))
    def test_non_finite_fare(self):
        r=deepcopy(self.rows[0]);r['fare_sar']='Infinity';self.assertIn('INVALID_FARE',row_quality_reasons(r,self.drivers))
    def test_negative_distance(self):
        r=deepcopy(self.rows[0]);r['distance_km']='-1.00';self.assertIn('INVALID_DISTANCE',row_quality_reasons(r,self.drivers))
    def test_zero_fare_is_allowed(self):
        r=deepcopy(self.rows[0]);r['fare_sar']='0.00';self.assertNotIn('INVALID_FARE',row_quality_reasons(r,self.drivers))
    def test_duration_mismatch(self):
        r=deepcopy(self.rows[0]);r['duration_seconds']+=1;self.assertIn('INVALID_DURATION',row_quality_reasons(r,self.drivers))
    def test_wrong_local_date(self):
        r=deepcopy(self.rows[0]);r['trip_date_local']='2026-06-30';self.assertIn('INVALID_LOCAL_DATE',row_quality_reasons(r,self.drivers))
    def test_invalid_revision(self):
        r=deepcopy(self.rows[0]);r['source_revision']=True;self.assertIn('INVALID_REVISION',row_quality_reasons(r,self.drivers))
    def test_unknown_driver_attributes(self):
        r=deepcopy(self.rows[0]);r['driver_rating']='6';self.assertIn('INVALID_DRIVER_ATTRIBUTES',row_quality_reasons(r,self.drivers))
    def test_empty_driver_dimension_rejected(self):
        with self.assertRaises(ValueError):evaluate_quality(self.rows,set())
    def test_bad_expected_count(self):
        with self.assertRaises(ValueError):evaluate_quality(self.rows,self.drivers,expected_rows=0)
    def test_freshness_equal_threshold(self):self.assertEqual(freshness('2026-06-04T03:00:00Z','2026-06-04T03:05:00Z',max_age_seconds=300)['status'],'PASS')
    def test_stale(self):self.assertEqual(freshness('2026-06-04T03:00:00Z','2026-06-04T03:05:01Z',max_age_seconds=300)['status'],'STALE')
    def test_future_not_fresh(self):self.assertEqual(freshness('2026-06-04T03:06:00Z','2026-06-04T03:05:00Z',max_age_seconds=300)['status'],'FUTURE_TIMESTAMP')
    def test_timezone_equivalence(self):self.assertEqual(freshness('2026-06-04T06:00:00+03:00','2026-06-04T03:00:00Z',max_age_seconds=0)['age_seconds'],0)
    def test_missing_clock_zone(self):
        with self.assertRaises(ValueError):freshness('2026-06-04T03:00:00','2026-06-04T03:05:00Z',max_age_seconds=300)
    def test_negative_freshness_threshold(self):
        with self.assertRaises(ValueError):freshness('2026-06-04T03:00:00Z','2026-06-04T03:05:00Z',max_age_seconds=-1)
    def test_distribution_identity(self):self.assertEqual(city_distribution(self.rows,self.rows)['value'],0)
    def test_distribution_warning(self):
        rows=deepcopy(self.rows)
        for r in rows:r['city']='Riyadh'
        self.assertEqual(city_distribution(rows,self.rows)['status'],'WARN')
    def test_distribution_empty_rejected(self):
        with self.assertRaises(ValueError):city_distribution([],self.rows)
    def test_distribution_bad_threshold(self):
        with self.assertRaises(ValueError):city_distribution(self.rows,self.rows,threshold=float('nan'))
    def test_topic_restricted(self):
        with self.assertRaises(ValueError):validate_topic('a-real-production-topic')
    def test_topic_valid(self):self.assertEqual(validate_topic('masar-day04-'+'a'*32),'masar-day04-'+'a'*32)
    def test_all_results_json_finite(self):json.dumps(self.result,allow_nan=False)

class Day04ConfigurationTests(unittest.TestCase):
    def test_compose_local_only(self):
        # Keep repository CI standard-library-only. This checks the explicit
        # reviewed Compose contract; it is not a Docker execution test.
        import re
        text=(ROOT/'infrastructure/kafka/compose.yaml').read_text()
        ports=re.search(r"^    ports:\n(.*?)(?=^    [a-z_]+:)",text,re.M|re.S)
        self.assertIsNotNone(ports)
        self.assertEqual(ports.group(1).strip(), '- "127.0.0.1:9092:9092"')
        self.assertIn('    image: apache/kafka:4.0.2',text)
        self.assertIn('volumes:\n  kafka-data:',text)
        self.assertNotIn('network_mode: host',text)
    def test_native_stream_source_and_checkpoint(self):
        s=inspect.getsource(consume_available)
        self.assertIn("format('kafka')",s);self.assertIn("format('delta')",s)
        self.assertIn("option('checkpointLocation'",s);self.assertIn("option('failOnDataLoss','true')",s)
        self.assertNotIn('foreachBatch',s)
    def test_publish_records_intent_and_raw_line(self):
        s=inspect.getsource(publish_fixture)
        self.assertIn('INTENT_RECORDED',s);self.assertIn("value=line.encode('utf-8')",s)
        self.assertIn('future.get(timeout=45)',s)
    def test_native_notebooks_will_be_registered(self):
        cfg=json.loads((ROOT/'course.json').read_text())
        day04=[x for x in cfg['learner_notebooks'] if x.startswith('day04/')]
        self.assertEqual(day04,['day04/STUDENT.ipynb'])
    def test_policies_match_business_fields(self):
        cfg=json.loads((ROOT/'config/day04_policy.json').read_text());self.assertEqual(cfg['schema_fields'],list(BUSINESS_FIELDS));self.assertEqual(cfg['expected_trip_rows'],75)
    def test_student_only_scope_preserved(self):
        cfg=json.loads((ROOT/'course.json').read_text());self.assertFalse(cfg.get('trainer_materials_current_scope',False));self.assertTrue(cfg['published']);self.assertFalse((ROOT/'INSTRUCTOR_PACKAGE.md').exists())
