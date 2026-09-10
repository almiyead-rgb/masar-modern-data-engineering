<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 01 · Land and inspect raw feeds</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 01 · استقبال المصادر وفحصها</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../../README.md">Course home</a> · <a href="../../docs/START_HERE.md">Start here</a> · <a href="../../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../../README.md">الرئيسية</a> · <a href="../../docs/START_HERE.md">ابدأ هنا</a> · <a href="../../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Contribution and status</h2><p>Day 1 · LO1, LO8 · <strong>PARTIAL</strong><br><a href="../../notebooks/day01/01_source_inspection.ipynb">Open the executed preparatory notebook</a><br>Delta writes, readback and append replay remain unverified.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الإضافة والحالة</h2><p>اليوم 1 · LO1، LO8 · <strong>PARTIAL</strong><br><a href="../../notebooks/day01/01_source_inspection.ipynb">افتح الدفتر التحضيري المنفذ</a><br>كتابة Delta وقراءتها وإعادة الاستيعاب ما تزال غير متحققة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Concept before code</h2><p><a href="../../day01/CONCEPTS.md">Read the detailed concept guide first</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المفهوم قبل الكود</h2><p><a href="../../day01/CONCEPTS.md">اقرأ دليل المفاهيم المفصل أولًا</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Exact input files</h2><ul><li><a href="../../data/masar-small-v1/trips.csv">trips.csv</a></li><li><a href="../../data/masar-small-v1/drivers.csv">drivers.csv</a></li><li><a href="../../data/masar-small-v1/gps.ndjson">gps.ndjson</a></li></ul><p>Use earlier lab outputs where the task requires Bronze or Silver; these source files do not replace those tables.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ملفات الإدخال المحددة</h2><ul><li><a href="../../data/masar-small-v1/trips.csv">trips.csv</a></li><li><a href="../../data/masar-small-v1/drivers.csv">drivers.csv</a></li><li><a href="../../data/masar-small-v1/gps.ndjson">gps.ndjson</a></li></ul><p>استخدم مخرجات اللابات السابقة عندما تتطلب المهمة Bronze أو Silver؛ ملفات المصدر لا تستبدل هذه الجداول.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Required workflow and checks</h2><ol><li>Read the source manifest and verify file hashes before processing.</li><li>Create real Delta Bronze tables with source and ingestion metadata.</li><li>Replay trips without overwriting history and explain the intended Bronze growth.</li><li>Record at least three quality risks; distinguish observed defects from risks.</li></ol></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الخطوات والفحوص المطلوبة</h2><ol><li>اقرأ سجل البيانات وتحقق من بصمات الملفات قبل المعالجة.</li><li>أنشئ جداول Bronze فعلية بصيغة Delta مع معلومات المصدر والاستيعاب.</li><li>أعد استقبال الرحلات دون مسح التاريخ واشرح النمو المقصود في Bronze.</li><li>وثق ثلاثة مخاطر جودة على الأقل وميّز العيب المرصود من الخطر المحتمل.</li></ol></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Save in the same project</h2><ul><li><code>mini_lakehouse/bronze/</code></li><li><code>LAB01_NOTES.md</code></li></ul><p><a href="../../templates/LAB_NOTES.md">Document the evidence</a> — paths above describe learner deliverables, not a claim that generated tables already exist in this source tree.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>احفظ داخل المشروع نفسه</h2><ul><li><code dir="ltr">mini_lakehouse/bronze/</code></li><li><code dir="ltr">LAB01_NOTES.md</code></li></ul><p><a href="../../templates/LAB_NOTES.md">وثق الأدلة</a> — تصف المسارات أعلاه مخرجات الطالب المطلوبة، ولا تدعي وجود الجداول المولدة مسبقًا في شجرة المصدر.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Stop, diagnose, preserve</h2><p>Keep the full error and the last successful step. Do not replace the engine with an unrelated calculation, delete failing checks, or reset unrelated files. Ask through the course support route with a redacted error and version details.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>توقف وشخّص واحفظ</h2><p>احتفظ بالخطأ وآخر خطوة نجحت. لا تستبدل المحرك بحساب لا يحققه، ولا تحذف الفحوص الفاشلة أو تعيد ضبط ملفات لا تخص التجربة. اطلب الدعم بقناة البرنامج مع خطأ منقح وبيانات النسخة.</p></td></tr></tbody>
</table>


<table dir="ltr" width="100%"><thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead><tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Detailed implementation now available</h2><p><a href="WALKTHROUGH.md">Read the guided lab</a> · <a href="../../notebooks/day01/03_bronze_delta.ipynb">Open the engine notebook draft</a>. The implementation is authored; execution remains unverified. The executed preparatory notebook above is retained.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التطبيق التفصيلي متاح الآن</h2><p><a href="WALKTHROUGH.md">اقرأ الشرح المتدرج للاب</a> · <a href="../../notebooks/day01/03_bronze_delta.ipynb">افتح مسودة دفتر المحرك</a>. الكود مكتوب؛ تشغيله ما يزال غير متحقق. الدفتر التحضيري المنفذ أعلاه محفوظ.</p></td></tr></tbody></table>
