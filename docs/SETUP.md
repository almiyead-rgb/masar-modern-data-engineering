<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Current runtime update · dbt connection authored</h2><p>The earlier adapter-configuration gap is now addressed in source: a local session profile, isolated source registration, six models, seven singular tests and a serial native runner. Engine validation is still blocked. See <a href="RUNTIME_DBT.md">the current runtime target</a>. No remote repository has been created or published.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تحديث البيئة الحالي · إعداد اتصال dbt</h2><p>عولج نقص إعداد الموصل في الملفات: ملف جلسة محلية، وتسجيل مصادر معزولة، وستة نماذج وسبعة اختبارات منفردة ومشغّل أصلي متسلسل. يظل التحقق من المحركات متوقفًا. راجع <a href="RUNTIME_DBT.md">هدف البيئة الحالي</a>. لم يُنشأ مستودع بعيد ولم يُنشر شيء.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Environment and execution boundaries</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>البيئة وحدود التنفيذ</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../docs/START_HERE.md">Start here</a> · <a href="../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../docs/START_HERE.md">ابدأ هنا</a> · <a href="../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Free and bounded</h2><p>No paid API, payment card, subscription or time-limited paid trial is part of the required path. Small source inspection and cost calculations use Python standard-library code. A Jupyter installation is needed to execute the notebooks; those helper scripts can also run directly from the repository root.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>مجاني ومحدود النطاق</h2><p>لا يدخل في المسار المطلوب API مدفوع أو بطاقة دفع أو اشتراك أو تجربة مدفوعة مؤقتة. يستخدم فحص المصادر وحساب التكلفة مكتبات Python القياسية. يحتاج تشغيل الدفاتر إلى Jupyter؛ ويمكن تشغيل سكربتات المساعدة مباشرة من جذر المستودع.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Readiness before installation</h2><p>Spark and Delta are still unverified in this build. Ten native engine notebook drafts are in this repository, explicitly marked ENGINE_NOT_EXECUTED. Historical attempt logs and the current runtime evidence are explicitly labeled in the evidence directory; the setup below is a candidate, not a tested classroom environment. Kafka/GX and classroom/Colab execution also remain unverified. Do not install an entire service stack merely to inspect the source files.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الجاهزية قبل التثبيت</h2><p>Spark وDelta غير متحققين في هذه النسخة. توجد عشر مسودات لدفاتر المحركات في المستودع بحالة ENGINE_NOT_EXECUTED صراحة. تحفظ سجلات المحاولات السابقة والحالية بحالتها الصريحة في مجلد الأدلة؛ والإعداد أدناه مرشح لا بيئة قاعة مختبرة. كذلك لم يتحقق تشغيل Kafka وGX أو بيئة القاعة وColab. لا تثبت منظومة الخدمات كاملة لمجرد فحص المصادر.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Run verified helper commands</h2><p>From the repository root, these commands verify the fixed inputs and the repository structure. They do not start Spark or claim a lakehouse has been built.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تشغيل أوامر المساعدة المتحققة</h2><p>من المجلد الرئيسي، تتحقق الأوامر من البيانات الثابتة وهيكل المستودع. لا تشغل Spark ولا تدعي بناء Lakehouse.</p></td></tr></tbody>
</table>


<div dir="ltr">

```bash
python scripts/inspect_sources.py
python scripts/cost_model.py
python -m unittest discover -s tests -v
python scripts/check_repository.py
```

</div>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Notebook execution</h2><p>Keep the whole repository together: notebooks import shared code from <code>src/masar/</code> and read <code>data/masar-small-v1/</code>. Outputs written by a rerun go to a new folder under <code>outputs/</code>; existing learner work is not deleted. Six supporting notebooks across the five days have executed reference outputs; the ten native notebooks remain unverified. Use the ordered learner route, not filenames alone, to decide what follows what. The native Day 2 notebooks reuse the successful Day 1 workspace; they do not delete old work.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تشغيل الدفاتر</h2><p>احتفظ بالمستودع كاملًا: تستورد الدفاتر الكود المشترك من <code dir="ltr">src/masar/</code>، وتقرأ <code dir="ltr">data/masar-small-v1/</code>. تكتب الإعادة مخرجاتها في مجلد جديد داخل <code dir="ltr">outputs/</code> دون حذف عمل الطالب. تتوفر ستة دفاتر مساندة عبر الأيام الخمسة بمخرجات مرجعية فعلية؛ وتبقى الدفاتر الأصلية العشرة غير متحقق منها. اتبع مسار المتدرب المرتب بدل الاعتماد على أسماء الملفات وحدها. يعيد دفترا اليوم الثاني الأصليان استخدام مساحة اليوم الأول الناجحة دون حذف العمل السابق.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Before classroom release</h2><p>A complete release requires clean end-to-end engine runs, saved outputs, repeatability, the selected hosting/local environment test. After content approval and authorization to publish, live GitHub rendering and public access are checked separately. The initial helper checks are not this release gate.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>قبل اعتماد القاعة</h2><p>يتطلب الإصدار الكامل تشغيل المحركات من البداية إلى النهاية ببيئة نظيفة، وحفظ المخرجات وإعادة الإنتاج، واختبار البيئة المحلية أو المستضافة المختارة. وبعد اعتماد المحتوى والإذن بالنشر، يفحص عرض GitHub والوصول العام بصورة منفصلة. فحوص المساعدة الأولى ليست بوابة الإصدار هذه.</p></td></tr></tbody>
</table>


<table dir="ltr" width="100%"><thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead><tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Candidate engine setup — provision before class</h2><p>Target: Python 3.11 for the unified native runtime, Java 17, PySpark 3.5.8 and delta-spark 3.3.2. The version pair follows the <a href="https://docs.delta.io/releases/">Delta compatibility matrix</a>; Java requirements follow <a href="https://spark.apache.org/docs/3.5.8/">Spark 3.5.8</a>. Documentation compatibility is not a successful runtime test. Use an isolated environment; no GPU, paid cloud, external data account or API key is required by the lab design.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>إعداد المحرك المرشح — يُجهز قبل القاعة</h2><p>المستهدف: Python 3.11 لبيئة التشغيل الأصلية الموحدة، وJava 17، وPySpark 3.5.8 وdelta-spark 3.3.2. يستند الاقتران إلى <a href="https://docs.delta.io/releases/">مصفوفة توافق Delta</a>، ومتطلبات Java إلى <a href="https://spark.apache.org/docs/3.5.8/">Spark 3.5.8</a>. التوافق في التوثيق لا يساوي نجاح التشغيل. تستخدم بيئة معزولة؛ ولا يتطلب تصميم اللاب GPU أو سحابة مدفوعة أو حساب بيانات خارجيًا أو مفتاح API.</p></td></tr></tbody></table>


<table dir="ltr" width="100%"><thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead><tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Install and verify only in the preparation environment</h2><p>With a compatible Java already installed, activate a dedicated Python environment, then use the commands below. Package installation needs connectivity or a previously prepared package cache. First Delta startup may also resolve Maven JAR dependencies via the <a href="https://docs.delta.io/quick-start/">standard Delta helper</a>. Notebook sessions must use that same environment. A successful package installation alone does not close the engine-validation gap.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التثبيت والتحقق في بيئة الإعداد فقط</h2><p>بعد توفر Java متوافقة، فعّل بيئة Python مخصصة ثم استخدم الأوامر أدناه. يحتاج تثبيت الحزم إلى اتصال أو حزم مهيأة مسبقًا. وقد يجلب إقلاع Delta الأول ملفات Maven JAR بواسطة <a href="https://docs.delta.io/quick-start/">أداة Delta القياسية</a>. يجب أن تستخدم الدفاتر البيئة نفسها. نجاح التثبيت وحده لا يغلق فجوة التحقق من المحرك.</p></td></tr></tbody></table>

```bash
python -m pip install -r requirements-course.txt
python -m pip check
python scripts/run_day01.py
```



<table dir="ltr" width="100%"><thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead><tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Open the native engine notebooks in order</h2><p><a href="../notebooks/day01/03_bronze_delta.ipynb">03 · Bronze</a> creates a fresh workspace and records success only after its actual checks. <a href="../notebooks/day01/04_spark_scan.ipynb">04 · Spark scans</a> consumes that recorded successful workspace. Missing prerequisites stop execution; there is no silent fallback to Python, no automated publishing and no deletion of an old run. Colab and a no-network runtime distribution have not been tested.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>افتح دفاتر المحرك بالترتيب</h2><p>ينشئ <a href="../notebooks/day01/03_bronze_delta.ipynb">03 · Bronze</a> مساحة جديدة ويسجل النجاح بعد فحوصه الفعلية فقط. ويستخدم <a href="../notebooks/day01/04_spark_scan.ipynb">04 · قياس Spark</a> مساحة العمل الناجحة المسجلة. يتوقف التنفيذ عند نقص المتطلبات؛ دون بديل Python صامت أو نشر آلي أو حذف تشغيل سابق. لم تختبر Colab أو توزيعة تشغيل دون شبكة.</p></td></tr></tbody></table>


<table dir="ltr" width="100%"><thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead><tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Two different gates</h2><p><code>python scripts/check_repository.py</code> checks source structure, links and declared notebook status; explicit drafts are warnings. <code>python scripts/check_repository.py --release</code> blocks a teaching release until lab and runtime evidence are complete. It does not require an already-published repository and does not authorize creating one.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>فحصان مختلفان</h2><p>يفحص <code>python scripts/check_repository.py</code> البنية والروابط وحالة الدفاتر؛ وتظهر المسودات المعلنة كتنبيهات. ويمنع <code>python scripts/check_repository.py --release</code> اعتماد الإصدار التدريسي حتى تكتمل اللابات وأدلة التشغيل. لا يشترط وجود مستودع منشور مسبقًا، ولا يمنح إذنًا بإنشائه.</p></td></tr></tbody></table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Day 3 continues the existing workspace</h2><p>After actual native Days 1 and 2 succeed, follow <a href="../day03/README.md">Day 3</a>. Use the existing completed workspace, not reference rows as a replacement Delta table. The new CLI is <code>python scripts/run_day03.py --part all</code>. It does not install packages, change source files, or reset previous runs.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>اليوم الثالث يستكمل مساحة العمل السابقة</h2><p>بعد نجاح اليومين الأول والثاني فعليًا بالمحرك، اتبع <a href="../day03/README.md">اليوم الثالث</a>. استخدم مساحة العمل المكتملة السابقة، لا صفوف المرجع لبناء بديل عن جدول Delta. الأمر الجديد <code>python scripts/run_day03.py --part all</code>. لا يثبت حزمًا، ولا يغير ملفات المصدر، ولا يعيد ضبط التشغيلات السابقة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Day 4 adds one local broker and a quality framework</h2><p><a href="../day04/SETUP.md">Day 4 setup</a> pins the candidate client/framework versions and a one-broker local Kafka container. Follow its same-machine boundary: a Colab localhost is not your computer. Installation and native execution are not verified in this build. Keep the reference notebook separate from broker and GX proof.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>يضيف اليوم الرابع وسيطًا محليًا وإطار جودة</h2><p>يثبت <a href="../day04/SETUP.md">إعداد اليوم الرابع</a> الإصدارات المرشحة للعميل والإطار وحاوية Kafka محلية ذات وسيط واحد. التزم بحد الجهاز نفسه؛ localhost في Colab ليس جهازك الشخصي. التثبيت والتنفيذ الأصلي غير متحققين في هذه النسخة. افصل الدفتر المرجعي عن إثبات الوسيط وGX.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Packaged local setup</h2><p>The <a href="RUNTIME_WORKBENCH.md">local workbench recipe</a> brings the same native dependencies together. It is a preparation path, not a completed image or an execution success claim.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تجهيز محلي مجمّع</h2><p>يجمع <a href="RUNTIME_WORKBENCH.md">وصف بيئة التشغيل المحلية</a> التبعيات الأصلية نفسها. هو مسار تجهيز، وليس صورة مكتملة أو إعلان نجاح تشغيل.</p></td></tr></tbody>
</table>
