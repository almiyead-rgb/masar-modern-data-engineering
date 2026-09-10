<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Local course workbench</h1><p><strong>Recipe authored; image build and native execution NOT verified.</strong> This is environment preparation for the same eight labs, not a new lab, project, or cloud platform.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>بيئة تشغيل الدورة المحلية</h1><p><strong>ملفات التجهيز مكتوبة؛ بناء الصورة والتنفيذ الأصلي غير متحققين.</strong> هذا إعداد لبيئة اللابات الثمانية نفسها، وليس لابًا أو مشروعًا أو منصة سحابية إضافية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="START_HERE.md">Start here</a> · <a href="RUNTIME_DBT.md">Pinned runtime</a> · <a href="RUNTIME_WORKBENCH_REVIEW.md">Actual validation boundary</a> · <a href="../infrastructure/runtime/compose.yaml">Service configuration</a> · <a href="../infrastructure/runtime/Dockerfile">Image recipe</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="START_HERE.md">ابدأ هنا</a> · <a href="RUNTIME_DBT.md">إصدارات التشغيل</a> · <a href="RUNTIME_WORKBENCH_REVIEW.md">حدود التحقق الفعلية</a> · <a href="../infrastructure/runtime/compose.yaml">إعداد الخدمات</a> · <a href="../infrastructure/runtime/Dockerfile">ملف بناء الصورة</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What stays the same</h2><p>The approved Python 3.11 / Java 17 / Spark 3.5.8 / Delta 3.3.2 target, existing dbt/GX/Kafka pins, fixed synthetic data, bilingual pages, five days and eight cumulative labs remain unchanged. The original host-based scripts and Kafka recipe remain available. Do not add a paid cloud account or a GPU.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما الذي لم يتغير؟</h2><p>تبقى بيئة Python 3.11 وJava 17 وSpark 3.5.8 وDelta 3.3.2 المستهدفة، وإصدارات dbt وGX وKafka القائمة، والبيانات الاصطناعية الثابتة، والصفحات الثنائية، والأيام الخمسة واللابات الثمانية التراكمية دون تغيير. ما زالت سكربتات التشغيل المباشر وإعداد Kafka السابق موجودة. لا يضاف حساب سحابي مدفوع أو GPU.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Prepare once before delivery</h2><p>The host needs a working container engine and its Compose plugin, plus network access for the initial image build. The Python command below manages only local services. It checks Compose, installs the existing pins inside the image, runs <code>pip check</code>, saves resolved package versions and image identities, and requires a genuine Delta write/read smoke check. A failed build stops; it is not a valid teaching image. A mutable base tag is not a reproducible image digest.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التجهيز مرة واحدة قبل التدريب</h2><p>يتطلب الجهاز محرك حاويات عاملًا وإضافة Compose، واتصالًا لتنزيل متطلبات البناء الأول. يدير أمر Python أدناه خدمات محلية فقط. يفحص Compose، ويثبت الإصدارات القائمة داخل الصورة، وينفذ <code>pip check</code>، ويحفظ الإصدارات التي حُلّت وهويات الصور، ويشترط اختبار كتابة وقراءة Delta فعليًا. يوقف فشل البناء العمل؛ ولا تصبح الصورة صالحة للتدريس بمجرد وجود الملف. اسم الصورة المتغير ليس بصمة إصدار قابل لإعادة الإنتاج.</p></td></tr></tbody>
</table>

```bash
# From the complete repository root. This is a preparation recipe, not a success receipt.
python scripts/workbench.py doctor
python scripts/workbench.py prepare
python scripts/workbench.py start
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Open the learning workspace</h2><p>After a successful start, Jupyter listens only on the host loopback port 8888. Use the local login URL and automatically generated token shown by Jupyter; authentication is not disabled. The source repository is mounted read-only, then copied once to a persistent learner volume. Open <code>docs/LEARNER_ROUTE.md</code> or the day notebook there. Startup does not overwrite learner edits.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>فتح مساحة التعلم</h2><p>بعد نجاح التشغيل، يتاح Jupyter على المنفذ المحلي 8888 فقط. يستخدم رابط الدخول المحلي والرمز الذي يولده Jupyter تلقائيًا؛ لم تُعطل المصادقة. يربط مستودع المصدر للقراءة فقط، ثم ينسخ مرة واحدة إلى مساحة تعلم دائمة. تفتح فيها صفحة <code>docs/LEARNER_ROUTE.md</code> أو دفتر اليوم. لا تستبدل إعادة التشغيل تعديلات المتدرب.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Two Kafka addresses, two contexts</h2><p>A Python process on the host uses <code>127.0.0.1:9092</code> with the original host broker recipe. A process in the new course container uses <code>kafka:29092</code>. Inside a container, loopback refers to that same container, not the separate broker. The new launcher selects the service address. Its broker is not published to a host port and must pass the health check before the workbench starts.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>عنوانان لـKafka بحسب مكان التنفيذ</h2><p>تستخدم عملية Python على الجهاز <code>127.0.0.1:9092</code> مع إعداد الوسيط السابق. وتستخدم العملية داخل حاوية الدورة الجديدة <code>kafka:29092</code>. يشير العنوان المحلي داخل الحاوية إلى الحاوية نفسها، لا إلى الوسيط المنفصل. يختار المشغّل الجديد عنوان الخدمة. لا ينشر وسيطه منفذًا على الجهاز، ويجب أن يجتاز فحص الصحة قبل بدء مساحة التعلم.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Engine verification is not a student assignment</h2><p>The verification coordinator creates two separate source copies, runs the original native integration and dbt in new processes, validates saved native reports and business-data digests, and then executes all ten native notebooks in another isolated copy. Ten notebooks implement eight labs because labs 03 and 04 have two parts. It stops at the first failure and preserves logs and outputs. It never changes course statuses to VERIFIED or publishes a repository.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التحقق التشغيلي ليس تكليفًا للمتدرب</h2><p>ينشئ منسق التحقق نسختين منفصلتين من المصدر، ويشغل التكامل الأصلي وdbt بعمليات جديدة، ويفحص التقارير المحفوظة وبصمات بيانات الأعمال، ثم ينفذ الدفاتر الأصلية العشرة في نسخة معزولة أخرى. تنفذ الدفاتر العشرة ثمانية لابات لأن اللابين 03 و04 مقسمان إلى جزأين. يتوقف عند أول فشل ويحفظ السجلات والمخرجات. ولا يغير حالات الدورة إلى VERIFIED ولا ينشر مستودعًا.</p></td></tr></tbody>
</table>

```bash
# Automated technical QA after a successfully built image and healthy local broker.
python scripts/workbench.py verify
# Inspect planned commands without executing services:
python scripts/workbench.py verify --plan
# Stop services without deleting learner work or Kafka checkpoints:
python scripts/workbench.py stop
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Preserve work, source versions and results</h2><p>Learner files, audit files and Kafka state use three separate persistent volumes. The verifier does not write into the learner volume. If the source version changes, startup refuses to overwrite an existing workspace. A different <code>--project</code> name creates a separate set of resources; keep the earlier project for recovery. No reset, volume deletion or destructive cleanup command is built in.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حفظ العمل والإصدارات والنتائج</h2><p>تستخدم ملفات المتدرب وملفات التحقق وحالة Kafka ثلاث وحدات تخزين دائمة منفصلة. لا يكتب المدقق في مساحة المتدرب. إذا تغير إصدار المصدر، يرفض البدء الكتابة فوق مساحة قائمة. ينشئ اسم مختلف في <code>--project</code> موارد مستقلة، مع إبقاء المشروع السابق للاسترجاع. لا يتضمن المشغّل أمر إعادة ضبط أو حذف تخزين أو تنظيفًا إتلافيًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Offline classroom boundary</h2><p>The image recipe preloads the same Delta and Kafka connector JARs. The Compose network is configured as internal, so runtime dependency downloads are not the intended classroom path. A successful real image build and a subsequent disconnected run are still required before calling this offline-ready. No downloadable image or fully resolved lock has been produced in this session.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حدود العمل دون تنزيل أثناء التدريب</h2><p>يتضمن وصف بناء الصورة تحميل ملفات Delta وموصل Kafka نفسها مسبقًا. وأعدت شبكة Compose داخلية، فلا يكون تنزيل التبعيات أثناء التدريب هو المسار المقصود. ما زال يلزم بناء فعلي ناجح، ثم اختبار لاحق دون اتصال خارجي، قبل وصفها بأنها جاهزة للعمل دون اتصال. لم تُنتج في هذه الجلسة صورة قابلة للتنزيل أو نسخة قفل مكتملة للتبعيات.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Primary references</h2><p><a href="https://docs.docker.com/compose/how-tos/networking/">Compose networking</a> · <a href="https://docs.docker.com/compose/how-tos/startup-order/">Health-gated startup</a> · <a href="https://github.com/docker-library/python/blob/master/3.11/slim-bookworm/Dockerfile">Official Python image recipe</a> · <a href="https://docs.jupyter.org/en/latest/running.html">Jupyter startup</a>. These explain the selected configuration; they do not certify this project’s execution.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>المراجع الأولية</h2><p><a href="https://docs.docker.com/compose/how-tos/networking/">شبكات Compose</a> · <a href="https://docs.docker.com/compose/how-tos/startup-order/">البدء المشروط بفحص الصحة</a> · <a href="https://github.com/docker-library/python/blob/master/3.11/slim-bookworm/Dockerfile">ملف بناء صورة Python الرسمي</a> · <a href="https://docs.jupyter.org/en/latest/running.html">تشغيل Jupyter</a>. تفسر المراجع الإعداد المختار، ولا تثبت تنفيذ هذا المشروع.</p></td></tr></tbody>
</table>
