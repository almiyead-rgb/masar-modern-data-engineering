"""Execute real Day 1 notebook twice; publish no success unless both runs pass."""
from pathlib import Path
import hashlib,json,os,shutil,sys,tempfile,subprocess
from datetime import datetime,timezone
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
REPO='https://github.com/almiyead-rgb/masar-modern-data-engineering'
summaries=[]; first_notebook=None; first_reports=None
for attempt in (1,2):
    temp=Path(tempfile.mkdtemp(prefix=f'masar_native_{attempt}_'))
    copy=temp/'course'
    shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','outputs','__pycache__','.venv'))
    nb=nbformat.read(copy/'DAY01_STUDENT.ipynb',4)
    try:
        NotebookClient(nb,timeout=600,kernel_name='python3',resources={'metadata':{'path':str(copy)}}).execute()
    finally:
        evidence=ROOT/'evidence/day01';evidence.mkdir(parents=True,exist_ok=True)
        nbformat.write(nb,evidence/f'attempt_{attempt}.ipynb')
    pointer=json.loads((copy/'outputs/day01_bronze_success.json').read_text())
    work=copy/pointer['workspace']
    bronze=json.loads((work/'reports/bronze.json').read_text())
    scan=json.loads((work/'reports/benchmark.json').read_text())
    assert bronze['engine_executed'] is True and all(v is True for v in bronze['checks'].values())
    assert scan['engine_executed'] is True and all(v is True for v in scan['checks'].values())
    assert bronze['counts']=={'trips':144,'drivers':6,'gps_events':216}
    assert scan['population_rows']==72 and scan['expected_and_observed_aggregate']['rows']==72
    actual=[]
    for files in bronze['artifacts'].values():
        for item in files['commits']+files['data_files']:
            p=work/item['path'];assert p.is_file() and p.stat().st_size>0
            assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
            actual.append(item)
    src=json.loads(next((copy/'outputs').rglob('source_inspection.json')).read_text())
    cost=json.loads(next((copy/'outputs').rglob('cost_model_result.json')).read_text())
    assert all(src['checks'].values()) and all(cost['checks'].values())
    summary={'attempt':attempt,'run_id':pointer['run_id'],'counts':bronze['counts'],
             'trip_keys':bronze['business_trip_count'],'payloads':bronze['payload_digests'],
             'aggregate':scan['expected_and_observed_aggregate'],'engine_checks':bronze['checks'],
             'scan_checks':scan['checks'],'measurements':scan['measurements'],
             'artifact_files_verified':len(actual),'source_profile':src['city_profile'],'cost':cost['base']}
    summaries.append(summary)
    (evidence/f'result_{attempt}.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    if attempt==1:
        first_notebook=nb
        first_reports={'bronze':bronze,'benchmark':scan,'source':src,'cost':cost}
        # Preserve actual small engine evidence as a downloadable artifact, not an invented table.
        shutil.copytree(work,evidence/'native_workspace',dirs_exist_ok=True)
assert summaries[0]['run_id']!=summaries[1]['run_id']
for key in ['counts','trip_keys','payloads','aggregate','source_profile','cost']:
    assert summaries[0][key]==summaries[1][key],key
first_notebook.metadata['masar']={'day':1,'labs':['01','02'],'execution_status':'PASSED','verified_runs':2,'environment':'GitHub Actions Python 3.11 + Java 17'}
nbformat.write(first_notebook,ROOT/'DAY01_STUDENT.ipynb')
# Same source cells, with actual outputs from the combined run. Not separate execution claims.
by_id={x.id:x for x in first_notebook.cells}
for path in (ROOT/'notebooks/day01').glob('*.ipynb'):
    old=nbformat.read(path,4)
    for cell in old.cells:
        if cell.cell_type=='code':
            match=by_id[cell.id]
            assert cell.source==match.source
            cell.outputs=match.outputs;cell.execution_count=match.execution_count
    old.metadata['masar']={'output_provenance':'identical cells executed in DAY01_STUDENT.ipynb','environment':'GitHub Actions Python 3.11 + Java 17'}
    nbformat.write(old,path)
report={'status':'PASSED','scope':'DAY01_ONLY','engine':'Spark 3.5.8 + Delta 3.3.2',
        'python':sys.version.split()[0],'java':subprocess.run(['java','-version'],capture_output=True,text=True).stderr.splitlines()[0],
        'verified_at_utc':datetime.now(timezone.utc).isoformat(),'independent_runs':2,
        'workflow_url':REPO+'/actions/runs/'+os.environ.get('GITHUB_RUN_ID','local'),
        'counts':summaries[0]['counts'],'business_trips':72,'aggregate':summaries[0]['aggregate'],
        'colab_host_tested':False,'days_2_to_5_tested':False,'runtime_seconds_comparable_across_runs':False}
(ROOT/'day01/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
def bi(en,ar):return '<table dir="ltr" width="100%"><tr><td width="50%" valign="top" dir="ltr" lang="en">'+en+'</td><td width="50%" valign="top" dir="rtl" lang="ar">'+ar+'</td></tr></table>\n\n'
text=bi('<h1>Day 1 · Published and executed</h1>','<h1>اليوم الأول · منشور ومنفذ</h1>')
text+=bi('<p>The full combined notebook completed in two new kernels and separate workspaces on GitHub Actions. Spark and Delta performed real writes, reads and queries; transaction logs and Parquet files were checked. <a href="'+report['workflow_url']+'">View the execution</a>.</p>','<p>اكتمل الدفتر الموحد في نواتين جديدتين ومساحتي عمل مستقلتين على GitHub Actions. نفذ Spark وDelta الكتابة والقراءة والاستعلامات فعليًا، وفُحصت سجلات المعاملات وملفات Parquet. <a href="'+report['workflow_url']+'">عرض التنفيذ</a>.</p>')
text+=bi('<p>After the intentional replay: 144 trip delivery rows, 72 business trips, 6 drivers and 216 event lines. The scan compares the original 72 rows on both sides. <a href="day01/verification.json">Machine-readable result</a>.</p>','<p>بعد الإعادة المقصودة: 144 صف استقبال للرحلات، و72 رحلة فعلية، و6 سائقين، و216 سطر أحداث. يقارن القياس 72 صفًا أصليًا في الطرفين. <a href="day01/verification.json">النتيجة القابلة للفحص</a>.</p>')
text+=bi('<p>Verified environment: Python 3.11, Java 17, Spark 3.5.8, Delta 3.3.2. This is Day 1 execution evidence, not whole-course certification, a Colab-host test, a cloud benchmark or a distributed-scale guarantee. Days 2–5 are outside this review; any existing later-day files are not approved by this check.</p>','<p>البيئة المختبرة: Python 3.11 وJava 17 وSpark 3.5.8 وDelta 3.3.2. هذا دليل تنفيذ اليوم الأول وليس اعتمادًا للدورة كاملة أو اختبارًا لخدمة Colab أو مقارنة سحابية أو ضمان توسع موزع. الأيام 2–5 خارج نطاق هذه المراجعة؛ وجود ملفاتها لا يعني اعتمادها بهذا الفحص.</p>')
text+=bi('<p><a href="day01/README.md">Start Day 1</a> · <a href="DAY01_STUDENT.ipynb">Executed notebook</a></p>','<p><a href="day01/README.md">ابدأ اليوم الأول</a> · <a href="DAY01_STUDENT.ipynb">الدفتر المنفذ</a></p>')
(ROOT/'STATUS.md').write_text(text,encoding='utf-8')
c=json.loads((ROOT/'course.json').read_text());c['day_plan'][0]['status']='PUBLISHED_NATIVE_VERIFIED';c['published_days']=[1]
(ROOT/'course.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
