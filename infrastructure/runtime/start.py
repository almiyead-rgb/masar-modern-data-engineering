"""Initialize a persistent learner/audit copy, then run the requested local command."""
from pathlib import Path
import os
import sys
sys.path.insert(0, '/opt/masar-course/src')
from masar.workbench import initialize_workspace

source = Path(os.environ.get('MASAR_SOURCE_ROOT', '/source-course'))
work = Path(os.environ.get('MASAR_WORK_ROOT', '/workspace'))
initialize_workspace(source, work)
os.chdir(work)
if len(sys.argv) < 2:
    raise SystemExit('A local workbench command is required')
# Keep Jupyter's default token authentication enabled. Never mount docker.sock.
os.execvp(sys.argv[1], sys.argv[1:])
