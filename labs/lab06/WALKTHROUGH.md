<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 06 · Guided implementation</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 06 · التطبيق المتدرج</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../../README.md">Course home</a> · <a href="../../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../../README.md">الرئيسية</a> · <a href="../../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Read before execution</h2><p><a href="../../day04/QUALITY_POLICY.md">Policy</a> · <a href="../../day04/OBSERVABILITY.md">Monitoring</a> · <a href="../../notebooks/day04/03_quality_gate_gx.ipynb">Native notebook</a>. ENGINE_NOT_EXECUTED.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>اقرأ قبل التنفيذ</h2><p><a href="../../day04/QUALITY_POLICY.md">السياسة</a> · <a href="../../day04/OBSERVABILITY.md">المراقبة</a> · <a href="../../notebooks/day04/03_quality_gate_gx.ipynb">الدفتر الأصلي</a>. ENGINE_NOT_EXECUTED.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>1 · Read actual Silver</h2><p>Check the native Day 3 report and corrected trip table. The reference amount is 1880.60 SAR for 75 trips. Read-only validation must not overwrite that table.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>1 · اقرأ Silver الفعلية</h2><p>تحقق من تقرير اليوم الثالث وجدول الرحلات المصحح. المبلغ المرجعي 1880.60 ريال لعدد 75 رحلة. لا يكتب الفحص فوق هذا الجدول.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>2 · State the suite</h2><p>Review required columns, row count, unique keys, relationships, accepted categories and ranges. The native suite tests these columns in a bounded snapshot collected from Delta.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>2 · حدد مجموعة الفحوص</h2><p>راجع الأعمدة والعدد والمفاتيح والعلاقات والفئات والنطاقات. تفحص المجموعة الأصلية هذه الأعمدة في نسخة محدودة تُقرأ من Delta.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>3 · Validate the trusted snapshot</h2><p>Run GX on the 75-row snapshot. Save Checkpoint JSON and generated local Data Docs. Also run row-policy checks; both must pass.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>3 · افحص النسخة الموثوقة</h2><p>شغّل GX على النسخة ذات 75 صفًا واحفظ JSON نقطة التنفيذ وData Docs المولدة محليًا. شغّل سياسة الصفوف أيضًا؛ يجب نجاح الاثنين.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>4 · Isolate the deliberate bad candidate</h2><p>Project quality_cases.csv using actual Spark types and union it with the trusted data into a new staging Delta table. Never append it to trusted Silver. The candidate contains 82 rows.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>4 · اعزل المرشح المعيب المقصود</h2><p>حوّل quality_cases.csv بأنواع Spark الفعلية واجمعها مع البيانات الموثوقة في جدول Delta مرحلي جديد. لا تضفها إلى Silver الموثوقة. يحتوي المرشح 82 صفًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>5 · Observe failure and quarantine</h2><p>GX must fail. The policy marks seven rows with reasons and writes a quarantine Delta table. Candidate failure is the expected successful test outcome, not permission to suppress the rule.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>5 · راقب الفشل والعزل</h2><p>يجب أن يفشل GX. تحدد السياسة سبعة صفوف وأسبابها وتكتب جدول Delta للعزل. فشل المرشح هنا النتيجة الصحيحة للاختبار، وليس مبررًا لتعطيل القاعدة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>6 · Revalidate separately</h2><p>Construct a new clean candidate from accepted rows. Run a fresh GX validation. Only after pass, write a new approved Delta snapshot and verify its readback matches the original 75 trips.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>6 · أعد التحقق منفصلًا</h2><p>أنشئ مرشحًا منقحًا من الصفوف المقبولة وشغّل تحقق GX جديدًا. بعد النجاح فقط اكتب نسخة Delta معتمدة جديدة وتحقق بقراءتها من تطابق الرحلات الـ75 الأصلية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>7 · Interpret monitoring and governance</h2><p>Reconcile 82=75+7, preserve the fare total and record freshness against the explicit scenario clock. Document lineage and access as design versus implementation, using the same project notes.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>7 · فسر المراقبة والحوكمة</h2><p>سوِّ 82=75+7، واحفظ مجموع الأجور، وسجل الحداثة وفق ساعة السيناريو المعلنة. وثق التتبع والوصول مع فصل التصميم عن التطبيق في ملاحظات المشروع نفسه.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>8 · Handoff without claiming certification</h2><p>Record LAB06_NOTES.md and GOVERNANCE.md, generated Data Docs locations and the approved snapshot pointer. Keep raw/quarantine output out of Git. A local passing test does not certify production or legal compliance.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>8 · سلّم دون ادعاء اعتماد</h2><p>سجل LAB06_NOTES.md وGOVERNANCE.md ومسارات Data Docs ومؤشر النسخة المعتمدة. أبق مخرجات الخام والعزل خارج Git. نجاح اختبار محلي لا يمنح اعتمادًا إنتاجيًا أو نظاميًا.</p></td></tr></tbody>
</table>
