"""Pinned local Spark setup. Dependency checks never count as engine proof."""
from __future__ import annotations
import importlib.metadata
import os
import re
import subprocess
import sys
from pathlib import Path

PINNED = {"pyspark": "3.5.8", "delta-spark": "3.3.3", "py4j": "0.10.9.9"}

class EnvironmentUnavailable(RuntimeError):
    pass

def java_major(output: str) -> int | None:
    match = re.search(r'(?:openjdk|java)\s+(?:version\s+)?["\s]*(\d+)(?:\.(\d+))?', output)
    if not match:
        return None
    return int(match.group(2)) if match.group(1) == "1" and match.group(2) else int(match.group(1))

def inspect_environment() -> dict:
    problems = []
    packages = {}
    for name, target in PINNED.items():
        try:
            observed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            observed = None
        packages[name] = {"required": target, "observed": observed}
        if observed != target:
            problems.append(f"{name}: required {target}, observed {observed}")
    major, line = None, "not available"
    try:
        java_command = str(Path(os.environ["JAVA_HOME"]) / "bin" / "java") if os.environ.get("JAVA_HOME") else "java"
        proc = subprocess.run([java_command, "-version"], capture_output=True, text=True, timeout=8, check=False)
        text = proc.stderr + proc.stdout
        line = text.splitlines()[0] if text.strip() else "no version output"
        major = java_major(text) if proc.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        pass
    if major != 17:
        problems.append("This unified course runtime requires Java 17; Java 21 is not the course target")
    if sys.version_info[:2] != (3, 11):
        problems.append("This complete course requires Python 3.11; use the documented virtual environment")
    return {"scope": "DEPENDENCY_PREFLIGHT_ONLY", "python": sys.version.split()[0],
            "java": line, "java_major": major, "packages": packages,
            "status": "BLOCKED_DEPENDENCIES" if problems else "DEPENDENCIES_PRESENT_ENGINE_NOT_TESTED",
            "issues": problems, "engine_executed": False}

def require_environment() -> dict:
    report = inspect_environment()
    if report["issues"]:
        raise EnvironmentUnavailable("; ".join(report["issues"]) + ". See docs/SETUP.md. No Spark job has run.")
    return report

def start_spark(work: Path, *, kafka: bool = False):
    """Real local PySpark+Delta, no silent alternative engine and no pip installs.

    Delta's standard helper may resolve JARs on first startup. The environment
    must be provisioned before teaching; dependency presence is not sufficient.
    """
    require_environment()
    from pyspark.sql import SparkSession
    from delta import configure_spark_with_delta_pip
    from masar.workspace import workspace_path
    if SparkSession.getActiveSession() is not None:
        raise RuntimeError("An active Spark session exists; stop it explicitly before this lab")
    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    os.environ["PYSPARK_PYTHON"] = sys.executable
    builder = (SparkSession.builder.master("local[2]").appName("Masar-Course")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.ansi.enabled", "true")
        .config("spark.pyspark.python", sys.executable)
        .config("spark.sql.timestampType", "TIMESTAMP_LTZ")
        .config("spark.sql.catalogImplementation", "in-memory")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.default.parallelism", "2")
        .config("spark.databricks.delta.snapshotPartitions", "2")
        .config("spark.jars.repositories", "https://repo.maven.apache.org/maven2")
        .config("spark.ui.enabled", "false")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.sql.warehouse.dir", str(workspace_path(work, "warehouse"))))
    if os.environ.get("MASAR_IVY_DIR"):
        builder = builder.config("spark.jars.ivy", str(Path(os.environ["MASAR_IVY_DIR"]).resolve()))
    extra = ["org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8"] if kafka else []
    spark = configure_spark_with_delta_pip(builder, extra_packages=extra).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark
