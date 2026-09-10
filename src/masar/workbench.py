"""Local runtime packaging helpers, not engine simulation or publication.

Source snapshots never overwrite learner edits. Unit tests of this module are
configuration/contract tests and must not be reported as native engine runs.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
from typing import Iterable
from masar.workspace import write_json

STAMP = '.masar-runtime-snapshot.json'
EXCLUDED_PARTS = {'.git', '__pycache__', '.ipynb_checkpoints', '.venv', 'outputs',
    'workspaces', 'mini_lakehouse', 'spark-warehouse', 'metastore_db',
    'instructor_only', 'authoring_private', 'target', 'logs', 'dbt_packages'}

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def source_files(root: Path) -> list[Path]:
    root = Path(root).resolve()
    if not (root / 'course.json').is_file():
        raise ValueError('Expected the complete course repository')
    result = []
    for parent, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(n for n in dirs if n not in EXCLUDED_PARTS and 'PRIVATE' not in n)
        for name in dirs:
            if (Path(parent) / name).is_symlink():
                raise ValueError('Source directories cannot be symlinks')
        for name in sorted(names):
            p = Path(parent) / name
            if (name == STAMP or name == 'derby.log' or name.startswith('.env')
                or 'PRIVATE' in name or name == 'INSTRUCTOR_PACKAGE.md'
                or p.suffix.lower() in {'.pyc', '.pyo', '.pem', '.key', '.pptx'}):
                continue
            if p == root / 'day02/dbt/profiles.yml':
                continue
            if p.is_symlink():
                raise ValueError('Source files cannot be symlinks')
            if p.is_file():
                result.append(p)
    return sorted(result)

def snapshot_digest(root: Path) -> str:
    root = Path(root).resolve()
    lines = [p.relative_to(root).as_posix() + '\0' + hashlib.sha256(p.read_bytes()).hexdigest()
             for p in source_files(root)]
    return hashlib.sha256(('\n'.join(lines) + '\n').encode()).hexdigest()

def copy_source(source: Path, destination: Path) -> str:
    source = Path(source).resolve()
    destination = Path(destination)
    if destination.is_symlink():
        raise ValueError('Workspace cannot be a symlink')
    dest = destination.resolve()
    if dest == source or source.is_relative_to(dest):
        raise ValueError('The destination cannot contain or be the source')
    # Snapshot the list before copying; a child output directory is allowed only
    # because source_files explicitly excludes every outputs directory.
    if dest.is_relative_to(source) and 'outputs' not in dest.relative_to(source).parts:
        raise ValueError('A nested copy must be under outputs')
    files = source_files(source)
    if dest.exists() and any(dest.iterdir()):
        raise ValueError('Refuse to overwrite a non-empty workspace')
    dest.mkdir(parents=True, exist_ok=True)
    digest = snapshot_digest(source)
    for p in files:
        target = dest / p.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
    return digest

def initialize_workspace(source: Path, destination: Path) -> dict:
    source = Path(source).resolve()
    destination = Path(destination)
    if destination.is_symlink():
        raise ValueError('Workspace cannot be a symlink')
    destination = destination.resolve()
    stamp = destination / STAMP
    digest = snapshot_digest(source)
    if stamp.exists():
        if stamp.is_symlink():
            raise ValueError('Snapshot identity cannot be a symlink')
        old = json.loads(stamp.read_text(encoding='utf-8'))
        if old.get('source_sha256') != digest:
            raise ValueError('Source version changed. Keep this workspace; use a new Compose project name for the new version.')
        if not (destination / 'course.json').is_file():
            raise ValueError('Workspace is incomplete; no automatic overwrite')
        return {'status': 'REUSED_WITHOUT_OVERWRITE', 'source_sha256': digest}
    copied = copy_source(source, destination)
    write_json(stamp, {'source_sha256': copied, 'created_at_utc': utc_now(),
        'meaning': 'Initial source snapshot only; learner edits may differ'})
    return {'status': 'CREATED', 'source_sha256': copied}

def command_plan(root: Path, action: str, project: str = 'masar-training') -> list[list[str]]:
    if not re.fullmatch(r'[a-z][a-z0-9-]{0,39}', project):
        raise ValueError('Use a short lowercase project name')
    base = ['docker', 'compose', '--project-name', project, '-f',
            str(Path(root).resolve() / 'infrastructure/runtime/compose.yaml')]
    actions = {
        'prepare': [base + ['config', '--quiet'], base + ['build', 'workbench'], base + ['pull', 'kafka'],
            ['docker', 'image', 'inspect', 'masar-course:local', 'apache/kafka:4.0.2', '--format',
             '{{json .Id}} {{json .RepoDigests}} {{json .Architecture}} {{json .Os}}']],
        'start': [base + ['up', '-d', '--wait', 'workbench']],
        'stop': [base + ['stop']],
        'verify': [base + ['up', '-d', '--wait', 'kafka'],
                   base + ['--profile', 'verification', 'run', '--no-deps', 'verify']],
    }
    if action not in actions:
        raise ValueError('Unknown local action')
    return actions[action]

def host_preflight() -> dict:
    docker = shutil.which('docker')
    result = {'scope': 'WORKBENCH_HOST_PREFLIGHT', 'checked_at_utc': utc_now(),
        'engine_executed': False, 'container_built': False, 'docker_cli': bool(docker),
        'docker_daemon': False, 'compose_plugin': False, 'issues': []}
    if not docker:
        result['issues'].append('Docker CLI/Engine is not available in this environment')
    else:
        for key, args in [('docker_daemon', [docker, 'info', '--format', '{{json .ServerVersion}}']),
                          ('compose_plugin', [docker, 'compose', 'version', '--short'])]:
            try:
                p = subprocess.run(args, capture_output=True, text=True, timeout=10, check=False)
                result[key] = p.returncode == 0
                if p.returncode:
                    result['issues'].append(key + ' is unavailable: ' + p.stderr.strip()[:400])
            except (OSError, subprocess.TimeoutExpired) as exc:
                result['issues'].append(key + ': ' + str(exc))
    result['status'] = 'BLOCKED_HOST_RUNTIME' if result['issues'] else 'HOST_PRESENT_NOT_ENGINE_PROOF'
    return result

def run_logged(args: Iterable[str], *, cwd: Path, log: Path, timeout: int = 5400) -> dict:
    """No shell interpolation; bounded process group; retain actual stdout/stderr."""
    if isinstance(args, str):
        raise TypeError('Use an argument list, not a shell command')
    args = list(args)
    if not args or not all(isinstance(a, str) and a for a in args):
        raise ValueError('A non-empty argument list is required')
    log.parent.mkdir(parents=True, exist_ok=True)
    result = {'command': args, 'started_at_utc': utc_now(), 'log': str(log), 'returncode': None}
    with log.open('w', encoding='utf-8') as handle:
        process = None
        try:
            process = subprocess.Popen(args, cwd=cwd, stdout=handle, stderr=subprocess.STDOUT,
                text=True, start_new_session=(os.name == 'posix'))
            result['process_id'] = process.pid
            process.wait(timeout=timeout)
            result['returncode'] = process.returncode
            result['status'] = 'PASSED_COMMAND' if process.returncode == 0 else 'FAILED_COMMAND'
        except subprocess.TimeoutExpired:
            if process is not None:
                if os.name == 'posix':
                    try: os.killpg(process.pid, signal.SIGTERM)
                    except ProcessLookupError: pass
                else:
                    process.terminate()
                try: process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if os.name == 'posix':
                        try: os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError: pass
                    else: process.kill()
                    process.wait()
                result['returncode'] = process.returncode
            result['status'] = 'TIMEOUT'
        except OSError as exc:
            result.update(status='START_FAILED', error=str(exc))
    result['finished_at_utc'] = utc_now()
    return result
