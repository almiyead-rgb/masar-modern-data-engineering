"""Execute the actual five-day learner route; keep real outputs and failures."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.native_contracts import read_stage_report
from masar.workspace import completed_bronze_workspace, DATASET_MANIFEST_SHA256

STAGES = {
    1: ['lab01_bronze', 'lab02_scan'],
    2: ['lab03a_staging', 'lab03b_silver'],
    3: ['lab04a_transactions', 'lab04b_maintenance'],
    4: ['lab05_streaming', 'lab06_quality'],
    5: ['lab07_gold_recovery', 'lab08_serving'],
}
EVIDENCE = ROOT / 'evidence/student-course/notebooks'
EVIDENCE.mkdir(parents=True, exist_ok=True)
URL = 'https://github.com/almiyead-rgb/masar-modern-data-engineering'
RUN_URL = URL + '/actions/runs/' + os.environ.get('GITHUB_RUN_ID', 'local')


def save(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str)+'\n', encoding='utf-8')


def retain_reports(copy: Path, target: Path) -> None:
    for path in (copy / 'outputs').rglob('*'):
        if path.is_file() and path.suffix in {'.json', '.log'} and '_delta_log' not in path.parts:
            dest = target / path.relative_to(copy)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)


def run_course(attempt: int) -> dict:
    copy = Path(tempfile.mkdtemp(prefix=f'masar_course_{attempt}_')) / 'course'
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git','outputs','evidence','__pycache__','.venv','metastore_db','derby.log'))
    target = EVIDENCE / f'run_{attempt}'
    result = {'attempt':attempt, 'status':'RUNNING', 'days':[], 'workflow_url':RUN_URL}
    try:
        for day, stages in STAGES.items():
            print(f'EXECUTING run {attempt} / day {day}', flush=True)
            relative = f'day{day:02}/STUDENT.ipynb'
            nb = nbformat.read(copy / relative, as_version=4)
            # Never allow saved outputs to stand in for execution.
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    cell.outputs = []
                    cell.execution_count = None
            try:
                NotebookClient(nb, timeout=900, kernel_name='python3',
                    resources={'metadata':{'path':str(copy)}}, allow_errors=False).execute()
            finally:
                target.mkdir(parents=True, exist_ok=True)
                nbformat.write(nb, target / f'day{day:02}.ipynb')
            if any(c.cell_type == 'code' and c.source.strip() and c.execution_count is None for c in nb.cells):
                raise AssertionError('A required code cell did not execute')
            work = completed_bronze_workspace(copy)
            reports = {stage: read_stage_report(work, stage) for stage in stages}
            day_result = {'day':day, 'status':'PASSED', 'stages':list(reports),
                'checks':{stage: report['checks'] for stage,report in reports.items()},
                'code_cells_executed':sum(c.cell_type == 'code' for c in nb.cells)}
            if day == 1:
                result['run_id'] = json.loads((work / '.masar-workspace.json').read_text())['run_id']
                result['bronze_counts'] = reports['lab01_bronze']['counts']
                result['base_aggregate'] = reports['lab02_scan']['expected_and_observed_aggregate']
            if day == 2:
                paths = list((copy/'outputs').rglob('dbt_attempt.json'))
                assert len(paths) == 1, 'Exactly one daily dbt run is required'
                dbt = json.loads(paths[0].read_text())
                assert dbt['status'] == 'PASSED_DBT_NATIVE' and dbt['dbt_executed'] is True
                assert [p['rows'] for p in dbt['phases']] == [72,72,75,75]
                result['dbt_phases'] = [{k:p[k] for k in ('phase','rows','total_fare_sar','business_digest')} for p in dbt['phases']]
                day_result['dbt_commands'] = len(dbt['commands'])
            if day == 5:
                result['serving_checks'] = reports['lab08_serving']['checks']
            import zipfile
            with zipfile.ZipFile(copy/f'outputs/day{day:02}_handoff.zip') as archive:
                assert archive.testzip() is None
                assert 'outputs/day01_bronze_success.json' in archive.namelist()
                assert any('/_delta_log/' in name for name in archive.namelist())
            day_result['handoff_zip_verified'] = True
            result['days'].append(day_result)
            save(target/'summary.json', result)
            print(f'PASSED run {attempt} / day {day}', flush=True)
        result['status'] = 'PASSED'
    except Exception as exc:
        result.update(status='FAILED', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        save(target/'summary.json', result)
        retain_reports(copy, target)
    return result


if __name__ == '__main__':
    results = [run_course(1), run_course(2)]
    assert results[0]['run_id'] != results[1]['run_id']
    for key in ('bronze_counts', 'base_aggregate', 'dbt_phases', 'serving_checks'):
        assert results[0][key] == results[1][key], f'Non-repeatable business result: {key}'
    verified = datetime.now(timezone.utc).isoformat()
    for day in STAGES:
        nb = nbformat.read(EVIDENCE/f'run_1/day{day:02}.ipynb', as_version=4)
        nb.metadata['masar'] = {'day':day, 'execution_status':'PASSED', 'independent_course_runs':2,
            'workflow_url':RUN_URL, 'verified_at_utc':verified, 'host':'GitHub Actions Ubuntu 24.04'}
        nbformat.write(nb, ROOT/f'day{day:02}/STUDENT.ipynb')
        evidence = {'day':day, 'status':'PASSED', 'independent_course_runs':2,
            'verified_at_utc':verified, 'workflow_url':RUN_URL,
            'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
            'checks':results[0]['days'][day-1], 'colab_host_tested':False}
        save(ROOT/f'day{day:02}/verification.json', evidence)
    summary = {'status':'PASSED', 'scope':'FIVE_STUDENT_NOTEBOOKS_WITH_NATIVE_ENGINES_AND_DBT',
        'independent_course_runs':2, 'notebook_executions':10, 'workflow_url':RUN_URL,
        'verified_at_utc':verified, 'python':sys.version.split()[0],
        'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
        'colab_host_tested':False, 'production_scale_tested':False,
        'results':results}
    save(ROOT/'docs/verification.json',summary)
    def bi(en,ar):
        return '<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" valign="top">'+en+'</td><td width="50%" dir="rtl" lang="ar" valign="top">'+ar+'</td></tr></table>\n\n'
    text = bi('<h1>Execution record</h1>','<h1>سجل التنفيذ</h1>')
    text += bi('<p>The five daily student notebooks completed in order in two independent workspaces, with a fresh kernel for each day. The notebooks contain the real outputs from the first complete run.</p>',
        '<p>اكتملت دفاتر الأيام الخمسة بالترتيب في مساحتي عمل مستقلتين، وبنواة جديدة لكل يوم. تحتوي الدفاتر على المخرجات الفعلية من التشغيل الكامل الأول.</p>')
    text += bi('<p>Native components exercised: Spark 3.5.8, Delta 3.3.2, Kafka 4.0.2, Great Expectations 1.7.0 and dbt-spark 1.9.1. Python 3.11 and Java 17 were used on GitHub Actions.</p>',
        '<p>المكونات المنفذة فعليًا: Spark 3.5.8 وDelta 3.3.2 وKafka 4.0.2 وGreat Expectations 1.7.0 وdbt-spark 1.9.1، باستخدام Python 3.11 وJava 17 على GitHub Actions.</p>')
    text += bi('<p><a href="'+RUN_URL+'">Actual execution logs</a> · <a href="verification.json">Machine-readable verification</a>. Positive timing samples vary by machine and are not performance guarantees. Colab hosting and distributed production scale were not separately tested.</p>',
        '<p><a href="'+RUN_URL+'">سجلات التنفيذ الفعلية</a> · <a href="verification.json">التحقق القابل للفحص</a>. تختلف أزمنة القياس بحسب الجهاز ولا تمثل ضمان أداء. لم تُختبر استضافة Colab أو أحمال الإنتاج الموزعة بصورة مستقلة.</p>')
    text += bi('<p>Run the notebook in order, retain your results, and explain any difference using the lab checks. <a href="../README.md">Return to the course</a>.</p>',
        '<p>شغّل الدفتر بالترتيب واحتفظ بنتائجك وفسّر أي اختلاف بالاستناد إلى فحوص اللاب. <a href="../README.md">العودة إلى الدورة</a>.</p>')
    (ROOT/'docs/VERIFICATION.md').write_text(text, encoding='utf-8')
    course = json.loads((ROOT/'course.json').read_text())
    for day in course['day_plan']:
        day['status'] = 'PUBLISHED_NATIVE_VERIFIED'
    save(ROOT/'course.json',course)
    print(json.dumps({'status':'PASSED','notebooks_executed':10,'workflow_url':RUN_URL},indent=2))
