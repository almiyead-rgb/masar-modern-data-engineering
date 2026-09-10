"""Apply learner-facing editorial fixes without changing lesson examples or data."""
from pathlib import Path
import re, json
from bs4 import BeautifulSoup
import nbformat
ROOT = Path(__file__).resolve().parents[1]
if not (ROOT/'course.json').exists(): ROOT=Path('/mnt/data/masar_delivery')

def bi(en, ar):
 return '<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top">'+en+'</td><td width="50%" dir="rtl" lang="ar" align="right" valign="top">'+ar+'</td></tr></table>\n\n'
def paragraph(name, marker, en, ar):
 p=ROOT/name;s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 found=False
 for t in s.find_all('table'):
  if marker not in t.get_text(' ',strip=True):continue
  cells=t.find_all('td',recursive=True)
  if len(cells)!=2:continue
  for cell, value in zip(cells,[en,ar]):
   old=cell.find('p')
   if old:
    new=BeautifulSoup('<p>'+value+'</p>','html.parser').p;old.replace_with(new)
  found=True;break
 if not found:raise ValueError((name,marker))
 p.write_text(str(s),encoding='utf-8')

paragraph('day02/COMPLETION.md','Definition of completion',
 'Complete both parts of Lab 03, run the dbt models and tests, inspect the saved Silver rows, and explain the source/ref relationships in LAB03_NOTES.md. Retain your notebook outputs and handoff archive.',
 'أكمل جزأي اللاب 03 وشغّل نماذج dbt واختباراتها وافحص صفوف Silver المحفوظة، ثم اشرح علاقة source وref في LAB03_NOTES.md. احتفظ بمخرجات دفترك وملف الانتقال.')
paragraph('day02/DBT_GUIDE.md','Connection and runner authored',
 'Use dbt to organize and test the same transformations in Lab 03. Continue with the same source data and document your results in the existing lab notes.',
 'استخدم dbt لتنظيم التحويلات نفسها واختبارها ضمن اللاب 03. تابع بالبيانات الأصلية نفسها ووثّق نتائجك في ملاحظات اللاب.')
paragraph('day02/DBT_GUIDE.md','11 · Keep it inside',
 'Record the roles of source/ref, the reason for the ingestion lookback, and the replay results in LAB03_NOTES.md. Retain the generated dbt reports with the daily handoff. The models belong to this lab, not a separate project.',
 'سجل دور source وref وسبب نافذة إعادة المعالجة ونتائج الإعادة في LAB03_NOTES.md. احتفظ بتقارير dbt المولدة ضمن مخرجات اليوم. النماذج جزء من هذا اللاب وليست مشروعًا منفصلًا.')
paragraph('day02/dbt/README.md','Six models, seven',
 'Run the six models, seven singular SQL tests, key/null tests and arrival-time freshness checks through the daily notebook. Read DBT_GUIDE.md for the dependency graph and interpretation.',
 'شغّل النماذج الستة واختبارات SQL المنفردة السبعة وفحوص المفاتيح والفراغ وحداثة الوصول من دفتر اليوم. اقرأ DBT_GUIDE.md لفهم ترتيب الاعتماد وتفسير النتائج.')
paragraph('day02/labs/lab03/WALKTHROUGH.md','The reference notebook contains',
 'Run STUDENT.ipynb to produce real Spark/Delta and dbt results. Compare the stored table values with the fixed-data expectations explained below. REFERENCE.ipynb is an optional independent arithmetic check, not the main lab.',
 'شغّل STUDENT.ipynb لإنتاج نتائج Spark وDelta وdbt الفعلية. قارن قيم الجداول المحفوظة بالتوقعات المحسوبة من البيانات الثابتة أدناه. الدفتر REFERENCE.ipynb فحص حسابي مستقل اختياري، وليس اللاب الأساسي.')
paragraph('day02/labs/lab03/README.md','PARTIAL / ENGINE_NOT_EXECUTED',
 'Day 2 · LO3 and LO8 · Parts 3a and 3b. Use the actual Day 1 Delta output to build typed staging and incremental Silver. The dbt models apply the same transformation rules.',
 'اليوم الثاني · LO3 وLO8 · الجزآن 3a و3b. استخدم مخرجات Delta الفعلية من اليوم الأول لبناء البيانات المهيأة وSilver تدريجيًا. تطبق نماذج dbt قواعد التحويل نفسها.')
for n in (5,6):
 name=f'day04/labs/lab{n:02}/README.md'
 paragraph(name,'PARTIAL:',
  ('Lab 05 · Receive the fixed event stream and test checkpoint recovery, replay and late arrival.' if n==5 else 'Lab 06 · Validate the mixed batch, quarantine rejected records with reasons, and revalidate the accepted data.'),
  ('اللاب 05 · استقبل الأحداث الثابتة واختبر الاستئناف والإعادة والوصول المتأخر.' if n==5 else 'اللاب 06 · افحص الدفعة المختلطة واعزل السجلات المرفوضة مع أسبابها، ثم أعد فحص البيانات المقبولة.'))
for n in (7,8):
 paragraph(f'day05/labs/lab{n:02}/README.md','PARTIAL / ENGINE_NOT_EXECUTED',
  ('Lab 07 · Build Gold from the accepted Day 4 data and test recovery while preserving the last valid release.' if n==7 else 'Lab 08 · Read a fixed release, inspect reporting and feature tables, run the BI query and retain your project evidence.'),
  ('اللاب 07 · ابنِ Gold من بيانات اليوم الرابع المقبولة واختبر التعافي مع الحفاظ على آخر إصدار سليم.' if n==7 else 'اللاب 08 · اقرأ إصدارًا محددًا وافحص جداول التقارير والخصائص ونفّذ استعلام BI، ثم احفظ أدلة مشروعك.'))
paragraph('data/DICTIONARY.md','The authored lab adds',
 'Bronze adds _source_file (file name), _source_sha256 (source-file hash), _batch_id (delivery identity) and _ingested_at (UTC ingestion timestamp). GPS lines remain raw_json and CSV values remain strings. The source files are never overwritten.',
 'تضيف Bronze الحقول _source_file لاسم الملف و_source_sha256 لبصمته و_batch_id لهوية الدفعة و_ingested_at لوقت الاستقبال بتوقيت UTC. تبقى أحداث GPS في raw_json وقيم CSV نصوصًا. لا تُستبدل ملفات المصدر الأصلية.')
paragraph('day03/CONCEPTS.md','Day 4 continues with',
 'Continue Day 4 with corrected Silver and the original event feeds. Do not use sandbox schema additions or deletion experiments as reporting facts or AI features. Retain the results in the completion checklist.',
 'تابع اليوم الرابع باستخدام Silver المصححة ومصادر الأحداث الأصلية. لا تستخدم إضافات المخطط أو تجارب الحذف المعزولة كوقائع تقارير أو خصائص ذكاء اصطناعي. احفظ النتائج المحددة في قائمة الاكتمال.')
paragraph('day05/CONCEPTS.md','Collect executed notebooks, notes',
 'Collect the executed daily notebooks, lab notes, architecture and governance decisions, measurements and the small output archive. Check the dbt result from Day 2 as well as the native pipeline results. Do not commit dependencies, caches or credentials.',
 'اجمع الدفاتر اليومية المنفذة وملاحظات اللابات وقرارات المعمارية والحوكمة والقياسات وملف المخرجات الصغير. راجع نتيجة dbt من اليوم الثاني ونتائج خط المعالجة الأصلي. لا ترفع المكتبات أو الملفات المؤقتة أو بيانات الدخول.')
paragraph('day05/INTEGRATION.md','Scope of “passed”',
 'The integration runner tests the native Spark/Delta, Kafka and GX sequence. Its status PASSED_NATIVE_PATH_DBT_NOT_VALIDATED means that dbt must also pass separately through the Day 2 notebook. Read both reports before submitting the project.',
 'يفحص مشغّل التكامل تسلسل Spark وDelta وKafka وGX. تعني حالته PASSED_NATIVE_PATH_DBT_NOT_VALIDATED ضرورة نجاح dbt أيضًا بصورة مستقلة من دفتر اليوم الثاني. اقرأ التقريرين قبل تسليم المشروع.')
paragraph('docs/ADMINISTRATION.md','Formal assessment versus',
 'Use the completion checklists to verify your technical work. Follow the organizer’s announced assessment and certification policy for formal evaluation.',
 'استخدم قوائم الاكتمال للتحقق من عملك التقني، واتبع سياسة التقييم والشهادة التي تعلنها الجهة المنظمة للتقييم الرسمي.')
paragraph('infrastructure/kafka/README.md','candidate configuration',
 'Start the local broker using the Day 4 setup and compose.yaml. Keep the named data volume between restarts and keep the host port restricted to the local machine.',
 'شغّل الوسيط المحلي باستخدام إعداد اليوم الرابع وcompose.yaml. احتفظ بوحدة تخزين البيانات عند إعادة التشغيل، وأبقِ المنفذ مقصورًا على الجهاز المحلي.')
# Remove paragraphs whose only purpose was describing the former authoring session.
for path in [ROOT/'SOURCES.md',ROOT/'day05/SOURCES.md']:
 s=BeautifulSoup(path.read_text(),'html.parser')
 for table in s.find_all('table'):
  text=table.get_text(' ',strip=True)
  if 'supplied training description' in text or 'No successful Spark/Delta/Kafka/GX' in text:table.decompose()
 text=str(s).replace('These references support the authored explanations, not a claim of completed engine execution.','Use these primary references to review the operations in the daily labs.')
 text=text.replace('Checked during this build on 10 September 2026:','Primary references (reviewed 10 September 2026):').replace('رُوجعت في هذا البناء بتاريخ ١٠ سبتمبر ٢٠٢٦:','مراجع أصلية (رُوجعت في ١٠ سبتمبر ٢٠٢٦):')
 path.write_text(text,encoding='utf-8')
# Student Git guide: no build-state history or private instructor materials.
(ROOT/'docs/GIT_WORKFLOW.md').write_text(bi('<h1>Save your work with Git</h1><p>Keep one repository for the cumulative project. Use a development branch for your changes, inspect the diff and commit meaningful learning steps. Keep file names and commit messages in English.</p>',
 '<h1>احفظ عملك باستخدام Git</h1><p>احتفظ بمستودع واحد للمشروع التراكمي. استخدم فرع تطوير لتعديلاتك وراجع الفروق واحفظ مراحل التعلم برسائل واضحة. استخدم الإنجليزية لأسماء الملفات ورسائل التعديل.</p>')+'''```bash
git switch -c develop
git status
git diff
git add day01/STUDENT.ipynb LAB01_NOTES.md LAB02_NOTES.md
git diff --staged
git commit -m "Complete Day 1 Bronze and scan experiments"
```

'''+bi('<p>Use the files you actually changed in git add. Keep outputs/, handoff ZIP files, virtual environments and credentials out of ordinary commits. Save the output archive through the approved submission channel; retain bounded results inside notebooks.</p><p>A private-looking folder name does not protect information in a public repository. Do not force-push or delete earlier work to repair a notebook error. See <a href="../project/SUBMISSION.md">submission</a>.</p>',
 '<p>حدد في git add الملفات التي عدلتها فعلًا. استبعد outputs/ وملفات الانتقال والبيئات الافتراضية وبيانات الدخول من التعديلات الاعتيادية. احفظ ملف المخرجات عبر قناة التسليم المعتمدة واحتفظ بالنتائج الصغيرة داخل الدفاتر.</p><p>اسم المجلد لا يحمي المعلومات في مستودع عام. لا تستخدم الدفع القسري أو تحذف عملك السابق لإصلاح خطأ في دفتر. راجع <a href="../project/SUBMISSION.md">التسليم</a>.</p>'),encoding='utf-8')
# Replace stale Day 1 execution narrative while retaining every concept section.
paragraph('day01/CONCEPTS.md','Day 1 workflow and learner evidence',
 'Read C01–C06 and complete the source inspection and Bronze sections of Lab 01. Read C07–C09 and complete the cost and Spark scan sections of Lab 02. Record your architecture decision, actual measurements and interpretation in the existing templates. Save your executed notebook and handoff ZIP. [S1]',
 'اقرأ C01–C06 وأكمل فحص المصدر وبناء Bronze ضمن اللاب 01، ثم اقرأ C07–C09 وأكمل التكلفة وقياس Spark ضمن اللاب 02. وثّق قرارك المعماري وقياساتك الفعلية وتفسيرها في القوالب الموجودة. احفظ دفترك المنفذ وملف الانتقال. [S1]')
# Straightforward sentence-level corrections across learning pages.
replacements={
 'Release boundary: useful parts, not a finished lakehouse':'Your Day 1 learning path',
 'حدود الإصدار: أجزاء مفيدة لا Lakehouse مكتملة':'مسار التعلم في اليوم الأول',
 'No content was published to GitHub.':'Follow the links to the daily notebook and sources.',
 'لم ينشر أي محتوى على GitHub.':'اتبع روابط دفتر اليوم والمراجع.',
 'Our planned proof requires':'The lab checks',
 'Runtime status remains ENGINE_NOT_EXECUTED.':'Run the daily notebook and retain its outputs.',
 'الحالة ENGINE_NOT_EXECUTED.':'شغّل دفتر اليوم واحتفظ بمخرجاته.',
 'ENGINE_NOT_EXECUTED.':'',
 'Status: PARTIAL — native code authored; execution unverified':'',
 'الحالة: PARTIAL — الكود الأصلي مكتوب والتنفيذ غير متحقق':'',
 'Status: PARTIAL':'','الحالة: PARTIAL':'',
 'Provision before teaching':'Prepare your environment',
 'تجهيز قبل التدريب':'جهّز بيئتك',
 'This build does not claim offline engine installation has been tested.':'Initial installation requires an internet connection.',
 'لا يدعي هذا البناء اختبار تثبيت المحرك دون اتصال.':'يحتاج التثبيت الأول إلى اتصال بالإنترنت.',
 'private instructor notes':'private information','ملاحظات المدربة':'معلومات خاصة',
 'No support email or unofficial service commitment is invented here.':'Use the support channel announced for your programme.',
 'لا يُختلق هنا بريد دعم أو التزام خدمة غير معتمد.':'استخدم قناة الدعم المعلنة للبرنامج.',
 'No attendance percentage or deadline is fabricated here.':'Check the announced arrangements before the first session.',
 'دون اختلاق نسب أو حدود.':'وفق التعليمات المعلنة.',
 'Remaining gate: execute the authored configuration in the pinned environment and review native artifacts.':'',
 'Runtime and connection':'Environment and execution',
 'Readiness':'Execution record','حالة الجاهزية':'سجل التنفيذ',
}
for p in ROOT.rglob('*.md'):
 text=p.read_text(encoding='utf-8')
 for a,b in replacements.items():text=text.replace(a,b)
 p.write_text(text,encoding='utf-8')
# Day 2 dbt remains in Lab 03, with its reports included in the daily handoff.
for day in range(2,6):
 path=ROOT/f'day{day:02}/STUDENT.ipynb';nb=nbformat.read(path,4)
 for c in nb.cells:
  if c.cell_type=='markdown':c.source=c.source.replace('03c ·','Lab 03 ·').replace('03c ·','اللاب 03 ·')
  if c.cell_type=='code' and day==2 and 'zipfile.ZipFile(archive' in c.source:
   c.source=c.source.replace("with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:","with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:\n    dbt_workspace = dbt_path.parent.parent\n    for p in sorted(dbt_workspace.rglob('*')):\n        if p.is_file():\n            bundle.write(p, p.relative_to(ROOT).as_posix())")
 nbformat.write(nb,path)
# Use the image's pre-owned Kafka storage directory.
for p in (ROOT/'infrastructure').rglob('*.yaml'):
 t=p.read_text().replace('/tmp/kraft-combined-logs','/var/lib/kafka/data');p.write_text(t)
for name in ['maintenance/finalize_day01.py','maintenance/restore_native_sources.py','scripts/validate_day01_native.py','scripts/run_student_notebook.py','scripts/execute_engine_notebooks.py','scripts/verify_native_runtime.py','scripts/workbench.py','RUN_PROJECT.py']:
 p=ROOT/name
 if p.is_file():p.unlink()
# The active learner flow has no one-off publishing/recovery scripts.
print('Removed authoring-session commentary; retained conceptual explanations and learner activities.')
