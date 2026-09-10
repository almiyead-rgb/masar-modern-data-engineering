<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 2 · ELT and trustworthy Silver</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الثاني · ELT وطبقة Silver الموثوقة</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">حالة الجاهزية</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Today’s question</h2><p>How can 144 received trip records represent only 72 trips, and how do three late trips enter without doubling the output? We build on Day 1, not on a new project.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>سؤال اليوم</h2><p>كيف تمثل 144 نسخة مستقبلة 72 رحلة فقط؟ وكيف ندخل ثلاث رحلات متأخرة دون مضاعفة الناتج؟ نكمل عمل اليوم الأول، ولا نبدأ مشروعًا جديدًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What you will be able to explain and build</h2><p>Distinguish ETL from ELT; design staging models; convert types safely; join a unique driver dimension; preserve one row per trip; explain incremental loading, retry, redelivery and backfill. Main outcome: LO3, with a contribution to LO8.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما الذي ستفهمه وتبنيه؟</h2><p>التمييز بين ETL وELT، وتصميم نماذج التهيئة، وتحويل الأنواع بأمان، والربط بجدول سائقين ذي مفاتيح فريدة، والحفاظ على صف لكل رحلة، وشرح التحميل التزايدي وإعادة المحاولة وإعادة الإرسال والاستكمال التاريخي. الهدف الرئيس LO3 مع إسهام في LO8.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Prerequisites and status</h2><p>Read the Day 1 concepts and retain the complete repository. The native notebooks require a successful Day 1 Bronze workspace. <strong>PARTIAL:</strong> detailed content and native code are authored; the reference notebook is executed, but Spark/Delta and the dbt demonstration are not verified.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المتطلبات والحالة</h2><p>اقرأ مفاهيم اليوم الأول واحتفظ بنسخة المستودع كاملة. يتطلب دفترا المحرك مساحة Bronze ناجحة من اليوم الأول. <strong>PARTIAL:</strong> المحتوى التفصيلي والكود الأصلي مكتوبان والدفتر المرجعي منفذ، لكن تشغيل Spark وDelta وعرض dbt غير متحقق.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Learning route</h2><ul><li><a href="CONCEPTS.md">1. Concepts and examples</a></li><li><a href="DBT_GUIDE.md">2. Model design with dbt</a></li><li><a href="../notebooks/day02/01_silver_reference.ipynb">3. Executed reference — expected values, not Delta</a></li><li><a href="../labs/lab03/WALKTHROUGH.md">4. Guided Lab 3a and 3b</a></li><li><a href="../notebooks/day02/02_staging_delta.ipynb">5. Native Lab 3a — execution pending</a></li><li><a href="../notebooks/day02/03_incremental_silver.ipynb">6. Native Lab 3b — execution pending</a></li><li><a href="PRACTICE.md">7. Reasoning prompts</a></li><li><a href="COMPLETION.md">8. Save and hand off</a></li><li><a href="GLOSSARY.md">Glossary and pronunciation</a></li><li><a href="SOURCES.md">Official technical sources</a></li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>مسار التعلم</h2><ul><li><a href="CONCEPTS.md">١. المفاهيم والأمثلة</a></li><li><a href="DBT_GUIDE.md">٢. تصميم النماذج باستخدام dbt</a></li><li><a href="../notebooks/day02/01_silver_reference.ipynb">٣. المرجع المنفذ: قيم متوقعة وليس Delta</a></li><li><a href="../labs/lab03/WALKTHROUGH.md">٤. شرح اللاب 3a و3b</a></li><li><a href="../notebooks/day02/02_staging_delta.ipynb">٥. اللاب 3a الأصلي: التنفيذ غير متحقق</a></li><li><a href="../notebooks/day02/03_incremental_silver.ipynb">٦. اللاب 3b الأصلي: التنفيذ غير متحقق</a></li><li><a href="PRACTICE.md">٧. أسئلة الفهم</a></li><li><a href="COMPLETION.md">٨. الحفظ والانتقال لليوم التالي</a></li><li><a href="GLOSSARY.md">المصطلحات والنطق</a></li><li><a href="SOURCES.md">المصادر التقنية الرسمية</a></li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Six-hour teaching envelope</h2><p>20 min recap · 55 min concepts · 15 min break · 45 min dbt design · 75 min Lab 3a · 30 min break/prayer · 80 min Lab 3b · 25 min checks and notes · 15 min close = 360 min. This is a proposed allocation, not a formal attendance schedule. The reference is integrated into explanation, not an extra assignment.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>إطار الساعات الست</h2><p>20 دقيقة مراجعة، و55 للمفاهيم، و15 استراحة، و45 لتصميم dbt، و75 للاب 3a، و30 للصلاة والاستراحة، و80 للاب 3b، و25 للتحقق والتوثيق، و15 للختام؛ المجموع 360 دقيقة. توزيع مقترح وليس جدول حضور رسميًا. يدمج المرجع في الشرح ولا يعد تكليفًا إضافيًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>One lab in two parts</h2><p>Lab 03 contains 3a (staging) and 3b (incremental Silver). It remains one of the eight cumulative project labs. Save LAB03_NOTES.md; do not submit a second project.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>لاب واحد بجزأين</h2><p>اللاب 03 يتكون من 3a للتهيئة و3b لبناء Silver تزايديًا. يظل لابًا واحدًا من اللابات الثمانية للمشروع التراكمي. احفظ LAB03_NOTES.md؛ لا تسلم مشروعًا ثانيًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../day01/README.md">Previous day</a> · <a href="../day03/README.md">Next day</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../day01/README.md">اليوم السابق</a> · <a href="../day03/README.md">اليوم التالي</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="DATA_CONTRACT.md">Silver field contract</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="DATA_CONTRACT.md">عقد حقول Silver</a></td></tr></tbody>
</table>
