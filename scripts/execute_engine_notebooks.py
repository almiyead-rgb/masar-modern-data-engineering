"""Execute native student notebooks in a throwaway source COPY, never source originals.

The results are execution evidence pending review, not automatic course approval.
"""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.workbench import utc_now
from masar.workspace import write_json, digest_file

def main() -> int:
    # This marker is created by the coordinator, not by a learner notebook.
    if not (ROOT / '.native-notebook-copy.json').is_file():
        raise SystemExit('Only run via verify_native_runtime.py in its isolated notebook copy')
    import nbformat
    from nbclient import NotebookClient
    registry = json.loads((ROOT / 'course.json').read_text())['notebooks']
    native = [n for n in registry if n['kind'] == 'engine' and not n.get('entrypoint_only', False)]
    if len(native) != 10:
        raise ValueError('The eight labs must have the expected ten native notebooks')
    evidence = ROOT / 'outputs/native_notebook_execution'
    report = {'scope': 'NATIVE_NOTEBOOK_EXECUTION', 'status': 'RUNNING',
        'started_at_utc': utc_now(), 'notebooks': [], 'teaching_approved': False}
    try:
        for item in native:
            path = ROOT / item['path']
            notebook = nbformat.read(path, as_version=4)
            record = {'path': item['path'], 'source_sha256': digest_file(path), 'status': 'STARTED'}
            report['notebooks'].append(record)
            try:
                NotebookClient(notebook, timeout=900, kernel_name='python3',
                    resources={'metadata': {'path': str(path.parent)}}, allow_errors=False).execute()
                code = [c for c in notebook.cells if c.cell_type == 'code']
                if not code or any(c.execution_count is None or any(o.output_type == 'error' for o in c.outputs) for c in code):
                    raise ValueError('The notebook did not execute every code cell successfully')
                record.update(status='EXECUTED_PENDING_REVIEW', code_cells=len(code))
                notebook.metadata['runtime_evidence'] = {'status': 'EXECUTED_PENDING_REVIEW', 'not_teaching_approval': True}
            except Exception as exc:
                record.update(status='FAILED', error_type=type(exc).__name__, error=str(exc))
                raise
            finally:
                saved = evidence / item['path']
                saved.parent.mkdir(parents=True, exist_ok=True)
                # Save actual outputs even on failure; never invent execution counts.
                nbformat.write(notebook, saved)
                record['saved_path'] = saved.relative_to(ROOT).as_posix()
                record['saved_sha256'] = digest_file(saved)
                write_json(evidence / 'summary.json', report)
        report['status'] = 'EXECUTED_PENDING_REVIEW'
    except Exception as exc:
        report.update(status='FAILED', error_type=type(exc).__name__, error=str(exc))
    report['finished_at_utc'] = utc_now()
    write_json(evidence / 'summary.json', report)
    print(json.dumps({'status': report['status'], 'notebooks_attempted': len(report['notebooks']),
        'summary': str((evidence / 'summary.json').relative_to(ROOT))}, indent=2))
    return 0 if report['status']=='EXECUTED_PENDING_REVIEW' else 1

if __name__=='__main__':
    raise SystemExit(main())
