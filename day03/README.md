<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 3 · Reliable Delta tables</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الثالث · جداول Delta الموثوقة</h1></td></tr></tbody>
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
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>One question</h2><p>A fare was corrected after Day 2. Can we apply the right value once, explain what changed, and inspect the old value without damaging trusted data? Day 3 implements LO4 and contributes to LO8.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>سؤال اليوم</h2><p>وصل تصحيح أجرة بعد اليوم الثاني. هل نطبق القيمة الصحيحة دون مضاعفة، ونشرح ما تغير، ونقرأ القيمة السابقة دون الإضرار بالبيانات الموثوقة؟ يحقق اليوم LO4 ويسهم في LO8.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Entry point</h2><p>Use the same MASAR_SMALL_V1 files and the successfully completed Day 2 workspace: 75 Silver trips. No new dataset, cloud account, paid API, or extra project is needed. The reference notebook can run without the engine; native notebooks require the actual earlier Delta outputs.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>نقطة البداية</h2><p>نستخدم ملفات MASAR_SMALL_V1 نفسها ومساحة عمل اليوم الثاني المكتملة فعليًا، وفيها 75 رحلة في Silver. لا بيانات جديدة أو حساب سحابي أو API مدفوع أو مشروع إضافي. يعمل الدفتر المرجعي دون المحرك؛ أما الدفتران الأصليان فيتطلبان مخرجات Delta الفعلية السابقة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Read and run in this order</h2><ul><li><a href="CONCEPTS.md">1. Concepts and examples</a></li><li><a href="CHANGE_POLICY.md">2. Revision and sandbox policy</a></li><li><a href="../labs/lab04/WALKTHROUGH.md">3. Lab 04 walkthrough</a></li><li><a href="../notebooks/day03/01_correction_reference.ipynb">4. Executed expected-value notebook</a></li><li><a href="../notebooks/day03/02_delta_transactions.ipynb">5. Lab 4a: native transactions draft</a></li><li><a href="../notebooks/day03/03_safe_maintenance.ipynb">6. Lab 4b: native maintenance draft</a></li><li><a href="PRACTICE.md">7. Explain the results</a></li><li><a href="COMPLETION.md">8. Carry the same project forward</a></li><li><a href="GLOSSARY.md">Glossary and pronunciation</a></li><li><a href="SOURCES.md">Official technical sources</a></li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>مسار القراءة والتطبيق</h2><ul><li><a href="CONCEPTS.md">1. المفاهيم والأمثلة</a></li><li><a href="CHANGE_POLICY.md">2. سياسة التصحيح والعزل</a></li><li><a href="../labs/lab04/WALKTHROUGH.md">3. خطوات اللاب 04</a></li><li><a href="../notebooks/day03/01_correction_reference.ipynb">4. دفتر التوقعات المنفذ</a></li><li><a href="../notebooks/day03/02_delta_transactions.ipynb">5. مسودة المعاملات الأصلية 4a</a></li><li><a href="../notebooks/day03/03_safe_maintenance.ipynb">6. مسودة الصيانة الأصلية 4b</a></li><li><a href="PRACTICE.md">7. تفسير النتائج</a></li><li><a href="COMPLETION.md">8. الانتقال بالمشروع نفسه</a></li><li><a href="GLOSSARY.md">المصطلحات والنطق</a></li><li><a href="SOURCES.md">المصادر التقنية الرسمية</a></li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Learning sequence within the course day</h2><p>Revisit Silver → distinguish revisions from table versions → calculate the correction → apply Lab 4a → inspect Lab 4b copies → document the evidence. Reading, discussion, breaks and guided practice fit the existing six-hour day; this is not an additional training day.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التسلسل داخل اليوم التدريبي</h2><p>مراجعة Silver ← تمييز مراجعة السجل عن نسخة الجدول ← حساب التصحيح ← تطبيق 4a ← فحص نسخ 4b المعزولة ← توثيق الأدلة. تقع القراءة والمناقشة والاستراحات والتطبيق الموجّه ضمن اليوم ذي الست ساعات؛ لا نضيف يومًا أو تكليفًا جديدًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What moves to Day 4</h2><p>The trusted trip table contains 75 trips with the approved correction. Schema additions, deletion/restore and maintenance trials stay in sandbox copies. Preserve the logs and the Lab 04 notes in this same cumulative project.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما ينتقل إلى اليوم الرابع</h2><p>يتضمن جدول الرحلات الموثوق 75 رحلة مع التصحيح المعتمد. تبقى زيادة الأعمدة وتجارب الحذف والاستعادة والصيانة في النسخ المعزولة. تحفظ السجلات وملاحظات اللاب 04 ضمن المشروع التراكمي نفسه.</p></td></tr></tbody>
</table>
