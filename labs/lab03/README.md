<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 03 · Staging and incremental Silver</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 03 · التهيئة وSilver التزايدية</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../../README.md">Course home</a> · <a href="../../STATUS.md">Readiness</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../../README.md">الرئيسية</a> · <a href="../../STATUS.md">حالة الجاهزية</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>One cumulative lab</h2><p>Day 2 · LO3 and LO8 · Parts 3a and 3b. <strong>PARTIAL / ENGINE_NOT_EXECUTED.</strong> No new project, dataset, payment account or API key. The native implementation uses the Day 1 Delta output.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>لاب تراكمي واحد</h2><p>اليوم الثاني · LO3 وLO8 · الجزآن 3a و3b. <strong>PARTIAL / ENGINE_NOT_EXECUTED.</strong> لا مشروع أو بيانات جديدة، ولا حساب مدفوع أو مفتاح API. يستخدم التطبيق الأصلي مخرجات Delta لليوم الأول.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><ul><li><a href="../../day02/CONCEPTS.md">Read the concepts</a></li><li><a href="WALKTHROUGH.md">Follow the walkthrough</a></li><li><a href="../../day02/DBT_GUIDE.md">Model design with dbt</a></li><li><a href="../../notebooks/day02/01_silver_reference.ipynb">Executed independent reference</a></li><li><a href="../../notebooks/day02/02_staging_delta.ipynb">Native Lab 3a</a></li><li><a href="../../notebooks/day02/03_incremental_silver.ipynb">Native Lab 3b</a></li><li><a href="../../day02/COMPLETION.md">Completion and handoff</a></li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><ul><li><a href="../../day02/CONCEPTS.md">المفاهيم</a></li><li><a href="WALKTHROUGH.md">الشرح المتدرج</a></li><li><a href="../../day02/DBT_GUIDE.md">تصميم dbt</a></li><li><a href="../../notebooks/day02/01_silver_reference.ipynb">المرجع المستقل المنفذ</a></li><li><a href="../../notebooks/day02/02_staging_delta.ipynb">اللاب 3a الأصلي</a></li><li><a href="../../notebooks/day02/03_incremental_silver.ipynb">اللاب 3b الأصلي</a></li><li><a href="../../day02/COMPLETION.md">الاكتمال والانتقال</a></li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Inputs and outputs</h2><p>Reuse the successful <code>mini_lakehouse/bronze/</code> workspace. The only new business arrivals today come from the fixed <a href="../../data/masar-small-v1/late_trips.csv">late_trips.csv</a>. Save staging snapshots, <code>mini_lakehouse/silver/trips/</code>, actual scenario evidence and LAB03_NOTES.md. These are output paths, not pre-existing tables in the source archive.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المدخلات والمخرجات</h2><p>أعد استخدام مساحة <code>mini_lakehouse/bronze/</code> الناجحة. تصل الرحلات الجديدة لليوم من ملف <a href="../../data/masar-small-v1/late_trips.csv">late_trips.csv</a> الثابت فقط. احفظ لقطات التهيئة و<code>mini_lakehouse/silver/trips/</code> وأدلة السيناريوهات الفعلية وLAB03_NOTES.md. هذه مسارات مخرجات وليست جداول موجودة مسبقًا في أرشيف المصدر.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Completion checks</h2><p>Typed staging; preserved Bronze; unique driver keys; no missing driver references; conflict detection before deduplication; 72 base trips and 75 after late arrival; equal business digests on retries; actual Delta artifacts. The dbt demonstration still requires adapter configuration and real execution before that part is marked complete.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>فحوص الاكتمال</h2><p>تهيئة موحدة الأنواع، وBronze محفوظة، ومفاتيح سائقين فريدة، وعدم وجود علاقات مفقودة، وكشف التعارض قبل إزالة التكرار، و72 رحلة أساسية و75 بعد الوصول المتأخر، وبصمات محتوى ثابتة عند الإعادة، وأدلة Delta فعلية. ما يزال عرض dbt يحتاج إعداد الموصل وتنفيذًا حقيقيًا قبل اعتبار جزئه مكتملًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../../day02/DATA_CONTRACT.md">Silver field contract</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../../day02/DATA_CONTRACT.md">عقد حقول Silver</a></td></tr></tbody>
</table>
