"""Offline helpers and negative tests only; no mocked result is engine evidence."""
from pathlib import Path
import importlib.metadata
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar import runtime
from masar.workspace import (MARKER, DATASET_MANIFEST_SHA256, new_workspace, workspace_path,
    write_json, rows_digest, summarize_samples, require_fixed_dataset,
    completed_bronze_workspace, record_bronze_success)
from masar.benchmark import expected_aggregate
DATA = ROOT / "data/masar-small-v1"

class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        (self.root / "course.json").write_text("{}")
    def tearDown(self):
        self.temp.cleanup()
    def test_fresh_runs_are_distinct(self):
        a, b = new_workspace(self.root), new_workspace(self.root)
        self.assertNotEqual(a, b)
        self.assertNotEqual(json.loads((a/MARKER).read_text())["run_id"], json.loads((b/MARKER).read_text())["run_id"])
    def test_old_work_preserved(self):
        a = new_workspace(self.root)
        (a/"keep.txt").write_text("retain")
        new_workspace(self.root)
        self.assertEqual((a/"keep.txt").read_text(), "retain")
    def test_missing_root_rejected(self):
        with self.assertRaises(ValueError): new_workspace(self.root/"missing")
    def test_unsafe_label_rejected(self):
        for label in ["../bad", "/tmp/bad", "A b", ""]:
            with self.subTest(label=label), self.assertRaises(ValueError): new_workspace(self.root, label)
    def test_nested_path_allowed(self):
        w = new_workspace(self.root)
        self.assertEqual(workspace_path(w,"reports/a.json"), w/"reports/a.json")
    def test_unsafe_paths_rejected(self):
        w = new_workspace(self.root)
        for path in ["../escape", "/etc/passwd", "a/../../bad", ""]:
            with self.subTest(path=path), self.assertRaises(ValueError): workspace_path(w,path)
    def test_unmarked_path_rejected(self):
        with self.assertRaises(ValueError): workspace_path(self.root,"reports")
    def test_bad_marker_rejected(self):
        w=new_workspace(self.root)
        (w/MARKER).write_text('{"dataset":"other","run_id":"x"}')
        with self.assertRaises(ValueError): workspace_path(w,"report")
    def test_symlink_parent_rejected(self):
        w=new_workspace(self.root)
        (w/"linked").symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(ValueError): workspace_path(w,"linked/file.json")
    def test_output_symlink_rejected(self):
        elsewhere = Path(self.temp.name)/"other";elsewhere.mkdir()
        (self.root/"outputs").symlink_to(elsewhere,target_is_directory=True)
        with self.assertRaises(ValueError): new_workspace(self.root)
    def test_json_written_atomically(self):
        w=new_workspace(self.root);p=w/"report.json"
        write_json(p,{"ar":"مسار","x":1})
        self.assertEqual(json.loads(p.read_text()), {"ar":"مسار","x":1})
        self.assertEqual(sorted(x.name for x in w.iterdir()), sorted([MARKER,"report.json"]))
    def test_nonfinite_json_rejected_without_change(self):
        w=new_workspace(self.root);p=w/"report.json";write_json(p,{"x":1})
        with self.assertRaises(ValueError):write_json(p,{"x":float("nan")})
        self.assertEqual(json.loads(p.read_text()),{"x":1})
    def test_missing_success_pointer_rejected(self):
        with self.assertRaises(FileNotFoundError):completed_bronze_workspace(self.root)
    def test_empty_bronze_report_cannot_record_success(self):
        w=new_workspace(self.root);write_json(w/"reports/bronze.json",{})
        with self.assertRaises(ValueError):record_bronze_success(self.root,w)
    def test_failed_bronze_report_cannot_record_success(self):
        w=new_workspace(self.root);write_json(w/"reports/bronze.json",{"scope":"DAY01_BRONZE_ENGINE","engine_executed":False})
        with self.assertRaises(ValueError):record_bronze_success(self.root,w)
    def test_pointer_traversal_rejected(self):
        (self.root/"outputs").mkdir();write_json(self.root/"outputs/day01_bronze_success.json",{"workspace":"../../escape"})
        with self.assertRaises(ValueError):completed_bronze_workspace(self.root)

class DeterministicHelperTests(unittest.TestCase):
    def test_manifest_pinned(self):self.assertEqual(require_fixed_dataset(DATA)["label"],"MASAR_SMALL_V1")
    def test_modified_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/"data";shutil.copytree(DATA,d);p=d/"manifest.json"
            m=json.loads(p.read_text());m["seed"]=99;p.write_text(json.dumps(m))
            with self.assertRaises(ValueError):require_fixed_dataset(d)
    def test_digest_order_independent(self):
        self.assertEqual(rows_digest([{"x":"a"},{"x":"b"}]),rows_digest([{"x":"b"},{"x":"a"}]))
    def test_digest_preserves_duplicates(self):
        self.assertNotEqual(rows_digest([{"x":"a"}]),rows_digest([{"x":"a"},{"x":"a"}]))
    def test_digest_preserves_whitespace(self):
        self.assertNotEqual(rows_digest([{"city":"Riyadh"}]),rows_digest([{"city":" Riyadh "}]))
    def test_digest_preserves_types(self):
        self.assertNotEqual(rows_digest([{"x":"1"}]),rows_digest([{"x":1}]))
    def test_median_not_minimum(self):
        r=summarize_samples([0.1,0.3,0.2,0.4]);self.assertEqual(r["median_s"],0.25);self.assertEqual(r["min_s"],0.1)
    def test_bad_durations_rejected(self):
        for vals in [[],[0],[-1],[float("nan")],[float("inf")],[True],["0.2"]]:
            with self.subTest(vals=vals),self.assertRaises(ValueError):summarize_samples(vals)
    def test_independent_fare_oracle(self):
        import csv
        from decimal import Decimal
        with (DATA/"trips.csv").open() as h: rows=list(csv.DictReader(h))
        expected={"rows":72,"nonnull_fares":72,"fare_total":format(sum(Decimal(x["fare_sar"]) for x in rows),".2f")}
        self.assertEqual(expected_aggregate(DATA),expected)

class EnvironmentTests(unittest.TestCase):
    def probe(self, versions=None, java='openjdk version "17.0.1"', returncode=0):
        versions=runtime.PINNED if versions is None else versions
        def version(name):
            if name not in versions:raise importlib.metadata.PackageNotFoundError(name)
            return versions[name]
        result=subprocess.CompletedProcess(["java"],returncode,stdout="",stderr=java)
        with patch.object(runtime.importlib.metadata,"version",side_effect=version),patch.object(runtime.subprocess,"run",return_value=result),patch.object(runtime.sys,"version_info",(3,11,0)):
            # Version acceptance is unit-tested against the course target, not this QA host.
            return runtime.inspect_environment()
    def test_parse_supported_java(self):
        for text, major in [('openjdk version "21.0.1"',21),('java version "17.0.2"',17),('openjdk 17.0.3',17),('java version "1.8.0_20"',8)]:
            with self.subTest(text=text):self.assertEqual(runtime.java_major(text),major)
    def test_invalid_java_output(self):self.assertIsNone(runtime.java_major("not Java"))
    def test_present_dependencies_are_not_engine_proof(self):
        r=self.probe();self.assertFalse(r["engine_executed"]);self.assertEqual(r["status"],"DEPENDENCIES_PRESENT_ENGINE_NOT_TESTED")
    def test_missing_packages_blocked(self):self.assertEqual(self.probe({})["status"],"BLOCKED_DEPENDENCIES")
    def test_wrong_version_blocked(self):self.assertTrue(self.probe({**runtime.PINNED,"pyspark":"3.5.1"})["issues"])
    def test_java8_blocked(self):self.assertTrue(self.probe(java='java version "1.8.0_20"')["issues"])
    def test_java_error_blocked(self):self.assertTrue(self.probe(returncode=1)["issues"])
    def test_environment_failure_raises_before_engine(self):
        with patch.object(runtime,"inspect_environment",return_value={"issues":["missing dependency"]}):
            with self.assertRaises(runtime.EnvironmentUnavailable):runtime.require_environment()

if __name__ == "__main__":unittest.main()
