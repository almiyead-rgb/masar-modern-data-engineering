<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h1>Lab 03 · Guided walkthrough</h1></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h1>اللاب 03 · شرح عملي متدرج</h1></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><a href="../../../README.md">Course home</a> · <a href="../../../STATUS.md">Execution record</a></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><a href="../../../README.md">الرئيسية</a> · <a href="../../../STATUS.md">سجل التنفيذ</a></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Read this boundary first</h2><p>Run STUDENT.ipynb to produce real Spark/Delta and dbt results. Compare the stored table values with the fixed-data expectations explained below. REFERENCE.ipynb is an optional independent arithmetic check, not the main lab.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>اقرأ حدود التنفيذ أولًا</h2><p>شغّل STUDENT.ipynb لإنتاج نتائج Spark وDelta وdbt الفعلية. قارن قيم الجداول المحفوظة بالتوقعات المحسوبة من البيانات الثابتة أدناه. الدفتر REFERENCE.ipynb فحص حسابي مستقل اختياري، وليس اللاب الأساسي.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 1 · Inspect the handoff</h2><p>Keep the complete repo. Native Lab 3a resolves the successful Bronze pointer written by Day 1; it does not guess a directory or reload source CSV as a substitute. The base snapshot is trips version 1, drivers version 0 and GPS version 0.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ١ · افحص نقطة التسليم</h2><p>احتفظ بالمستودع كاملًا. يستخدم اللاب 3a مؤشر مساحة Bronze الناجحة الذي كتبه اليوم الأول، ولا يخمن مجلدًا ولا يستبدل الجداول بملفات CSV. لقطة الأساس هي نسخة الرحلات 1 والسائقين 0 والمواقع 0.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 2 · Run the reference explanation</h2><p>Open 01_silver_reference.ipynb. Inspect city normalization, the midnight example, the five scenario counts and the GPS join pitfall. The notebook writes only reference evidence in a new output folder. It is a teaching/checking aid within Lab 03, not an additional assignment.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ٢ · نفذ الشرح المرجعي</h2><p>افتح 01_silver_reference.ipynb وافحص توحيد المدن ومثال منتصف الليل وأعداد السيناريوهات الخمسة وخطأ ربط المواقع. لا يكتب الدفتر إلا أدلة مرجعية في مجلد مخرجات جديد. هو أداة شرح وفحص ضمن اللاب 03 وليس تكليفًا إضافيًا.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 3 · Build three staging models</h2><p>Native Lab 3a creates stg_trips, stg_drivers and stg_gps. The receipt count remains 144 at trip staging; typing is not deduplication. Drivers remain 6, events 216. Preview the schemas and a few rows before continuing.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ٣ · ابنِ نماذج التهيئة الثلاثة</h2><p>يبني اللاب 3a الأصلي stg_trips وstg_drivers وstg_gps. يبقى عدد نسخ الرحلات 144 في التهيئة؛ تحويل الأنواع ليس إزالة تكرار. يبقى السائقون 6 والأحداث 216. اعرض المخططات وعدة صفوف قبل الإكمال.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 4 · Validate, then enrich</h2><p>Reject invalid typed values, unknown drivers, duplicate driver keys and malformed GPS. Then join trips to drivers and verify that the count did not change. Do not join raw GPS to trip-level fares. The small quality fixture is used only for isolated reference test cases today, not fed into production Silver.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ٤ · افحص ثم أضف الصفات</h2><p>ارفض القيم غير الصالحة والسائقين المجهولين ومفاتيح السائقين المكررة وأحداث المواقع غير السليمة. بعدها اربط الرحلات بالسائقين وتحقق من ثبات العدد. لا تربط أحداث المواقع الخام بأجور الرحلات مباشرة. ملف أخطاء الجودة الصغير يستخدم اليوم لفحوص مرجعية معزولة، ولا يغذى إلى Silver.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 5 · Resolve duplicates without hiding conflicts</h2><p>Compare business payloads per trip/revision first. Any conflict stops the lab. For identical receipts use row_number with stable source ordering. The result has 72 candidate trip rows. Save actual staging snapshots and the staging report before opening Lab 3b.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ٥ · أزل التكرار دون إخفاء التعارض</h2><p>قارن محتوى الأعمال لكل رحلة ومراجعة أولًا؛ يوقف أي تعارض اللاب. للنسخ المتطابقة استخدم row_number بترتيب مصدر ثابت. الناتج 72 صفًا مرشحًا. احفظ لقطات التهيئة الفعلية وتقريرها قبل فتح اللاب 3b.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 6 · Create the initial Silver table</h2><p>Native Lab 3b reads the successful workspace and requires a valid staging report. It writes a real Delta Silver table, then reads the content back and compares it with the independent reference. The expected initial fare sum is 1,794.60 SAR across 72 trips.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ٦ · أنشئ Silver الأولية</h2><p>يقرأ اللاب 3b مساحة التشغيل الناجحة ويتطلب تقرير تهيئة صالحًا. يكتب جدول Silver فعليًا بصيغة Delta، ثم يعيد قراءة المحتوى ويقارنه بالمرجع المستقل. مجموع الأجور الأولي المتوقع 1,794.60 ريال عبر 72 رحلة.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 7 · Exercise retry and late arrival</h2><p>Run the five scenarios in the table below. The insert-only MERGE checks existing content before inserting missing keys. A changed fare for an existing key is not accepted as a duplicate; Day 3 will handle corrections explicitly.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ٧ · جرب الإعادة والوصول المتأخر</h2><p>نفذ السيناريوهات الخمسة الموضحة أدناه. يفحص MERGE المخصص للإضافة محتوى المفاتيح الموجودة قبل إدخال الناقص. اختلاف أجرة مفتاح موجود لا يعد تكرارًا؛ يعالج اليوم الثالث التصحيحات صراحةً.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 8 · Check full content, not just the count</h2><p>After late arrival, expect 75 trips and 1,875.60 SAR, an increase of 81.00 SAR. Compare keys, typed values, local dates and driver attributes as well as the logical content hash. Output versions may increase on a no-op engine transaction; that does not imply duplicated business rows.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ٨ · افحص المحتوى كاملًا لا العدد فقط</h2><p>بعد الوصول المتأخر نتوقع 75 رحلة و1,875.60 ريال، بزيادة 81.00 ريال. قارن المفاتيح والقيم المحولة والتواريخ المحلية وصفات السائقين إضافة إلى بصمة المحتوى المنطقي. قد يزيد رقم نسخة المحرك مع معاملة لا تغير المحتوى؛ لا يعني ذلك تكرار صفوف الأعمال.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Step 9 · Preserve evidence and stop safely</h2><p>A completed rerun is read-only and checks the existing Silver content. An interrupted partial run is preserved; the teaching recovery path creates a new complete Day 1 workspace instead of deleting directories. Never rerun an earlier-day transformation over a table already modified by a later day.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الخطوة ٩ · احفظ الأدلة وتوقف بأمان</h2><p>تعيد الإعادة بعد الاكتمال قراءة Silver وتفحص محتواها دون تعديله. تحفظ المحاولة الجزئية المتوقفة؛ ويستخدم الاسترجاع التدريبي مساحة يوم أول كاملة جديدة بدل حذف المجلدات. لا تعاود تشغيل تحويل يوم سابق فوق جدول عدله يوم لاحق.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Expected scenario reconciliation — not engine results</h2><p>Base + replay: <strong>144 → 72</strong><br/>Transform rerun: <strong>144 → 72</strong><br/>late_003: <strong>147 → 75</strong><br/>Retry late_003: <strong>147 → 75</strong><br/>Redeliver as late_replay_004: <strong>150 → 75</strong><br/>Each arrow means Bronze receipt rows → Silver business rows.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>تسوية السيناريوهات المتوقعة — ليست نتائج المحرك</h2><p>الأساس مع إعادة الإرسال: <strong>144 صف استقبال، 72 رحلة</strong><br/>إعادة التحويل: <strong>144 صف استقبال، 72 رحلة</strong><br/>late_003: <strong>147 صف استقبال، 75 رحلة</strong><br/>إعادة late_003: <strong>147 صف استقبال، 75 رحلة</strong><br/>إرسال جديد late_replay_004: <strong>150 صف استقبال، 75 رحلة</strong><br/>العدد الأول لنسخ الوصول في Bronze، والثاني لرحلات الأعمال في Silver.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Equivalent command-line route</h2><p>These commands run the same shared code as the native notebooks, only after dependencies and Day 1 have passed. They are not an extra task. Do not run both routes to satisfy a duplicate requirement.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>المسار المكافئ من سطر الأوامر</h2><p>تشغل الأوامر الكود المشترك نفسه الذي تستخدمه الدفاتر الأصلية، بعد نجاح المتطلبات واليوم الأول. ليست مهمة إضافية، ولا يلزم تشغيل المسارين لتلبية متطلب مكرر.</p></td></tr></tbody>
</table>

```bash
python scripts/run_day02.py --part staging
python scripts/run_day02.py --part silver
```

<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><a href="../../COMPLETION.md">Save your cumulative handoff</a></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><a href="../../COMPLETION.md">احفظ التسليم التراكمي</a></td></tr></tbody>
</table>
