<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 2 · Completion and Day 3 handoff</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الثاني · الاكتمال وتسليم اليوم الثالث</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">حالة الجاهزية</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Definition of completion</h2><p>Read the concepts, complete Lab 3a and 3b, inspect real native outputs, document the dbt model mapping and retain evidence. The current authored build is not yet a completed teaching release because native execution and the dbt demo remain unverified.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تعريف الاكتمال</h2><p>اقرأ المفاهيم، وأكمل 3a و3b، وافحص المخرجات الأصلية الفعلية، ووثق خريطة نماذج dbt واحفظ الأدلة. البناء المكتوب الحالي ليس إصدارًا تدريسيًا مكتملًا لأن التنفيذ الأصلي وعرض dbt لم يتحققا بعد.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What to preserve</h2><p>Keep the successful workspace; three typed staging snapshots; Silver trips; reports/day02_silver.json; the readback reconciliation; notebook outputs; and LAB03_NOTES.md. Git stores code and bounded evidence, not all generated data folders. Do not force-add outputs/ or create a second project. Use <a href="../project/SUBMISSION.md">the existing submission rules</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما الذي تحفظه؟</h2><p>احتفظ بمساحة التشغيل الناجحة ولقطات التهيئة الثلاث وSilver وتقرير reports/day02_silver.json وتسوية القراءة ومخرجات الدفاتر وLAB03_NOTES.md. يحفظ Git الكود والأدلة المحدودة، وليس جميع مجلدات البيانات المولدة. لا تضف outputs/ بالقوة ولا تنشئ مشروعًا ثانيًا. اتبع <a href="../project/SUBMISSION.md">تعليمات التسليم السابقة</a>.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What Day 3 receives</h2><p>A real Delta table with 75 valid unique trip keys, a traceable source/revision contract and replay evidence. The existing correction.csv is not ingested today. Day 3 adds revision-aware updates, schema controls and version inspection to this same table. Do not restart the business dataset.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما الذي يستلمه اليوم الثالث؟</h2><p>جدول Delta فعلي يحتوي على 75 مفتاح رحلة صالحًا وفريدًا، وعقد مصدر ومراجعة قابل للتتبع، وأدلة إعادة التشغيل. لا نستقبل correction.csv اليوم. يضيف اليوم الثالث التحديث المعتمد على المراجعة وضبط المخطط وفحص النسخ إلى الجدول نفسه. لا تبدأ بيانات الأعمال من جديد.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>When a check fails</h2><p>Preserve the actual error, runtime versions, last successful step and workspace identity. A failed native check is not replaced by the reference notebook. No Spark, dbt, Kafka or GX execution is claimed by a standard-library success.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>عند فشل فحص</h2><p>احفظ الخطأ الفعلي وإصدارات البيئة وآخر خطوة ناجحة وهوية مساحة العمل. لا يستبدل فشل الفحص الأصلي بالدفتر المرجعي. نجاح المكتبة القياسية لا يثبت تشغيل Spark أو dbt أو Kafka أو GX.</p></td></tr></tbody>
</table>
