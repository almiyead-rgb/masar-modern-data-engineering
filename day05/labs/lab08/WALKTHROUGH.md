<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 08 · Guided AI/BI handoff</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 08 · تقديم AI وBI خطوة بخطوة</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../../../README.md">Course home</a> · <a href="../../../STATUS.md">Execution record</a> · <a href="../../README.md">Day 5</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../../../README.md">الرئيسية</a> · <a href="../../../STATUS.md">الجاهزية</a> · <a href="../../README.md">اليوم الخامس</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>1. Select only the committed release</h2><p>Load the latest manifest through <a href="../../../src/masar/serving.py">read_release</a>. Verify its hash, identity, table set, pinned Delta versions and actual row content. Do not scan arbitrary folders and guess which files belong together.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>١. اختر الإصدار المعتمد فقط</h2><p>حمّل سجل الإصدار الأخير عبر <a href="../../../src/masar/serving.py">read_release</a>. تحقق من بصمته وهويته ومجموعة الجداول ونسخ Delta والمحتوى الفعلي. لا تفحص مجلدات عشوائية وتخمن الملفات التي تنتمي إلى إصدار واحد.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>2. Inspect the BI star</h2><p>Check all fact keys resolve to date, zone and driver dimensions and that each dimension key is unique. Explain why the compact date dimension covers only the observed three dates. The fact row count must stay 75 after adding descriptions.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٢. افحص المخطط النجمي</h2><p>تحقق من ارتباط مفاتيح الوقائع بأبعاد التاريخ والمنطقة والسائق وفردية مفاتيح الأبعاد. اشرح اقتصار بُعد التاريخ الصغير على الأيام الثلاثة المرصودة. يجب أن يبقى عدد صفوف الوقائع 75 بعد إضافة الأوصاف.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>3. Run the read-only BI query</h2><p>The native notebook reads the pinned fact version and executes an actual Spark SQL city aggregation. Compare each city and the 1880.60 SAR grand total with the independent reference. Do not compare different releases or count raw GPS messages as trips.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٣. نفذ استعلام BI للقراءة فقط</h2><p>يقرأ الدفتر الأصلي نسخة الوقائع الثابتة وينفذ تجميع المدن فعليًا بـSpark SQL. قارن كل مدينة والإجمالي 1880.60 ريال بالمرجع المستقل. لا تقارن إصدارين مختلفين ولا تعد رسائل GPS رحلات.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>4. Inspect the feature allowlist</h2><p>Show the cutoff, prior-24-hour window and next-hour horizon. Select only the four documented feature inputs. Explain the difference between the historical average duration and an unknown future target. Keep metadata for audit without feeding all columns to a model.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٤. افحص قائمة الخصائص المسموحة</h2><p>اعرض وقت القطع ونافذة 24 ساعة الماضية وأفق الساعة التالية. اختر المدخلات الأربعة الموثقة فقط. اشرح الفرق بين متوسط مدة تاريخي ونتيجة مستقبلية مجهولة. احتفظ ببيانات التدقيق دون إدخال كل الأعمدة إلى النموذج.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>5. Retain unknown labels</h2><p>The three label-status rows must remain UNOBSERVED with NULL targets. The dataset is not evidence that future demand equals zero. Do not compute model accuracy, train/test split scores or an invented prediction from these rows.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٥. احتفظ بالنتائج المجهولة</h2><p>يجب أن تبقى صفوف النتائج الثلاثة UNOBSERVED وبأهداف NULL. البيانات ليست دليلًا على أن الطلب المستقبلي صفر. لا تحسب دقة نموذج أو درجات تقسيم تدريب واختبار أو تنبؤًا مختلقًا من هذه الصفوف.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>6. Export and validate the bounded files</h2><p>Write the eight table exports to a new reports/serving directory. Re-read each CSV and check headers, row values and counts, then save SHA-256 hashes in the serving report. Empty fields represent NULL; schema contracts must accompany the exports. These are local files, not a deployed data service.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٦. صدّر الملفات الصغيرة وافحصها</h2><p>اكتب الجداول الثمانية في مجلد reports/serving جديد. أعد قراءة كل CSV وافحص الرؤوس والقيم والأعداد ثم احفظ بصمات SHA-256 في تقرير التقديم. تمثل الحقول الفارغة NULL ويجب إرفاق العقود. هذه ملفات محلية وليست خدمة بيانات منشورة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>7. Finish the same project submission</h2><p>Answer the final four embedded questions in LAB08_NOTES.md. Collect prior lab evidence and use <a href="../../../project/SUBMISSION.md">the existing submission route</a>. The optional inventory command below helps find missing documents; it is not a grade or independent proof of engine execution.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٧. أكمل تسليم المشروع نفسه</h2><p>أجب عن الأسئلة المدمجة الأربعة الأخيرة في LAB08_NOTES.md. اجمع أدلة اللابات السابقة واتبع <a href="../../../project/SUBMISSION.md">مسار التسليم الحالي</a>. يساعد أمر الحصر الاختياري أدناه على كشف المستندات الناقصة؛ ولا يمنح درجة أو يثبت التشغيل بصورة مستقلة.</p></td></tr></tbody>
</table>

```bash
python scripts/check_submission.py --submission /path/to/your-project --workspace /path/to/course/outputs/your-workspace
```
