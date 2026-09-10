<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 4 · Governance within the same project</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الرابع · الحوكمة داخل المشروع نفسه</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Purpose and data boundary</h2><p>Purpose: learn ingestion, quality and lineage with MASAR_SMALL_V1 synthetic data. Do not import real customer trips, phone numbers, national IDs or GPS traces. Keep attribution to Meaad Al-Marri and the program without claiming official certification of this repository.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الغرض وحدود البيانات</h2><p>الغرض تعلم الاستيعاب والجودة والتتبع ببيانات MASAR_SMALL_V1 الاصطناعية. لا تستورد رحلات عملاء أو أرقام هواتف أو هويات أو مسارات GPS حقيقية. احفظ نسبة العمل لميعاد المري والبرنامج دون ادعاء اعتماد رسمي للمستودع.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Lineage you can trace</h2><p>Source filename + SHA-256 → producer receipt → Kafka (topic, partition, offset) → raw Delta path/checkpoint → event snapshot. For trips: Day 3 Silver version → candidate → quality rules/GX result → quarantine or revalidated snapshot → Day 5 consumers. Record the actual run paths, not hypothetical diagram paths.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تتبع يمكن مراجعته</h2><p>اسم المصدر وبصمته ← تأكيد المنتج ← الموضوع والقسم والإزاحة في Kafka ← مسار Delta الخام ونقطة التحقق ← نسخة الأحداث. وللرحلات: نسخة Silver في اليوم الثالث ← المرشح ← قواعد الجودة ونتيجة GX ← العزل أو النسخة المعاد فحصها ← مستهلكو اليوم الخامس. سجل مسارات التشغيل الفعلية لا مسارات رسم توضيحي.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Roles, not extra staff requirements</h2><p>Data owner approves purpose and access. Pipeline operator investigates runs. Data steward explains rule failures. Consumer uses only approved outputs. One learner may document all four roles for this project; no extra team or project is required.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>أدوار وليست اشتراطات أفراد إضافيين</h2><p>يعتمد مالك البيانات الغرض والوصول، ويحقق مشغل الخط في التنفيذ، ويفسر مسؤول جودة البيانات الفشل، ويستخدم المستهلك المخرجات المعتمدة فقط. يمكن للمتدرب توثيق الأدوار الأربعة بنفسه؛ لا فريق إضافيًا ولا مشروعًا جديدًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Access controls: describe versus enforce</h2><p>Proposed: consumers read approved tables; operators access raw and quarantine; configuration changes are reviewed. Actual: this local lab binds Kafka to loopback but does not implement authentication, TLS, row policies or multi-user authorization. Mark access controls as a design unless separately implemented and tested.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ضوابط الوصول: الوصف مقابل التطبيق</h2><p>المقترح: يقرأ المستهلك الجداول المعتمدة، ويصل المشغل إلى الخام والعزل، وتُراجع تغييرات الإعداد. الفعلي: يربط اللاب Kafka بالواجهة المحلية لكنه لا يطبق المصادقة أو TLS أو سياسات الصفوف أو تفويض المستخدمين. وسم ضوابط الوصول «تصميم» ما لم تنفذ وتختبر منفصلة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Retention is purpose-led</h2><p>Keep lab evidence until submission and required review. Do not invent an official organizational retention period. Kafka retention and Delta time-travel retention are different mechanisms. A seven-day classroom broker setting is an example, not a PDPL retention rule. Do not disable the Delta VACUUM safety window or delete checkpoint volumes to hide failures.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الاحتفاظ مرتبط بالغرض</h2><p>احتفظ بأدلة اللاب حتى التسليم والمراجعة المطلوبة دون اختلاق مدة احتفاظ رسمية للجهة. احتفاظ Kafka واحتفاظ نسخ Delta آليتان مختلفتان. إعداد وسيط التدريب لسبعة أيام مثال وليس مدة نظامية لحماية البيانات. لا تعطل نافذة أمان VACUUM ولا تحذف نقاط التحقق لإخفاء الأخطاء.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>PDPL reference and GPS reasoning</h2><p>PDPL covers information that can identify a person directly or indirectly. Therefore real linked GPS may require personal-data safeguards even without a name. The legal definition of sensitive data is specific; do not expand it automatically to every location field. Refer to the official law and regulations for real deployments. <a href="SOURCES.md">S10–S12</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>مرجع النظام والتفكير في GPS</h2><p>يشمل تعريف البيانات الشخصية ما يجعل التعرف على الفرد ممكنًا مباشرة أو غير مباشرة؛ لذلك قد تتطلب بيانات GPS الحقيقية المرتبطة بضوابط حماية حتى بلا اسم. تعريف البيانات الحساسة نظامًا محدد؛ لا توسّعه تلقائيًا ليشمل كل حقل موقع. راجع النظام واللوائح الأصلية عند التطبيق الحقيقي. <a href="SOURCES.md">S10–S12</a>.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Submission hygiene</h2><p>Use <a href="../templates/GOVERNANCE.md">GOVERNANCE.md</a> for your decisions. Do not commit generated raw/quarantine tables, broker volumes, credentials or local GX output. Summarize the synthetic results and keep detailed evidence in the designated submission location. Check .gitignore before every commit.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>سلامة التسليم</h2><p>استخدم <a href="../templates/GOVERNANCE.md">GOVERNANCE.md</a> لقراراتك. لا ترفع الجداول الخام أو المعزولة المولدة أو وحدات تخزين الوسيط أو الأسرار أو مخرجات GX المحلية. لخص النتائج الاصطناعية واحفظ الأدلة التفصيلية في موقع التسليم المخصص. افحص .gitignore قبل كل حفظ في Git.</p></td></tr></tbody>
</table>
