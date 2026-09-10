<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 06 · GX quality gate, quarantine and revalidation</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 06 · بوابة GX والعزل وإعادة التحقق</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../../README.md">Course home</a> · <a href="../../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../../README.md">الرئيسية</a> · <a href="../../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Contribution and status</h2><p>LO6 + LO8. PARTIAL: native implementation and walkthrough are authored; ENGINE_NOT_EXECUTED. This is part of the same cumulative final project.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الإضافة والحالة</h2><p>LO6 وLO8. الحالة PARTIAL: كود التنفيذ الأصلي والشرح مكتوبان، وحالة التشغيل ENGINE_NOT_EXECUTED. اللاب جزء من المشروع النهائي التراكمي نفسه.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Start here</h2><ul><li><a href="../../day04/CONCEPTS.md">Concepts</a></li><li><a href="WALKTHROUGH.md">Guided steps</a></li><li><a href="../../notebooks/day04/01_stream_quality_reference.ipynb">Executed source reference</a></li><li><a href="../../notebooks/day04/03_quality_gate_gx.ipynb">Native notebook draft</a></li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ابدأ هنا</h2><ul><li><a href="../../day04/CONCEPTS.md">المفاهيم</a></li><li><a href="WALKTHROUGH.md">الخطوات الموجهة</a></li><li><a href="../../notebooks/day04/01_stream_quality_reference.ipynb">مرجع المصدر المنفذ</a></li><li><a href="../../notebooks/day04/03_quality_gate_gx.ipynb">دفتر التنفيذ الأصلي غير المعتمد</a></li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Precondition</h2><p>Use actual Day 3 corrected Silver and the pinned local environment. Do not regenerate a fake Silver table from the reference notebook to bypass an incomplete prior lab.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المتطلب السابق</h2><p>استخدم جدول Silver الفعلي المصحح في اليوم الثالث والبيئة المحلية المثبتة. لا تولّد جدول Silver وهميًا من الدفتر المرجعي لتجاوز لاب سابق غير مكتمل.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Stop without damage</h2><p>Preserve the failed report and last trusted state. Do not delete checkpoints, source data or passing history. Native prerequisites and exact limitations are documented in <a href="../../day04/SETUP.md">Day 4 setup</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التوقف دون إتلاف</h2><p>احفظ تقرير الفشل وآخر حالة موثوقة. لا تحذف نقاط التحقق أو بيانات المصدر أو تاريخ النجاح. توثق المتطلبات والحدود في <a href="../../day04/SETUP.md">إعداد اليوم الرابع</a>.</p></td></tr></tbody>
</table>
