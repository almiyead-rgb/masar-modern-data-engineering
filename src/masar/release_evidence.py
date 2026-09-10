"""Fail-closed, file-backed acceptance checks for two local native executions.

This is an integrity and completeness audit of trusted local runs, not remote
attestation. It neither provisions services nor approves teaching/publication.
"""
from __future__ import annotations
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from masar.native_contracts import STAGES, read_stage_report, verify_artifact_records
from masar.workspace import DATASET_MANIFEST_SHA256, workspace_path, digest_file, write_json

SHA256 = re.compile(r'[0-9a-f]{64}')
RUN_ID = re.compile(r'[0-9a-f]{32}')
EVIDENCE_TREES = ('reports', 'mini_lakehouse', 'checkpoints', 'sandbox')
INVENTORY = 'reports/integration_inventory.json'


def implementation_digest(root: Path) -> str:
    """Hash runtime sources, SQL, dbt inputs and pins, not outputs or status flags."""
    root = Path(root).resolve()
    selected = []
    for folder in ('src', 'scripts', 'config', 'sql', 'day05/sql', 'day02/dbt', 'infrastructure'):
        for p in (root / folder).rglob('*'):
            if (p.is_file() and (p.suffix in {'.py', '.sql', '.yml', '.yaml', '.json', '.txt', '.sh'} or p.name == 'Dockerfile')
                    and not any(x in {'target', 'logs', 'dbt_packages', '__pycache__'} for x in p.parts)
                    and (p.name != 'profiles.yml' or p.parent == root / 'day02/dbt/profiles')):
                selected.append(p)
    selected.extend(root.glob('requirements*.txt'))
    if (root / '.dockerignore').is_file():
        selected.append(root / '.dockerignore')
    if (root / 'runtime-target.json').is_file():
        selected.append(root / 'runtime-target.json')
    lines = [p.relative_to(root).as_posix() + '\0' + digest_file(p) for p in sorted(set(selected))]
    return hashlib.sha256(('\n'.join(lines) + '\n').encode()).hexdigest()


def _safe_path(root: Path, relative: str) -> Path:
    root = Path(root).resolve()
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Expected a portable relative evidence path')
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Evidence path escapes repository')
    p = root / rel
    for part in [p, *p.parents]:
        if part == root:
            break
        if part.is_symlink():
            raise ValueError('Symlink evidence is not accepted')
    if not p.resolve().is_relative_to(root):
        raise ValueError('Evidence path escapes repository')
    return p


def _object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('Evidence must be a JSON object: ' + path.name)
    return value


def _record(root: Path, reference: dict) -> tuple[Path, dict]:
    if (not isinstance(reference, dict) or set(reference) != {'path', 'sha256'}
            or not isinstance(reference['sha256'], str) or not SHA256.fullmatch(reference['sha256'])):
        raise ValueError('Evidence requires a path and SHA256 descriptor')
    p = _safe_path(root, reference['path'])
    if not p.is_file() or p.stat().st_size == 0 or digest_file(p) != reference['sha256']:
        raise ValueError('Missing or changed evidence: ' + reference['path'])
    return p, _object(p)


def inventory_files(work: Path) -> dict[str, str]:
    """Seal actual output evidence, excluding the inventory's own self-reference."""
    files = {'.masar-workspace.json': digest_file(workspace_path(work, '.masar-workspace.json'))}
    for name in EVIDENCE_TREES:
        parent = workspace_path(work, name)
        for p in parent.rglob('*'):
            if p.is_symlink():
                raise ValueError('Symlink in runtime evidence')
            if p.is_file():
                relative = p.relative_to(work).as_posix()
                if relative != INVENTORY:
                    files[relative] = digest_file(workspace_path(work, relative))
    return dict(sorted(files.items()))


def seal_inventory(work: Path) -> dict:
    record = {'scope': 'NATIVE_OUTPUT_FILE_INVENTORY', 'files': inventory_files(work)}
    path = workspace_path(work, INVENTORY)
    write_json(path, record)
    return {'path': path.as_posix(), 'sha256': digest_file(path)}


def _native_run(root: Path, item: dict) -> dict:
    from masar.serving_reference import TABLE_COLUMNS
    if not isinstance(item, dict):
        raise ValueError('Each native run must be an object')
    work = _safe_path(root, item.get('workspace'))
    marker = _object(workspace_path(work, '.masar-workspace.json'))
    run_id = item.get('run_id')
    if not isinstance(run_id, str) or not RUN_ID.fullmatch(run_id) or marker['run_id'] != run_id:
        raise ValueError('Independent workspace identity is missing or inconsistent')
    report_path, report = _record(root, item.get('report'))
    if report_path != workspace_path(work, 'reports/integration.json'):
        raise ValueError('Integration report must belong to its stated workspace')
    if (report.get('scope') != 'MASAR_NATIVE_INTEGRATION'
            or report.get('status') != 'PASSED_NATIVE_PATH_DBT_NOT_VALIDATED'
            or report.get('engine_executed') is not True or report.get('run_id') != run_id
            or report.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256
            or report.get('implementation_sha256') != implementation_digest(root)
            or report.get('stage_names') != list(STAGES)):
        raise ValueError('Full native integration evidence is incomplete or stale')
    pid = report.get('process_id')
    if type(pid) is not int or pid <= 0:
        raise ValueError('Native process identity is missing')
    start = datetime.fromisoformat(report['started_at_utc'])
    finish = datetime.fromisoformat(report['finished_at_utc'])
    if start.tzinfo is None or finish.tzinfo is None or finish <= start:
        raise ValueError('Native execution time range is missing or invalid')
    inventory_path, inventory = _record(root, item.get('inventory'))
    if (inventory_path != workspace_path(work, INVENTORY)
            or inventory.get('scope') != 'NATIVE_OUTPUT_FILE_INVENTORY'
            or inventory.get('files') != inventory_files(work)):
        raise ValueError('Native output files do not match the sealed inventory')
    journal = _object(workspace_path(work, 'reports/integration_stages.json'))
    stages = journal.get('stages')
    if (journal.get('status') != 'PASSED' or not isinstance(stages, list)
            or [s.get('stage') for s in stages if isinstance(s, dict)] != list(STAGES)):
        raise ValueError('The complete ordered stage journal is required')
    for name, entry in zip(STAGES, stages):
        actual = read_stage_report(work, name)
        if entry.get('status') != 'PASSED' or entry.get('result') != actual:
            raise ValueError('Journal differs from saved native stage report: ' + name)
    pointer = _object(workspace_path(work, 'reports/day05_gold_latest.json'))
    manifest = workspace_path(work, pointer['manifest'])
    if digest_file(manifest) != pointer['manifest_sha256']:
        raise ValueError('Gold manifest changed')
    gold = _object(manifest)
    if (gold.get('scope') != 'DAY05_NATIVE_GOLD' or gold.get('engine_executed') is not True
            or gold.get('run_id') != pointer.get('run_id')
            or gold.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256
            or not isinstance(gold.get('checks'), dict) or not gold['checks']
            or not all(v is True for v in gold['checks'].values())
            or set(gold.get('tables', {})) != set(TABLE_COLUMNS)):
        raise ValueError('Complete verified Gold release is missing')
    digests = {}
    for name, table in gold['tables'].items():
        value = table.get('content_sha256')
        if (not isinstance(value, str) or not SHA256.fullmatch(value)
                or type(table.get('version')) is not int or table['version'] < 0
                or type(table.get('row_count')) is not int or table['row_count'] <= 0
                or verify_artifact_records(work, table.get('artifacts')) < 2):
            raise ValueError('Gold table lacks actual version/data evidence: ' + name)
        digests[name] = value
    return {'run_id': run_id, 'process_id': pid, 'workspace': str(work), 'table_digests': digests}


def engine_evidence_issues(root: Path) -> list[str]:
    path = Path(root) / 'evidence/engine_validation.json'
    if not path.is_file():
        return ['Teaching release blocked: no independent engine-run validation evidence']
    try:
        record = _object(_safe_path(root, 'evidence/engine_validation.json'))
        if (record.get('scope') != 'TWO_NATIVE_RUNS_FILE_BACKED'
                or record.get('status') != 'PASSED' or record.get('all_eight_labs_verified') is not True
                or record.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256):
            raise ValueError('Unreviewed or wrong-scope engine evidence index')
        runs = record.get('runs')
        if not isinstance(runs, list) or len(runs) != 2:
            raise ValueError('Two complete native runs are required')
        results = [_native_run(Path(root), item) for item in runs]
        for key in ('run_id', 'workspace', 'process_id'):
            if len({r[key] for r in results}) != 2:
                raise ValueError('Runs are not independent: ' + key)
        if results[0]['table_digests'] != results[1]['table_digests']:
            raise ValueError('Native business-table contents differ across runs')
        # Every verified notebook must be bound to this reviewed evidence package.
        cfg = _object(Path(root) / 'course.json')
        wanted = {n['path'] for n in cfg['notebooks'] if n['kind'] == 'engine'}
        refs = record.get('notebooks')
        if not isinstance(refs, dict) or set(refs) != wanted:
            raise ValueError('All ten executed native notebooks require file hashes')
        for relative, sha in refs.items():
            nb_path = _safe_path(root, relative)
            if not isinstance(sha, str) or not SHA256.fullmatch(sha) or digest_file(nb_path) != sha:
                raise ValueError('Executed notebook is missing or changed: ' + relative)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        return ['Teaching release blocked: invalid file-backed native evidence: ' + str(exc)]
    return []


def dbt_evidence_issues(root: Path) -> list[str]:
    path = Path(root) / 'evidence/dbt_validation.json'
    if not path.is_file():
        return ['Teaching release blocked: no actual dbt run artifacts']
    try:
        record = _object(_safe_path(root, 'evidence/dbt_validation.json'))
        if (record.get('scope') != 'DBT_EXECUTION_EVIDENCE' or record.get('status') != 'PASSED'
                or record.get('dbt_executed') is not True or record.get('adapter') != 'spark'):
            raise ValueError('Invalid dbt execution summary')
        _, result = _record(root, record.get('run_results'))
        _, manifest = _record(root, record.get('manifest'))
        invocation = result.get('metadata', {}).get('invocation_id')
        if not invocation or invocation != manifest.get('metadata', {}).get('invocation_id'):
            raise ValueError('dbt artifact invocation identities differ')
        nodes = manifest.get('nodes', {})
        observed = result.get('results')
        if (not isinstance(observed, list) or not observed
                or any(not isinstance(n, dict) or n.get('status') not in {'success', 'pass'} for n in observed)):
            raise ValueError('dbt models/tests did not all succeed')
        ids = [n.get('unique_id') for n in observed]
        if len(ids) != len(set(ids)) or any(n not in nodes for n in ids):
            raise ValueError('dbt result nodes are missing or repeated')
        project = Path(root) / 'day02/dbt'
        for folder, kind in [('models', 'model'), ('tests', 'test')]:
            required = {p.stem for p in (project / folder).rglob('*.sql')}
            actual = {nodes[n].get('name') for n in ids if nodes[n].get('resource_type') == kind}
            if not required or not required.issubset(actual):
                raise ValueError('dbt ' + kind + ' coverage is incomplete')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        return ['Teaching release blocked: invalid dbt evidence: ' + str(exc)]
    return []
