<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 3 · Completion and handoff</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الثالث · الاكتمال والانتقال</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">حالة الجاهزية</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Build status: PARTIAL</h2><p>The business-value reference is executed. Native Spark/Delta notebooks are authored but <strong>ENGINE_NOT_EXECUTED</strong>. They are not approved for live teaching. Required engine evidence is still missing.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حالة البناء: جزئية</h2><p>نُفذ مرجع قيم الأعمال. أما دفترا Spark وDelta فكُتبا وحالتهما <strong>ENGINE_NOT_EXECUTED</strong>؛ لم يُعتمدا للتطبيق المباشر، وما يزال دليل تنفيذ المحرك مطلوبًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Complete within the same Lab 04 notes</h2><ol><li>Record before/after counts, fare totals and the corrected trip.</li><li>Record actual Delta versions and distinguish them from source_revision.</li><li>Save replay, stale-redelivery and conflict results.</li><li>Save real constraint/schema rejection evidence.</li><li>Save copy-only schema, compaction and recovery results.</li><li>Save VACUUM dry-run candidates and the retention setting.</li><li>Confirm trusted Silver and the raw files were not damaged by experiments.</li></ol></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>أكمل ضمن ملاحظات اللاب 04 نفسه</h2><ol><li>سجل الأعداد ومجاميع الأجرة والرحلة المصححة قبل وبعد.</li><li>سجل نسخ Delta الفعلية وميزها عن source_revision.</li><li>احفظ نتائج الإعادة والوصول القديم والتعارض.</li><li>احفظ أدلة رفض القيود والمخطط الحقيقية.</li><li>احفظ نتائج المخطط ودمج الملفات والاستعادة المعزولة.</li><li>احفظ مرشحي معاينة VACUUM وإعداد الاحتفاظ.</li><li>تحقق من عدم إضرار التجارب بـSilver الموثوقة وملفات المصدر.</li></ol></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Expected trusted result</h2><p>75 distinct trips; fare total 1880.60 SAR; SYN_T0001=23.00 SAR with source_revision=2; other trips unchanged. This expectation is derived from the fixed sources. The native readback and history are still required to establish actual completion.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>النتيجة الموثوقة المتوقعة</h2><p>75 رحلة مميزة؛ إجمالي أجرة 1880.60 ريال؛ أجرة SYN_T0001 تساوي 23.00 ومراجعتها 2؛ وبقية الرحلات دون تغيير. يستند هذا التوقع إلى المصادر الثابتة. تظل القراءة والسجل الفعليان من المحرك مطلوبين لإثبات الاكتمال.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Where native evidence is written</h2><p>Within the existing workspace: <code>reports/day03_transactions.json</code> and <code>reports/day03_maintenance_latest.json</code>, plus immutable per-run maintenance reports. Actual Delta artifacts live in the trusted table and new sandbox folders. Record the observed active-file counts and compaction metrics in the project’s existing <code>BENCHMARKS.md</code>, using <a href="../templates/BENCHMARKS.md">the shared benchmark template</a>, without claiming a speed gain. Use the supplied <a href="../templates/LAB_NOTES.md">lab-notes template</a>; do not copy a Python reference report into an engine-evidence slot.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>مكان كتابة الأدلة الأصلية</h2><p>داخل مساحة العمل السابقة: <code>reports/day03_transactions.json</code> و<code>reports/day03_maintenance_latest.json</code>، إضافة إلى تقارير صيانة منفصلة لكل تشغيل. تبقى ملفات Delta الفعلية في الجدول الموثوق ومجلدات العزل الجديدة. سجل أعداد الملفات النشطة ومقاييس دمج الملفات المرصودة في <code>BENCHMARKS.md</code> الموجود للمشروع، باستخدام <a href="../templates/BENCHMARKS.md">نموذج القياسات المشترك</a> دون ادعاء تسارع. استخدم <a href="../templates/LAB_NOTES.md">نموذج ملاحظات اللاب</a>؛ ولا تضع تقرير مرجع Python بدل دليل المحرك.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Continue without an extra project</h2><p>Keep these outputs alongside Labs 01–03. Day 4 uses the corrected trusted table and the fixed event feeds for streaming and quality; it does not use recovery or schema sandboxes as production facts. Optional distinction stays optional.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>استكمل دون مشروع إضافي</h2><p>احتفظ بالمخرجات إلى جانب اللابات 01–03. يستخدم اليوم الرابع الجدول الموثوق المصحح وأحداث المصدر الثابتة للتدفق والجودة؛ ولا يستخدم نسخ الاستعادة أو المخطط كحقائق إنتاجية. يبقى مسار التميز اختياريًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../day04/README.md">Next: Day 4 (planned)</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../day04/README.md">التالي: اليوم الرابع (مخطط)</a></td></tr></tbody>
</table>
