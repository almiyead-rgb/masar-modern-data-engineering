<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 4 · Quality and promotion policy</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الرابع · سياسة الجودة والترقية</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Execution record</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">سجل التنفيذ</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>The decision precedes the tool</h2><p>Policy MASAR_QUALITY_V1 is a strict whole-candidate gate. Candidate failure keeps the last trusted output unchanged. Quarantine is an explicit application action; Great Expectations does not automatically move or repair rows.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>القرار قبل الأداة</h2><p>السياسة MASAR_QUALITY_V1 ترفض المرشح كاملًا عند فشله، وتحافظ على آخر مخرج موثوق دون تغيير. العزل إجراء ينفذه كود التطبيق صراحة؛ Great Expectations لا ينقل الصفوف أو يصلحها تلقائيًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What is validated</h2><p>Validate the actual corrected Silver snapshot: BUSINESS_FIELDS from Day 2, one row per trip, 75 rows in this fixture. Check required fields, unique trip IDs, known drivers, supported cities, valid times, positive duration and distance, non-negative fare, driver attributes and positive source revision. Schema or volume failure can block a batch even when individual rows look good.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما الذي نفحصه؟</h2><p>افحص نسخة Silver المصححة الفعلية: حقول BUSINESS_FIELDS المحددة في اليوم الثاني، وصف لكل رحلة، و75 صفًا لهذه العينة. افحص الحقول المطلوبة والمفاتيح الفريدة والسائقين والمدن والتوقيتات والمدة والمسافة والأجرة وخصائص السائق ومراجعة المصدر. قد يمنع خطأ الحجم أو المخطط دفعةً تبدو صفوفها سليمة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Seven deliberate root defects</h2><ul><li>MISSING_TRIP_ID: key absent.</li><li>INVALID_FARE: negative fare.</li><li>UNKNOWN_DRIVER: missing dimension relationship.</li><li>INVALID_TIMESTAMP: unparseable start time.</li><li>INVALID_DURATION: end before start.</li><li>INVALID_DISTANCE: zero distance.</li><li>INVALID_CITY: unsupported city.</li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>سبعة عيوب جذرية مقصودة</h2><ul><li>MISSING_TRIP_ID: مفتاح الرحلة مفقود.</li><li>INVALID_FARE: أجرة سالبة.</li><li>UNKNOWN_DRIVER: علاقة سائق غير موجودة.</li><li>INVALID_TIMESTAMP: وقت بداية لا يقبل التحويل.</li><li>INVALID_DURATION: نهاية تسبق البداية.</li><li>INVALID_DISTANCE: مسافة صفرية.</li><li>INVALID_CITY: مدينة خارج النطاق.</li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Three separately recorded validations</h2><p>1. Trusted 75-row snapshot must pass. 2. Mixed 82-row candidate must fail and isolate seven rows. 3. The 75-row clean subset must pass a new validation and Delta readback before a new approved-output pointer is written. The original Silver table is never overwritten.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ثلاث عمليات تحقق مستقلة في السجل</h2><p>1. تنجح النسخة الموثوقة من 75 صفًا. 2. تفشل الدفعة المختلطة من 82 صفًا ويُعزل سبعة. 3. تجتاز المجموعة المنقحة من 75 صفًا تحققًا جديدًا وقراءة Delta قبل إنشاء مؤشر اعتماد جديد. لا يُكتب فوق جدول Silver الأصلي.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>The GX implementation boundary</h2><p>The native wrapper reads real Delta data, then collects a bounded snapshot of at most 500 rows for GX Pandas validation. GX suites test actual columns, not fabricated success flags. Additional policy checks calculate quarantine reasons. The bounded design teaches quality control; it is not a distributed validation benchmark. <a href="SOURCES.md">S6–S9</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حدود تنفيذ GX</h2><p>تقرأ طبقة التنفيذ بيانات Delta الحقيقية ثم تجمع نسخة محدودة بحد أقصى 500 صف لفحص GX باستخدام Pandas. تفحص مجموعة GX الأعمدة الفعلية لا أعلام نجاح مصطنعة، وتحسب السياسة أسباب العزل. هذا التصميم المحدود يعلم ضبط الجودة ولا يقيس فحصًا موزعًا. <a href="SOURCES.md">S6–S9</a>.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>No silent relaxation</h2><p>Do not suppress a failed Expectation, replace null with a made-up driver, remove volume checks or promote the accepted subset under the failed validation. Duplicate keys are quarantined on every occurrence; same-key conflict resolution belongs to a documented upstream policy.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>لا تخفيف صامت للفحوص</h2><p>لا تحذف توقعًا فاشلًا، ولا تستبدل القيمة المفقودة بسائق مختلق، ولا تلغ فحص الحجم، ولا ترقِّ المجموعة المقبولة اعتمادًا على نتيجة فاشلة. تُعزل جميع تكرارات المفتاح، وتسوية تعارضاته تتطلب سياسة موثقة سابقة.</p></td></tr></tbody>
</table>
