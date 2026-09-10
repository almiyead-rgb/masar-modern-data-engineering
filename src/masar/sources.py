"""Inspect the unchanged synthetic fixture without mutating source data.

Scope: standard-library input validation only; never an engine-runtime proof.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

APPROVED_MANIFEST_SHA256 = "20a7e45bed2980b9394c10e8532da3b9f40f614366bb2df26a88610253e768e3"

EXPECTED_COUNTS = {"trips": 72, "drivers": 6, "gps_events": 216}

def verify_manifest(source: Path) -> dict:
    source = Path(source).resolve()
    manifest_bytes = (source / "manifest.json").read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != APPROVED_MANIFEST_SHA256:
        raise ValueError("The approved source manifest changed")
    manifest = json.loads(manifest_bytes)
    if manifest.get("label") != "MASAR_SMALL_V1" or not manifest.get("synthetic"):
        raise ValueError("Unexpected or non-synthetic dataset manifest")
    records = manifest.get("files")
    if not isinstance(records, list) or len(records) != 10:
        raise ValueError("Expected ten manifest file entries")
    seen = set()
    for record in records:
        name = record["path"]
        if name in seen:
            raise ValueError("Duplicate manifest entry")
        seen.add(name)
        path = (source / name).resolve()
        if not path.is_relative_to(source) or not path.is_file():
            raise ValueError("Unsafe or missing manifest path")
        payload = path.read_bytes()
        if len(payload) != record["bytes"]:
            raise ValueError("Dataset byte count changed: " + name)
        if hashlib.sha256(payload).hexdigest() != record["sha256"]:
            raise ValueError("Dataset SHA-256 mismatch: " + name)
        if record["rows"] is not None:
            if path.suffix == ".csv":
                with path.open(encoding="utf-8", newline="") as handle:
                    observed = sum(1 for _ in csv.DictReader(handle))
            elif path.suffix == ".ndjson":
                observed = sum(bool(line.strip()) for line in payload.decode().splitlines())
            else:
                raise ValueError("Unexpected counted file type")
            if observed != record["rows"]:
                raise ValueError("Dataset row count changed: " + name)
    return manifest

def load_sources(source: Path) -> dict:
    source = Path(source)
    verify_manifest(source)
    feeds = {}
    for name, filename in [("trips", "trips.csv"), ("drivers", "drivers.csv")]:
        with (source / filename).open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise ValueError("Missing CSV header")
            rows = list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            raise ValueError("Malformed CSV row")
        feeds[name] = rows
    feeds["gps_events"] = [json.loads(line) for line in
        (source / "gps.ndjson").read_text(encoding="utf-8").splitlines() if line.strip()]
    if {k: len(v) for k, v in feeds.items()} != EXPECTED_COUNTS:
        raise ValueError("The base fixture count is not the approved count")
    return feeds

def valid_location(event: dict) -> bool:
    location = event.get("location")
    if not isinstance(location, dict):
        return False
    lat, lon = location.get("lat"), location.get("lon")
    return (type(lat) in (int, float) and type(lon) in (int, float)
            and math.isfinite(lat) and math.isfinite(lon)
            and -90 <= lat <= 90 and -180 <= lon <= 180)

def profile_sources(source: Path) -> dict:
    feeds = load_sources(source)
    keys = {"trips": "trip_id", "drivers": "driver_id", "gps_events": "event_id"}
    profiles = {}
    for name, rows in feeds.items():
        frequencies = Counter(row.get(keys[name]) for row in rows)
        columns = sorted({column for row in rows for column in row})
        profiles[name] = {
            "rows": len(rows), "key": keys[name],
            "duplicate_key_groups": sum(n > 1 for n in frequencies.values()),
            "duplicate_excess_rows": sum(n - 1 for n in frequencies.values() if n > 1),
            "missing_top_level_fields": {c: sum(row.get(c) in (None, "") for row in rows) for c in columns},
        }
    trips, drivers, events = feeds["trips"], feeds["drivers"], feeds["gps_events"]
    trip_ids = {r["trip_id"] for r in trips}
    driver_ids = {r["driver_id"] for r in drivers}
    relations = {
        "trips_without_driver": sum(r["driver_id"] not in driver_ids for r in trips),
        "events_without_trip": sum(r["trip_id"] not in trip_ids for r in events),
        "events_with_invalid_coordinates": sum(not valid_location(r) for r in events),
    }
    per_trip = Counter(r["trip_id"] for r in events)
    cities = {
        "original_labels": dict(sorted(Counter(r["city"] for r in trips).items())),
        "normalized_labels": dict(sorted(Counter(r["city"].strip().title() for r in trips).items())),
        "rows_changed_by_normalization": sum(r["city"] != r["city"].strip().title() for r in trips),
    }
    checks = {
        "source_counts": {k: len(v) for k, v in feeds.items()} == EXPECTED_COUNTS,
        "unique_base_keys": all(p["duplicate_key_groups"] == 0 for p in profiles.values()),
        "base_top_level_complete": all(not any(p["missing_top_level_fields"].values()) for p in profiles.values()),
        "valid_links_and_coordinates": not any(relations.values()),
        "three_events_per_trip": len(per_trip) == 72 and set(per_trip.values()) == {3},
        "base_city_set": set(cities["normalized_labels"]) == {"Riyadh", "Jeddah", "Dammam"},
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {"scope": "SOURCE_FILE_INSPECTION_ONLY", "delta_executed": False,
        "dataset": "MASAR_SMALL_V1", "counts": EXPECTED_COUNTS,
        "profile": profiles, "relations": relations, "city_profile": cities, "checks": checks}
