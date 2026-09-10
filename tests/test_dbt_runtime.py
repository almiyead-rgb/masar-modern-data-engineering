"""Offline contract tests only. All dbt-shaped fixtures below are SYNTHETIC.
They test failure handling, not an actual adapter/Spark/dbt execution.
"""
from pathlib import Path
from contextlib import nullcontext
from copy import deepcopy
from decimal import Decimal
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar import runtime, dbt_lab
from masar.workspace import write_json, digest_file
from masar.silver_reference import reference_result
from masar.delta_reference import day03_reference

class UnifiedTargetTests(unittest.TestCase):
    def test_direct_pins_match_runtime_target(self):
        target=json.loads((ROOT/'runtime-target.json').read_text())
        self.assertEqual(target['python'],'3.11');self.assertEqual(target['java_major'],17)
        self.assertEqual(target['scala_binary'],'2.12')
        for name,version in {**runtime.PINNED,**dbt_lab.DBT_PINS}.items():
            self.assertEqual(target['packages'][name],version)
        self.assertLess(int(runtime.PINNED['pyspark'].split('.')[0]),4)
        self.assertFalse(target['native_execution_verified'])
    def test_requirements_do_not_silently_select_preview_adapter(self):
        text=(ROOT/'requirements-dbt.txt').read_text()
        self.assertIn('dbt-spark[session]==1.9.1',text)
        self.assertIn('dbt-core==1.9.8',text)
        self.assertNotIn('--pre',text)
    def test_current_kafka_coordinate_matches_runtime(self):
        from masar.streaming import KAFKA_SPARK_PACKAGE
        self.assertEqual(KAFKA_SPARK_PACKAGE,'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8')
    def test_native_number_api_is_compatible_and_rejects_arbitrary_identifier(self):
        from masar.silver import _number
        import inspect
        src=inspect.getsource(_number)
        self.assertIn('F.expr',src)
        with self.assertRaises(ValueError):_number("fare');drop table t;--")
    def test_java21_and_python313_rejected_as_native_course_target(self):
        def ver(name):return runtime.PINNED[name]
        proc=subprocess.CompletedProcess(['java'],0,'','openjdk version "21.0.1"')
        with patch.object(runtime.importlib.metadata,'version',side_effect=ver),patch.object(runtime.subprocess,'run',return_value=proc),patch.object(runtime.sys,'version_info',(3,13,0)):
            result=runtime.inspect_environment()
        self.assertTrue(any('Java 17' in s for s in result['issues']))
        self.assertTrue(any('Python 3.11' in s for s in result['issues']))
    def test_dbt_preflight_checks_both_pins(self):
        base={'packages':{},'issues':[],'engine_executed':False}
        with patch.object(dbt_lab,'inspect_environment',return_value=base),patch.object(dbt_lab.importlib.metadata,'version',side_effect=lambda name:dbt_lab.DBT_PINS[name]):
            result=dbt_lab.inspect_dbt_environment()
        self.assertFalse(result['dbt_executed']);self.assertFalse(result['engine_executed'])
        self.assertEqual(result['status'],'DEPENDENCIES_PRESENT_ENGINE_NOT_TESTED')
    def test_missing_dbt_is_a_blocker(self):
        with patch.object(dbt_lab,'inspect_environment',return_value={'packages':{},'issues':[],'engine_executed':False}),patch.object(dbt_lab.importlib.metadata,'version',side_effect=importlib.metadata.PackageNotFoundError):
            result=dbt_lab.inspect_dbt_environment()
        self.assertEqual(len(result['issues']),2);self.assertEqual(result['status'],'BLOCKED_DEPENDENCIES')

class DbtWorkspaceSafetyTests(unittest.TestCase):
    def test_generated_identifier_allowed(self):self.assertEqual(dbt_lab.identifier('masar_dbt_ab12'),'masar_dbt_ab12')
    def test_unsafe_identifiers_rejected(self):
        for value in ['a.b','a`','../x','x;drop table y','',3,'a'*64]:
            with self.subTest(value=value),self.assertRaises(ValueError):dbt_lab.identifier(value)
    def test_sql_path_allows_spaces_but_not_literal_escape(self):
        self.assertIn('with space',dbt_lab.sql_path(Path('/tmp/with space/a')))
        for text in ["/tmp/o'reilly",'/tmp/a\\b','/tmp/a\nb']:
            with self.assertRaises(ValueError):dbt_lab.sql_path(Path(text))
    def test_environment_restored_even_after_exception(self):
        key='MASAR_TEST_DBT_ENV';old=os.environ.get(key)
        with self.assertRaises(RuntimeError):
            with dbt_lab.process_environment({key:'temporary'}):
                self.assertEqual(os.environ[key],'temporary');raise RuntimeError('test')
        self.assertEqual(os.environ.get(key),old)
    def test_existing_environment_restored(self):
        with patch.dict(os.environ,{'MASAR_TEST_DBT_ENV':'previous'}):
            with dbt_lab.process_environment({'MASAR_TEST_DBT_ENV':'changed'}):pass
            self.assertEqual(os.environ['MASAR_TEST_DBT_ENV'],'previous')
    def test_preflight_failure_is_saved_and_never_calls_spark(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'course.json').write_text('{}')
            shutil.copytree(ROOT/'data',root/'data')
            with patch.object(dbt_lab,'inspect_dbt_environment',return_value={'issues':['unavailable'],'engine_executed':False}),patch.object(dbt_lab,'start_spark') as start:
                result,path=dbt_lab.run_dbt_lab(root)
                start.assert_not_called()
            self.assertTrue(path.is_file());self.assertEqual(result['status'],'BLOCKED_DEPENDENCIES')
            self.assertEqual(result['phases'],[]);self.assertFalse(result['dbt_executed']);self.assertFalse(result['engine_executed'])
            self.assertEqual(json.loads(path.read_text())['run_id'],result['run_id'])
    def test_changed_dataset_stops_before_spark(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'course.json').write_text('{}');shutil.copytree(ROOT/'data',root/'data')
            (root/'data/masar-small-v1/trips.csv').write_text('corrupted')
            with patch.object(dbt_lab,'inspect_dbt_environment',return_value={'issues':[]}),patch.object(dbt_lab,'start_spark') as start:
                result,path=dbt_lab.run_dbt_lab(root);start.assert_not_called()
            self.assertEqual(result['status'],'FAILED');self.assertFalse(result['dbt_executed'])

class DbtArtifactContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.target=Path(self.temp.name)
        self.model=f'model.{dbt_lab.PROJECT}.silver_trips';self.test=f'test.{dbt_lab.PROJECT}.assert_mart_key'
        self.results={'metadata':{'invocation_id':'synthetic-test-only'},'results':[{'unique_id':self.model,'status':'success'},{'unique_id':self.test,'status':'pass'}]}
        self.manifest={'metadata':{'invocation_id':'synthetic-test-only'},'nodes':{self.model:{'name':'silver_trips','resource_type':'model'},self.test:{'name':'assert_mart_key','resource_type':'test'}}}
        self.save()
    def tearDown(self):self.temp.cleanup()
    def save(self):
        write_json(self.target/'run_results.json',self.results);write_json(self.target/'manifest.json',self.manifest)
    def test_correct_fixture_shape_is_only_contract_validation(self):
        result=dbt_lab.validate_dbt_artifacts(self.target,models={'silver_trips'},tests={'assert_mart_key'})
        self.assertEqual(result['results'],2);self.assertNotIn('engine_executed',result)
    def test_empty_results_rejected(self):
        self.results['results']=[];self.save()
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def test_failed_warning_or_skipped_build_rejected(self):
        for value in ['error','fail','skipped','warn',None]:
            self.results['results'][0]['status']=value;self.save()
            with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def test_invocation_mismatch_rejected(self):
        self.manifest['metadata']['invocation_id']='other';self.save()
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def test_missing_invocation_rejected(self):
        self.results['metadata']={};self.save()
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def test_duplicate_results_rejected(self):
        self.results['results'].append(self.results['results'][0]);self.save()
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def test_nonstring_result_id_rejected(self):
        self.results['results'][0]['unique_id']={};self.save()
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def test_unselected_required_model_rejected(self):
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target,models=dbt_lab.MODEL_NAMES)
    def test_unselected_required_test_rejected(self):
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target,tests=dbt_lab.ALL_TEST_NAMES)
    def test_unknown_manifest_node_rejected(self):
        self.manifest['nodes'].pop(self.model);self.save()
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def test_node_status_must_match_resource_type(self):
        self.results['results'][0]['status']='pass';self.save()
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def test_symlinked_artifact_rejected(self):
        path=self.target/'manifest.json';path.rename(self.target/'actual.json');path.symlink_to(self.target/'actual.json')
        with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target)
    def freshness(self):
        return {'metadata':{'invocation_id':'synthetic-freshness'},'results':[
          {'unique_id':f'source.{dbt_lab.PROJECT}.bronze.{n}','status':'pass',
           'max_loaded_at':'2026-09-10T07:00:00+00:00','snapshotted_at':'2026-09-10T07:01:00+00:00'}
          for n in sorted(dbt_lab.SOURCE_NAMES)]}
    def test_freshness_covers_three_sources(self):
        write_json(self.target/'sources.json',self.freshness())
        self.assertEqual(dbt_lab.validate_dbt_artifacts(self.target,freshness=True)['results'],3)
    def test_freshness_warning_is_visible_not_silently_passed(self):
        data=self.freshness();data['results'][0]['status']='warn';write_json(self.target/'sources.json',data)
        self.assertEqual(dbt_lab.validate_dbt_artifacts(self.target,freshness=True)['warning_count'],1)
    def test_freshness_missing_clock_or_source_rejected(self):
        for missing in ['timestamp','source']:
            data=self.freshness()
            if missing=='source':data['results'].pop()
            else:data['results'][0]['max_loaded_at']=None
            write_json(self.target/'sources.json',data)
            with self.assertRaises(ValueError):dbt_lab.validate_dbt_artifacts(self.target,freshness=True)

class DbtModelDesignTests(unittest.TestCase):
    def test_same_six_models_and_seven_singular_tests(self):
        base=ROOT/'day02/dbt'
        self.assertEqual({p.stem for p in (base/'models').rglob('*.sql')},dbt_lab.MODEL_NAMES)
        self.assertEqual({p.stem for p in (base/'tests').glob('*.sql')},dbt_lab.ALL_TEST_NAMES)
    def test_lookback_uses_arrival_clock_and_explicit_reprocess(self):
        text=(ROOT/'day02/dbt/models/silver/silver_trips.sql').read_text()
        self.assertIn('max(_ingested_at)',text);self.assertIn('interval 3 days',text)
        self.assertIn("var('reprocess_all', false)",text)
        self.assertIn('s.source_revision > t.source_revision',text)
        self.assertNotIn('where trip_date_local',text)
    def test_ranking_precedes_incremental_filter(self):
        text=(ROOT/'day02/dbt/models/intermediate/int_trip_candidates.sql').read_text()
        self.assertIn('source_revision desc',text);self.assertNotIn('is_incremental()',text)
    def test_profile_has_no_credentials_and_only_one_thread(self):
        text=(ROOT/'day02/dbt/profiles/profiles.yml').read_text()
        for value in ['method: session','threads: 1','catalogImplementation: in-memory']:
            self.assertIn(value,text)
        for value in ['password:','token:','endpoint:']:self.assertNotIn(value,text)
    def test_expected_totals_come_from_existing_fixed_data(self):
        source=ROOT/'data/masar-small-v1';rows=reference_result(source)['expected_silver_rows']
        base=[r for r in rows if not r['trip_id'].startswith('SYN_LATE')]
        self.assertEqual((len(base),sum(Decimal(r['fare_sar']) for r in base)),(72,Decimal('1794.60')))
        self.assertEqual((len(rows),sum(Decimal(r['fare_sar']) for r in rows)),(75,Decimal('1875.60')))
        corrected=day03_reference(source)['expected_corrected_rows']
        self.assertEqual(sum(Decimal(r['fare_sar']) for r in corrected),Decimal('1880.60'))

if __name__=='__main__':unittest.main()
