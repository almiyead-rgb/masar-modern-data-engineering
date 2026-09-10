"""Observe real Spark actions on equal 72-row inputs, without speed-up promises."""
from __future__ import annotations
import csv
import io
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from time import perf_counter
from masar.bronze import raw_frame
from masar.workspace import DATASET_MANIFEST_SHA256, require_fixed_dataset, rows_digest, summarize_samples, workspace_path, write_json

def expected_aggregate(source: Path) -> dict:
    """Independent arithmetic oracle, never a fabricated runtime measurement."""
    require_fixed_dataset(source)
    with (Path(source) / "trips.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {"rows": len(rows), "nonnull_fares": len(rows),
            "fare_total": format(sum((Decimal(r["fare_sar"]) for r in rows), Decimal("0")), ".2f")}

def benchmark(spark, source: Path, work: Path, repetitions: int = 4) -> dict:
    from pyspark.sql import functions as F
    require_fixed_dataset(source)
    if type(repetitions) is not int or not 2 <= repetitions <= 10 or repetitions % 2:
        raise ValueError("Use an even repetition count between 2 and 10 for balanced order")
    table = workspace_path(work, "mini_lakehouse/bronze/trips")
    # Version 0 is the same initial 72-row population as CSV, not the 144-row replay state.
    def frame(name):
        if name == "csv":
            return raw_frame(spark, source, "trips")
        return spark.read.format("delta").option("versionAsOf", 0).load(str(table))
    columns = raw_frame(spark, source, "trips").columns
    payload_hashes = {name: rows_digest([r.asDict() for r in frame(name).select(*columns).collect()])
                      for name in ("csv", "delta_v0")}
    if len(set(payload_hashes.values())) != 1:
        raise AssertionError("Cannot compare different source populations")
    expected = expected_aggregate(source)
    def query(name):
        return frame(name).select(F.col("fare_sar").cast("decimal(12,2)").alias("fare"))\
            .agg(F.count("*").alias("rows"), F.count("fare").alias("nonnull_fares"), F.sum("fare").alias("fare_total"))
    def execute(name):
        # Deliberately include query construction/planning plus Spark action and collect.
        result = query(name).collect()[0].asDict()
        result["fare_total"] = format(result["fare_total"], ".2f")
        if result != expected:
            raise AssertionError({"query": name, "expected": expected, "actual": result})
        return result
    plans = {}
    for name in ("csv", "delta_v0"):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            query(name).explain(mode="formatted")
        text = buffer.getvalue()
        if not text.strip():
            raise AssertionError("Missing actual Spark query plan")
        dest = workspace_path(work, "reports/plans/" + name + ".txt")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        plans[name] = str(dest.relative_to(work))
    # No explicit DataFrame cache is used. OS / JVM / Delta metadata caches may remain warm.
    spark.catalog.clearCache()
    for name in ("csv", "delta_v0"):
        execute(name)
    measurements = {"csv": [], "delta_v0": []}
    order = []
    for i in range(repetitions):
        names = ("csv", "delta_v0") if i % 2 == 0 else ("delta_v0", "csv")
        order.append(list(names))
        for name in names:
            start = perf_counter()
            execute(name)
            measurements[name].append(perf_counter() - start)
    report = {"scope": "DAY01_SPARK_LOCAL_BENCHMARK", "engine_executed": True,
        "spark_version": spark.version, "dataset_manifest_sha256": DATASET_MANIFEST_SHA256,
        "checks": {"equal_source_populations": len(set(payload_hashes.values())) == 1,
                   "query_results_match_oracle": True, "positive_measured_samples": all(
                       bool(summarize_samples(v)) for v in measurements.values()),
                   "query_plans_saved": set(plans) == {"csv", "delta_v0"}},
        "expected_and_observed_aggregate": expected,
        "snapshot_version": 0, "population_rows": 72, "payload_hashes": payload_hashes,
        "warmups_per_variant": 1, "repetitions_per_variant": repetitions,
        "execution_order": order, "plans": plans,
        "timing_scope": "query construction, planning, Spark action and collect; excludes session startup and ingestion",
        "cache_condition": "no explicit Spark cache; repeated local reads; OS/JVM/metadata caches not controlled",
        "measurements": {name: summarize_samples(values) for name, values in measurements.items()},
        "limitations": ["Tiny synthetic fixture", "Local CPU and storage only", "No guaranteed ranking or speed-up", "Not cloud pricing or distributed scalability evidence"]}
    write_json(workspace_path(work, "reports/benchmark.json"), report)
    return report
