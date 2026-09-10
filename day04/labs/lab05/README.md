<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h1>Lab 05 · Kafka to Delta with restart evidence</h1></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h1>اللاب 05 · من Kafka إلى Delta مع أدلة الاستئناف</h1></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><p><a href="../../../README.md">Course home</a> · <a href="../../../STATUS.md">Execution record</a></p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><p><a href="../../../README.md">الرئيسية</a> · <a href="../../../STATUS.md">سجل التنفيذ</a></p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Contribution and status</h2><p>Lab 05 · Receive the fixed event stream and test checkpoint recovery, replay and late arrival.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>الإضافة والحالة</h2><p>اللاب 05 · استقبل الأحداث الثابتة واختبر الاستئناف والإعادة والوصول المتأخر.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Start here</h2><ul><li><a href="../../CONCEPTS.md">Concepts</a></li><li><a href="WALKTHROUGH.md">Guided steps</a></li><li><a href="../../REFERENCE.ipynb">Executed source reference</a></li><li><a href="../../STUDENT.ipynb">Native notebook draft</a></li></ul></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>ابدأ هنا</h2><ul><li><a href="../../CONCEPTS.md">المفاهيم</a></li><li><a href="WALKTHROUGH.md">الخطوات الموجهة</a></li><li><a href="../../REFERENCE.ipynb">مرجع المصدر المنفذ</a></li><li><a href="../../STUDENT.ipynb">دفتر التنفيذ الأصلي غير المعتمد</a></li></ul></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Precondition</h2><p>Use actual Day 3 corrected Silver and the pinned local environment. Do not regenerate a fake Silver table from the reference notebook to bypass an incomplete prior lab.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>المتطلب السابق</h2><p>استخدم جدول Silver الفعلي المصحح في اليوم الثالث والبيئة المحلية المثبتة. لا تولّد جدول Silver وهميًا من الدفتر المرجعي لتجاوز لاب سابق غير مكتمل.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Stop without damage</h2><p>Preserve the failed report and last trusted state. Do not delete checkpoints, source data or passing history. Native prerequisites and exact limitations are documented in <a href="../../SETUP.md">Day 4 setup</a>.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>التوقف دون إتلاف</h2><p>احفظ تقرير الفشل وآخر حالة موثوقة. لا تحذف نقاط التحقق أو بيانات المصدر أو تاريخ النجاح. توثق المتطلبات والحدود في <a href="../../SETUP.md">إعداد اليوم الرابع</a>.</p></td></tr></tbody>
</table>
