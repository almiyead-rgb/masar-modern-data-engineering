<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 07 · Guided integration</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 07 · التكامل خطوة بخطوة</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../../README.md">Course home</a> · <a href="../../STATUS.md">Readiness</a> · <a href="../../day05/README.md">Day 5</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../../README.md">الرئيسية</a> · <a href="../../STATUS.md">الجاهزية</a> · <a href="../../day05/README.md">اليوم الخامس</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>1. Verify the upstream handoff</h2><p>Open the Day 4 stream and quality reports. Native input loading checks their scopes, exact required checks, dataset identity and actual Delta files. The approved Silver snapshot must match the corrected 75 trips; the event snapshot must contain 217 distinct events. Stop on any mismatch.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>١. تحقق من مخرجات المرحلة السابقة</h2><p>افتح تقريري التدفق والجودة من اليوم الرابع. يفحص تحميل المدخلات نطاقهما وفحوصهما المطلوبة وهوية البيانات وملفات Delta الفعلية. يجب مطابقة Silver المعتمدة للرحلات المصححة الـ75، واحتواء نسخة الأحداث 217 حدثًا مختلفًا. توقف عند أي اختلاف.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>2. Pin both input versions</h2><p>Read the Delta history once, select each version, and read versionAsOf. Record source paths, versions and report hashes. Do not read one product from the approved table and another from the deliberately bad candidate.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٢. ثبت نسختي المدخلات</h2><p>اقرأ تاريخ Delta واختر النسخة واقرأها عبر versionAsOf. سجل المسارات والنسخ وبصمات التقارير. لا تبنِ مخرجًا من الجدول المعتمد وآخر من الدفعة المعيبة المقصودة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>3. Follow the actual transformation code</h2><p>In <a href="../../src/masar/serving.py">build_frames</a>, Spark joins the city lookup, aggregates GPS by trip, creates hourly and daily summaries, derives dimensions and applies both event-time and availability-time filters for features. Reference functions are used only to check the resulting native rows, never to populate native fact tables.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٣. تتبع كود التحويل الفعلي</h2><p>في <a href="../../src/masar/serving.py">build_frames</a> يربط Spark قاموس المدن ويجمع GPS حسب الرحلة ويبني الملخصين والأبعاد ويطبق قاعدتي وقت الحدث ووقت الإتاحة للخصائص. تستخدم الدوال المرجعية لفحص النتائج الأصلية فقط، ولا تملأ جداول الوقائع الأصلية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>4. Build the first good release</h2><p>Each output table is written with errorifexists into a fresh release directory. Read it back through Delta, validate its schema and keys, and compare canonical rows against the independent calculation. Only after all eight tables pass is release.json written and the latest pointer advanced.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٤. ابن الإصدار السليم الأول</h2><p>يكتب كل جدول بوضع errorifexists داخل مجلد إصدار جديد. يُقرأ ثانية من Delta، ويفحص مخططه ومفاتيحه، وتقارن صفوفه الموحدة بالحساب المستقل. لا يكتب release.json ولا يتقدم المؤشر الأخير إلا بعد نجاح الجداول الثمانية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>5. Observe an intentional failure</h2><p>The recovery exercise fails a second build after its first output table. Verify that the latest pointer bytes are unchanged and that the former good release still passes native readback. A caught InjectedFailure is expected; any unrelated exception must fail the notebook.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٥. راقب الفشل المقصود</h2><p>يفشل تمرين التعافي محاولة ثانية بعد أول جدول مخرج. تحقق من ثبات ملف المؤشر ومن استمرار اجتياز الإصدار السابق القراءة الأصلية. الخطأ InjectedFailure متوقع، أما أي استثناء آخر فيجب أن يفشل الدفتر.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>6. Rebuild and compare</h2><p>Rebuild with a new release identity. Compare the logical hashes of every table with the first good release. Keep both successful manifests and the failed-candidate report. The same-session exercise proves a controlled recovery behaviour only when the native run succeeds.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٦. أعد البناء وقارن</h2><p>أعد البناء بمعرف إصدار جديد. قارن بصمة المحتوى لكل جدول بالإصدار السليم الأول. احفظ السجلين السليمين وتقرير المحاولة الفاشلة. يثبت تمرين الجلسة الواحدة سلوك التعافي المضبوط فقط عند نجاح التنفيذ الأصلي.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>7. Record your explanation and continue</h2><p>Complete the first four <a href="../../day05/PRACTICE.md">embedded questions</a> in LAB07_NOTES.md. Continue to <a href="../lab08/WALKTHROUGH.md">Lab 08</a>. Read <a href="../../day05/INTEGRATION.md">the integration guide</a> for the later clean end-to-end check.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>٧. سجل تفسيرك وانتقل</h2><p>أكمل الأسئلة الأربعة الأولى من <a href="../../day05/PRACTICE.md">التطبيق المدمج</a> في LAB07_NOTES.md، ثم انتقل إلى <a href="../lab08/WALKTHROUGH.md">اللاب 08</a>. راجع <a href="../../day05/INTEGRATION.md">دليل التكامل</a> للفحص الشامل اللاحق من بداية نظيفة.</p></td></tr></tbody>
</table>
