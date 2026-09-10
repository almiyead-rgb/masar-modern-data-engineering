<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 3 · Change and safety policy</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الثالث · سياسة التغيير والسلامة</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../README.md">Course home</a> · <a href="../STATUS.md">Execution record</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">سجل التنفيذ</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Operational scope</h2><p>The only approved business change to trusted Silver is correction.csv, assigned source_revision=2, for SYN_T0001. Preserve every raw source file. Do not rerun insert-only Day 2 transformations over Day 3 corrections.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>النطاق التشغيلي</h2><p>التغيير المعتمد الوحيد في Silver الموثوقة هو correction.csv للرحلة SYN_T0001، وتمنحه سياسة السيناريو source_revision=2. حافظ على كل ملفات المصدر. لا تعاود تحويلات اليوم الثاني المخصصة للإضافة فوق تصحيحات اليوم الثالث.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Revision decision table</h2><ul><li>Missing key → insert a valid new trip.</li><li>Higher revision → update.</li><li>Same revision + identical payload → preserve values.</li><li>Lower revision → ignore stale data.</li><li>Same revision + different payload → stop before MERGE.</li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>قواعد قرار المراجعة</h2><ul><li>مفتاح غير موجود ← إضافة رحلة جديدة صالحة.</li><li>مراجعة أعلى ← تحديث.</li><li>المراجعة والمحتوى متطابقان ← الحفاظ على القيم.</li><li>مراجعة أقل ← تجاهل البيانات القديمة.</li><li>المراجعة نفسها ومحتوى مختلف ← التوقف قبل MERGE.</li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Sandbox boundary</h2><p>Constraint probes, schema evolution, compaction and DELETE/RESTORE are written into fresh <code>sandbox/day03/</code> tables with independent data files. These are not shallow clones. The helper rejects maintenance paths outside that directory, parent traversal and symlinks.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حدود العزل</h2><p>تكتب تجارب القيود وتطور المخطط ودمج الملفات وDELETE/RESTORE في جداول جديدة داخل <code>sandbox/day03/</code> بملفات بيانات مستقلة، وليست نسخًا سطحية تشارك الملفات. ترفض الأداة مسارات الصيانة خارج المجلد والانتقال إلى المجلد الأب والروابط الرمزية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Protected operations</h2><p>Do not edit <code>_delta_log</code>, remove Parquet files manually, overwrite previous runs, or turn off retention safety. VACUUM in this lab is dry-run only with at least 168 hours. A successful dry run is not proof that any expired files were deleted.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>العمليات المحمية</h2><p>لا تعدل <code>_delta_log</code>، ولا تحذف ملفات Parquet يدويًا، ولا تكتب فوق التشغيلات السابقة، ولا تعطل حماية الاحتفاظ. VACUUM في هذا اللاب معاينة فقط باحتفاظ لا يقل عن 168 ساعة. نجاح المعاينة لا يثبت حذف ملفات قديمة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Expected failure means a specific failure</h2><p>A negative test passes only when the intended schema/constraint error occurs and the table’s committed state remains unchanged. Unexpected engine errors are re-raised. The negative-fare test includes one valid row in the same write to check that partial acceptance does not occur.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>معنى الفشل المتوقع</h2><p>ينجح الاختبار السلبي فقط إذا ظهر خطأ المخطط أو القيد المقصود وبقيت الحالة المعتمدة للجدول ثابتة. يعاد إظهار أخطاء المحرك غير المتوقعة. يضم اختبار الأجرة السالبة صفًا صحيحًا في الكتابة نفسها للتحقق من عدم قبول جزء من الدفعة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What to compare</h2><p>Expected current values: 75 unique trips, 1880.60 SAR, one source revision 2. Compare the canonical business digest; do not compare physical filenames or elapsed times across runs. The schema sandbox has an extra field, but trusted Silver keeps its existing contract.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما الذي تقارنه؟</h2><p>القيم الحالية المتوقعة: 75 رحلة فريدة، و1880.60 ريال، وصف واحد بالمراجعة 2. قارن بصمة الأعمال المعيارية؛ لا تقارن أسماء الملفات أو الأزمنة بين التشغيلات. تضيف نسخة المخطط المعزولة حقلًا، بينما تحتفظ Silver الموثوقة بعقدها السابق.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Restart without losing work</h2><p>A completed 4a rerun rechecks current values without claiming to repeat historical tests. 4b creates new copies each time. An incomplete attempt or a changed later-day table is preserved and reported, not reset silently. Restore a fresh end-to-end workspace for a clean full repeat; retain the previous attempt for diagnosis.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الإعادة دون فقدان العمل</h2><p>تعيد 4a المكتملة فحص القيم الحالية دون ادعاء إعادة الاختبارات التاريخية. تنشئ 4b نسخًا جديدة في كل مرة. تحفظ المحاولة غير المكتملة أو الجدول المعدل لاحقًا ويبلغ عنها، ولا يعاد ضبطها بصمت. للتكرار الكامل النظيف استخدم مساحة جديدة من بداية الخط، مع إبقاء المحاولة السابقة للتشخيص.</p></td></tr></tbody>
</table>
