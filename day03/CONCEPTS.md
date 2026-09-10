<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 3 · Understand safe change</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الثالث · فهم التغيير الآمن</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">حالة الجاهزية</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Before the first command</h2><p>Read the table as one row per trip. From the executed source reference: 75 trips total 1875.60 SAR before correction; SYN_T0001 changes from 18.00 to 23.00 SAR. We expect 75 trips and 1880.60 SAR afterward. These are expected business values, not saved Delta execution results.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>قبل أول أمر</h2><p>اقرأ الجدول على أساس صف واحد لكل رحلة. وفق مرجع المصدر المنفذ: 75 رحلة بإجمالي 1875.60 ريال قبل التصحيح؛ تتغير أجرة SYN_T0001 من 18.00 إلى 23.00 ريال. نتوقع بعده 75 رحلة وإجمالي 1880.60 ريال. هذه قيم أعمال متوقعة وليست نتائج تشغيل محفوظة لمحرك Delta.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>1. The table is more than its data files</h2><p>Parquet files contain columnar data; the Delta transaction log records the table’s committed state. Read the path using the Delta reader, rather than collecting every Parquet file in the folder. Old files may remain after a change. See <a href="SOURCES.md">D1</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>1. الجدول أكثر من ملفات البيانات</h2><p>تحتوي ملفات Parquet على البيانات العمودية، بينما يسجل سجل معاملات Delta حالة الجدول المعتمدة. اقرأ المسار بقارئ Delta، ولا تجمع جميع ملفات Parquet في المجلد؛ فقد تبقى ملفات قديمة بعد التغيير. انظر <a href="SOURCES.md">D1</a>.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>2. Four letters, practical meaning</h2><p>Atomicity: a table write commits as a unit. Consistency: defined constraints must hold. Isolation: readers work with a consistent snapshot. Durability: committed state persists under the supported storage guarantees. A successful table write does not make the whole multi-table pipeline one transaction, nor prove the business rules you forgot to define. See D2 and D3.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>2. أربعة أحرف ومعنى عملي</h2><p>الذرّية: تعتمد كتابة الجدول كوحدة واحدة. الاتساق: يجب تحقق القيود المعرفة. العزل: يقرأ المستهلك لقطة متسقة. الديمومة: تبقى الحالة المعتمدة وفق ضمانات التخزين المدعوم. نجاح كتابة جدول لا يجعل الخط متعدد الجداول معاملة واحدة، ولا يثبت قواعد أعمال لم نعرفها. انظر D2 وD3.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>3. Two different version numbers</h2><p><code>source_revision</code> orders corrections for a trip. A Delta table version numbers committed table changes. Revision 2 on one row is not table version 2. Capture actual versions from history; never infer them from the trip count. In this lab, the fixed correction is assigned revision 2 by scenario metadata, not by a nonexistent CSV column.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>3. رقمان مختلفان للنسخة</h2><p>يرتب <code>source_revision</code> مراجعات الرحلة. أما نسخة جدول Delta فترقم تغيرات الجدول المعتمدة. المراجعة 2 في صف ليست نسخة الجدول 2. تؤخذ أرقام نسخ الجدول من السجل الفعلي، لا من عدد الرحلات. في هذا اللاب تمنح بيانات السيناريو التصحيح الثابت المراجعة 2؛ وليست عمودًا موجودًا في CSV.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>4. Decide precedence before MERGE</h2><p>New trip: insert. Newer revision of an existing trip: update. Identical revision and payload: keep the same values. Older revision: ignore it. Same revision with conflicting content: stop. Receiving an old file later must not erase a valid correction. This is our explicit application policy, not an automatic Delta business rule.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>4. حدد الأولوية قبل MERGE</h2><p>رحلة جديدة: إضافة. مراجعة أحدث لرحلة موجودة: تحديث. المراجعة والمحتوى متطابقان: الحفاظ على القيم. مراجعة أقدم: تجاهلها. المراجعة نفسها بمحتوى متعارض: توقف. وصول ملف قديم متأخرًا لا يجب أن يلغي تصحيحًا صحيحًا. هذه سياسة تطبيق نعرفها نحن، وليست قاعدة أعمال تلقائية في Delta.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>5. MERGE is not “append everything”</h2><p>Use <code>trip_id</code> for matching and allow updates only when the incoming revision is higher. Validate source and target key uniqueness first. Multiple source rows for one target can make an update ambiguous. The fixed correction targets an existing trip, so the expected row count remains 75. See D4.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>5. MERGE ليس «أضف كل شيء»</h2><p>استخدم <code>trip_id</code> للمطابقة، واسمح بالتحديث فقط عندما تكون مراجعة المصدر أعلى. تحقق أولًا من تفرد مفاتيح المصدر والهدف؛ فقد يجعل تعدد صفوف المصدر لنفس الهدف التحديث ملتبسًا. يستهدف التصحيح الثابت رحلة موجودة، لذا يبقى العدد المتوقع 75. انظر D4.</p></td></tr></tbody>
</table>

```python
# After validating schemas, keys and same-revision conflicts:
(delta_table.alias("t")
 .merge(incoming.alias("s"), "t.trip_id = s.trip_id")
 .whenMatchedUpdateAll(condition="s.source_revision > t.source_revision")
 .whenNotMatchedInsertAll()
 .execute())
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>6. Rerun business results, not physical layout</h2><p>Compare sorted business values or a canonical digest. A replay may leave logical contents unchanged even if the engine records an operation. Do not demand identical commit IDs, filenames, execution times, or transaction counts between independent runs.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>6. قارن نتائج الأعمال لا شكل الملفات</h2><p>قارن قيم الأعمال المرتبة أو بصمتها المعيارية. قد تبقى القيم ثابتة عند الإعادة حتى لو سجل المحرك عملية. لا تشترط تطابق معرفات المعاملات أو أسماء الملفات أو أزمنة التنفيذ أو عدد المعاملات بين تشغيلين مستقلين.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>7. A schema is not the whole quality contract</h2><p>A decimal fare can still be negative. A string driver identifier can still be unknown. Schema enforcement controls column structure and types. CHECK/NOT NULL constraints and explicit relationship/uniqueness checks cover other rules. In this local setup, do not assume a declared business key is an automatically enforced unique key. See D3.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>7. المخطط ليس عقد الجودة كاملًا</h2><p>قد تكون الأجرة عشرية لكنها سالبة، وقد يكون معرف السائق نصًا لكنه غير معروف. يضبط فرض المخطط بنية الأعمدة وأنواعها. وتغطي CHECK وNOT NULL وفحوص العلاقات والتفرد قواعد أخرى. لا تفترض في هذا الإعداد المحلي أن مفتاح الأعمال المعلن يفرض التفرد تلقائيًا. انظر D3.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>8. Reject the intended failure, not every exception</h2><p>The native test submits one valid row and one negative-fare row to a constrained sandbox table. A known constraint rejection plus unchanged committed rows/schema/version demonstrates the expected failure. A missing package, disconnected JVM or unrelated exception is a failed test, not evidence that a data rule worked.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>8. ارفض الخطأ المقصود لا أي استثناء</h2><p>يرسل الاختبار الأصلي صفًا صحيحًا وصفًا بأجرة سالبة إلى جدول معزول ذي قيد. رفض معروف بسبب القيد، مع ثبات الصفوف والمخطط والنسخة المعتمدة، يثبت النتيجة المطلوبة للاختبار. غياب مكتبة أو انقطاع JVM أو استثناء آخر يعني فشل الاختبار، وليس نجاح قاعدة البيانات.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>9. Read history without changing today</h2><p><code>history()</code> shows committed operations. <code>versionAsOf</code> reads a recorded older version; it does not replace the current table. The lab records the version before correction and checks that SYN_T0001 still reads as 18.00 there while current Silver reads as 23.00. See D1 and D5.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>9. اقرأ التاريخ دون تغيير الحاضر</h2><p>يعرض <code>history()</code> العمليات المعتمدة. ويقرأ <code>versionAsOf</code> نسخة قديمة مسجلة دون استبدال الجدول الحالي. يسجل اللاب النسخة السابقة للتصحيح، ثم يفحص أن SYN_T0001 تقرأ فيها 18.00، بينما تقرأ في Silver الحالية 23.00. انظر D1 وD5.</p></td></tr></tbody>
</table>

```python
# Capture this value from history, not from the row's source_revision.
previous = (spark.read.format("delta")
            .option("versionAsOf", version_before_correction)
            .load(str(trusted_silver_path)))
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>10. Approve one schema change deliberately</h2><p>The fixed schema fixture adds <code>surcharge_sar</code>. Its meaning is a separate surcharge, not a replacement for <code>fare_sar</code>. The first write is expected to fail without permission; a subsequent sandbox-only write uses <code>mergeSchema=true</code>. Existing rows have null for the new field. Do not enable session-wide automatic evolution just to hide mismatches. See D1.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>10. وافق على تغيير مخطط محدد</h2><p>يضيف ملف السيناريو الثابت <code>surcharge_sar</code> بمعنى رسم إضافي منفصل، لا بديلًا عن <code>fare_sar</code>. يتوقع رفض الكتابة الأولى دون إذن؛ ثم تستخدم كتابة معزولة محددة <code>mergeSchema=true</code>. تكون قيمة الحقل الجديد فارغة في الصفوف السابقة. لا تفعل التطور التلقائي على مستوى الجلسة لإخفاء الاختلافات. انظر D1.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>11. Preserve the grain in a schema demo</h2><p>SYN_T0002 already exists. Appending its extended record to a full copy would produce a duplicate. Instead, create a new sandbox with the other 74 trips, then append the extended row once. The copy returns to 75 unique trips: 74 null surcharges and one value of 2.00. Trusted Silver is untouched.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>11. حافظ على مستوى الصف عند تجربة المخطط</h2><p>الرحلة SYN_T0002 موجودة مسبقًا. إضافة صفها الموسع إلى نسخة كاملة تنتج تكرارًا. لذلك ننشئ نسخة معزولة جديدة بالرحلات الـ74 الأخرى، ثم نضيف الصف الموسع مرة واحدة. تعود النسخة إلى 75 رحلة فريدة: 74 قيمة رسم فارغة وقيمة واحدة 2.00. لا يتغير جدول Silver الموثوق.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>12. DELETE and RESTORE belong in a copy here</h2><p>The recovery sandbox starts with 75 trips. Delete SYN_T0001 there: 74 remain. Read the earlier version, then restore it: current contents return to 75 through a new commit. RESTORE does not erase history. This exercise must not modify trusted Silver or be treated as a production backup plan. See D5 and D6.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>12. الحذف والاستعادة هنا في نسخة معزولة</h2><p>تبدأ نسخة الاستعادة بـ75 رحلة. احذف SYN_T0001 فيها فيبقى 74. اقرأ النسخة السابقة ثم استعدها: تعود المحتويات الحالية إلى 75 بمعاملة جديدة. لا يمحو RESTORE التاريخ. يجب ألا تعدل التجربة Silver الموثوقة، ولا تعاملها كخطة نسخ احتياطي للإنتاج. انظر D5 وD6.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>13. Compaction changes files, not business meaning</h2><p>OPTIMIZE compacts data files. Record active file counts from table details and compare business contents before/after. Old physical files can still exist, so counting all Parquet files on disk is not the active-file count. On 75 trips, no speed gain or file-count reduction is guaranteed. See D7.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>13. دمج الملفات لا يغير معنى البيانات</h2><p>يدمج OPTIMIZE ملفات البيانات. سجل عدد الملفات النشطة من تفاصيل الجدول وقارن قيم الأعمال قبل العملية وبعدها. قد تبقى ملفات قديمة فعليًا؛ لذا عد كل ملفات Parquet على القرص لا يمثل الملفات النشطة. لا نضمن تسارعًا أو انخفاض العدد في عينة من 75 رحلة. انظر D7.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>14. Preview cleanup; keep retention protection</h2><p>Our exercise runs VACUUM with <code>RETAIN 168 HOURS DRY RUN</code> on the sandbox. It lists candidates without deleting them; zero candidates is acceptable in a fresh lab. We never disable retention safeguards. Cleanup can limit older-version access; retention must account for readers and lagging streams. See D5 and D8.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>14. عاين التنظيف وأبقِ حماية الاحتفاظ</h2><p>تشغل التجربة VACUUM مع <code>RETAIN 168 HOURS DRY RUN</code> على النسخة المعزولة. تعرض مرشحي الحذف دون حذفهم؛ وصفر مرشحين نتيجة مقبولة في تجربة جديدة. لا نعطل حماية الاحتفاظ. قد تحد الصيانة من الوصول إلى النسخ القديمة، وتراعى القراءات والتدفقات المتأخرة عند تحديد الاحتفاظ. انظر D5 وD8.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>15. Audit changes without overclaiming ACID</h2><p>Keep source filename/hash, revision policy, before/after business values, real table versions and operation history. The exercise is single-writer and table-scoped. It does not benchmark concurrency, inject crashes or test a distributed production deployment. Those limits remain true even after all native lab checks pass.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>15. دقق التغيير دون مبالغة في إثبات ACID</h2><p>احفظ اسم المصدر وبصمته وسياسة المراجعة وقيم الأعمال قبل وبعد وأرقام نسخ الجدول الحقيقية وسجل العمليات. التجربة ذات كاتب واحد وفي نطاق الجدول؛ لا تقيس التزامن، ولا تحقن أعطالًا، ولا تختبر نشرًا إنتاجيًا موزعًا. تظل هذه الحدود صحيحة حتى بعد نجاح جميع فحوص اللاب الأصلي.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>16. Carry only trusted outputs forward</h2><p>Day 4 continues with corrected trusted Silver, unchanged raw files and the original event feeds. Sandbox schema additions and deletion experiments are not training features or reporting facts. Use <a href="COMPLETION.md">the completion checklist</a> to distinguish saved evidence from merely authored code.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>16. انقل المخرجات الموثوقة فقط</h2><p>يستكمل اليوم الرابع بـSilver المصححة وملفات المصدر الثابتة وأحداث المواقع الأصلية. لا تصبح أعمدة النسخ المعزولة أو تجارب الحذف خصائص تدريب أو حقائق تقارير. استخدم <a href="COMPLETION.md">قائمة الاكتمال</a> للتمييز بين الدليل المحفوظ والكود المكتوب فقط.</p></td></tr></tbody>
</table>
