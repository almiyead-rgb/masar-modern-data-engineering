<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 4 · Streaming contract</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الرابع · عقد التدفق</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Two identities, two checks</h2><p>Transport key: (topic, partition, offset). Business key: event_id. Require unique transport positions after resume; allow deliberate repeated business events in raw Bronze; reject conflicting payloads before business deduplication.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>هويتان وفحصان</h2><p>مفتاح النقل: الموضوع والقسم والإزاحة. مفتاح الأعمال: event_id. يجب ألا تتكرر مواقع النقل بعد الاستئناف؛ يُسمح بتكرار حدث الأعمال عمدًا في Bronze الخام، ويُرفض تعارض المحتوى قبل إزالة تكرار الأعمال.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Payload schema</h2><ul><li>event_id: non-empty string.</li><li>trip_id: identifier in the corrected Silver trip table.</li><li>event_ts: ISO timestamp with explicit timezone.</li><li>city: Riyadh, Jeddah or Dammam.</li><li>location: numeric finite lat in [-90,90], lon in [-180,180].</li><li>synthetic: exactly true; no extra payload fields.</li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>مخطط الرسالة</h2><ul><li>event_id: نص غير فارغ.</li><li>trip_id: معرف موجود في جدول Silver المصحح.</li><li>event_ts: توقيت ISO مع منطقة زمنية صريحة.</li><li>city: الرياض أو جدة أو الدمام بالقيم الإنجليزية المتفق عليها.</li><li>location: خط عرض محدود بين -90 و90 وخط طول بين -180 و180 دون قيم غير منتهية.</li><li>synthetic: القيمة true فقط، دون أعمدة إضافية في الرسالة.</li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Source batches, unchanged</h2><p>gps.ndjson: 216 messages. gps_replay.ndjson: 2 existing events. gps_late.ndjson: 1 new event with an old timestamp. Total messages: 219. Distinct events: 217. The producer preserves each source JSON line; it does not rewrite dates to today.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>دفعات المصدر دون تغيير</h2><p>gps.ndjson: عدد 216 رسالة. gps_replay.ndjson: حدثان معروفان. gps_late.ndjson: حدث جديد بوقت قديم. المجموع 219 رسالة و217 حدثًا مختلفًا. يحفظ المنتج كل سطر JSON كما هو؛ لا يغير التواريخ إلى تاريخ اليوم.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Checkpoint ownership</h2><p>One checkpoint per query/run pair. The four test phases share that checkpoint and destination. A new complete lab run receives a fresh topic, target and checkpoint. Existing topics are never deleted or reused silently. A stopped or failed publish intent is retained for diagnosis.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ملكية نقطة التحقق</h2><p>نقطة تحقق واحدة لكل استعلام ضمن تشغيله. تشترك المراحل الأربع في النقطة والوجهة نفسيهما. يحصل التشغيل الكامل الجديد على موضوع ووجهة ونقطة جديدة. لا تحذف الموضوعات السابقة أو تعاد استخدامها بصمت، ويحفظ سجل إرسال متوقف أو فاشل للتشخيص.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Local service boundary</h2><p>The broker binds only to 127.0.0.1:9092. Spark and the Python producer run on that same machine. A remote Colab notebook cannot reach your laptop through its own localhost. Keep the broker storage and the checkpoint; do not remove volumes during a resume experiment. There is no authentication, TLS or failover in this synthetic single-broker lab.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حدود الخدمة المحلية</h2><p>يرتبط الوسيط محليًا فقط بالعنوان 127.0.0.1:9092. يعمل Spark والمنتج على الجهاز نفسه. لا يصل دفتر Colab البعيد إلى الحاسب الشخصي عبر localhost الخاص به. احتفظ بتخزين الوسيط ونقطة التحقق ولا تحذف وحدات التخزين أثناء تجربة الاستئناف. لا يوفر اللاب الاصطناعي أحادي الوسيط مصادقة أو TLS أو تجاوز أعطال.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Evidence boundary</h2><p>Record actual acknowledgments, offsets, query IDs, progress reports, checkpoint files and Delta artifacts. Reference counts alone do not prove delivery or recovery. See <a href="SOURCES.md">S1–S5 and S13</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حدود الدليل</h2><p>احفظ التأكيدات والإزاحات وهويات الاستعلام وتقارير التقدم وملفات نقطة التحقق وأدلة Delta الفعلية. الأعداد المرجعية وحدها لا تثبت النقل أو الاستعادة. راجع <a href="SOURCES.md">S1–S5 وS13</a>.</p></td></tr></tbody>
</table>
