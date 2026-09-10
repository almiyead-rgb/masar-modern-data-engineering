<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 05 · Guided implementation</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 05 · التطبيق المتدرج</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../../README.md">Course home</a> · <a href="../../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../../README.md">الرئيسية</a> · <a href="../../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Read before execution</h2><p><a href="../../day04/SETUP.md">Environment</a> · <a href="../../day04/STREAM_CONTRACT.md">Contract</a> · <a href="../../notebooks/day04/02_kafka_delta_streaming.ipynb">Native notebook</a>. Runtime status remains ENGINE_NOT_EXECUTED.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>اقرأ قبل التنفيذ</h2><p><a href="../../day04/SETUP.md">البيئة</a> · <a href="../../day04/STREAM_CONTRACT.md">العقد</a> · <a href="../../notebooks/day04/02_kafka_delta_streaming.ipynb">الدفتر الأصلي</a>. الحالة ENGINE_NOT_EXECUTED.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>1 · Confirm inputs</h2><p>Open the executed reference. Identify 216 base messages, two repeated events and one late new event. Confirm the source manifest; do not change it.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>1 · تحقق من المدخلات</h2><p>افتح المرجع المنفذ وحدد 216 رسالة أساسية وحدثين مكررين وحدثًا جديدًا متأخرًا. تحقق من سجل بصمات المصدر ولا تغيره.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>2 · Start the local broker</h2><p>Provision the pinned packages and the official broker image before class. Use the SETUP commands. A successful TCP connection is only a preflight check, not a successful Kafka exchange.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>2 · جهز الوسيط المحلي</h2><p>جهز الحزم المثبتة وصورة الوسيط الرسمية قبل التدريب باستخدام تعليمات الإعداد. اتصال TCP الناجح فحص أولي فقط، وليس تبادل Kafka ناجحًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>3 · Open the cumulative workspace</h2><p>The native notebook locates the successful Bronze workspace and reads the Day 3 report and Delta Silver contents. It refuses missing or changed predecessor outputs.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>3 · افتح مساحة المشروع التراكمي</h2><p>يحدد الدفتر مساحة Bronze الناجحة ثم يقرأ تقرير اليوم الثالث وبيانات Delta Silver. يرفض المخرجات السابقة المفقودة أو المتغيرة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>4 · Publish the base batch</h2><p>Create a unique two-partition topic. Record publish intent before sending. Send each original JSON line keyed by trip_id and save acknowledgments with actual offsets.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>4 · أرسل دفعة الأساس</h2><p>أنشئ موضوعًا فريدًا بقسمين، وسجل نية الإرسال قبل التنفيذ. أرسل أسطر JSON الأصلية بمفتاح trip_id واحفظ التأكيدات بإزاحاتها الفعلية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>5 · Ingest with a persistent checkpoint</h2><p>Read the Kafka source and write raw_json plus transport metadata to a new Delta Bronze path. availableNow finishes after consuming available data. Save recentProgress and Delta artifacts.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>5 · استوعب بنقطة تحقق مستديمة</h2><p>اقرأ مصدر Kafka واكتب raw_json وبيانات النقل إلى مسار Delta Bronze جديد. ينتهي availableNow بعد البيانات المتاحة. احفظ recentProgress وأدلة Delta.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>6 · Resume without sending</h2><p>Start the same query with the same checkpoint and destination. Expect 216 rows, the same query_id and a different query_run_id. Do not edit starting offsets or create a new checkpoint for this test.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>6 · استأنف دون إرسال</h2><p>أعد الاستعلام بنقطة التحقق والوجهة نفسيهما. توقع 216 صفًا وهوية query_id ثابتة وهوية query_run_id جديدة. لا تغير الإزاحات ولا تنشئ نقطة جديدة لهذا الاختبار.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>7 · Send replay then late input</h2><p>Publish replay: transport count 218, distinct events 216. Publish late: transport count 219, distinct events 217. Compare full payloads before deduplicating by event_id; conflicting duplicates fail.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>7 · أرسل الإعادة ثم المتأخر</h2><p>أرسل الإعادة: 218 رسالة نقل و216 حدثًا مختلفًا. أرسل المتأخر: 219 رسالة و217 حدثًا. قارن المحتوى كاملًا قبل إزالة التكرار بمعرف الحدث؛ يُرفض التعارض.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>8 · Save usable evidence</h2><p>Save LAB05_NOTES.md, producer receipts, all four phase reports, checkpoint location and approved event-table path. Explain why a clean resume test does not establish broker failover or watermark semantics.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>8 · احفظ أدلة قابلة للاستخدام</h2><p>احفظ LAB05_NOTES.md وتأكيدات المنتج وتقارير المراحل الأربع ومسار نقطة التحقق وجدول الأحداث. اشرح لماذا لا يثبت اختبار الاستئناف السليم تجاوز أعطال الوسيط أو دلالات العلامة المائية.</p></td></tr></tbody>
</table>
