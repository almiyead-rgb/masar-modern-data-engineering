"""A small executable data preview, NOT a substitute for the native course labs."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import json
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.workspace import require_fixed_dataset, DATASET_MANIFEST_SHA256
from masar.silver_reference import reference_result
from masar.delta_reference import day03_reference
from masar.trust_reference import day04_reference
from masar.serving_reference import day05_reference

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("Expected a non-empty teaching table")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

def main() -> int:
    source = ROOT / "data/masar-small-v1"
    require_fixed_dataset(source)
    outputs = ROOT / "outputs"
    if outputs.is_symlink():
        raise ValueError("Outputs must be a local directory")
    outputs.mkdir(exist_ok=True)
    target = Path(tempfile.mkdtemp(prefix="student_demo_", dir=outputs))
    silver = reference_result(source)
    corrected = day03_reference(source)
    trust = day04_reference(source)
    gold = day05_reference(source)
    for name, rows in gold["tables"].items():
        write_csv(target / (name.replace(".", "_") + ".csv"), rows)
    write_csv(target / "silver_corrected_reference.csv", corrected["expected_corrected_rows"])
    summary = {
        "scope": "EXECUTED_DATA_PREVIEW_NOT_NATIVE_LAKEHOUSE",
        "engine_executed": False,
        "dataset_manifest_sha256": DATASET_MANIFEST_SHA256,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_trips": silver["stages"][0]["silver_rows"],
        "final_trips": corrected["after"]["rows"],
        "fare_sar": corrected["after"]["fare_sar"],
        "event_deliveries": trust["deliveries"]["total"],
        "unique_events": trust["distinct_events"],
        "quarantined_rows": trust["quality_mixed"]["rejected_rows"],
        "gold_row_counts": gold["row_counts"],
        "checks_passed": sum(sum(v is True for v in x["checks"].values()) for x in [silver, corrected, trust, gold]),
        "future_labels": gold["label_status"],
        "native_status": "NOT_EXECUTED_BY_THIS_COMMAND",
        "results": target.relative_to(ROOT).as_posix(),
    }
    (target / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
