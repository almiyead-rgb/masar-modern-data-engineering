"""Manage the LOCAL environment only. This never creates/pushes a GitHub repo."""
from pathlib import Path
import argparse
import json
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.workbench import command_plan, host_preflight, run_logged, utc_now
from masar.workspace import write_json

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['doctor', 'prepare', 'start', 'stop', 'verify'], nargs='?', default='doctor')
    parser.add_argument('--plan', action='store_true', help='Print command arrays without starting anything')
    parser.add_argument('--project', default='masar-training')
    args = parser.parse_args()
    if args.plan:
        print(json.dumps({'scope': 'PLAN_ONLY', 'action': args.action, 'engine_executed': False,
            'commands': [] if args.action == 'doctor' else command_plan(ROOT, args.action, args.project)}, indent=2))
        return 0
    parent = ROOT / 'outputs'
    if parent.is_symlink():
        raise ValueError('Outputs cannot be a symlink')
    parent.mkdir(exist_ok=True)
    attempt = Path(tempfile.mkdtemp(prefix='workbench_', dir=parent))
    preflight = host_preflight()
    record = {'scope': 'LOCAL_WORKBENCH_LIFECYCLE', 'action': args.action,
        'started_at_utc': utc_now(), 'preflight': preflight, 'commands': [],
        'engine_executed': False, 'teaching_approved': False, 'published': False}
    if preflight['issues']:
        record['status'] = 'BLOCKED_HOST_RUNTIME'
    elif args.action == 'doctor':
        record['status'] = 'HOST_PRESENT_NOT_ENGINE_PROOF'
    else:
        record['status'] = 'RUNNING'
        for number, command in enumerate(command_plan(ROOT, args.action, args.project), 1):
            result = run_logged(command, cwd=ROOT, log=attempt / f'{number:02d}_{args.action}.log')
            record['commands'].append(result)
            write_json(attempt / 'attempt.json', record)
            if result['returncode'] != 0:
                record['status'] = result['status']
                break
        else:
            record['status'] = 'LOCAL_COMMANDS_COMPLETED_CHECK_COMPONENT_REPORTS'
    record['finished_at_utc'] = utc_now()
    write_json(attempt / 'attempt.json', record)
    print(json.dumps({'status': record['status'], 'report': str((attempt / 'attempt.json').relative_to(ROOT)),
        'teaching_approved': False, 'published': False}, indent=2))
    return 2 if record['status'].startswith('BLOCKED') else (1 if record['status'] in {'TIMEOUT', 'START_FAILED', 'FAILED_COMMAND'} else 0)

if __name__ == '__main__':
    raise SystemExit(main())
