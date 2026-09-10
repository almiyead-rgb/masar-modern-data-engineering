"""Small, standard-library safety helpers; not a Spark execution substitute."""
from __future__ import annotations
import hashlib
import json
import math
import re
import tempfile
import uuid
from pathlib import Path
from statistics import median

MARKER = ".masar-workspace.json"
DATASET_MANIFEST_SHA256 = "20a7e45bed2980b9394c10e8532da3b9f40f614366bb2df26a88610253e768e3"

def digest_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def require_fixed_dataset(source: Path) -> dict:
    """Pin the manifest itself, then verify every unchanged source payload."""
    from masar.sources import verify_manifest
    source = Path(source).resolve()
    if digest_file(source / "manifest.json") != DATASET_MANIFEST_SHA256:
        raise ValueError("The approved dataset manifest has changed")
    return verify_manifest(source)

def new_workspace(root: Path, label: str = "day01") -> Path:
    """Create a new output directory; never remove or overwrite an old run."""
    root = Path(root).resolve()
    if not (root / "course.json").is_file():
        raise ValueError("Expected the complete course repository")
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,30}", label):
        raise ValueError("Invalid workspace label")
    parent = root / "outputs"
    if parent.is_symlink():
        raise ValueError("Outputs must not be a symlink")
    parent.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=label + "_", dir=parent))
    write_json(work / MARKER, {"dataset": "MASAR_SMALL_V1", "run_id": uuid.uuid4().hex})
    return work

def workspace_path(work: Path, relative: str) -> Path:
    """Only allow descendants of an explicitly marked Masar workspace."""
    original = Path(work)
    if original.is_symlink():
        raise ValueError("Workspace must not be a symlink")
    work = original.resolve()
    marker = work / MARKER
    if not marker.is_file() or marker.is_symlink():
        raise ValueError("Not an initialized Masar workspace")
    state = json.loads(marker.read_text(encoding="utf-8"))
    if state.get("dataset") != "MASAR_SMALL_V1" or not re.fullmatch(r"[0-9a-f]{32}", state.get("run_id", "")):
        raise ValueError("Invalid workspace marker")
    rel = Path(relative)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        raise ValueError("Use a relative path without parent traversal")
    target = work / rel
    for part in [target, *target.parents]:
        if part == work:
            break
        if part.is_symlink():
            raise ValueError("Symlink within workspace")
    if not target.resolve().is_relative_to(work):
        raise ValueError("Path leaves workspace")
    return target

def write_json(path: Path, value: dict) -> None:
    """Atomic JSON replacement; reject non-finite numbers in evidence."""
    path = Path(path)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as f:
        temp = Path(f.name)
        f.write(payload)
    try:
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)

def rows_digest(rows: list[dict]) -> str:
    """Order-independent multiset hash: duplicate rows remain significant."""
    lines = sorted(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) for row in rows)
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()

def summarize_samples(values: list[float]) -> dict:
    if not values or any(type(x) not in (int, float) or not math.isfinite(x) or x <= 0 for x in values):
        raise ValueError("Measured durations must be non-empty, finite and positive")
    return {"samples_s": values, "median_s": median(values), "min_s": min(values), "max_s": max(values)}

def record_bronze_success(root: Path, work: Path) -> None:
    """Record the last successful Bronze run for the next cumulative lab."""
    root = Path(root).resolve()
    work = Path(work).resolve()
    if not work.is_relative_to(root / "outputs"):
        raise ValueError("Bronze workspace must be under course outputs")
    report_path = workspace_path(work, "reports/bronze.json")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if (report.get("scope") != "DAY01_BRONZE_ENGINE" or report.get("engine_executed") is not True
        or report.get("counts") != {"trips": 144, "drivers": 6, "gps_events": 216}
        or not report.get("checks") or not all(v is True for v in report["checks"].values())
        or report.get("dataset_manifest_sha256") != DATASET_MANIFEST_SHA256):
        raise ValueError("Bronze has not passed its required checks")
    marker = json.loads((work / MARKER).read_text(encoding="utf-8"))
    write_json(root / "outputs/day01_bronze_success.json", {
        "workspace": work.relative_to(root).as_posix(), "run_id": marker["run_id"],
        "bronze_report_sha256": digest_file(report_path),
        "meaning": "Last successful Bronze run; not full-course approval"})

def completed_bronze_workspace(root: Path) -> Path:
    """Reuse exactly the successful workspace instead of rebuilding source data."""
    root = Path(root).resolve()
    pointer = root / "outputs/day01_bronze_success.json"
    if not pointer.is_file() or pointer.is_symlink():
        raise FileNotFoundError("Run the Bronze notebook successfully before the scan notebook")
    info = json.loads(pointer.read_text(encoding="utf-8"))
    relative = Path(info["workspace"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Unsafe saved workspace")
    work = root / relative
    if work.is_symlink() or not work.resolve().is_relative_to(root / "outputs"):
        raise ValueError("Saved workspace leaves course outputs")
    report_path = workspace_path(work, "reports/bronze.json")
    if digest_file(report_path) != info["bronze_report_sha256"]:
        raise ValueError("Saved Bronze report was changed")
    if json.loads((work / MARKER).read_text())["run_id"] != info["run_id"]:
        raise ValueError("Saved workspace identity mismatch")
    return work.resolve()
