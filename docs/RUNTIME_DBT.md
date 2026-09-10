<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>One runtime · Spark, Delta and dbt</h1><p><strong>Provisioning recipe and connection authored; engine validation pending.</strong> This page is the current target. Older evidence logs preserve earlier attempted environments and do not certify this one.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>بيئة واحدة · Spark وDelta وdbt</h1><p><strong>أُعد وصف التجهيز والاتصال؛ والتحقق من المحرك معلّق.</strong> هذه الصفحة هي الهدف الحالي. تحتفظ السجلات السابقة بالبيئات التي جُربت سابقًا ولا تثبت نجاح هذه البيئة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="SETUP.md">Course setup</a> · <a href="../day02/DBT_GUIDE.md">dbt lesson</a> · <a href="../runtime-target.json">Machine-readable target</a> · <a href="../requirements-course.txt">All direct pins</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="SETUP.md">إعداد الدورة</a> · <a href="../day02/DBT_GUIDE.md">درس dbt</a> · <a href="../runtime-target.json">الهدف بصيغة قابلة للفحص</a> · <a href="../requirements-course.txt">الإصدارات المباشرة</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Why the target changed</h2><p>The earlier Spark 4.0.1 / Delta 4.0.1 candidate did not satisfy the chosen stable dbt-spark session extra. Use Python 3.11, Java 17, PySpark 3.5.8, Delta 3.3.2, Py4J 0.10.9.9, dbt-core 1.9.8 and dbt-spark 1.9.1. Kafka/GX retain their existing pins. The Spark Kafka connector uses Scala <code>_2.12:3.5.8</code>. Do not mix 2.13 JARs or the old Delta version into this environment.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>لماذا تغير الهدف؟</h2><p>لم يلبّ المرشح السابق Spark 4.0.1 وDelta 4.0.1 شرط موصل جلسة dbt-spark المستقر المختار. الهدف: Python 3.11 وJava 17 وPySpark 3.5.8 وDelta 3.3.2 وPy4J 0.10.9.9 وdbt-core 1.9.8 وdbt-spark 1.9.1. تبقى إصدارات Kafka وGX المحددة سابقًا. يستخدم موصل Kafka في Spark لاحقة Scala <code>_2.12:3.5.8</code>؛ لا تخلط ملفات 2.13 أو إصدار Delta القديم معها.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Prepare before the lab, not during it</h2><p>Use a new Python 3.11 virtual environment with Java 17 on PATH. Install <code>requirements-course.txt</code>, run <code>pip check</code>, then freeze resolved versions for the actual successful target. Internet/Maven access is needed for initial packages and JARs. The direct-pins file is not a fully resolved lock, and a clean dependency check is not a successful engine test. No GPU is required by this tiny project.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>جهز قبل اللاب لا أثناءه</h2><p>تستخدم بيئة افتراضية جديدة بـPython 3.11 وJava 17 في PATH. تثبت <code>requirements-course.txt</code>، ثم يفحص <code>pip check</code>، وتُحفظ إصدارات التبعيات التي حُلّت فعلًا للهدف الناجح. يحتاج التجهيز الأول إلى الإنترنت وMaven للحزم وملفات JAR. ملف الإصدارات المباشرة ليس قفلًا كاملًا؛ ونجاح فحص التبعيات لا يثبت نجاح المحرك. لا يحتاج المشروع الصغير إلى GPU.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Connection and source isolation</h2><p>The runner requires the verified Day 1 Bronze pointer. It copies trip version 1, driver version 0 and GPS version 0 to a fresh workspace, preserving source values and arrival timestamps. It registers external Delta tables with generated safe schema names and uses the tracked local profile. It never points dbt at production data or edits the original course workspace.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الاتصال وعزل المصادر</h2><p>يتطلب المشغّل مؤشر Bronze ناجحًا من اليوم الأول. ينسخ إصدار الرحلات 1 والسائقين 0 والمواقع 0 إلى مساحة جديدة مع حفظ القيم وتوقيت الاستقبال. يسجل جداول Delta بأسماء مخططات آمنة مولدة، ويستخدم ملف الاتصال المحلي المرفق. لا يوجّه dbt إلى بيانات إنتاجية ولا يعدل مساحة الدورة الأصلية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Commands after provisioning</h2><p>Run from the repository root. Preflight only diagnoses packages; the second command requires actual Day 1 tables. The later-day correction flag revisits existing project data and is not extra homework.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الأوامر بعد التجهيز</h2><p>تنفذ من جذر المستودع. يشخّص الأمر الأول الحزم فقط؛ ويتطلب الثاني جداول اليوم الأول الفعلية. يعيد خيار التصحيح اللاحق استخدام بيانات المشروع القائمة، وليس واجبًا إضافيًا.</p></td></tr></tbody>
</table>

```bash
python scripts/run_dbt.py --preflight
python scripts/run_dbt.py
# Later-day QA using the existing correction, not an additional lab:
python scripts/run_dbt.py --include-correction
# Deliberate reconciliation outside the three-day ingestion lookback:
python scripts/run_dbt.py --reprocess-all
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>How a blocked attempt is represented</h2><p>The runner writes <code>reports/dbt_attempt.json</code> under a newly marked workspace even when preflight fails. <code>engine_executed=false</code>, <code>dbt_executed=false</code> and an empty phase list mean nothing ran. An authored profile or passing helper tests cannot change those flags. Native success does not automatically authorize course release or publishing.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>كيف تمثل المحاولة المتوقفة؟</h2><p>يحفظ المشغّل <code>reports/dbt_attempt.json</code> تحت مساحة جديدة موسومة حتى عند فشل فحص المتطلبات. تعني حالتا <code>engine_executed=false</code> و<code>dbt_executed=false</code> مع مراحل فارغة أن التنفيذ لم يحدث. لا يغير ملف اتصال مكتوب أو اختبارات مساندة ناجحة هذه الحقيقة. ولا يأذن نجاح الجزء الأصلي تلقائيًا باعتماد الدورة أو نشرها.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Version-specific primary references</h2><p><a href="https://github.com/dbt-labs/dbt-spark/blob/v1.9.1/setup.py">Stable adapter dependency range</a> · <a href="https://github.com/dbt-labs/dbt-spark/blob/v1.9.1/dbt/adapters/spark/session.py">Session implementation</a> · <a href="https://github.com/dbt-labs/dbt-spark/blob/v1.9.1/dbt/adapters/spark/connections.py">Profile contract</a> · <a href="https://docs.delta.io/releases/">Delta/Spark compatibility</a> · <a href="https://spark.apache.org/docs/3.5.8/">Spark 3.5.8 requirements</a> · <a href="https://docs.getdbt.com/reference/programmatic-invocations">Programmatic API: select Core v1, not Fusion v2</a>. Checked 10 September 2026.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>مراجع أولية مرتبطة بالإصدار</h2><p><a href="https://github.com/dbt-labs/dbt-spark/blob/v1.9.1/setup.py">اعتماديات الموصل المستقر</a> · <a href="https://github.com/dbt-labs/dbt-spark/blob/v1.9.1/dbt/adapters/spark/session.py">تطبيق الاتصال بالجلسة</a> · <a href="https://github.com/dbt-labs/dbt-spark/blob/v1.9.1/dbt/adapters/spark/connections.py">عقد ملف الاتصال</a> · <a href="https://docs.delta.io/releases/">توافق Delta وSpark</a> · <a href="https://spark.apache.org/docs/3.5.8/">متطلبات Spark 3.5.8</a> · <a href="https://docs.getdbt.com/reference/programmatic-invocations">الواجهة البرمجية: اختر Core v1 لا Fusion v2</a>. روجعت في 10 سبتمبر 2026.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Provision the selected target</h2><p>Use the <a href="RUNTIME_WORKBENCH.md">container recipe and verification coordinator</a> to prepare this target without changing the learner host libraries. The recipe is authored, not executed here.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تجهيز البيئة المستهدفة</h2><p>أضيف <a href="RUNTIME_WORKBENCH.md">وصف الحاوية ومنسق التحقق</a> لتجهيز هذه البيئة دون تغيير مكتبات جهاز المتدرب. الوصف مكتوب، ولم يُنفذ هنا.</p></td></tr></tbody>
</table>
