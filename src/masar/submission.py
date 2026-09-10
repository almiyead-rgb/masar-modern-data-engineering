"""A conservative submission-file audit, not an automatic grade or certificate."""
from __future__ import annotations
import json,re
from pathlib import Path
from urllib.parse import urlsplit
from masar.workspace import workspace_path,digest_file,DATASET_MANIFEST_SHA256
from masar.native_contracts import STAGES, read_stage_report

NOTES=['README.md','BENCHMARKS.md','GOVERNANCE.md','DECISIONS.md']+[f'LAB{i:02d}_NOTES.md' for i in range(1,9)]
REPORTS={path: scope for path, scope, _ in STAGES.values()}



def audit_submission(submission:Path,work:Path) -> dict:
    """Missing prerequisites remain BLOCKED; placeholders never receive a grade.

    The report files are a packaging inventory. Actual notebook execution and
    the native two-run acceptance record are still required for teaching release.
    """
    submission=Path(submission).resolve();issues=[];files={}
    for name in NOTES:
        p=submission/name
        if p.is_symlink() or not p.is_file():issues.append('Missing or unsafe document: '+name);continue
        text=p.read_text(encoding='utf-8')
        if len(text.strip())<80 or re.search(r'\b(TODO|TBD|REPLACE_ME)\b',text,re.I):
            issues.append('Document is incomplete: '+name)
        files[name]=digest_file(p)
    meta_path=submission/'submission.json'
    try:
        if meta_path.is_symlink():raise ValueError('Symlink metadata')
        meta=json.loads(meta_path.read_text(encoding='utf-8'))
        if not isinstance(meta,dict):raise ValueError('Metadata must be an object')
        url=urlsplit(meta.get('repository_url',''))
        if (url.scheme!='https' or url.hostname!='github.com' or url.username or url.password
            or not re.fullmatch(r'/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?',url.path)
            or url.query or url.fragment):issues.append('A final GitHub repository URL is required at submission, not during this local build')
        if not isinstance(meta.get('participant_name'),str) or not meta['participant_name'].strip():issues.append('Participant name is missing')
    except (OSError,ValueError,TypeError):issues.append('Missing or invalid submission.json')
    for stage, (relative, scope, _) in STAGES.items():
        try:
            report = read_stage_report(work, stage)
            path = workspace_path(work, relative)
            files[relative] = digest_file(path)
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            issues.append('Missing, unsafe or incomplete native report/artifacts: ' + relative)
    # Required dbt demonstration must not disappear merely because the Spark path ran.
    issues.append('Manual acceptance still required: dbt adapter execution, native two-run evidence, notebook outputs, and organizer assessment')
    return {'scope':'SUBMISSION_INVENTORY_NOT_GRADING','status':'NEEDS_REVIEW' if len(issues)==1 else 'BLOCKED',
        'issues':issues,'file_sha256':files,'grade_awarded':False,'publication_approved':False,
        'repository_url_checked_online':False,'engine_execution_independently_verified':False}
