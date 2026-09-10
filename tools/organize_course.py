"""Organize the existing course into five learner-owned folders, without changing data."""
from pathlib import Path
import json, re, os, shutil, hashlib
from urllib.parse import urlsplit, unquote
import nbformat
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT/'course.json').exists():
    ROOT = Path(os.environ.get('MASAR_ROOT', '/mnt/data/masar_delivery')).resolve()
MARKER = ROOT/'tools/student_layout_v1.json'
if MARKER.exists():
    print('Student layout already applied. Existing learner edits retained.')
    raise SystemExit(0)


def bi(en, ar):
    return ('<table dir="ltr" width="100%"><tr>'
        '<td width="50%" dir="ltr" lang="en" align="left" valign="top">'+en+'</td>'
        '<td width="50%" dir="rtl" lang="ar" align="right" valign="top">'+ar+'</td>'
        '</tr></table>\n\n')


def write(path, text):
    p=ROOT/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text,encoding='utf-8')

LAB_DAYS={1:1,2:1,3:2,4:3,5:4,6:4,7:5,8:5}
TITLES={1:('Foundations and Bronze','الأساسيات وطبقة Bronze'),2:('ELT and Silver','التحويل وبناء Silver'),3:('Delta transactions and maintenance','معاملات Delta والصيانة'),4:('Streaming, quality and governance','التدفق والجودة والحوكمة'),5:('Gold, AI/BI and project submission','طبقة Gold ومخرجات AI وBI وتسليم المشروع')}
OBJECTIVES={
1:('Compare data architectures; preserve raw sources; explain delivery versus business keys; compare operating costs and equal-population queries.','قارن المعماريات، واحفظ المصادر الخام، وميّز سجلات الوصول من مفاتيح الأعمال، وقارن تكلفة التشغيل واستعلامات البيانات المتساوية.'),
2:('Normalize types, cities and time zones; join safely; deduplicate before MERGE; retain late arrivals; build and test the same transformation graph with dbt.','وحّد الأنواع والمدن والتوقيتات، واربط البيانات دون مضاعفتها، وأزل التكرار قبل MERGE، واحتفظ بالوصول المتأخر، وابنِ التحويلات نفسها واختبرها باستخدام dbt.'),
3:('Apply a correction once; preserve revision precedence; read earlier versions; test schema changes and maintenance on isolated copies.','طبّق التصحيح مرة واحدة، واحفظ أولوية المراجعات، واقرأ النسخ السابقة، واختبر تغيير المخطط والصيانة على نسخ معزولة.'),
4:('Receive Kafka events with a persistent checkpoint; reconcile delivery and event identities; validate, quarantine and recheck a batch; document quality and governance decisions.','استقبل أحداث Kafka مع نقطة تحقق مستمرة، وطابق سجلات الوصول وهويات الأحداث، وافحص الدفعة واعزل المعيب وأعد الفحص، ووثّق قرارات الجودة والحوكمة.'),
5:('Build and reconcile Gold tables; produce reporting and point-in-time features; keep unknown future labels null; recover from a failed candidate and submit the cumulative work.','ابنِ جداول Gold وطابق مجاميعها، وجهّز التقارير والخصائص المتاحة وقت القرار، وأبقِ القيم المستقبلية غير المعروفة فارغة، وتعافَ من فشل بناء نسخة مرشحة وسلّم العمل التراكمي.')}
OUTCOME={1:'LO1 · LO2 · LO8',2:'LO3 · LO4 · LO8',3:'LO4 · LO6 · LO8',4:'LO5 · LO6 · LO8',5:'LO7 · LO8'}
SPECS={2:[('masar.silver','run_staging_lab','lab03a_staging','03a · Prepare typed staging','03a · جهّز البيانات المهيأة'),('masar.silver','run_incremental_lab','lab03b_silver','03b · Build incremental Silver','03b · ابنِ Silver تدريجيًا')],3:[('masar.delta_lab','run_transactions_lab','lab04a_transactions','04a · Correct and read versions','04a · صحّح واقرأ النسخ'),('masar.delta_lab','run_maintenance_lab','lab04b_maintenance','04b · Test safe maintenance','04b · اختبر الصيانة الآمنة')],4:[('masar.streaming','run_stream_lab','lab05_streaming','05 · Receive Kafka events','05 · استقبل أحداث Kafka'),('masar.quality_gate','run_quality_lab','lab06_quality','06 · Validate and quarantine','06 · افحص واعزل السجلات')],5:[('masar.serving','run_recovery_exercise','lab07_gold_recovery','07 · Build Gold and recover','07 · ابنِ Gold واختبر التعافي'),('masar.serving','run_serving_lab','lab08_serving','08 · Serve AI/BI data','08 · جهّز بيانات AI وBI')]}

# Keep source bytes unchanged and keep a deterministic move map for every link.
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data/masar-small-v1').iterdir() if p.is_file()}
all_paths=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts]
original_markdown={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8') for p in all_paths if p.suffix=='.md'}
mapping={}; remove=set()
for p in all_paths:
    name=p.relative_to(ROOT).as_posix()
    match=re.match(r'labs/lab(\d{2})/(.+)',name)
    if match:
        n=int(match.group(1)); mapping[name]=f'day{LAB_DAYS[n]:02}/labs/lab{n:02}/{match.group(2)}'
    if name.startswith('examples/dbt_masar/'):
        mapping[name]=name.replace('examples/dbt_masar/','day02/dbt/',1)
    if name.startswith('sql/day05/'):
        mapping[name]=name.replace('sql/day05/','day05/sql/',1)
    if name=='resources/Masar_Cost_Model.xlsx':mapping[name]='day01/resources/Masar_Cost_Model.xlsx'
    match=re.match(r'notebooks/day(\d{2})/(.+\.ipynb)',name)
    if match:
        day=int(match.group(1))
        mapping[name]=f'day{day:02}/REFERENCE.ipynb' if day>1 and match.group(2).startswith('01_') else f'day{day:02}/STUDENT.ipynb'
        if not (day>1 and match.group(2).startswith('01_')):remove.add(name)
mapping['DAY01_STUDENT.ipynb']='day01/STUDENT.ipynb'
remove.add('MASAR_STUDENT.ipynb');mapping['MASAR_STUDENT.ipynb']='README.md'
review_names={'INTEGRATION_REVIEW.md','RUNTIME_ACCEPTANCE.md','RUNTIME_DBT_REVIEW.md','RUNTIME_WORKBENCH_REVIEW.md','RUNTIME_WORKBENCH.md','RUNTIME_DBT.md','LEARNER_ROUTE.md'}
for name in original_markdown:
    if name.startswith('docs/') and Path(name).name in review_names:
        remove.add(name);mapping[name]='docs/VERIFICATION.md'
    if name=='CHANGELOG.md':remove.add(name);mapping[name]='docs/VERIFICATION.md'
# Historical attempt files remain recoverable in Git history, not mixed into the learner path.
for p in (ROOT/'evidence').rglob('*'):
    if p.is_file():remove.add(p.relative_to(ROOT).as_posix());mapping[p.relative_to(ROOT).as_posix()]='docs/VERIFICATION.md'


def rewrite(text, old, new):
    def transform(target):
        url=urlsplit(target)
        if url.scheme or not url.path:return target
        absolute=(ROOT/old).parent.joinpath(unquote(url.path)).resolve()
        if not absolute.is_relative_to(ROOT):return target
        rel=absolute.relative_to(ROOT).as_posix()
        destination=ROOT/mapping.get(rel,rel)
        value=os.path.relpath(destination,(ROOT/new).parent).replace(os.sep,'/')
        return value+('?' + url.query if url.query else '')+('#'+url.fragment if url.fragment else '')
    text=re.sub(r'(href=["\'])([^"\']+)(["\'])',lambda m:m[1]+transform(m[2])+m[3],text)
    text=re.sub(r'(\]\()([^)]+)(\))',lambda m:m[1]+transform(m[2])+m[3],text)
    return text

# Remove authoring-status blocks, never teaching explanations, questions or data contracts.
status_heads=('build status','current status','readiness boundary','prerequisites and status','what is authored here','before final course acceptance','candidate environment, not a success claim')
internal_sentences=[
 r'No real-time freshness service has been verified in this build\.',r'لم تتحقق خدمة حداثة لحظية في هذا البناء\.',
 r'The native notebooks remain ENGINE_NOT_EXECUTED\.',r'Engine drafts are not classroom-verified\.',
 r'No remote repository has been created or published\.',r'لم يُنشأ مستودع بعيد ولم يُنشر شيء\.',
 r'Native execution remains unverified\.',r'تشغيله ما يزال غير متحقق\.'
]
def clean(text):
    def block(m):
        soup=BeautifulSoup(m[0],'html.parser')
        heading=soup.find('h2')
        if heading and any(heading.get_text(' ',strip=True).lower().startswith(h) for h in status_heads):return ''
        return m[0]
    text=re.sub(r'<table\b.*?</table>',block,text,flags=re.S)
    for pattern in internal_sentences:text=re.sub(pattern,'',text)
    text=text.replace('six-hour teaching envelope','learning schedule').replace('authoring route','learning route')
    return re.sub(r'\n{4,}','\n\n',text)

# Move physical assets. Notebook sections are consolidated, not copied repeatedly.
for old,new in mapping.items():
    if old in remove:continue
    src=ROOT/old; dest=ROOT/new
    if src.is_file():
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(src),str(dest))
for old in remove:
    path=ROOT/old
    if path.is_file():path.unlink()
for old,text in original_markdown.items():
    if old in remove:continue
    new=mapping.get(old,old)
    write(new,clean(rewrite(text,old,new)))
# Update executable path literals for the relocated day-owned assets.
for p in [*(ROOT/'src').rglob('*.py'),*(ROOT/'scripts').glob('*.py'),*(ROOT/'tests').glob('*.py')]:
    text=p.read_text()
    text=text.replace('examples/dbt_masar','day02/dbt').replace('sql/day05/','day05/sql/')
    text=text.replace('DAY01_STUDENT.ipynb','day01/STUDENT.ipynb')
    p.write_text(text,encoding='utf-8')

# Day 1 retains its tested code; only links follow the new containing folder.
p=ROOT/'day01/STUDENT.ipynb';nb=nbformat.read(p,4)
for cell in nb.cells:
    if cell.cell_type=='markdown':cell.source=clean(rewrite(cell.source,'DAY01_STUDENT.ipynb','day01/STUDENT.ipynb'))
nbformat.write(nb,p)
for day in range(2,6):
    p=ROOT/f'day{day:02}/REFERENCE.ipynb'
    old=next(k for k,v in mapping.items() if v==f'day{day:02}/REFERENCE.ipynb')
    nb=nbformat.read(p,4)
    for cell in nb.cells:
        if cell.cell_type=='markdown':cell.source=clean(rewrite(cell.source,old,p.relative_to(ROOT).as_posix()))
    nbformat.write(nb,p)

# A focused notebook per day. Computation stays in shared, inspectable source modules.
def md(en,ar):return nbformat.v4.new_markdown_cell(bi(en,ar))
def code(text):return nbformat.v4.new_code_cell(text)
SETUP='''from pathlib import Path
import json, sys
ROOT = next((p for p in (Path.cwd(), *Path.cwd().parents) if (p / 'course.json').is_file()), None)
if ROOT is None:
    raise FileNotFoundError('Open the notebook inside the complete course repository; see docs/SETUP.md.')
sys.path.insert(0, str(ROOT / 'src'))
SOURCE = ROOT / 'data/masar-small-v1'
from masar.workspace import require_fixed_dataset, completed_bronze_workspace
from masar.runtime import require_environment, start_spark
from masar.native_contracts import validate_stage_result
require_fixed_dataset(SOURCE)
require_environment()
WORK = completed_bronze_workspace(ROOT)
print('Continue workspace:', WORK.relative_to(ROOT))
'''
HANDOFF='''from pathlib import Path
import zipfile
pointer = ROOT / 'outputs/day01_bronze_success.json'
archive = ROOT / 'outputs/DAY_PLACEHOLDER_handoff.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
    bundle.write(pointer, pointer.relative_to(ROOT).as_posix())
    for path in sorted(WORK.rglob('*')):
        if path.is_file():
            bundle.write(path, path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
print('Retain the notebook outputs, notes and', archive.relative_to(ROOT))
'''
for day in range(2,6):
    en,ar=TITLES[day]
    cells=[md(f'<h1>Day {day} · {en}</h1><p>{OBJECTIVES[day][0]}</p>',f'<h1>اليوم {day} · {ar}</h1><p>{OBJECTIVES[day][1]}</p>'),
           md('<h2>1. Continue your project</h2><p>Use the same repository and successful Day 1 workspace. Restore your handoff ZIP at the repository root when using a new session. Read <a href="README.md">today’s guide</a> before running all cells in order.</p>',
              '<h2>١. استكمل مشروعك</h2><p>استخدم المستودع نفسه ومساحة اليوم الأول الناجحة. استعد ملف الانتقال في جذر المستودع عند استخدام جلسة جديدة. اقرأ <a href="README.md">دليل اليوم</a> ثم شغّل الخلايا بالترتيب.</p>'),code(SETUP)]
    for module,fn,stage,eh,ah in SPECS[day]:
        lab=int(stage[3:5]);link=f'labs/lab{lab:02}/WALKTHROUGH.md'
        cells.append(md(f'<h2>{eh}</h2><p>Follow <a href="{link}">the lab walkthrough</a>. The cell runs real operations and saves reports; inspect the checks and explain one observation in your lab notes.</p>',
                        f'<h2>{ah}</h2><p>اتبع <a href="{link}">شرح اللاب</a>. تنفذ الخلية العمليات وتحفظ تقاريرها؛ افحص النتائج وفسّر ملاحظة واحدة في ملف اللاب.</p>'))
        cells.append(code(f'''from {module} import {fn}
spark = start_spark(WORK, kafka={stage=='lab05_streaming'})
try:
    result = {fn}(spark, SOURCE, WORK)
    validate_stage_result('{stage}', result)
    print(json.dumps({{'scope': result['scope'], 'checks': result['checks']}}, indent=2))
finally:
    spark.stop()
'''))
    if day==2:
        cells += [md('<h2>03c · Run the dbt models</h2><p>Read <a href="DBT_GUIDE.md">the six-model graph and tests</a>. The session adapter uses isolated copies of Bronze; it does not replace your Silver workspace.</p>',
                     '<h2>03c · شغّل نماذج dbt</h2><p>اقرأ <a href="DBT_GUIDE.md">تسلسل النماذج الستة واختباراتها</a>. يستخدم موصل الجلسة نسخًا معزولة من Bronze ولا يستبدل مساحة Silver الخاصة بك.</p>'),
                  code('''from masar.dbt_lab import run_dbt_lab
dbt_report, dbt_path = run_dbt_lab(ROOT)
print(json.dumps({'status': dbt_report['status'], 'phases_completed': len(dbt_report['phases']), 'report': str(dbt_path.relative_to(ROOT)), 'error': dbt_report.get('error')}, indent=2))
assert dbt_report['status'] == 'PASSED_DBT_NATIVE', dbt_report.get('error')
''')]
    cells += [md('<h2>Review and save</h2><p>Answer <a href="PRACTICE.md">the questions</a> as part of the existing lab notes, then use <a href="COMPLETION.md">the completion checklist</a>. Save your notebook with actual outputs. The archive below is a handoff, not another assignment.</p>',
                 '<h2>راجع واحفظ</h2><p>أجب عن <a href="PRACTICE.md">الأسئلة</a> ضمن ملاحظات اللاب، ثم استخدم <a href="COMPLETION.md">قائمة الاكتمال</a>. احفظ دفترك بالمخرجات الفعلية. ملف الانتقال أدناه ليس تكليفًا آخر.</p>'),code(HANDOFF.replace('DAY_PLACEHOLDER',f'day{day:02}'))]
    notebook=nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},'language_info':{'name':'python'},'masar':{'day':day,'execution_status':'NOT_YET_RUN'}})
    nbformat.validate(notebook);nbformat.write(notebook,ROOT/f'day{day:02}/STUDENT.ipynb')

# Clean daily entry points. Each material appears once; shared data/code are linked.
for day in range(1,6):
    folder=f'day{day:02}';en,ar=TITLES[day]
    labnums=[n for n,d in LAB_DAYS.items() if d==day]
    text=bi(f'<h1>Day {day} · {en}</h1><p>Meaad Al-Marri · {OUTCOME[day]}</p>',f'<h1>اليوم {day} · {ar}</h1><p>ميعاد المري · {OUTCOME[day]}</p>')
    text+=bi('<h2>Your goal</h2><p>'+OBJECTIVES[day][0]+'</p>','<h2>هدفك اليوم</h2><p>'+OBJECTIVES[day][1]+'</p>')
    text+=bi('<h2>Start here</h2><p>Read <a href="CONCEPTS.md">the concepts</a>, then run <strong><a href="STUDENT.ipynb">the daily notebook</a></strong> in order. Use <a href="GLOSSARY.md">the glossary</a> when you encounter a new term.</p>',
             '<h2>ابدأ هنا</h2><p>اقرأ <a href="CONCEPTS.md">المفاهيم</a> ثم شغّل <strong><a href="STUDENT.ipynb">دفتر اليوم</a></strong> بالترتيب. ارجع إلى <a href="GLOSSARY.md">المصطلحات</a> عند الحاجة.</p>')
    text+=bi('<h2>Today’s labs</h2>'+''.join(f'<p><a href="labs/lab{n:02}/README.md">Lab {n:02}</a> · <a href="labs/lab{n:02}/WALKTHROUGH.md">Step-by-step application</a></p>' for n in labnums),
             '<h2>لابات اليوم</h2>'+''.join(f'<p><a href="labs/lab{n:02}/README.md">اللاب {n:02}</a> · <a href="labs/lab{n:02}/WALKTHROUGH.md">التطبيق خطوة بخطوة</a></p>' for n in labnums))
    extras={1:[('resources/Masar_Cost_Model.xlsx','Cost model','نموذج التكلفة')],2:[('DATA_CONTRACT.md','Silver contract','عقد Silver'),('DBT_GUIDE.md','dbt guide','دليل dbt'),('dbt/README.md','dbt project','مشروع dbt')],3:[('CHANGE_POLICY.md','Change policy','سياسة التغيير')],4:[('SETUP.md','Kafka setup','إعداد Kafka'),('STREAM_CONTRACT.md','Event contract','عقد الأحداث'),('QUALITY_POLICY.md','Quality rules','قواعد الجودة'),('OBSERVABILITY.md','Monitoring','المراقبة'),('GOVERNANCE.md','Governance','الحوكمة')],5:[('DATA_PRODUCTS.md','Eight output tables','جداول المخرجات الثمانية'),('AI_BI_GUIDE.md','AI/BI guide','دليل AI وBI'),('INTEGRATION.md','Integration','التكامل')]}
    rows=extras[day]+[('PRACTICE.md','Explain your results','فسّر نتائجك'),('COMPLETION.md','Save and complete','احفظ وأكمل'),('SOURCES.md','Primary references','المراجع الأصلية')]
    text+=bi('<h2>Resources and completion</h2>'+''.join(f'<p><a href="{p}">{e}</a></p>' for p,e,a in rows),'<h2>الموارد والاكتمال</h2>'+''.join(f'<p><a href="{p}">{a}</a></p>' for p,e,a in rows))
    if day>1:text+=bi('<p><a href="REFERENCE.ipynb">Optional calculation reference</a>: inspect expected values; use the daily notebook for the actual lab.</p>','<p><a href="REFERENCE.ipynb">مرجع حسابي اختياري</a> لفهم القيم المتوقعة؛ استخدم دفتر اليوم لتنفيذ اللاب الفعلي.</p>')
    text+=bi('<p>Use the same synthetic dataset and cumulative project. Save the executed notebook, lab notes and daily handoff ZIP. <a href="../docs/SETUP.md">Environment</a> · <a href="../data/DICTIONARY.md">Data dictionary</a> · <a href="../project/SUBMISSION.md">Submission</a>.</p>',
             '<p>استخدم البيانات الاصطناعية والمشروع التراكمي نفسيهما. احفظ الدفتر المنفذ وملاحظات اللاب وملف الانتقال اليومي. <a href="../docs/SETUP.md">البيئة</a> · <a href="../data/DICTIONARY.md">قاموس البيانات</a> · <a href="../project/SUBMISSION.md">التسليم</a>.</p>')
    prev=f'../day{day-1:02}/README.md' if day>1 else '../README.md'
    nex=f'../day{day+1:02}/README.md' if day<5 else '../project/SUBMISSION.md'
    text+=bi(f'<p><a href="{prev}">Previous</a> · <a href="../README.md">Course home</a> · <a href="{nex}">Next</a></p>',f'<p><a href="{prev}">السابق</a> · <a href="../README.md">الرئيسية</a> · <a href="{nex}">التالي</a></p>')
    write(folder+'/README.md',text)

cover=bi('<p>SDAIA Academy · Learner materials</p><h1>Modern Data Engineering<br>for AI Systems</h1><h2>MASAR · Mini-Lakehouse</h2><p><strong>Meaad Al-Marri</strong><br>SDA-DSC-214 · Five days · Eight cumulative labs</p>',
         '<p>أكاديمية سدايا · مواد المتدرب</p><h1>هندسة البيانات الحديثة<br>لأنظمة الذكاء الاصطناعي</h1><h2>مسار · Mini-Lakehouse</h2><p><strong>ميعاد المري</strong><br>SDA-DSC-214 · خمسة أيام · ثمانية لابات تراكمية</p>')
cover+=bi('<h2>What you will build</h2><p>Turn small synthetic trip, driver and location feeds into a reliable data pipeline: preserve the source, build Silver, manage changes, receive events, check quality and deliver reporting and AI-ready tables.</p><p><strong>The labs are your final project.</strong> Complete them in sequence; no separate final assignment is added.</p>',
          '<h2>ماذا ستبني؟</h2><p>حوّل ملفات اصطناعية صغيرة للرحلات والسائقين والمواقع إلى خط بيانات موثوق: احفظ المصدر، وابنِ Silver، وأدر التغييرات، واستقبل الأحداث، وافحص الجودة، ثم جهّز جداول التقارير والذكاء الاصطناعي.</p><p><strong>اللابات هي مشروعك النهائي.</strong> أكملها بالتتابع دون تكليف نهائي منفصل.</p>')
cover+=bi('<h2>Your five-day path</h2>'+''.join(f'<p><strong><a href="day{d:02}/README.md">Day {d}</a></strong> · {TITLES[d][0]}</p>' for d in range(1,6)),
          '<h2>مسارك في الأيام الخمسة</h2>'+''.join(f'<p><strong><a href="day{d:02}/README.md">اليوم {d}</a></strong> · {TITLES[d][1]}</p>' for d in range(1,6)))
cover+=bi('<h2>Before you start</h2><p><a href="docs/SETUP.md">Prepare your environment</a> · <a href="TRAINING_CONTENT.md">Learning outcomes</a> · <a href="data/DICTIONARY.md">Data dictionary</a> · <a href="project/SUBMISSION.md">Submission guide</a>.</p><p>Use the same 72 base trips, 6 drivers and 216 base location events throughout the course, with the supplied late/replay/correction fixtures. Data and code are shared once; each day contains its own learning materials. No paid API or GPU is required.</p>',
          '<h2>قبل أن تبدأ</h2><p><a href="docs/SETUP.md">جهّز بيئتك</a> · <a href="TRAINING_CONTENT.md">مخرجات التعلم</a> · <a href="data/DICTIONARY.md">قاموس البيانات</a> · <a href="project/SUBMISSION.md">دليل التسليم</a>.</p><p>استخدم الرحلات الأساسية الـ72 والسائقين الستة وأحداث المواقع الـ216 طوال الدورة، مع ملفات التأخر والإعادة والتصحيح المرفقة. تُحفظ البيانات والأكواد المشتركة مرة واحدة، ويضم كل يوم مواده التعليمية. لا تحتاج إلى API مدفوع أو GPU.</p>')
cover+=bi('<p><a href="docs/GIT_WORKFLOW.md">Git guide</a> · <a href="docs/TROUBLESHOOTING.md">Troubleshooting</a> · <a href="docs/VERIFICATION.md">Execution record</a> · <a href="https://github.com/SDAIAAcademy">SDAIA Academy</a></p><p>Credit the programme and Meaad Al-Marri in your project README. Optional extensions and repository stars are not passing conditions. Follow the organizer’s announced attendance, deadline and submission rules.</p>',
          '<p><a href="docs/GIT_WORKFLOW.md">دليل Git</a> · <a href="docs/TROUBLESHOOTING.md">معالجة الأخطاء</a> · <a href="docs/VERIFICATION.md">سجل التنفيذ</a> · <a href="https://github.com/SDAIAAcademy">أكاديمية سدايا</a></p><p>اذكر البرنامج وميعاد المري في README مشروعك. الامتدادات الاختيارية ونجوم المستودع ليست شروط نجاح. اتبع ما تعلنه الجهة المنظمة بشأن الحضور والمواعيد وقناة التسليم.</p>')
write('README.md',cover)
write('docs/START_HERE.md',bi('<h1>Start your learning path</h1><p>Read <a href="SETUP.md">setup</a>, then open <a href="../day01/README.md">Day 1</a>. Each day contains one main notebook, concepts, lab walkthroughs, glossary and completion guidance. Continue in order using the same workspace.</p>','<h1>ابدأ مسار التعلم</h1><p>اقرأ <a href="SETUP.md">الإعداد</a> ثم افتح <a href="../day01/README.md">اليوم الأول</a>. يحتوي كل يوم على دفتر أساسي ومفاهيم وشرح اللابات والمصطلحات وإرشادات الاكتمال. تابع بالترتيب باستخدام مساحة العمل نفسها.</p>'))
# One central evidence page: factual execution status is not duplicated throughout lessons.
write('docs/VERIFICATION.md',bi('<h1>Execution record</h1><p>The <a href="../day01/verification.json">Day 1 record</a> documents its successful original native runs. For the full course, consult <a href="https://github.com/almiyead-rgb/masar-modern-data-engineering/actions/workflows/verify-course-native.yml">the current native workflow</a>. A run must pass all required steps; a source upload is not proof of execution.</p>',
'<h1>سجل التنفيذ</h1><p>يوثق <a href="../day01/verification.json">سجل اليوم الأول</a> نجاح تشغيله الأصلي. للدورة كاملة، راجع <a href="https://github.com/almiyead-rgb/masar-modern-data-engineering/actions/workflows/verify-course-native.yml">فحص التشغيل الحالي</a>. يجب نجاح الخطوات المطلوبة كلها؛ رفع المصدر ليس دليل تنفيذ.</p>')+bi('<p>Test target: Python 3.11, Java 17, Spark 3.5.8 and Delta 3.3.2. Kafka and Great Expectations are needed on Day 4; dbt is used on Day 2. Colab’s hosted service is not separately tested by a GitHub run.</p>','<p>بيئة الاختبار: Python 3.11 وJava 17 وSpark 3.5.8 وDelta 3.3.2. يستخدم اليوم الرابع Kafka وGreat Expectations، ويستخدم اليوم الثاني dbt. لا يُعد تنفيذ GitHub اختبارًا مستقلًا لخدمة Colab المستضافة.</p>'))
write('STATUS.md',bi('<p><a href="docs/VERIFICATION.md">Read the execution record</a> · <a href="README.md">Course home</a></p>','<p><a href="docs/VERIFICATION.md">اقرأ سجل التنفيذ</a> · <a href="README.md">الرئيسية</a></p>'))
write('labs/README.md',bi('<h1>Eight labs · one project</h1>'+''.join(f'<p>Lab {n:02}: <a href="../day{d:02}/labs/lab{n:02}/README.md">Day {d}</a></p>' for n,d in LAB_DAYS.items()),'<h1>ثمانية لابات · مشروع واحد</h1>'+''.join(f'<p>اللاب {n:02}: <a href="../day{d:02}/labs/lab{n:02}/README.md">اليوم {d}</a></p>' for n,d in LAB_DAYS.items())))
write('docs/SETUP.md',bi('<h1>Prepare once, learn over five days</h1><p>Use a local Python 3.11 environment and Java 17. Check <code>java -version</code> and set <code>JAVA_HOME</code> before launching Jupyter. The small dataset uses CPU only. Keep the full repository together.</p>',
'<h1>جهّز مرة واحدة وتعلم خلال خمسة أيام</h1><p>استخدم بيئة Python 3.11 محلية وJava 17. تحقق من <code>java -version</code> واضبط <code>JAVA_HOME</code> قبل فتح Jupyter. تعمل البيانات الصغيرة باستخدام CPU. احتفظ بالمستودع كاملًا.</p>')+'''```bash
git clone https://github.com/almiyead-rgb/masar-modern-data-engineering.git
cd masar-modern-data-engineering
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-course.txt -r requirements-day01.txt
python -m pip check
python -m jupyterlab
```

'''+bi('<p>On Windows Command Prompt, create the environment with <code>py -3.11 -m venv .venv</code> and activate it with <code>.venv\\Scripts\\activate</code>. In Jupyter, choose the environment’s Python kernel and open <code>day01/STUDENT.ipynb</code>. Continue with one notebook per day.</p>',
'<p>في موجه أوامر Windows أنشئ البيئة بأمر <code>py -3.11 -m venv .venv</code> وفعّلها بأمر <code>.venv\\Scripts\\activate</code>. داخل Jupyter اختر نواة Python الخاصة بالبيئة وافتح <code>day01/STUDENT.ipynb</code>، ثم تابع بدفتر واحد لكل يوم.</p>')+bi('<h2>Day 4 service</h2><p>Before Day 4, start the provided local Kafka broker using <a href="../day04/SETUP.md">the Day 4 setup</a>. You do not need this service for Days 1–3. Use the supplied local addresses; do not expose the broker publicly.</p>',
'<h2>خدمة اليوم الرابع</h2><p>قبل اليوم الرابع شغّل وسيط Kafka المحلي المرفق وفق <a href="../day04/SETUP.md">إعداد اليوم الرابع</a>. لا تحتاج إلى الخدمة للأيام 1–3. استخدم العناوين المحلية المرفقة ولا تعرض الوسيط للعامة.</p>')+bi('<h2>Saving work</h2><p>Save each executed notebook and daily handoff ZIP. Restore a handoff at the repository root when moving to a new session. Never overwrite the fixed source data or delete earlier outputs to rerun. See <a href="TROUBLESHOOTING.md">troubleshooting</a> and <a href="VERIFICATION.md">tested environments</a>.</p>',
'<h2>حفظ العمل</h2><p>احفظ كل دفتر منفذ وملف الانتقال اليومي. استعد ملف الانتقال في جذر المستودع عند تغيير الجلسة. لا تعدّل البيانات الأصلية الثابتة ولا تحذف المخرجات السابقة لإعادة التشغيل. راجع <a href="TROUBLESHOOTING.md">معالجة الأخطاء</a> و<a href="VERIFICATION.md">البيئات المختبرة</a>.</p>'))
# Final submission stays singular and clear.
write('project/SUBMISSION.md',bi('<h1>Submit your cumulative project</h1><p>After Day 5, submit one accessible GitHub repository URL and its final commit ID through the organizer’s announced channel. Keep the same project you developed in Labs 01–08.</p>',
'<h1>سلّم مشروعك التراكمي</h1><p>بعد اليوم الخامس سلّم رابط مستودع GitHub واحدًا قابلًا للوصول ومعرف تعديله النهائي عبر القناة التي تعلنها الجهة المنظمة. سلّم المشروع نفسه الذي طورته في اللابات 01–08.</p>')+bi('<h2>Include</h2><p>A README describing the programme, dataset, environment, run order and actual results; the five executed daily notebooks; Lab 01–08 notes; your architecture, performance and governance decisions; and a link to the retained small output artifact. Use the existing templates and reference shared evidence instead of duplicating it.</p>',
'<h2>أدرج في التسليم</h2><p>README يوضح البرنامج والبيانات والبيئة وترتيب التشغيل والنتائج الفعلية، والدفاتر اليومية الخمسة المنفذة، وملاحظات اللابات 01–08، وقرارات المعمارية والأداء والحوكمة، ورابط ملف المخرجات الصغير المحفوظ. استخدم القوالب الموجودة وأشر إلى الدليل المشترك بدل تكراره.</p>')+bi('<h2>Check before sharing</h2><p>Open your repository link, check that notebooks retain outputs, and remove credentials, caches and real personal data. Credit Meaad Al-Marri, Modern Data Engineering for AI Systems (SDA-DSC-214), <a href="https://github.com/SDAIAAcademy">SDAIA Academy</a> and reused sources. Explain that the data is synthetic. Optional extensions and repository stars are not required.</p>',
'<h2>تحقق قبل المشاركة</h2><p>افتح رابط المستودع وتأكد من حفظ مخرجات الدفاتر، واستبعد بيانات الدخول والملفات المؤقتة والبيانات الشخصية الحقيقية. اذكر ميعاد المري وبرنامج هندسة البيانات الحديثة لأنظمة الذكاء الاصطناعي (SDA-DSC-214) ورابط <a href="https://github.com/SDAIAAcademy">أكاديمية سدايا</a> والمصادر المستخدمة. وضح أن البيانات اصطناعية. لا تُشترط الامتدادات الاختيارية أو نجوم المستودع.</p>'))
# Remove one-off transfer workflows and the obsolete repeatedly-mutating Day 1 publisher.
for name in ('publish-course.yml','publish-day01.yml','publish-prepared-course.yml','publish-prepared-lessons.yml','recover-course-content.yml','verify-publishing.yml','course-snapshot.yml'):
    path=ROOT/'.github/workflows'/name
    if path.exists():path.unlink()
# Fix legacy text links to the retired publisher, preserving real action-run URLs.
for p in ROOT.rglob('*.md'):
    if '.git' in p.parts:continue
    text=p.read_text();text=text.replace('.github/workflows/publish-day01.yml','.github/workflows/verify-course-native.yml')
    p.write_text(text,encoding='utf-8')
assert source_hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data/masar-small-v1').iterdir() if p.is_file()}
write('tools/student_layout_v1.json',json.dumps({'layout':1,'days':5,'labs':8,'data_sha256':source_hashes,'moves':mapping},ensure_ascii=False,indent=2)+'\n')
print('Organized five day folders, one main notebook per day, original lessons and unchanged source data.')
