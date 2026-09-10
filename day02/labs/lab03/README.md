<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h1>Lab 03 · Staging and incremental Silver</h1></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h1>اللاب 03 · التهيئة وSilver التزايدية</h1></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><a href="../../../README.md">Course home</a> · <a href="../../../STATUS.md">Execution record</a></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><a href="../../../README.md">الرئيسية</a> · <a href="../../../STATUS.md">سجل التنفيذ</a></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>One cumulative lab</h2><p>Day 2 · LO3 and LO8 · Parts 3a and 3b. Use the actual Day 1 Delta output to build typed staging and incremental Silver. The dbt models apply the same transformation rules.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>لاب تراكمي واحد</h2><p>اليوم الثاني · LO3 وLO8 · الجزآن 3a و3b. استخدم مخرجات Delta الفعلية من اليوم الأول لبناء البيانات المهيأة وSilver تدريجيًا. تطبق نماذج dbt قواعد التحويل نفسها.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><ul><li><a href="../../CONCEPTS.md">Read the concepts</a></li><li><a href="WALKTHROUGH.md">Follow the walkthrough</a></li><li><a href="../../DBT_GUIDE.md">Model design with dbt</a></li><li><a href="../../REFERENCE.ipynb">Executed independent reference</a></li><li><a href="../../STUDENT.ipynb">Native Lab 3a</a></li><li><a href="../../STUDENT.ipynb">Native Lab 3b</a></li><li><a href="../../COMPLETION.md">Completion and handoff</a></li></ul></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><ul><li><a href="../../CONCEPTS.md">المفاهيم</a></li><li><a href="WALKTHROUGH.md">الشرح المتدرج</a></li><li><a href="../../DBT_GUIDE.md">تصميم dbt</a></li><li><a href="../../REFERENCE.ipynb">المرجع المستقل المنفذ</a></li><li><a href="../../STUDENT.ipynb">اللاب 3a الأصلي</a></li><li><a href="../../STUDENT.ipynb">اللاب 3b الأصلي</a></li><li><a href="../../COMPLETION.md">الاكتمال والانتقال</a></li></ul></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Inputs and outputs</h2><p>Reuse the successful <code>mini_lakehouse/bronze/</code> workspace. The only new business arrivals today come from the fixed <a href="../../../data/masar-small-v1/late_trips.csv">late_trips.csv</a>. Save staging snapshots, <code>mini_lakehouse/silver/trips/</code>, actual scenario evidence and LAB03_NOTES.md. These are output paths, not pre-existing tables in the source archive.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>المدخلات والمخرجات</h2><p>أعد استخدام مساحة <code>mini_lakehouse/bronze/</code> الناجحة. تصل الرحلات الجديدة لليوم من ملف <a href="../../../data/masar-small-v1/late_trips.csv">late_trips.csv</a> الثابت فقط. احفظ لقطات التهيئة و<code>mini_lakehouse/silver/trips/</code> وأدلة السيناريوهات الفعلية وLAB03_NOTES.md. هذه مسارات مخرجات وليست جداول موجودة مسبقًا في أرشيف المصدر.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Completion checks</h2><p>Typed staging; preserved Bronze; unique driver keys; no missing driver references; conflict detection before deduplication; 72 base trips and 75 after late arrival; equal business digests on retries; actual Delta artifacts. The dbt demonstration still requires adapter configuration and real execution before that part is marked complete.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>فحوص الاكتمال</h2><p>تهيئة موحدة الأنواع، وBronze محفوظة، ومفاتيح سائقين فريدة، وعدم وجود علاقات مفقودة، وكشف التعارض قبل إزالة التكرار، و72 رحلة أساسية و75 بعد الوصول المتأخر، وبصمات محتوى ثابتة عند الإعادة، وأدلة Delta فعلية. ما يزال عرض dbt يحتاج إعداد الموصل وتنفيذًا حقيقيًا قبل اعتبار جزئه مكتملًا.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><a href="../../DATA_CONTRACT.md">Silver field contract</a></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><a href="../../DATA_CONTRACT.md">عقد حقول Silver</a></td></tr></tbody>
</table>
