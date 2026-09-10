<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 4 · Concepts before implementation</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الرابع · المفاهيم قبل التطبيق</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Execution record</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">سجل التنفيذ</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Learning goal</h2><p>Explain one event through the pipeline, then justify when a candidate must be stopped. Read alongside the <a href="STREAM_CONTRACT.md">stream contract</a> and <a href="QUALITY_POLICY.md">quality policy</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>هدف التعلم</h2><p>تتبع حدثًا واحدًا عبر الخط، ثم برر متى يجب إيقاف البيانات المرشحة. اقرأ مع <a href="STREAM_CONTRACT.md">عقد التدفق</a> و<a href="QUALITY_POLICY.md">سياسة الجودة</a>.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>01 · Continuous arrival, bounded classroom run</h2><p>An event describes something that happened, such as a synthetic GPS observation. Our file supplies reproducible input to a real Kafka producer; it is not itself a Kafka broker. The lab drains currently available messages with availableNow, which lets a classroom exercise finish instead of waiting forever.</p><p>Reference: S1, S2 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>01 · وصول مستمر وتجربة محدودة</h2><p>الحدث يصف شيئًا وقع، مثل رصد موقع اصطناعي. يقدم الملف مدخلات قابلة للإعادة إلى منتج Kafka فعلي؛ الملف ليس وسيط Kafka. يستخدم اللاب availableNow لمعالجة الرسائل المتاحة ثم الانتهاء، بدل ترك التمرين ينتظر بلا نهاية.</p><p>الاستناد: S1, S2 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>02 · Producer, broker and consumer</h2><p>The producer sends JSON. Kafka stores messages. Spark consumes them and writes a Delta table. Ask three separate questions: was the send acknowledged, was the message consumed, and was the Delta write committed? One success does not prove all three.</p><p>Reference: S1, S3, S5 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>02 · المنتج والوسيط والمستهلك</h2><p>يرسل المنتج JSON، ويحفظ Kafka الرسائل، ويقرأها Spark ليكتب جدول Delta. اسأل ثلاث مرات: هل تأكد الإرسال؟ هل قُرئت الرسالة؟ هل ثُبتت الكتابة في Delta؟ نجاح خطوة لا يثبت نجاح جميع الخطوات.</p><p>الاستناد: S1, S3, S5 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>03 · Topic and partition</h2><p>Think of a topic as the named event channel and a partition as one ordered lane. This exercise creates two partitions. A trip identifier is the message key, so one trip follows a consistent lane while the topic configuration remains stable. Do not infer a global order across lanes.</p><p>Reference: S13 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>03 · الموضوع والقسم</h2><p>الموضوع قناة مسماة للأحداث، والقسم مسار مرتب داخلها. ننشئ قسمين. نستخدم معرف الرحلة مفتاحًا للرسالة كي تتبع أحداث الرحلة مسارًا متسقًا مع ثبات الإعداد. لا تستنتج ترتيبًا عامًا بين القسمين.</p><p>الاستناد: S13 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>04 · Offset is not a business key</h2><p>A message location is the combination of topic, partition and offset. The event_id identifies the real-world observation in the teaching model. Sending the same observation again can create another offset with the same event_id. Therefore record both identities.</p><p>Reference: S1 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>04 · الإزاحة ليست مفتاح أعمال</h2><p>هوية موضع الرسالة تتكون من الموضوع والقسم والإزاحة. أما event_id فيعرّف الرصد في نموذج التدريب. قد ينشئ إرسال الرصد مرة ثانية إزاحة جديدة تحمل معرف الحدث نفسه؛ لذا نحفظ الهويتين.</p><p>الاستناد: S1 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>05 · Acknowledgment does not remove deliberate duplicates</h2><p>We request acknowledgments and enable producer idempotence for transport retries. When our program deliberately calls send again in a new phase, that is a new send, not a deduplicated business decision. The application still needs event-key conflict checks.</p><p>Reference: S5, S13 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>05 · تأكيد الاستلام لا يلغي إعادة الإرسال المقصودة</h2><p>نطلب تأكيد الاستلام ونفعّل عدم التكرار لمعالجة محاولات النقل. لكن استدعاء send عمدًا في مرحلة جديدة إرسال جديد، وليس قرارًا لإزالة تكرار الأعمال. لا بد من فحص معرفات الأحداث والتعارض بينها.</p><p>الاستناد: S5, S13 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>06 · Preserve raw deliveries in Bronze</h2><p>Bronze keeps raw_json and transport metadata. We do not delete a late event just because it is inconvenient. The Day 4 stream uses a distinct path from Day 1 GPS ingestion; combining both blindly would double-count the base sample.</p><p>Reference: Masar design · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>06 · حفظ الوصول الخام في Bronze</h2><p>تحفظ Bronze النص الخام وبيانات النقل. لا نحذف حدثًا متأخرًا لأنه غير ملائم. يستخدم تدفق اليوم الرابع مسارًا منفصلًا عن استقبال GPS في اليوم الأول؛ جمع المسارين دون تمييز يضاعف عينة الأساس.</p><p>الاستناد: Masar design · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>07 · What a checkpoint remembers</h2><p>A Spark checkpoint records the progress of a streaming query. Reuse it with the same compatible query, source and destination to test resume. The startingOffsets setting initializes a new query; it is not a command to reset an existing checkpoint.</p><p>Reference: S1, S2 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>07 · ما الذي تتذكره نقطة التحقق؟</h2><p>تحفظ نقطة تحقق Spark تقدم الاستعلام المتدفق. أعد استخدامها مع الاستعلام المتوافق والمصدر والوجهة نفسيهما لاختبار الاستئناف. يحدد startingOffsets بداية استعلام جديد؛ وليس أمرًا لتصفير نقطة تحقق موجودة.</p><p>الاستناد: S1, S2 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>08 · Restart test versus crash guarantee</h2><p>Our first run expects 216 transport rows. A clean stop and resume without new sends should leave 216. Save query identity, execution identity and checkpoint files. This is evidence for that scenario, not proof of arbitrary crashes, broker failover or a multi-node deployment.</p><p>Reference: Masar design; S2 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>08 · اختبار الاستئناف لا يساوي ضمان الأعطال</h2><p>نتوقع 216 صف نقل في التشغيل الأول. يفترض أن يظل العدد 216 بعد إنهاء سليم واستئناف بلا إرسال جديد. احفظ هوية الاستعلام وهوية التنفيذ وملفات نقطة التحقق. هذا دليل للسيناريو المحدد، لا ضمان لجميع الأعطال أو فقد وسيط أو تشغيل متعدد العقد.</p><p>الاستناد: Masar design; S2 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>09 · Event time, broker time and processing time</h2><p>event_ts comes from the observation. broker_timestamp belongs to Kafka metadata and depends on broker timestamp policy. ingested_at marks processing into Bronze. Keep these meanings separate; do not label all three as event time.</p><p>Reference: S1 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>09 · وقت الحدث والوسيط والمعالجة</h2><p>يأتي event_ts من الرصد. ويخص broker_timestamp بيانات Kafka ويتأثر بسياسة التوقيت في الوسيط. أما ingested_at فيسجل وقت المعالجة إلى Bronze. افصل المعاني ولا تسمّها جميعًا وقت الحدث.</p><p>الاستناد: S1 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>10 · A late event is not necessarily invalid</h2><p>The supplied late event has a new event_id and an old event_ts. It adds one distinct observation after replay. Lateness is a timing property; invalid coordinates or a missing key are quality defects. Handle them by different policies.</p><p>Reference: Masar source fixtures · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>10 · الحدث المتأخر ليس معيبًا بالضرورة</h2><p>للحدث المتأخر المرفق معرف جديد ووقت قديم، فيضيف رصدًا مختلفًا بعد الإعادة. التأخر خاصية زمنية، أما الإحداثيات المعيبة أو المفتاح المفقود فأخطاء جودة. لكل منهما سياسة مختلفة.</p><p>الاستناد: Masar source fixtures · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>11 · Watermarks are not wall-clock expiry</h2><p>A watermark helps bound state in supported event-time operations. It is not a universal delete rule on Bronze. This lab does not execute a stateful watermark experiment; it preserves the late event and asks you to explain the trade-off between waiting and bounded state.</p><p>Reference: S2 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>11 · العلامة المائية ليست انتهاءً بحسب ساعة الجهاز</h2><p>تساعد العلامة المائية على ضبط حجم الحالة في عمليات تدعم وقت الحدث، وليست قاعدة حذف عامة لطبقة Bronze. لا ينفذ هذا اللاب تجربة علامة مائية ذات حالة؛ يحفظ الحدث المتأخر ويطلب تفسير الموازنة بين الانتظار وحجم الحالة.</p><p>الاستناد: S2 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>12 · Data quality needs an explicit contract</h2><p>State the row grain, required columns, types, valid ranges and relationships before calling data good. The contract here is one row per trip. A valid decimal fare, a known driver and a positive duration address different failure modes.</p><p>Reference: Masar quality policy · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>12 · الجودة تحتاج عقدًا واضحًا</h2><p>حدد معنى الصف والأعمدة والأنواع والنطاقات والعلاقات قبل وصف البيانات بالجيدة. العقد هنا صف واحد لكل رحلة. الأجرة العشرية الصحيحة والسائق المعروف والمدة الموجبة تعالج أخطاء مختلفة.</p><p>الاستناد: Masar quality policy · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>13 · Expectation, suite and Checkpoint</h2><p>An Expectation is a testable assertion. A suite groups assertions. A GX Checkpoint runs validation definitions and actions, including local Data Docs updates. A GX Checkpoint is not a Spark streaming checkpoint, even though the English name overlaps.</p><p>Reference: S6, S7, S8 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>13 · التوقع ومجموعة الفحوص ونقطة التنفيذ</h2><p>التوقع قاعدة قابلة للفحص، وتجمعها مجموعة فحوص. تشغل نقطة التنفيذ في GX تعريفات التحقق والإجراءات ومنها تحديث تقارير Data Docs المحلية. لا تخلط بينها وبين نقطة تحقق Spark رغم تشابه الاسم الإنجليزي.</p><p>الاستناد: S6, S7, S8 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>14 · Fail, quarantine, revalidate</h2><p>The mixed candidate has 82 rows: 75 trusted rows and 7 deliberate probes. We fail the whole candidate and isolate the seven bad rows with reasons. A clean subset is a new candidate; it must pass a fresh GX run before it is eligible for downstream use.</p><p>Reference: Masar strict promotion policy · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>14 · ارفض واعزل ثم أعد التحقق</h2><p>تضم الدفعة المرشحة 82 صفًا: 75 موثوقًا و7 حالات اختبار معيبة. نرفض الدفعة كاملة ونعزل السبعة بأسبابها. المجموعة المنقحة مرشح جديد لا يُستخدم لاحقًا قبل اجتياز فحص GX جديد.</p><p>الاستناد: Masar strict promotion policy · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>15 · Quality is more than row validity</h2><p>All present rows can be valid while half the delivery is missing. Monitor volume, schema, freshness and distribution as well. In this fixed exercise, the expected trip count is 75; do not copy that constant into a real production monitor.</p><p>Reference: Masar monitoring policy · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>15 · الجودة أوسع من صحة الصف</h2><p>قد تكون الصفوف الموجودة سليمة ونصف الدفعة مفقودًا. راقب الحجم والمخطط والحداثة والتوزيع أيضًا. العدد المتوقع هنا 75 ضمن تمرين ثابت؛ لا تنقل هذه القيمة الثابتة إلى مراقبة إنتاجية حقيقية.</p><p>الاستناد: Masar monitoring policy · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>16 · Reconcile before drawing a conclusion</h2><p>Expected transport counts are 216 → 216 → 218 → 219. Expected distinct event counts are 216 → 216 → 216 → 217. For quality: 82 = 75 accepted + 7 quarantined, and the retained fare total stays 1880.60 SAR. These are source-derived expectations until native output is available.</p><p>Reference: Executed source reference · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>16 · سوِّ الأعداد قبل الاستنتاج</h2><p>أعداد النقل المتوقعة 216 ثم 216 ثم 218 ثم 219؛ والأحداث المختلفة 216 ثم 216 ثم 216 ثم 217. وفي الجودة: 82 = 75 مقبولًا + 7 معزولة، ويبقى مجموع الأجور 1880.60 ريال. هذه توقعات مشتقة من المصدر حتى تتوفر مخرجات المحرك.</p><p>الاستناد: Executed source reference · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>17 · Governance travels with the data</h2><p>Document purpose, ownership, lineage, access and retention beside each output. A folder named restricted is not an enforced access control. Keep raw GPS and quarantine details out of public submissions even when practicing the design on synthetic data.</p><p>Reference: Masar design; S10–S12 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>17 · الحوكمة ترافق البيانات</h2><p>وثق الغرض والملكية والتتبع والوصول والاحتفاظ بجانب كل مخرج. تسمية المجلد «مقيد» ليست صلاحية مطبقة. اجعل تفاصيل GPS الخام والعزل خارج التسليم العام حتى عند تدريب التصميم على بيانات اصطناعية.</p><p>الاستناد: Masar design; S10–S12 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>18 · Privacy: synthetic is a boundary, not a magic label</h2><p>Only the supplied synthetic fixtures may be used. Real linked coordinates may make a person identifiable even without a name; assess that risk against the applicable law. Do not automatically classify every coordinate as a legally defined sensitive category. This local lab is not a production privacy deployment.</p><p>Reference: S10–S12 · <a href="SOURCES.md">Sources</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>18 · الخصوصية: الاصطناع قيد وليس ملصقًا سحريًا</h2><p>استخدم الملفات الاصطناعية المرفقة فقط. قد تجعل الإحداثيات الحقيقية المرتبطة ببيانات أخرى الشخص قابلًا للتعرف رغم غياب الاسم؛ قيّم الخطر وفق النظام. لا تصنف كل إحداثية تلقائيًا ضمن الفئات الحساسة المحددة نظامًا. هذا اللاب المحلي ليس تطبيق خصوصية إنتاجيًا.</p><p>الاستناد: S10–S12 · <a href="SOURCES.md">المصادر</a></p></td></tr></tbody>
</table>
