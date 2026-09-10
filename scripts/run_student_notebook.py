"""Run the single eight-lab notebook once, saving actual outputs even on failure."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    outputs = ROOT / "outputs"
    if outputs.is_symlink():
        raise ValueError("Outputs must be a local directory")
    outputs.mkdir(exist_ok=True)
    attempt = Path(tempfile.mkdtemp(prefix="student_native_", dir=outputs))
    report = {"scope": "SINGLE_STUDENT_NOTEBOOK_EXECUTION", "status": "STARTED",
              "labs": list(range(1, 9)), "complete_native_run": False,
              "started_at_utc": datetime.now(timezone.utc).isoformat()}
    notebook = None
    try:
        import nbformat
        from nbclient import NotebookClient
        notebook = nbformat.read(ROOT / "MASAR_STUDENT.ipynb", as_version=4)
        NotebookClient(notebook, timeout=1200, kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}}, allow_errors=False).execute()
        cells = [c for c in notebook.cells if c.cell_type == "code"]
        if not cells or any(c.execution_count is None or any(o.output_type == "error" for o in c.outputs) for c in cells):
            raise RuntimeError("Not all code cells completed")
        report.update(status="PASSED", complete_native_run=True, executed_code_cells=len(cells))
        return_code = 0
    except Exception as exc:
        report.update(status="FAILED", error_type=type(exc).__name__, error=str(exc))
        return_code = 1
    finally:
        report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        if notebook is not None:
            import nbformat
            notebook.metadata["execution_evidence"] = {
                "status": report["status"], "complete_native_run": report["complete_native_run"]}
            nbformat.write(notebook, attempt / "MASAR_STUDENT.executed.ipynb")
        (attempt / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "complete_native_run": report["complete_native_run"],
                      "evidence": attempt.relative_to(ROOT).as_posix()}, indent=2))
    return return_code

if __name__ == "__main__":
    raise SystemExit(main())
