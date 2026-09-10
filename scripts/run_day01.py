"""Run real Day 1 engine work; failures return nonzero and retain diagnostics.

Usage from the repository root: python scripts/run_day01.py
No installation, publishing, cleanup or replacement engine is performed.
"""
from __future__ import annotations
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.runtime import EnvironmentUnavailable, inspect_environment, require_environment, start_spark
from masar.workspace import MARKER, new_workspace, workspace_path, write_json, record_bronze_success

def main() -> int:
    work = new_workspace(ROOT, "day01_engine")
    result = {"scope": "DAY01_ENGINE_ATTEMPT", "started_at": datetime.now(timezone.utc).isoformat(),
        "run_id": json.loads((work / MARKER).read_text())["run_id"],
        "preflight": inspect_environment(), "status": "STARTED", "engine_executed": False}
    spark = None
    try:
        require_environment()
        from masar.bronze import build_bronze
        from masar.benchmark import benchmark
        spark = start_spark(work)
        result["engine_executed"] = True
        result["bronze"] = build_bronze(spark, ROOT / "data/masar-small-v1", work)
        record_bronze_success(ROOT, work)
        result["benchmark"] = benchmark(spark, ROOT / "data/masar-small-v1", work)
        result["status"] = "PASSED"
    except EnvironmentUnavailable as exc:
        result.update(status="BLOCKED_DEPENDENCIES", error=str(exc))
    except Exception as exc:
        result.update(status="FAILED", error=f"{type(exc).__name__}: {exc}")
        workspace_path(work, "traceback.txt").write_text(traceback.format_exc(), encoding="utf-8")
    finally:
        if spark is not None:
            try:
                spark.stop()
            except Exception as exc:
                result.update(status="FAILED_STOP", stop_error=f"{type(exc).__name__}: {exc}")
        result["finished_at"] = datetime.now(timezone.utc).isoformat()
        write_json(workspace_path(work, "run.json"), result)
    print(json.dumps({"status": result["status"], "engine_executed": result["engine_executed"],
                     "evidence": str(work.relative_to(ROOT) / "run.json")}, indent=2))
    return 0 if result["status"] == "PASSED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
