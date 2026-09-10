<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Run and verify the same project</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>تشغيل المشروع نفسه والتحقق منه</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a> · <a href="../day05/README.md">Day 5</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">الجاهزية</a> · <a href="../day05/README.md">اليوم الخامس</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Normal route: continue the accumulated workspace</h2><p>Complete the native Day 4 notebooks first, then run Lab 07 and Lab 08. No source data is reselected and no learner output is deleted. Lab 07 performs a good build, one deliberate failed build, and a recovery build within the same Spark session; it is not a two-environment acceptance test.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المسار المعتاد: استكمل مساحة العمل المتراكمة</h2><p>أكمل دفتري اليوم الرابع الأصليين أولًا، ثم اللابين 07 و08. لا نعيد اختيار البيانات ولا نحذف مخرجات المتدرب. ينفذ اللاب 07 بناءً سليمًا ومحاولة فاشلة مقصودة ثم تعافيًا داخل جلسة Spark نفسها؛ وليس اختبار قبول في بيئتين مستقلتين.</p></td></tr></tbody>
</table>

```bash
python scripts/run_day05.py --preflight
python scripts/run_day05.py --part all
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Clean integration check</h2><p>The integrated runner creates a new marked workspace and executes the previously written native functions in dependency order. It does not substitute the reference calculations for any stage. It requires the actual local Kafka broker and pinned Spark/Delta/GX prerequisites. First-startup dependency downloads must be completed before class.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>فحص التكامل من بداية نظيفة</h2><p>ينشئ مشغل التكامل مساحة جديدة معلّمة وينفذ الدوال الأصلية المكتوبة سابقًا وفق الاعتماد بينها. لا يستبدل أي مرحلة بالحساب المرجعي. يتطلب وسيط Kafka المحلي الفعلي ومتطلبات Spark وDelta وGX المحددة. يجب تجهيز تحميلات الاعتماد الأولية قبل القاعة.</p></td></tr></tbody>
</table>

```bash
python scripts/run_day05.py --part integration --preflight
python scripts/run_day05.py --part integration
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Dependency order</h2><p>Bronze → measured scan → staging → incremental Silver → transactions → safe maintenance → Kafka stream → GX gate → Gold recovery → AI/BI serving. The full journal is saved under reports/integration_stages.json. A failure records its stage and blocks all downstream stages.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ترتيب الاعتماد</h2><p>Bronze ثم قياس القراءة ثم التهيئة ثم Silver التراكمية ثم المعاملات ثم الصيانة الآمنة ثم تدفق Kafka ثم بوابة GX ثم التعافي في Gold ثم تقديم AI وBI. يُحفظ السجل الكامل في reports/integration_stages.json. يوثق الفشل مرحلته ويمنع المراحل التالية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Safe publication within the local lab</h2><p>Fresh tables are written under mini_lakehouse/serving_releases/&lt;run_id&gt;/. The release.json file is created only after all native readbacks match the independent expectations. The local latest pointer changes last. A failed candidate is never selected by this consumer, but its files remain for diagnosis.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الإتاحة الآمنة داخل اللاب المحلي</h2><p>تكتب جداول جديدة داخل mini_lakehouse/serving_releases/&lt;run_id&gt;/. لا ينشأ release.json إلا بعد مطابقة القراءات الأصلية للتوقعات المستقلة. يتغير المؤشر المحلي الأخير في النهاية. لا يختار هذا المستهلك محاولة فاشلة، لكن تبقى ملفاتها للتشخيص.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Scope of “passed”</h2><p>A successful native integration path is labelled PASSED_NATIVE_PATH_DBT_NOT_VALIDATED. It does not automatically validate the dbt adapter, model profile, every runtime environment, production deployment or course publication. The separate repository release gate must continue to reject a course with missing native/dbt evidence.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>نطاق كلمة «نجح»</h2><p>يسمى نجاح المسار الأصلي PASSED_NATIVE_PATH_DBT_NOT_VALIDATED. لا يتحقق تلقائيًا من موصل dbt أو إعداده أو كل البيئات أو النشر الإنتاجي أو نشر الدورة. يجب أن يظل فحص جاهزية الإصدار يرفض دورة تفتقر إلى دليل المحرك أو dbt.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Before final course acceptance</h2><p>Run the complete native path twice from fresh workspaces and independent processes in the target environment. Compare table content and contract checks; preserve distinct run identities and actual logs. Separately validate dbt and review notebook outputs. No helper test or manually edited status flag can replace that work.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>قبل القبول النهائي للدورة</h2><p>شغل المسار الأصلي كاملًا مرتين بمساحتي عمل جديدتين وعمليتين مستقلتين في البيئة المستهدفة. قارن محتوى الجداول وفحوص العقود، واحفظ المعرفات المستقلة والسجلات الفعلية. تحقق من dbt بصورة منفصلة وراجع مخرجات الدفاتر. لا يعوض ذلك اختبار مساعد أو تعديل يدوي للحالة.</p></td></tr></tbody>
</table>
