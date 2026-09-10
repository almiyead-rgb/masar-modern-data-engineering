"""Apply final learner-path corrections without changing the synthetic dataset."""
from pathlib import Path
import json
import re
import nbformat
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def write(path, text):
    target = ROOT / path
    if target.suffix == '.py':
        compile(text, path, 'exec')
    target.write_text(text, encoding='utf-8')


def bi(en, ar):
    return ('<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top">'
            + en + '</td><td width="50%" dir="rtl" lang="ar" align="right" valign="top">'
            + ar + '</td></tr></table>\n\n')


def replace_paragraph(path, lang, marker, replacement):
    target = ROOT / path
    soup = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
    changed = 0
    for cell in soup.find_all('td', lang=lang):
        for paragraph in cell.find_all('p'):
            if marker in paragraph.get_text():
                paragraph.clear()
                for node in list(BeautifulSoup(replacement, 'html.parser').contents):
                    paragraph.append(node)
                changed += 1
    if changed:
        write(path, str(soup))


# Keep the original dbt command and coverage checks. Read native structured
# metadata during docs generation instead of parsing SHOW TABLE display text.
p = ROOT / 'src/masar/dbt_lab.py'
text = p.read_text()
if 'structured_spark_catalog' not in text:
    text = text.replace('from contextlib import contextmanager, redirect_stdout, redirect_stderr',
                        'from contextlib import contextmanager, redirect_stdout, redirect_stderr, nullcontext\nfrom masar.dbt_catalog import structured_spark_catalog')
    text = text.replace('with redirect_stdout(log), redirect_stderr(log):',
                        'with redirect_stdout(log), redirect_stderr(log), (structured_spark_catalog() if docs else nullcontext()):')
    text = text.replace("checked = {'catalog_sha256': digest_file(target / 'catalog.json')}",
        "required_sources = {f'source.{PROJECT}.bronze.{n}' for n in SOURCE_NAMES}\n        if not required_sources <= set(catalog.get('sources', {})):\n            raise ValueError('Generated dbt catalog does not cover the three actual sources')\n        checked = {'catalog_sha256': digest_file(target / 'catalog.json'),\n                   'models_documented': len(nodes), 'sources_documented': len(catalog['sources']),\n                   'metadata_method': 'native DESCRIBE TABLE EXTENDED'}")
    write('src/masar/dbt_lab.py', text)

# Show observed data beside the assertions; source code remains shared once.
for day in range(2, 6):
    path = f'day{day:02}/STUDENT.ipynb'
    notebook = nbformat.read(ROOT/path, as_version=4)
    for cell in notebook.cells:
        if cell.cell_type != 'code' or '# Observed learning output' in cell.source:
            continue
        extra = None
        if 'result = run_staging_lab(' in cell.source:
            extra = "print('Observed staging row counts:', result['counts'])\n    preview = WORK / ('mini_lakehouse/staging/day02_' + result['run_id'] + '/stg_trips')\n    spark.read.format('delta').load(str(preview)).select('trip_id', 'city', 'fare_sar').orderBy('trip_id').show(5, truncate=False)"
        elif 'result = run_incremental_lab(' in cell.source:
            extra = "spark.read.format('delta').load(str(WORK/'mini_lakehouse/silver/trips')).select('trip_id', 'city', 'fare_sar').orderBy('trip_id').show(5, truncate=False)"
        elif 'result = run_transactions_lab(' in cell.source:
            extra = "print(json.dumps({k: result[k] for k in ('before','after_correction','past_version_read')}, indent=2, default=str))"
        elif 'result = run_maintenance_lab(' in cell.source:
            extra = "print(json.dumps({'recovery': result['recovery'], 'vacuum': result['vacuum']}, indent=2, default=str))"
        elif 'result = run_stream_lab(' in cell.source:
            extra = "print('Transport rows:', [phase['transport_rows'] for phase in result['phases']])\n    print('Unique event IDs:', [phase['unique_event_ids'] for phase in result['phases']])\n    spark.read.format('delta').load(str(WORK/result['event_table'])).select('event_id','trip_id','event_ts').orderBy('event_id').show(5, truncate=False)"
        elif 'result = run_quality_lab(' in cell.source:
            extra = "print('Quarantined records:')\n    spark.read.format('delta').load(str(WORK/result['quarantine_table'])).show(7, truncate=False)\n    print('Approved rows:', spark.read.format('delta').load(str(WORK/result['approved_table'])).count())"
        elif 'result = run_serving_lab(' in cell.source:
            extra = "print('BI totals:', json.dumps(result['bi_summary'], indent=2))\n    from masar.serving import read_release\n    _, observed_tables = read_release(spark, WORK)\n    print('AI feature example:', observed_tables['ai.zone_hourly_features'][0])\n    print('Future label example:', observed_tables['ai.zone_hourly_labels'][0])"
        if extra and '\nfinally:' in cell.source:
            cell.source = cell.source.replace('\nfinally:', '\n    # Observed learning output\n    ' + extra + '\nfinally:')
            cell.outputs = []; cell.execution_count = None
        if 'dbt_report, dbt_path = run_dbt_lab(ROOT)' in cell.source:
            cell.source += "\n# Observed learning output\nfor phase in dbt_report['phases']:\n    print(phase['phase'], 'rows:', phase['rows'], 'fare SAR:', phase['total_fare_sar'])\nprint('Catalog evidence:', dbt_report['commands'][-1])\n"
            cell.outputs = []; cell.execution_count = None
    nbformat.validate(notebook)
    nbformat.write(notebook, ROOT/path)

replace_paragraph('day01/CONCEPTS.md', 'ar', 'لم يُنشر محتوى في GitHub',
    'راجع <a href="SOURCES.md">المراجع الأصلية</a> و<a href="README.md">مسار اليوم</a>. شغّل <a href="STUDENT.ipynb">دفتر المتدرب</a> بالترتيب واحتفظ بمخرجاتك وتفسيرك للنتائج.')
replace_paragraph('day01/CONCEPTS.md', 'en', 'keep the Spark measurement outstanding',
    'Read C01–C06, then complete Lab 01 and its notes. Read C07–C09, complete Lab 02, and compare the observed scan measurements. Record your architecture decision: the need, chosen design, alternatives and limitations. Save these results as the first stage of your cumulative project. [S1]')
replace_paragraph('day01/CONCEPTS.md', 'ar', 'اترك قياس',
    'اقرأ C01–C06 ثم أكمل اللاب 01 وملاحظاته. اقرأ C07–C09 ثم أكمل اللاب 02 وقارن قياسات الاستعلام الفعلية. وثّق قرارك المعماري: الحاجة والتصميم المختار والبدائل والحدود. احفظ هذه النتائج بوصفها المرحلة الأولى من مشروعك التراكمي. [S1]')
replace_paragraph('docs/ADMINISTRATION.md', 'ar', 'موعدًا مختلقًا',
    'احضر الجلسات اليومية وسجل الحضور بالطريقة المعتمدة، وأبلغ عن مشكلات الوصول أو الغياب عبر قناة البرنامج المعلنة. تحدد الجهة أوقات البدء والاستراحات والصلاة وموعد التسليم وقواعد الشهادات. راجع الترتيبات المعلنة قبل الجلسة الأولى.')
replace_paragraph('day02/dbt/README.md', 'en', 'metadata-reviewed candidate',
    'Use Python 3.11, Java 17, Spark 3.5.8 and Delta 3.3.3 with the supplied requirements. Run the daily notebook in order. The runner copies your Bronze snapshots into an isolated workspace; it does not connect to production. Read <a href="../../docs/VERIFICATION.md">the execution record</a> for the tested environment.')
replace_paragraph('day02/dbt/README.md', 'ar', 'المرشح الموحد',
    'استخدم Python 3.11 وJava 17 وSpark 3.5.8 وDelta 3.3.3 مع ملف المتطلبات المرفق. شغّل دفتر اليوم بالترتيب. ينسخ المشغّل لقطات Bronze إلى مساحة معزولة دون الاتصال بالإنتاج. راجع <a href="../../docs/VERIFICATION.md">سجل التنفيذ</a> لمعرفة البيئة المختبرة.')
replace_paragraph('day05/COMPLETION.md', 'en', 'authorize GitHub publication',
    'Use the inventory to check filenames and retained evidence, then follow the <a href="../project/SUBMISSION.md">submission guide</a>. Technical checks do not replace the organizer’s formal assessment and certification policy. Distinction extensions remain optional.')
replace_paragraph('day05/COMPLETION.md', 'ar', 'يأذن بالنشر',
    'استخدم الحصر لفحص أسماء الملفات والأدلة المحفوظة، ثم اتبع <a href="../project/SUBMISSION.md">دليل التسليم</a>. لا تستبدل الفحوص التقنية سياسة التقييم والشهادة التي تعلنها الجهة. تظل امتدادات التميز اختيارية.')

# Static specifications reference the execution evidence rather than carrying
# outdated authoring-state flags that contradict current runs.
p=ROOT/'runtime-target.json'; cfg=json.loads(p.read_text())
for key in ('native_execution_verified','reason','retired_candidate','transitive_lock_verified'):
    cfg.pop(key,None)
cfg.update(scope='LEARNER_RUNTIME_SPECIFICATION', execution_record='docs/verification.json')
write('runtime-target.json',json.dumps(cfg,indent=2)+'\n')
p=ROOT/'tests/test_dbt_runtime.py'
write('tests/test_dbt_runtime.py',p.read_text().replace("self.assertFalse(target['native_execution_verified'])", "self.assertEqual(target['execution_record'],'docs/verification.json')"))
write('day02/dbt/design_status.json',json.dumps({
    'scope':'DBT_PROJECT_SPECIFICATION','adapter':'spark','method':'session',
    'adapter_version':'1.9.1','dbt_core_version':'1.9.8','models':6,'singular_tests':7,
    'incremental_lookback_days':3,'lookback_clock':'_ingested_at',
    'source_registration':'Actual Day 1 Delta snapshots in an isolated workspace',
    'execution_record':'../verification.json'},indent=2)+'\n')
p=ROOT/'day02/dbt/README.md'
write('day02/dbt/README.md',p.read_text().replace('Exact status','Project specification').replace('الحالة الدقيقة','مواصفات المشروع'))

# Keep only one canonical checklist for each day's technical work.
text=bi('<h1>Complete your cumulative project</h1>','<h1>أكمل مشروعك التراكمي</h1>')
text+=bi('<p>Check each day’s evidence using its own checklist. Keep all eight labs in the same repository.</p>',
    '<p>راجع أدلة كل يوم باستخدام قائمة اكتماله. احتفظ باللابات الثمانية داخل المستودع نفسه.</p>')
text+=bi(''.join(f'<p><a href="../day{d:02}/COMPLETION.md">Day {d} completion</a></p>' for d in range(1,6)),
    ''.join(f'<p><a href="../day{d:02}/COMPLETION.md">اكتمال اليوم {d}</a></p>' for d in range(1,6)))
text+=bi('<p>Before submitting, check that your README explains the run order, your results and limitations; retain your executed notebooks and notes; exclude credentials and large caches. Submit through the organizer’s channel using <a href="SUBMISSION.md">the submission guide</a>.</p>',
    '<p>قبل التسليم، تحقق أن README يشرح ترتيب التشغيل ونتائجك وحدودها، واحتفظ بالدفاتر المنفذة وملاحظاتك، واستبعد بيانات الدخول وذاكرة الحزم الكبيرة. سلّم عبر قناة الجهة وفق <a href="SUBMISSION.md">دليل التسليم</a>.</p>')
write('project/COMPLETION.md',text)
p=ROOT/'README.md'
text=p.read_text().replace('مسار · Mini-Lakehouse','مسار · بيئة بيانات مصغرة')
text=text.replace('<a href="docs/GIT_WORKFLOW.md">Git guide</a>', '<a href="docs/ADMINISTRATION.md">Participation and support</a> · <a href="docs/GIT_WORKFLOW.md">Git guide</a>')
text=text.replace('<a href="docs/GIT_WORKFLOW.md">دليل Git</a>', '<a href="docs/ADMINISTRATION.md">المشاركة والدعم</a> · <a href="docs/GIT_WORKFLOW.md">دليل Git</a>')
write('README.md',text)
p=ROOT/'.gitignore'; text=p.read_text()
if '\nevidence/\n' not in text:
    write('.gitignore',text+'\n# Generated validation logs and notebook attempts\nevidence/\n')
print('Catalog coverage, observed notebook examples and learner-facing navigation updated.')
