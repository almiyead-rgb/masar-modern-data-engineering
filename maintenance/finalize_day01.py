"""Idempotent Day 1 publication fixes; never modify subsequent course days."""
from pathlib import Path
import re
import nbformat

ROOT = Path(__file__).resolve().parents[1]

CHECKER = r'''"""Validate only the published Day 1 learning path, including notebook links."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit
import nbformat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.sources import verify_manifest

verify_manifest(ROOT / "data/masar-small-v1")
required = ["DAY01_STUDENT.ipynb", "README.md", "course.json",
            "resources/Masar_Cost_Model.xlsx", "docs/START_HERE.md", "docs/SETUP.md",
            "docs/TROUBLESHOOTING.md", "docs/GIT_WORKFLOW.md",
            "project/README.md", "project/SUBMISSION.md"]
required += ["day01/" + name + ".md" for name in
             ["README", "CONCEPTS", "GLOSSARY", "SOURCES", "PRACTICE", "COMPLETION"]]
required += [f"labs/lab0{number}/{name}.md" for number in (1, 2)
             for name in ("README", "WALKTHROUGH")]
missing = [path for path in required if not (ROOT / path).is_file()]
if missing:
    raise AssertionError({"missing_day01_files": missing})
# Later-day drafts/tests are deliberately outside this publication's scope.
markdown = [ROOT / path for path in ["README.md", "STATUS.md", "TRAINING_CONTENT.md",
    "labs/README.md", "data/README.md", "data/DICTIONARY.md",
    "docs/START_HERE.md", "docs/SETUP.md", "docs/TROUBLESHOOTING.md",
    "docs/GIT_WORKFLOW.md", "project/README.md", "project/SUBMISSION.md",
    "templates/DECISIONS.md", "templates/LAB_NOTES.md", "templates/BENCHMARKS.md"]]
for folder in ["day01", "labs/lab01", "labs/lab02"]:
    markdown.extend((ROOT / folder).glob("*.md"))
errors, checked_links = [], 0

def check_links(path, text):
    global checked_links
    targets = re.findall(r'href=["\']([^"\']+)["\']', text)
    targets += re.findall(r'\]\(([^)]+)\)', text)
    for target in targets:
        url = urlsplit(target)
        if url.scheme or not url.path:
            continue
        checked_links += 1
        resolved = (path.parent / unquote(url.path)).resolve()
        if not resolved.is_relative_to(ROOT) or not resolved.exists():
            errors.append((str(path.relative_to(ROOT)), target))

for path in sorted(set(markdown)):
    check_links(path, path.read_text(encoding="utf-8"))
notebooks = [ROOT / "DAY01_STUDENT.ipynb", *sorted((ROOT / "notebooks/day01").glob("*.ipynb"))]
for path in notebooks:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            check_links(path, cell.source)
if errors:
    raise AssertionError({"broken_day01_links": errors})
print(json.dumps({"scope": "DAY01_ONLY", "required_files": len(required),
    "markdown_pages": len(set(markdown)), "notebooks": len(notebooks),
    "internal_links": checked_links, "dataset": "unchanged", "status": "PASSED"}, indent=2))
'''
(ROOT / 'scripts/check_day01.py').write_text(CHECKER, encoding='utf-8')


def replace_paragraph(path, marker, replacement):
    text = path.read_text(encoding='utf-8')
    pattern = r'<p>(?:(?!</p>).)*' + re.escape(marker) + r'(?:(?!</p>).)*</p>'
    text, count = re.subn(pattern, lambda match: '<p>' + replacement + '</p>', text, flags=re.S)
    if count > 1:
        raise AssertionError(f'Ambiguous paragraph in {path}: {marker}')
    path.write_text(text, encoding='utf-8')

for number in (1, 2):
    path = ROOT / f'labs/lab0{number}/README.md'
    objectives = 'LO1, LO8' if number == 1 else 'LO2, LO8'
    # Replace the two language-specific status paragraphs without collapsing columns.
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'<p>Day 1 · (?:(?!</p>).)*<strong>PARTIAL</strong>(?:(?!</p>).)*</p>',
        f'<p>Day 1 · {objectives}. <a href="../../DAY01_STUDENT.ipynb">Open the combined learner notebook</a>. '
        'The source and native sections belong to this same lab. '
        '<a href="../../STATUS.md">Latest execution evidence and tested environment</a>.</p>', text, flags=re.S)
    text = re.sub(r'<p>اليوم 1 · (?:(?!</p>).)*<strong>PARTIAL</strong>(?:(?!</p>).)*</p>',
        f'<p>اليوم الأول · {objectives}. <a href="../../DAY01_STUDENT.ipynb">افتح دفتر المتدرب الموحد</a>. '
        'الأجزاء التحضيرية وأجزاء المحرك هي أجزاء من اللاب نفسه. '
        '<a href="../../STATUS.md">نتيجة التنفيذ الأحدث والبيئة المختبرة</a>.</p>', text, flags=re.S)
    text = text.replace('Open the engine notebook draft', 'Open the native notebook section')
    text = text.replace('افتح مسودة دفتر المحرك', 'افتح جزء التطبيق بالمحرك')
    text = text.replace('The implementation is authored; execution remains unverified. The executed preparatory notebook above is retained.',
        'Use the combined notebook for the full ordered lab. This separate notebook contains the same code cells and records their output provenance.')
    text = text.replace('الكود مكتوب؛ تشغيله ما يزال غير متحقق. الدفتر التحضيري المنفذ أعلاه محفوظ.',
        'استخدم الدفتر الموحد لتنفيذ اللاب كاملًا بالترتيب. يحتوي هذا الدفتر المنفصل على الخلايا البرمجية نفسها مع توثيق مصدر مخرجاتها.')
    old_en = 'Use earlier lab outputs where the task requires Bronze or Silver; these source files do not replace those tables.'
    old_ar = 'استخدم مخرجات اللابات السابقة عندما تتطلب المهمة Bronze أو Silver؛ ملفات المصدر لا تستبدل هذه الجداول.'
    if number == 1:
        en = 'This is the first lab: start from these three fixed raw feeds. No earlier Bronze or Silver tables are required.'
        ar = 'هذا هو اللاب الأول: ابدأ بملفات المصدر الخام الثلاثة الثابتة. لا تحتاج إلى جداول Bronze أو Silver سابقة.'
    else:
        en = 'Use the successful Bronze workspace from Lab 01. Compare the original CSV with Delta version 0 so both scans contain the same 72 trips.'
        ar = 'استخدم مساحة Bronze الناجحة من اللاب 01. قارن CSV الأصلي بنسخة Delta رقم صفر حتى يحتوي طرفا القياس على الرحلات الـ72 نفسها.'
    path.write_text(text.replace(old_en, en).replace(old_ar, ar), encoding='utf-8')

path = ROOT / 'day01/CONCEPTS.md'
replace_paragraph(path, 'Real Bronze writes and the Spark benchmark remain unverified.',
    'This guide covers the source inspection, Delta Bronze writes and Spark scan measurement in Labs 01 and 02. '
    'Use the combined notebook for the full sequence. <a href="../STATUS.md">Execution evidence and environment limits</a> '
    'are recorded separately from the conceptual explanation.')
replace_paragraph(path, 'تبقى الكتابة الحقيقية إلى Bronze وقياس Spark غير متحققين.',
    'يغطي هذا الدليل فحص المصادر وكتابة Bronze باستخدام Delta وقياس Spark ضمن اللابين 01 و02. '
    'استخدم الدفتر الموحد للتنفيذ بالترتيب. تُوثق <a href="../STATUS.md">أدلة التنفيذ وحدود البيئة</a> '
    'بصورة منفصلة عن الشرح المفاهيمي.')

path = ROOT / 'day01/COMPLETION.md'
replace_paragraph(path, 'Day 1 remains <strong>PARTIAL</strong>',
    'Finish both labs in the combined notebook and retain the generated reports and handoff ZIP. '
    '<a href="../STATUS.md">The execution record</a> shows the tested environment; '
    'your own run must also complete its assertions before you proceed.')
replace_paragraph(path, 'يبقى اليوم الأول <strong>PARTIAL</strong>',
    'أكمل اللابين في الدفتر الموحد واحتفظ بالتقارير المولدة وملف ZIP للانتقال. '
    'يوضح <a href="../STATUS.md">سجل التنفيذ</a> البيئة المختبرة؛ '
    'ويجب أن تنجح فحوص تشغيلك أيضًا قبل الانتقال.')
text = path.read_text(encoding='utf-8')
text = text.replace('Current status is partial', 'Complete the verified learning sequence')
text = text.replace('الحالة الحالية جزئية', 'أكمل مسار التعلم وفحوصه')
text = text.replace('the executed Bronze and scan notebooks when available', 'your executed Bronze and scan sections')
text = text.replace('ودفتري Bronze والقياس المنفذين عندما يتاحان', 'وأجزاء Bronze والقياس المنفذة في دفترك')
text = text.replace('The Day 2 page (next stage / المرحلة التالية) remains a planned stage.',
                    'Day 2 is a separate publication and review stage.')
text = text.replace('تظل صفحة اليوم الثاني (next stage / المرحلة التالية) مرحلة مخططة.',
                    'يُنشر اليوم الثاني ويُراجع في مرحلة منفصلة.')
text = text.replace('secrets or instructor-only material', 'secrets or personal information')
text = text.replace('أسرارًا أو مواد خاصة بالمدربة', 'أسرارًا أو معلومات شخصية')
text += '\n<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" valign="top"><h2>Handoff ZIP</h2><p>The final cell saves <code>outputs/day01_handoff.zip</code>: the successful-workspace pointer, Delta tables, transaction logs, lab reports and source/cost reports. Extract it into the next session\'s repository root to preserve the same relative paths. Save the executed notebook and learning notes separately.</p></td><td width="50%" dir="rtl" lang="ar" valign="top"><h2>ملف الانتقال</h2><p>تحفظ الخلية الأخيرة <code>outputs/day01_handoff.zip</code>: مؤشر مساحة العمل الناجحة وجداول Delta وسجلات المعاملات وتقارير اللابين وفحص المصدر والتكلفة. فك ضغطه في جذر مستودع الجلسة التالية للحفاظ على المسارات نفسها. احفظ الدفتر المنفذ وملاحظات التعلم بصورة منفصلة.</p></td></tr></table>\n' if 'Handoff ZIP</h2>' not in text else ''
path.write_text(text, encoding='utf-8')
path = ROOT / 'labs/lab02/WALKTHROUGH.md'
text = path.read_text(encoding='utf-8').replace('the scan notebook draft', 'the scan notebook').replace('مسودة دفتر القياس', 'دفتر القياس')
path.write_text(text, encoding='utf-8')

path = ROOT / 'DAY01_STUDENT.ipynb'
notebook = nbformat.read(path, as_version=4)
for cell in notebook.cells:
    if cell.cell_type == 'markdown':
        # These sections were originally stored two directories below the repository root.
        cell.source = re.sub(r'(href=["\'])\.\./\.\./', r'\1', cell.source)
        cell.source = re.sub(r'(\]\()\.\./\.\./', r'\1', cell.source)
        cell.source = cell.source.replace('href="04_spark_scan.ipynb"', 'href="notebooks/day01/04_spark_scan.ipynb"')
    if cell.cell_type == 'code' and ('shutil.make_archive' in cell.source or 'DAY01_HANDOFF_V2' in cell.source):
        cell.source = '''# DAY01_HANDOFF_V2: retain the pointer and all small reports as well as Delta files.
from pathlib import Path
import zipfile
from masar.workspace import completed_bronze_workspace
WORK = completed_bronze_workspace(ROOT)
pointer = ROOT / 'outputs/day01_bronze_success.json'
files_to_save = {pointer, *(p for p in WORK.rglob('*') if p.is_file())}
for name in ('source_inspection.json', 'cost_model_result.json'):
    files_to_save.update((ROOT / 'outputs').rglob(name))
archive = ROOT / 'outputs/day01_handoff.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted(files_to_save):
        bundle.write(path, arcname=path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    assert bundle.read('outputs/day01_bronze_success.json') == pointer.read_bytes()
    assert any(name.endswith('source_inspection.json') for name in bundle.namelist())
    assert any(name.endswith('cost_model_result.json') for name in bundle.namelist())
print('Keep this ZIP for the next day:', archive)
print('Also save this notebook with outputs and your LAB01/LAB02 notes.')
if IS_COLAB:
    from google.colab import files
    files.download(str(archive))'''
nbformat.validate(notebook)
nbformat.write(notebook, path)

path = ROOT / 'scripts/validate_day01_native.py'
text = path.read_text(encoding='utf-8')
text = text.replace('Days 2–5 are not published in this stage.', 'Days 2–5 are outside this review; any existing later-day files are not approved by this check.')
text = text.replace('الأيام 2–5 غير منشورة في هذه المرحلة.', 'الأيام 2–5 خارج نطاق هذه المراجعة؛ وجود ملفاتها لا يعني اعتمادها بهذا الفحص.')
path.write_text(text, encoding='utf-8')
print('Day 1 links, completion guidance, handoff and scoped checks updated; no later-day files modified.')
