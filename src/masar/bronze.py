"""Native PySpark/Delta Bronze lab implementation; runtime validation is pending.

Single local writer only. The explicit batch guard is not a distributed
exactly-once protocol. A fresh notebook run creates a new isolated workspace.
"""
from __future__ import annotations
import csv
import re
from pathlib import Path
from masar.workspace import digest_file, require_fixed_dataset, rows_digest, workspace_path, write_json

FEEDS = {"trips": "trips.csv", "drivers": "drivers.csv", "gps_events": "gps.ndjson"}

def source_payload_rows(source: Path, feed: str) -> list[dict]:
    """Read fixed source values independently of Spark for readback comparison."""
    if feed not in FEEDS:
        raise ValueError("Unknown source feed")
    path = Path(source) / FEEDS[feed]
    if feed == "gps_events":
        return [{"raw_json": line} for line in path.read_text(encoding="utf-8").splitlines()]
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def raw_frame(spark, source: Path, feed: str):
    """Preserve CSV strings and original event lines; do not clean Bronze."""
    from pyspark.sql import types as T
    from pyspark.sql import functions as F
    if feed not in FEEDS:
        raise ValueError("Unknown source feed")
    path = Path(source) / FEEDS[feed]
    if feed == "gps_events":
        return spark.read.text(str(path)).select(F.col("value").alias("raw_json"))
    with path.open(encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle))
    schema = T.StructType([T.StructField(name, T.StringType(), True) for name in header])
    return (spark.read.schema(schema).option("header", True).option("enforceSchema", False)
        .option("mode", "FAILFAST").option("ignoreLeadingWhiteSpace", False)
        .option("ignoreTrailingWhiteSpace", False).csv(str(path)))

def ingest_feed(spark, source: Path, work: Path, feed: str, batch_id: str) -> dict:
    from pyspark.sql import functions as F
    from delta.tables import DeltaTable
    require_fixed_dataset(source)
    if feed not in FEEDS or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", batch_id):
        raise ValueError("Invalid feed or batch identifier")
    target = workspace_path(work, "mini_lakehouse/bronze/" + feed)
    exists = DeltaTable.isDeltaTable(spark, str(target))
    if target.exists() and not exists:
        raise ValueError("Destination exists but is not a Delta table; nothing was overwritten")
    if exists and spark.read.format("delta").load(str(target)).where(F.col("_batch_id") == batch_id).limit(1).count():
        raise ValueError("This batch id was already committed; use a NEW id for intentional redelivery")
    raw = raw_frame(spark, source, feed)
    expected = {"trips": 72, "drivers": 6, "gps_events": 216}[feed]
    if raw.count() != expected:
        raise ValueError("Source row count does not match the fixed base batch")
    enriched = (raw.withColumn("_source_file", F.lit(FEEDS[feed]))
        .withColumn("_source_sha256", F.lit(digest_file(Path(source) / FEEDS[feed])))
        .withColumn("_batch_id", F.lit(batch_id))
        .withColumn("_ingested_at", F.current_timestamp()))
    # Append preserves earlier transactions. Never use overwrite on Bronze.
    enriched.write.format("delta").mode("append").save(str(target))
    total = spark.read.format("delta").load(str(target)).count()
    version = int(DeltaTable.forPath(spark, str(target)).history(1).select("version").first()[0])
    return {"feed": feed, "batch_id": batch_id, "appended_rows": expected, "total_rows": total, "version": version}

def verify_bronze(spark, source: Path, work: Path) -> dict:
    from pyspark.sql import functions as F
    from delta.tables import DeltaTable
    require_fixed_dataset(source)
    counts, payloads, logs = {}, {}, {}
    for feed, filename in FEEDS.items():
        target = workspace_path(work, "mini_lakehouse/bronze/" + feed)
        if not DeltaTable.isDeltaTable(spark, str(target)):
            raise AssertionError("Missing real Delta table: " + feed)
        data = spark.read.format("delta").load(str(target))
        counts[feed] = data.count()
        if data.where((F.col("_source_sha256") != digest_file(Path(source) / filename)) | (F.col("_source_file") != filename)).count():
            raise AssertionError("Source hash metadata mismatch")
        for field in ["_source_file", "_source_sha256", "_batch_id", "_ingested_at"]:
            if data.where(F.col(field).isNull()).count():
                raise AssertionError("Null ingestion metadata")
        cols = raw_frame(spark, source, feed).columns
        payloads[feed] = {}
        source_rows = source_payload_rows(source, feed)
        for batch in (r[0] for r in data.select("_batch_id").distinct().collect()):
            rows = [r.asDict() for r in data.where(F.col("_batch_id") == batch).select(*cols).collect()]
            if rows_digest(rows) != rows_digest(source_rows):
                raise AssertionError("Bronze changed source values or multiplicity")
            payloads[feed][batch] = rows_digest(rows)
        commits = sorted((target / "_delta_log").glob("[0-9]" * 20 + ".json"))
        parquet = sorted(target.rglob("*.parquet"))
        if not commits or not parquet:
            raise AssertionError("Missing Delta log or Parquet data files")
        if any(p.stat().st_size == 0 for p in commits + parquet):
            raise AssertionError("Empty engine artifact")
        logs[feed] = {"commits": [{"path": str(p.relative_to(work)), "sha256": digest_file(p)} for p in commits],
            "data_files": [{"path": str(p.relative_to(work)), "sha256": digest_file(p)} for p in parquet]}
    trips = spark.read.format("delta").load(str(workspace_path(work, "mini_lakehouse/bronze/trips")))
    batches = {r["_batch_id"]: r["count"] for r in trips.groupBy("_batch_id").count().collect()}
    initial = spark.read.format("delta").option("versionAsOf", 0).load(str(workspace_path(work, "mini_lakehouse/bronze/trips")))
    checks = {
        "expected_totals": counts == {"trips": 144, "drivers": 6, "gps_events": 216},
        "two_trip_deliveries": batches == {"base_001": 72, "replay_002": 72},
        "business_trip_count_unchanged": trips.select("trip_id").distinct().count() == 72,
        "initial_snapshot_retained": initial.count() == 72,
        "base_csv_columns_are_strings": all(f.dataType.simpleString() == "string" for f in initial.schema if not f.name.startswith("_")),
        "payloads_and_source_hashes_preserved": True,
        "real_delta_files_present": True,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    report = {"scope": "DAY01_BRONZE_ENGINE", "engine_executed": True,
        "spark_version": spark.version, "checks": checks, "counts": counts,
        "business_trip_count": 72, "batch_counts": batches, "payload_digests": payloads,
        "artifacts": logs, "dataset_manifest_sha256": digest_file(Path(source) / "manifest.json")}
    write_json(workspace_path(work, "reports/bronze.json"), report)
    return report

def build_bronze(spark, source: Path, work: Path) -> dict:
    for feed in FEEDS:
        ingest_feed(spark, source, work, feed, "base_001")
    ingest_feed(spark, source, work, "trips", "replay_002")
    return verify_bronze(spark, source, work)
