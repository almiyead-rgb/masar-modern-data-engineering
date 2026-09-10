"""Offline packaging/behavior tests. None is evidence of Spark/Delta/Kafka/dbt execution."""
from pathlib import Path
from contextlib import nullcontext
import importlib.util
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
from masar import workbench, streaming
from masar.release_evidence import implementation_digest

class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.home=Path(self.temp.name)
        self.source=self.home/'source';self.source.mkdir()
        (self.source/'course.json').write_text('{}');(self.source/'lesson.txt').write_text('approved')
        self.dest=self.home/'workspace'
    def tearDown(self):self.temp.cleanup()
    def test_first_copy_is_complete(self):
        result=workbench.initialize_workspace(self.source,self.dest)
        self.assertEqual(result['status'],'CREATED');self.assertEqual((self.dest/'lesson.txt').read_text(),'approved')
    def test_restart_preserves_learner_edits(self):
        workbench.initialize_workspace(self.source,self.dest);(self.dest/'lesson.txt').write_text('my notes')
        self.assertEqual(workbench.initialize_workspace(self.source,self.dest)['status'],'REUSED_WITHOUT_OVERWRITE')
        self.assertEqual((self.dest/'lesson.txt').read_text(),'my notes')
    def test_changed_course_does_not_overwrite_workspace(self):
        workbench.initialize_workspace(self.source,self.dest);(self.source/'lesson.txt').write_text('new release')
        with self.assertRaises(ValueError):workbench.initialize_workspace(self.source,self.dest)
        self.assertEqual((self.dest/'lesson.txt').read_text(),'approved')
    def test_unmarked_nonempty_workspace_rejected(self):
        self.dest.mkdir();(self.dest/'notes').write_text('keep')
        with self.assertRaises(ValueError):workbench.initialize_workspace(self.source,self.dest)
        self.assertEqual((self.dest/'notes').read_text(),'keep')
    def test_credentials_history_and_outputs_excluded(self):
        for name in ['.env','.env.token','INSTRUCTOR_PACKAGE.md','slides.pptx','secret.key']:(self.source/name).write_text('do not copy')
        for folder in ['.git','outputs','instructor_only','authoring_private']:
            p=self.source/folder;p.mkdir();(p/'sensitive.txt').write_text('private')
        workbench.initialize_workspace(self.source,self.dest)
        self.assertEqual({p.name for p in self.dest.iterdir()},{'course.json','lesson.txt',workbench.STAMP})
    def test_source_symlink_rejected(self):
        (self.source/'escape').symlink_to(self.home/'elsewhere')
        with self.assertRaises(ValueError):workbench.copy_source(self.source,self.dest)
    def test_destination_symlink_rejected(self):
        actual=self.home/'actual';actual.mkdir();self.dest.symlink_to(actual)
        with self.assertRaises(ValueError):workbench.initialize_workspace(self.source,self.dest)
    def test_unsafe_nested_copy_rejected(self):
        with self.assertRaises(ValueError):workbench.copy_source(self.source,self.source/'recursive')
    def test_source_parent_as_destination_rejected(self):
        with self.assertRaises(ValueError):workbench.copy_source(self.source,self.home)
    def test_output_copy_does_not_recursively_copy_itself(self):
        dest=self.source/'outputs'/'run1';workbench.copy_source(self.source,dest)
        self.assertFalse((dest/'outputs').exists())
    def test_digest_ignores_previous_outputs(self):
        before=workbench.snapshot_digest(self.source);p=self.source/'outputs';p.mkdir();(p/'test.json').write_text('{}')
        self.assertEqual(before,workbench.snapshot_digest(self.source))
    def test_digest_detects_source_change(self):
        before=workbench.snapshot_digest(self.source);(self.source/'lesson.txt').write_text('changed')
        self.assertNotEqual(before,workbench.snapshot_digest(self.source))

class KafkaEndpointTests(unittest.TestCase):
    def test_default_remains_host_local(self):
        with patch.dict(os.environ,{},clear=True):self.assertEqual(streaming.bootstrap_address(),'127.0.0.1:9092')
    def test_compose_uses_service_dns_and_internal_port(self):
        with patch.dict(os.environ,{'MASAR_KAFKA_BOOTSTRAP':'kafka:29092'}):self.assertEqual(streaming.bootstrap_address(),'kafka:29092')
    def test_arbitrary_remote_endpoint_rejected(self):
        for value in ['example.org:9092','kafka:9092','127.0.0.1:1','', 'kafka:29092;echo pwned']:
            with self.subTest(value=value),patch.dict(os.environ,{'MASAR_KAFKA_BOOTSTRAP':value}),self.assertRaises(ValueError):streaming.bootstrap_address()
    def test_preflight_uses_selected_socket_address_without_claiming_kafka_ran(self):
        with patch.dict(os.environ,{'MASAR_KAFKA_BOOTSTRAP':'kafka:29092'}),patch.object(streaming.importlib.metadata,'version',return_value=streaming.KAFKA_CLIENT_VERSION),patch.object(streaming.socket,'create_connection',return_value=nullcontext()) as connect:
            report=streaming.stream_preflight()
        connect.assert_called_once_with(('kafka',29092),timeout=2)
        self.assertEqual(report['bootstrap_servers'],'kafka:29092');self.assertFalse(report['kafka_executed'])

class LocalLifecycleTests(unittest.TestCase):
    def test_plan_never_publishes_deletes_or_disables_auth(self):
        plans=[workbench.command_plan(ROOT,a) for a in ['prepare','start','stop','verify']]
        text=json.dumps(plans)
        for forbidden in ['push','down','--volumes','prune','--privileged','docker.sock','password=','token=']:
            self.assertNotIn(forbidden,text)
    def test_image_identity_is_collected_after_build(self):
        commands=workbench.command_plan(ROOT,'prepare')
        self.assertEqual(commands[-1][:3],['docker','image','inspect'])
        self.assertIn('masar-course:local',commands[-1])
    def test_stop_preserves_volumes(self):self.assertEqual(workbench.command_plan(ROOT,'stop')[0][-1],'stop')
    def test_unknown_action_rejected(self):
        with self.assertRaises(ValueError):workbench.command_plan(ROOT,'publish')
    def test_unsafe_project_names_rejected(self):
        for value in ['a;rm -rf /','../x','', 'A', 'a'*60]:
            with self.subTest(value=value),self.assertRaises(ValueError):workbench.command_plan(ROOT,'start',value)
    def test_missing_docker_records_blocked_not_engine_success(self):
        with patch.object(workbench.shutil,'which',return_value=None),patch.object(workbench.subprocess,'run') as run:
            report=workbench.host_preflight();run.assert_not_called()
        self.assertEqual(report['status'],'BLOCKED_HOST_RUNTIME');self.assertFalse(report['engine_executed'])
    def test_cli_without_daemon_is_not_ready(self):
        proc=subprocess.CompletedProcess([],1,'','daemon unavailable')
        with patch.object(workbench.shutil,'which',return_value='/docker'),patch.object(workbench.subprocess,'run',return_value=proc):report=workbench.host_preflight()
        self.assertEqual(report['status'],'BLOCKED_HOST_RUNTIME')
    def test_successful_logged_python_command(self):
        with tempfile.TemporaryDirectory() as d:
            log=Path(d)/'out.log';result=workbench.run_logged([sys.executable,'-c','print("diagnostic only")'],cwd=Path(d),log=log,timeout=5)
            self.assertEqual(result['returncode'],0);self.assertIn('diagnostic only',log.read_text())
    def test_nonzero_exit_is_not_success(self):
        with tempfile.TemporaryDirectory() as d:
            result=workbench.run_logged([sys.executable,'-c','raise SystemExit(7)'],cwd=Path(d),log=Path(d)/'log')
        self.assertEqual(result['returncode'],7);self.assertEqual(result['status'],'FAILED_COMMAND')
    def test_timeout_is_retained_as_failure(self):
        with tempfile.TemporaryDirectory() as d:
            result=workbench.run_logged([sys.executable,'-c','import time;time.sleep(10)'],cwd=Path(d),log=Path(d)/'log',timeout=0.1)
        self.assertEqual(result['status'],'TIMEOUT');self.assertNotEqual(result['returncode'],0)
    def test_shell_string_rejected(self):
        with self.assertRaises(TypeError):workbench.run_logged('echo unsafe',cwd=ROOT,log=ROOT/'unused.log')

class PackagingContractTests(unittest.TestCase):
    def test_day01_sources_point_to_current_student_notebook(self):
        text=(ROOT/'day01/SOURCES.md').read_text()
        self.assertIn('STUDENT.ipynb',text)
        for old in ['INSTRUCTOR_PACKAGE.md','NEXT_CHAT_HANDOFF_AR.md','../notebooks/02_cost_and_local_benchmark.ipynb','Slides cite','instructor evidence']:
            self.assertNotIn(old,text)
    def test_build_requires_real_smoke_not_only_pip(self):
        text=(ROOT/'infrastructure/runtime/Dockerfile').read_text()
        self.assertIn('RUN python scripts/prime_runtime.py',text)
        self.assertIn('python -m pip check',text)
        self.assertIn('USER masar',text)
        self.assertIn('resolved-requirements.txt',text)
    def test_network_and_auth_configuration_not_a_running_container_claim(self):
        text=(ROOT/'infrastructure/runtime/compose.yaml').read_text()
        for fragment in ['kafka:29092','condition: service_healthy','127.0.0.1:8888:8888','internal: true','read_only: true','learner-data','verification-data']:
            self.assertIn(fragment,text)
        self.assertNotIn('privileged:',text);self.assertNotIn('docker.sock',text)
        image=(ROOT/'infrastructure/runtime/Dockerfile').read_text()
        self.assertNotIn('token=',image);self.assertNotIn('password=',image)
    def test_infrastructure_changes_invalidate_future_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);folder=r/'infrastructure/runtime';folder.mkdir(parents=True)
            p=folder/'Dockerfile';p.write_text('FROM example:v1')
            first=implementation_digest(r);p.write_text('FROM example:v2')
            self.assertNotEqual(first,implementation_digest(r))
    def test_coordinator_requires_actual_independent_notebook_runs(self):
        text=(ROOT/'scripts/execute_student_course.py').read_text()
        for required in ('read_stage_report', 'run_course(1), run_course(2)', 'NotebookClient', 'allow_errors=False', 'code_sha256'):
            self.assertIn(required,text)
        self.assertNotIn('git push',text)

if __name__=='__main__':unittest.main()
