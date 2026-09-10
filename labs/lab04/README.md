<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 04 · Delta operations: 4a + 4b</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 04 · عمليات Delta: ‏4a و4b</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../../README.md">Course home</a> · <a href="../../STATUS.md">Readiness</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../../README.md">الرئيسية</a> · <a href="../../STATUS.md">حالة الجاهزية</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Build status: PARTIAL</h2><p>The business-value reference is executed. Native Spark/Delta notebooks are authored but <strong>ENGINE_NOT_EXECUTED</strong>. They are not approved for live teaching. Required engine evidence is still missing.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حالة البناء: جزئية</h2><p>نُفذ مرجع قيم الأعمال. أما دفترا Spark وDelta فكُتبا وحالتهما <strong>ENGINE_NOT_EXECUTED</strong>؛ لم يُعتمدا للتطبيق المباشر، وما يزال دليل تنفيذ المحرك مطلوبًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>One lab, two sections</h2><p>4a corrects the trusted trip table and validates its past/current contents. 4b tests schema evolution, deletion/recovery and maintenance on new copies. Both are Lab 04 in the same eight-lab final project; the reference notebook is a support tool, not an extra lab.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>لاب واحد بجزأين</h2><p>تصحح 4a جدول الرحلات الموثوق وتفحص محتوياته الحالية والسابقة. وتختبر 4b تطور المخطط والحذف والاستعادة والصيانة على نسخ جديدة. كلاهما اللاب 04 ضمن المشروع النهائي ذي اللابات الثمانية؛ والدفتر المرجعي أداة مساندة لا لاب إضافي.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Material</h2><ul><li><a href="../../day03/CONCEPTS.md">Concepts</a></li><li><a href="../../day03/CHANGE_POLICY.md">Change policy</a></li><li><a href="WALKTHROUGH.md">Step-by-step lab</a></li><li><a href="../../notebooks/day03/01_correction_reference.ipynb">Executed source-derived expectations</a></li><li><a href="../../notebooks/day03/02_delta_transactions.ipynb">4a native notebook draft</a></li><li><a href="../../notebooks/day03/03_safe_maintenance.ipynb">4b native notebook draft</a></li><li><a href="../../day03/COMPLETION.md">Completion evidence</a></li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المواد</h2><ul><li><a href="../../day03/CONCEPTS.md">المفاهيم</a></li><li><a href="../../day03/CHANGE_POLICY.md">سياسة التغيير</a></li><li><a href="WALKTHROUGH.md">الخطوات التفصيلية</a></li><li><a href="../../notebooks/day03/01_correction_reference.ipynb">توقعات المصدر المنفذة</a></li><li><a href="../../notebooks/day03/02_delta_transactions.ipynb">مسودة دفتر 4a الأصلي</a></li><li><a href="../../notebooks/day03/03_safe_maintenance.ipynb">مسودة دفتر 4b الأصلي</a></li><li><a href="../../day03/COMPLETION.md">أدلة الاكتمال</a></li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Inputs</h2><p>Use actual Day 2 Silver with 75 trips, plus <a href="../../data/masar-small-v1/correction.csv">correction.csv</a>, <a href="../../data/masar-small-v1/schema_change.csv">schema_change.csv</a> and <a href="../../data/masar-small-v1/quality_cases.csv">quality_cases.csv</a>. Native code also reads the existing Bronze driver data.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المدخلات</h2><p>استخدم Silver الفعلية من اليوم الثاني وفيها 75 رحلة، مع <a href="../../data/masar-small-v1/correction.csv">correction.csv</a> و<a href="../../data/masar-small-v1/schema_change.csv">schema_change.csv</a> و<a href="../../data/masar-small-v1/quality_cases.csv">quality_cases.csv</a>. يقرأ الكود الأصلي أيضًا بيانات السائقين الموجودة في Bronze.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Expected completion</h2><p>Correction and replay preserve 75 unique trips; old versions show the previous value; a mixed invalid batch does not partially commit; schema changes are explicit; all destructive exercises are isolated; maintenance preserves business values. Actual engine outputs must be saved before claiming completion.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الاكتمال المتوقع</h2><p>يحافظ التصحيح والإعادة على 75 رحلة فريدة؛ تعرض النسخة القديمة القيمة السابقة؛ لا تعتمد الدفعة المختلطة المعيبة جزئيًا؛ يكون تغيير المخطط صريحًا؛ تعزل تجارب الحذف؛ وتحافظ الصيانة على قيم الأعمال. يجب حفظ نتائج المحرك الفعلية قبل إعلان الاكتمال.</p></td></tr></tbody>
</table>
