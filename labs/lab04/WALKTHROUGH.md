<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Lab 04 · Walkthrough</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اللاب 04 · الشرح التطبيقي</h1></td></tr></tbody>
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
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>0. Inspect the expected change</h2><p>Open the reference notebook. Read the before/after row and total. Explain why one updated trip changes the total by 5.00 SAR but not the row count. This step verifies arithmetic and policy, not Delta.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>0. افحص التغيير المتوقع</h2><p>افتح الدفتر المرجعي. اقرأ الصف والمجموع قبل وبعد. اشرح لماذا يغير تحديث رحلة واحدة المجموع بمقدار 5.00 ريال ولا يغير عدد الصفوف. تثبت هذه الخطوة الحساب والسياسة، لا Delta.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>1. Start from real prior outputs</h2><p>The native 4a notebook requires the saved successful Bronze workspace and Day 2 Silver report. It does not rebuild “Silver” from Python reference rows. Complete the prerequisites before running its engine cell. Missing packages or prior outputs are blockers, not a skipped pass.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>1. ابدأ من مخرجات سابقة فعلية</h2><p>يتطلب دفتر 4a الأصلي مساحة Bronze المحفوظة الناجحة وتقرير Silver لليوم الثاني. لا يعيد بناء «Silver» من صفوف المرجع البرمجي. تكتمل المتطلبات قبل خلية المحرك. غياب الحزم أو المخرجات السابقة عائق، وليس نجاحًا متجاوزًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>2. Record current state</h2><p>Read the real current Delta version, schema, business digest and row count. Keep the version before correction for the later read. Source revision and table version must be recorded separately.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>2. سجل الحالة الحالية</h2><p>اقرأ نسخة Delta الحالية الفعلية والمخطط وبصمة الأعمال وعدد الصفوف. احتفظ برقم النسخة قبل التصحيح للقراءة اللاحقة. سجل مراجعة المصدر ونسخة الجدول كلًا على حدة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>3. Land and type the correction</h2><p>The native helper reads correction.csv with explicit string fields, saves a separate Bronze correction receipt, parses the types with Spark, enriches from the existing drivers and assigns revision 2. The resulting row must match the independently calculated expectation before MERGE.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>3. استقبل التصحيح ووحد أنواعه</h2><p>تقرأ الأداة الأصلية correction.csv بأعمدة نصية محددة، وتحفظ استقبالًا منفصلًا في Bronze، وتحول الأنواع باستخدام Spark، وتربط بالسائقين الموجودين، وتمنح المراجعة 2. يجب أن يطابق الصف الناتج التوقع المحسوب مستقلًا قبل MERGE.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>4. Apply, replay, and send stale data</h2><p>Use the revision-aware MERGE. Compare current values after the first write, after replaying the same correction and after resending the old snapshot. All three should have the same corrected business digest. A transient same-revision/different-value probe must be rejected before a write.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>4. طبق وأعد ثم أرسل بيانات قديمة</h2><p>استخدم MERGE المعتمد على المراجعة. قارن القيم الحالية بعد الكتابة الأولى، ثم إعادة التصحيح نفسه، ثم إعادة اللقطة القديمة. يجب أن تتطابق بصمة الأعمال المصححة في الحالات الثلاث. ويرفض اختبار مؤقت بمراجعة مساوية وقيمة مختلفة قبل الكتابة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>5. Read the earlier version</h2><p>Use the captured pre-correction table version. Check that the earlier SYN_T0001 fare is 18.00 and current fare is 23.00. Save real history entries. Do not invent a version number if the engine has not run.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>5. اقرأ النسخة السابقة</h2><p>استخدم نسخة الجدول المسجلة قبل التصحيح. تحقق من أجرة SYN_T0001 السابقة 18.00 والحالية 23.00. احفظ سجل العمليات الحقيقي. لا تخترع رقم نسخة عندما لا يعمل المحرك.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>6. Verify rejection on a constrained copy</h2><p>The helper creates a new full copy and adds fare and key-presence checks. It attempts a two-row append containing one valid probe and the fixed negative-fare case. Verify the intended rejection and no change to committed rows, schema, or table version. Files staged by a failed write are not committed table rows.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>6. تحقق من الرفض على نسخة ذات قيود</h2><p>تنشئ الأداة نسخة كاملة جديدة وتضيف قيدي الأجرة ووجود المفتاح. وتحاول إضافة صفين: اختبار صحيح وحالة الأجرة السالبة الثابتة. تحقق من الرفض المقصود وثبات الصفوف والمخطط ونسخة الجدول المعتمدة. الملفات المرحلية الناتجة من كتابة فاشلة لا تعد صفوفًا معتمدة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>7. Test a deliberate extra column in 4b</h2><p>Create a new 74-row copy without SYN_T0002. First reject its extended row without schema permission. Then accept the single explicitly approved evolution. Check 75 unique trips, one surcharge of 2.00 and 74 null values. Fare totals stay unchanged; the trusted table has no added surcharge field.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>7. اختبر عمودًا إضافيًا مقصودًا في 4b</h2><p>أنشئ نسخة جديدة من 74 صفًا دون SYN_T0002. ارفض صفها الموسع أولًا دون إذن المخطط؛ ثم اقبل التطور المحدد صراحة. افحص 75 رحلة فريدة ورسمًا واحدًا 2.00 و74 قيمة فارغة. لا تتغير مجاميع الأجرة، ولا يضاف حقل الرسم إلى الجدول الموثوق.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>8. Compact a separate copy</h2><p>Record table details before and after OPTIMIZE; compare canonical business contents. Do not infer performance improvement from the command merely succeeding, and do not count obsolete files as active files.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>8. ادمج ملفات نسخة منفصلة</h2><p>سجل تفاصيل الجدول قبل OPTIMIZE وبعده، وقارن قيم الأعمال المعيارية. لا تستنتج تحسن الأداء لمجرد نجاح الأمر، ولا تعد الملفات القديمة ضمن الملفات النشطة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>9. Delete, inspect, restore in a recovery copy</h2><p>Record the new copy’s starting version. Delete only SYN_T0001 and verify 74 rows. Read the old version, then restore it; verify 75 rows and a later commit version. Trusted Silver must still have its corrected 75 rows throughout.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>9. احذف وافحص واستعد في نسخة الاستعادة</h2><p>سجل نسخة بداية الجدول المعزول. احذف SYN_T0001 فقط وتحقق من 74 صفًا. اقرأ النسخة القديمة ثم استعدها؛ تحقق من 75 صفًا ونسخة معاملة أحدث. يجب أن تحتفظ Silver الموثوقة طوال ذلك برحلاتها المصححة الـ75.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>10. Preview cleanup without removing data</h2><p>Execute the helper’s sandbox-only VACUUM DRY RUN at 168 hours. Save its candidates; an empty list is valid. Check the table state did not change. No retention override, manual file deletion or actual VACUUM deletion occurs in this lab.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>10. عاين التنظيف دون إزالة بيانات</h2><p>نفذ VACUUM DRY RUN عبر الأداة على النسخة المعزولة فقط، باحتفاظ 168 ساعة. احفظ المرشحين؛ والقائمة الفارغة صحيحة. تحقق من ثبات حالة الجدول. لا تتضمن التجربة تجاوز حماية الاحتفاظ أو حذفًا يدويًا أو حذفًا فعليًا باستخدام VACUUM.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>11. Save evidence in the same project</h2><p>Keep the two native reports, recorded histories, completed notebook outputs and LAB04_NOTES.md. The notebook/reference checks do not replace these native outputs. Follow <a href="../../day03/COMPLETION.md">Day 3 completion</a> before handing data to Day 4.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>11. احفظ الأدلة في المشروع نفسه</h2><p>احتفظ بتقريري المحرك وسجلات العمليات ومخرجات الدفاتر المنفذة وLAB04_NOTES.md. لا تحل فحوص المرجع أو الدفتر وحدها محل نتائج المحرك. اتبع <a href="../../day03/COMPLETION.md">اكتمال اليوم الثالث</a> قبل تسليم البيانات لليوم الرابع.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Equivalent local command</h2><p>From the repository root after the prior native labs have passed, the following command runs both parts. It does not install dependencies silently and it does not delete old workspaces.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>أمر محلي مكافئ</h2><p>من جذر المستودع وبعد نجاح اللابات الأصلية السابقة، يشغل الأمر التالي الجزأين. لا يثبت الاعتمادات خفية، ولا يحذف مساحات العمل القديمة.</p></td></tr></tbody>
</table>

```bash
python scripts/run_day03.py --part all
```
