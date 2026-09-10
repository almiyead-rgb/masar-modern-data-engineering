from pathlib import Path
import json, shutil, sys, tempfile, unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.sources import verify_manifest, load_sources, profile_sources, valid_location
SOURCE = ROOT / "data" / "masar-small-v1"
class SourceTests(unittest.TestCase):
    def test_manifest(self):
        self.assertEqual(len(verify_manifest(SOURCE)["files"]), 10)
    def test_counts(self):
        self.assertEqual({k:len(v) for k,v in load_sources(SOURCE).items()}, {"trips":72,"drivers":6,"gps_events":216})
    def test_checks_and_engine_boundary(self):
        r=profile_sources(SOURCE)
        self.assertTrue(all(r["checks"].values()))
        self.assertIs(r["delta_executed"],False)
    def test_observed_city_variants(self):
        self.assertEqual(profile_sources(SOURCE)["city_profile"]["rows_changed_by_normalization"],10)
    def test_deterministic_results(self):
        self.assertEqual(profile_sources(SOURCE),profile_sources(SOURCE))
    def test_source_bytes_unchanged(self):
        before={p.name:p.read_bytes() for p in SOURCE.iterdir()}
        profile_sources(SOURCE)
        self.assertEqual(before,{p.name:p.read_bytes() for p in SOURCE.iterdir()})
    def test_corruption_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            copy=Path(d)/"data";shutil.copytree(SOURCE,copy)
            with (copy/"trips.csv").open("a") as f:f.write("bad\n")
            with self.assertRaises(ValueError):verify_manifest(copy)
    def test_missing_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            copy=Path(d)/"data";shutil.copytree(SOURCE,copy);(copy/"drivers.csv").unlink()
            with self.assertRaises(ValueError):verify_manifest(copy)
    def test_duplicate_manifest_entry_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            copy=Path(d)/"data";shutil.copytree(SOURCE,copy)
            m=json.loads((copy/"manifest.json").read_text());m["files"][1]=m["files"][0]
            (copy/"manifest.json").write_text(json.dumps(m))
            with self.assertRaises(ValueError):verify_manifest(copy)
    def test_valid_location_boundaries(self):
        self.assertTrue(valid_location({"location":{"lat":90,"lon":-180}}))
    def test_invalid_locations(self):
        for event in [{},{"location":{}},{"location":{"lat":True,"lon":1}},{"location":{"lat":float("nan"),"lon":1}},{"location":{"lat":91,"lon":1}}]:
            with self.subTest(event=event):self.assertFalse(valid_location(event))
