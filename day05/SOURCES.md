<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 5 sources and evidence</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>مصادر اليوم الخامس وأدلته</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a> · <a href="../day05/README.md">Day 5</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">الجاهزية</a> · <a href="../day05/README.md">اليوم الخامس</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Primary technical documentation</h2><p>Checked during this build on 10 September 2026: <a href="https://docs.delta.io/delta-batch/">Delta versioned batch reads</a>; <a href="https://docs.delta.io/concurrency-control/">Delta concurrency</a>; <a href="https://learn.microsoft.com/en-us/power-bi/guidance/star-schema">Microsoft star schema</a>; <a href="https://docs.feast.dev/getting-started/concepts/point-in-time-joins">Feast point-in-time concept</a>; <a href="https://spark.apache.org/docs/4.0.0/api/python/reference/pyspark.sql/functions.html">Spark function reference</a>. Feast is a concept source, not a new required dependency; no external engine test is borrowed as proof for this project.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التوثيق التقني الأصلي</h2><p>رُوجعت في هذا البناء بتاريخ ١٠ سبتمبر ٢٠٢٦: <a href="https://docs.delta.io/delta-batch/">قراءة نسخ Delta</a>؛ <a href="https://docs.delta.io/concurrency-control/">التزامن في Delta</a>؛ <a href="https://learn.microsoft.com/en-us/power-bi/guidance/star-schema">المخطط النجمي من Microsoft</a>؛ <a href="https://docs.feast.dev/getting-started/concepts/point-in-time-joins">مفهوم وقت القرار من Feast</a>؛ <a href="https://spark.apache.org/docs/4.0.0/api/python/reference/pyspark.sql/functions.html">مرجع دوال Spark</a>. Feast مصدر مفهوم لا اعتماد جديد مطلوب؛ ولا نستعير نجاح اختبار خارجي لإثبات مشروعنا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Local numerical evidence</h2><p>All course numbers are computed from <a href="../data/README.md">MASAR_SMALL_V1</a> by <a href="../notebooks/day05/01_gold_serving_reference.ipynb">the executed reference notebook</a>. <a href="../evidence/day05_reference.json">Saved source-derived results</a> include table contents, checks, count reconciliation and logical hashes. They explicitly state engine_executed=false.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الدليل العددي المحلي</h2><p>تُحسب أرقام الدورة من <a href="../data/README.md">MASAR_SMALL_V1</a> داخل <a href="../notebooks/day05/01_gold_serving_reference.ipynb">الدفتر المرجعي المنفذ</a>. تتضمن <a href="../evidence/day05_reference.json">النتائج المشتقة من المصدر</a> محتوى الجداول والفحوص وتسوية الأعداد والبصمات، وتصرح بأن engine_executed=false.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Unavailable evidence remains unavailable</h2><p>No successful Spark/Delta/Kafka/GX or dbt execution is claimed by this authoring stage. The dependency/native-attempt record and teaching-release status are retained separately from the reference result.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>يبقى الدليل غير المتاح غير متاح</h2><p>لا تدعي مرحلة البناء نجاح تشغيل Spark أو Delta أو Kafka أو GX أو dbt. يُحفظ سجل المتطلبات ومحاولة التنفيذ وحالة جاهزية التدريس بصورة منفصلة عن النتيجة المرجعية.</p></td></tr></tbody>
</table>
