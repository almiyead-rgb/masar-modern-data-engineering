<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 4 · Observability and incident reasoning</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الرابع · المراقبة وتفسير التعثر</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Four different observations</h2><p>Volume: counts at a stated grain. Freshness: age of a stated timestamp. Schema: expected fields/types. Distribution: city shares relative to a named baseline. They answer different questions; a healthy process can still emit bad data.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>أربع ملاحظات مختلفة</h2><p>الحجم: عدد عند مستوى صف محدد. الحداثة: عمر توقيت محدد. المخطط: الحقول والأنواع المتوقعة. التوزيع: حصص المدن مقارنة بخط أساس مسمى. لكل منها سؤال مختلف؛ قد تعمل العملية تقنيًا وتنتج بيانات معيبة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Use the scenario clock for historical fixtures</h2><p>Scenario as-of: 2026-06-04T03:04:00Z, not today. Latest event: 2026-06-03T17:45:00Z; age 33540 seconds (9h 19m), within the example 12-hour source threshold. Delivery at 03:00:00Z is 240 seconds old, within the example 300-second delivery threshold. The thresholds are teaching assumptions.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>استخدم ساعة السيناريو للبيانات التاريخية</h2><p>وقت التقييم: 2026-06-04T03:04:00Z، وليس اليوم. أحدث حدث عند 2026-06-03T17:45:00Z؛ عمره 33540 ثانية، أي 9 ساعات و19 دقيقة، ضمن مثال حداثة المصدر البالغ 12 ساعة. عمر التسليم عند 03:00:00Z يساوي 240 ثانية، ضمن مثال حد 300 ثانية. العتبات افتراضات تعليمية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Fresh data can describe an old event</h2><p>Do not confuse arrival freshness with event freshness. A negative age means a future timestamp or clock inconsistency, not excellent freshness. For actual operational latency use real broker/ingestion times from the native run, clearly separated from the historical scenario clock.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>قد تصل بيانات حديثًا عن حدث قديم</h2><p>لا تخلط حداثة الوصول بحداثة الحدث. العمر السالب يدل على توقيت مستقبلي أو عدم اتساق الساعة، لا حداثة ممتازة. لقياس تأخر التشغيل استخدم توقيتات الوسيط والاستيعاب الحقيقية، منفصلة عن ساعة السيناريو التاريخية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Distribution is a warning here</h2><p>Total variation distance = half the sum of absolute differences in city shares. The accepted 75-row set against Day 3 has distance 0. The example warning threshold is 0.10. This is a deterministic classroom diagnostic, not a significance test and not evidence about Saudi travel patterns.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التوزيع هنا مؤشر تنبيه</h2><p>مسافة التباين الكلي = نصف مجموع الفروق المطلقة بين حصص المدن. المسافة بين الصفوف المقبولة الـ75 وخط أساس اليوم الثالث تساوي صفرًا. عتبة التنبيه المثال 0.10. هذا فحص تعليمي حتمي، لا اختبار دلالة إحصائية أو دليل عن أنماط التنقل السعودية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Record a useful incident</h2><ul><li>Identify the run, source and last successful phase.</li><li>State observed/expected counts and the failed rule.</li><li>Preserve checkpoint and last trusted version.</li><li>Explain whether the blocker is environment, delivery, data or policy.</li><li>Revalidate after a documented fix; do not edit the failed evidence.</li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>سجل تعثرًا قابلًا للمعالجة</h2><ul><li>حدد التشغيل والمصدر وآخر مرحلة ناجحة.</li><li>سجل العدد المرصود والمتوقع والقاعدة الفاشلة.</li><li>احفظ نقطة التحقق وآخر نسخة موثوقة.</li><li>حدد هل السبب البيئة أو النقل أو البيانات أو السياسة.</li><li>أعد التحقق بعد معالجة موثقة ولا تعدّل دليل الفشل.</li></ul></td></tr></tbody>
</table>
