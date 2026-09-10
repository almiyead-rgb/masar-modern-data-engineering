<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Start here</h1><p><a href="../README.md">Home</a> · <a href="../MASAR_STUDENT.ipynb">Student notebook</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>ابدأ هنا</h1><p><a href="../README.md">الرئيسية</a> · <a href="../MASAR_STUDENT.ipynb">دفتر المتدرب</a></p></td></tr></tbody>
</table>
<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>The shortest route</h2><p>Open the full course folder. From a host with Python and Docker, run the command below. It builds the supplied environment, starts Kafka and Jupyter, and displays the local Jupyter access link. Keep the default token authentication.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المسار المختصر</h2><p>افتح مجلد الدورة كاملًا. من جهاز يحتوي على Python وDocker شغّل الأمر أدناه. يبني البيئة المرفقة، ويشغل Kafka وJupyter، ويعرض رابط Jupyter المحلي. تبقى حماية الدخول بالرمز الافتراضي مفعلة.</p></td></tr></tbody>
</table>

```bash
python RUN_PROJECT.py start
```
<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p>In Jupyter open <code>MASAR_STUDENT.ipynb</code>. Run setup once, then Labs 01–08 in order. Use the daily concept pages when a term needs explanation. Do not run the daily notebooks as an extra submission.</p><p>Save the notebook outputs and existing lab notes. Stop the services without deleting your work:</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p>داخل Jupyter افتح <code>MASAR_STUDENT.ipynb</code>. شغّل البداية مرة واحدة ثم اللابات 01–08 بالترتيب. ارجع لصفحات مفاهيم الأيام لتفسير المصطلحات. لا تشغّل الدفاتر اليومية كتسليم إضافي.</p><p>احفظ مخرجات الدفتر وملاحظات اللابات الموجودة. لإيقاف الخدمات دون حذف العمل:</p></td></tr></tbody>
</table>

```bash
python RUN_PROJECT.py stop
```
<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Explore the data without installing the engines</h2><p>The command below produces the expected Silver/Gold tables with the existing reference functions. It is a data preview, not a native Lakehouse or completion of the eight labs.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>استكشف البيانات دون تثبيت المحركات</h2><p>ينتج الأمر التالي جداول Silver وGold المتوقعة باستخدام الحسابات المرجعية الموجودة. هو معاينة للبيانات، وليس Lakehouse أصلية أو إكمالًا للابات الثمانية.</p></td></tr></tbody>
</table>

```bash
python RUN_PROJECT.py demo
```
<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What is verified?</h2><p>Native notebook execution is not yet verified here. On GitHub, the public-repository execution workflow is configured to run the actual notebook and keep success or failure outputs. It never publishes a course release automatically. The <a href="SETUP.md">detailed setup</a>, <a href="LEARNER_ROUTE.md">daily route</a> and <a href="../project/SUBMISSION.md">submission guide</a> remain available.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما الذي تم التحقق منه؟</h2><p>تشغيل الدفتر الأصلي لم يتحقق هنا بعد. أُعد فحص المستودع العام في GitHub لتشغيل الدفتر الفعلي وحفظ نتائج النجاح أو الخطأ. لا ينشر إصدارًا معتمدًا تلقائيًا. يبقى <a href="SETUP.md">الإعداد التفصيلي</a> و<a href="LEARNER_ROUTE.md">المسار اليومي</a> و<a href="../project/SUBMISSION.md">دليل التسليم</a> متاحًا.</p></td></tr></tbody>
</table>
