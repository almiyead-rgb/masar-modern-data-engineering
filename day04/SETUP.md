<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 4 · One-machine setup</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الرابع · إعداد على جهاز واحد</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Execution record</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">سجل التنفيذ</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Prepare your environment</h2><p>Use a dedicated virtual environment (Python 3.11 is the preferred classroom target), Java 17, and Docker Engine with Compose. The source-reference notebook uses the standard library and does not need the services. Actual native notebooks need the full preceding project state.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>جهز قبل التدريب</h2><p>استخدم بيئة افتراضية مستقلة؛ Python 3.11 هو الهدف المفضل للقاعة، مع Java 17 وDocker Engine وCompose. لا يحتاج الدفتر المرجعي إلى الخدمات، لأنه يستخدم المكتبة القياسية؛ أما الدفاتر الأصلية فتحتاج حالة المشروع السابق كاملة.</p></td></tr></tbody>
</table>

```bash
python -m venv .venv
# Activate this environment using the command for your operating system.
python -m pip install -r requirements-day04.txt
docker compose -f infrastructure/kafka/compose.yaml up -d --wait --wait-timeout 120
python scripts/run_day04.py --preflight
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Execute from the repository root</h2><p>After Days 1–3 have actually passed, use the notebook or these commands. Choose one route; running both creates separate full test runs, not a checkpoint resume. No GPU, external dataset account or paid API is required by the code.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>نفذ من جذر المستودع</h2><p>بعد نجاح الأيام 1–3 فعليًا، استخدم الدفتر أو الأوامر التالية. اختر مسارًا واحدًا؛ تنفيذ الاثنين ينشئ تشغيلين كاملين لا استئنافًا لنقطة تحقق. لا يتطلب الكود GPU أو حساب بيانات خارجيًا أو واجهة مدفوعة.</p></td></tr></tbody>
</table>

```bash
python scripts/run_day04.py --part streaming
python scripts/run_day04.py --part quality
# Stop the broker after the exercise without deleting its volume.
docker compose -f infrastructure/kafka/compose.yaml stop
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Error interpretation</h2><ul><li>Missing package: provision the pinned environment; do not bypass the preflight.</li><li>Kafka connection: verify the same-machine boundary and advertised listeners.</li><li>Unknown Spark kafka source: the matching spark-sql-kafka connector and JAR dependencies must be available.</li><li>Missing Day 3 report: complete prior native labs; the reference is not a substitute.</li><li>Partial send: preserve the intent and offsets; do not automatically resend the fixture.</li><li>Missing GX Data Docs: validation alone does not satisfy the report requirement.</li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تفسير الأخطاء</h2><ul><li>حزمة مفقودة: جهز البيئة المثبتة ولا تتجاوز الفحص الأولي.</li><li>اتصال Kafka: تحقق من العمل على الجهاز نفسه والعناوين المعلنة.</li><li>مصدر kafka غير معروف في Spark: وفر الموصل المطابق وتبعيات JAR.</li><li>تقرير اليوم الثالث مفقود: أكمل اللابات الأصلية؛ المرجع لا يستبدلها.</li><li>إرسال جزئي: احفظ النية والإزاحات ولا تعِد الدفعة آليًا.</li><li>Data Docs مفقودة: نجاح الفحص وحده لا يحقق متطلب التقرير.</li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Safety and portability</h2><p>The Compose volume is named; the host port is loopback-only. Do not use down -v or reset checkpoints as a repair shortcut. Do not expose this unauthenticated broker publicly. Hosted notebooks require a co-located broker or an explicitly provisioned secure route; the local setup is not claimed to work on Colab.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>السلامة وقابلية النقل</h2><p>وحدة التخزين في Compose مسماة والمنفذ محلي فقط. لا تستخدم down -v أو تصفير النقاط اختصارًا للإصلاح، ولا تعرض الوسيط بلا مصادقة للعامة. تحتاج الدفاتر المستضافة وسيطًا معها أو مسارًا آمنًا مجهزًا صراحة؛ لا يُدّعى تشغيل هذا الإعداد المحلي في Colab.</p></td></tr></tbody>
</table>
