<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h1>Local Kafka service</h1></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h1>خدمة Kafka المحلية</h1></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><p><a href="../../README.md">Course home</a> · <a href="../../STATUS.md">Execution record</a></p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><p><a href="../../README.md">الرئيسية</a> · <a href="../../STATUS.md">سجل التنفيذ</a></p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>One-machine synthetic-data service</h2><p>Start the local broker using the Day 4 setup and compose.yaml. Keep the named data volume between restarts and keep the host port restricted to the local machine.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>خدمة اصطناعية على جهاز واحد</h2><p>شغّل الوسيط المحلي باستخدام إعداد اليوم الرابع وcompose.yaml. احتفظ بوحدة تخزين البيانات عند إعادة التشغيل، وأبقِ المنفذ مقصورًا على الجهاز المحلي.</p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th align="left" dir="ltr" lang="en" width="50%">English</th><th align="right" dir="rtl" lang="ar" width="50%">العربية</th></tr></thead>
<tbody><tr><td align="left" dir="ltr" lang="en" valign="top" width="50%"><h2>Preserve checkpoint dependencies</h2><p>Keep the named broker volume while testing resume. No credentials or production records belong here. Do not expose port 9092 publicly. The service is not required for the source-reference notebook.</p></td><td align="right" dir="rtl" lang="ar" valign="top" width="50%"><h2>احفظ ما تعتمد عليه نقاط التحقق</h2><p>احتفظ بوحدة التخزين المسماة أثناء اختبار الاستئناف. لا أسرار أو بيانات إنتاجية هنا، ولا تعرض المنفذ 9092 للعامة. الخدمة ليست مطلوبة للدفتر المرجعي.</p></td></tr></tbody>
</table>
