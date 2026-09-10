<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Connect AI and BI consumers</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>ربط مستهلكي الذكاء الاصطناعي وذكاء الأعمال</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Execution record</a> · <a href="README.md">Day 5</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">الجاهزية</a> · <a href="README.md">اليوم الخامس</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>BI: start from the fact</h2><p>Join fact_trips to dim_zone, dim_driver and dim_date using their unique keys. These dimensions filter the measures; raw GPS does not join directly into fare sums. The native notebook executes <a href="sql/bi_zone_summary.sql">the same read-only BI query</a> on the pinned fact version.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>BI: ابدأ بالوقائع</h2><p>اربط fact_trips بأبعاد المنطقة والسائق والتاريخ بمفاتيحها الفريدة. ترشح الأبعاد المقاييس، ولا يربط GPS الخام مباشرة بمجاميع الأجور. ينفذ الدفتر الأصلي <a href="sql/bi_zone_summary.sql">استعلام BI للقراءة فقط</a> على نسخة الوقائع الثابتة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Expected reconciled totals</h2><p>Riyadh: 25 trips and 585.00 SAR; Jeddah: 25 and 625.20 SAR; Dammam: 25 and 670.40 SAR. Total: 75 and 1880.60 SAR. These are synthetic fixture values computed by the reference notebook, not operational transport statistics.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الإجماليات المرجعية المتسقة</h2><p>الرياض: 25 رحلة و585.00 ريال؛ جدة: 25 و625.20 ريال؛ الدمام: 25 و670.40 ريال. المجموع 75 رحلة و1880.60 ريال. هذه قيم اصطناعية محسوبة في الدفتر المرجعي وليست إحصاءات تشغيل للنقل.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Optional desktop BI use</h2><p>The bounded CSV exports can be imported into a compatible BI tool after native success. Define the one-to-many dimension relationships and preserve the data types. The course does not require a paid service or claim a Power BI connector was tested. The required consumer evidence is the native SQL reconciliation and documented star schema.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>استخدام أداة تقارير مكتبية اختياري</h2><p>يمكن استيراد ملفات CSV الصغيرة إلى أداة تقارير متوافقة بعد نجاح التشغيل. عرّف علاقات الواحد إلى متعدد وحافظ على الأنواع. لا تتطلب الدورة خدمة مدفوعة ولا تدعي اختبار موصل Power BI. الدليل المطلوب هو تسوية SQL الفعلية وتوثيق المخطط النجمي.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>AI: define a forecast request</h2><p>The request is one city proxy for the next complete hour after the fixed cutoff. The eligible history contains eight completed trips per city in the preceding 24 hours. Mean durations are 1230.00 seconds for Riyadh, 1350.00 for Jeddah and 1470.00 for Dammam. They are historical features, not predicted demand.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>AI: عرّف طلب التنبؤ</h2><p>الطلب هو مدينة تمثيلية للساعة الكاملة التالية للحظة القطع الثابتة. يتضمن التاريخ المؤهل ثماني رحلات منتهية لكل مدينة خلال 24 ساعة سابقة. متوسط المدد 1230.00 ثانية للرياض و1350.00 لجدة و1470.00 للدمام. هذه خصائص تاريخية لا تنبؤات بالطلب.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What is excluded from model inputs</h2><p>Use only the allowlist in the contract. Future target count, current-trip fare or end time, GPS count and identifiers must not be silently added. A historical average duration is permitted because it concerns already completed and delivered trips, not the target hour.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما المستبعد من مدخلات النموذج؟</h2><p>استخدم قائمة المدخلات المحددة فقط. لا تضف خفية عدد الرحلات المستهدف أو أجرة رحلة حالية أو نهايتها أو عدد GPS أو المعرفات. يجوز استخدام متوسط مدة تاريخي لأنه يخص رحلات انتهت ووصلت بالفعل، لا ساعة التنبؤ.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>No fabricated training results</h2><p>All three future labels are unobserved. There are zero supervised training examples for that horizon, not three examples with a target of zero. The notebook tests that a fabricated zero label is rejected. Model fitting, backtesting, an API, and a live feature store remain optional extensions requiring suitable additional evidence—not mandatory tasks in this project.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>لا نتائج تدريب مختلقة</h2><p>النتائج المستقبلية الثلاث غير مرصودة. لا توجد أمثلة تدريب إشرافي لذلك الأفق، وليس لدينا ثلاثة أمثلة هدفها صفر. يختبر الدفتر رفض الصفر المختلق. يبقى تدريب النموذج والاختبار التاريخي وAPI ومخزن الخصائص الحي امتدادات اختيارية تتطلب أدلة مناسبة إضافية، لا مهام إلزامية في المشروع.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Serving remains a bounded data handoff</h2><p>The actual native lab exports eight small CSV tables and writes their hashes into a serving report. Labels remain separate and NULL stays empty in CSV. Keep the schema contract beside the files so a consumer does not infer missing values as zero or confuse seconds and minutes.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التقديم هنا تسليم بيانات محدود</h2><p>يصدر اللاب الأصلي الفعلي ثمانية جداول CSV صغيرة ويسجل بصماتها في تقرير تقديم. تبقى النتائج المستهدفة منفصلة وNULL فارغة في CSV. احفظ عقد المخطط مع الملفات حتى لا يفسر المستهلك الفراغ صفرًا أو يخلط الثواني بالدقائق.</p></td></tr></tbody>
</table>
