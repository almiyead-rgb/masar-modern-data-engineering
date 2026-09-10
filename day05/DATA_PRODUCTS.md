<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Serving table contracts</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>عقود جداول التقديم</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a> · <a href="../day05/README.md">Day 5</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">الجاهزية</a> · <a href="../day05/README.md">اليوم الخامس</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>One release, eight tables</h2><p>The exact machine-readable column order and keys are in <a href="../src/masar/serving_reference.py">TABLE_COLUMNS and TABLE_KEYS</a>. Monetary sums have two decimal places; duration is seconds; distance is kilometres. JSON NULL exports as an empty CSV field. These table definitions are teaching contracts, not production SLOs.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>إصدار واحد وثمانية جداول</h2><p>يوضح <a href="../src/masar/serving_reference.py">TABLE_COLUMNS وTABLE_KEYS</a> ترتيب الأعمدة والمفاتيح آليًا. للأجور منزلتان عشريتان، وللمدة وحدة الثانية، وللمسافة الكيلومتر. تصدر NULL في CSV كحقل فارغ. التعريفات عقود تدريب لا مستويات خدمة إنتاجية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>gold.zone_hourly_demand</h2><p>One observed city proxy × UTC trip-start hour. Keys: zone_key + hour_utc. Values: trip_count, total_fare_sar, total_duration_seconds. hour_local includes +03:00. Only observed hours are present.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>gold.zone_hourly_demand</h2><p>مدينة تمثيلية وساعة بداية UTC مرصودتان. المفتاح zone_key مع hour_utc. المقاييس عدد الرحلات ومجموع الأجور والثواني. يحمل hour_local إزاحة +03:00. تظهر الساعات المرصودة فقط.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>gold.driver_daily</h2><p>One driver × local trip-start date. Keys: driver_key + trip_date_local. 18 rows in this fixture; totals reconcile to 75 trips and 1880.60 SAR.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>gold.driver_daily</h2><p>سائق واحد وتاريخ بداية محلي. المفتاح driver_key مع trip_date_local. توجد 18 مجموعة في العينة وتتسوى مع 75 رحلة و1880.60 ريال.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>bi.dim_zone</h2><p>Three stable city proxies. zone_key is unique; city is descriptive; zone_resolution is always city_proxy. No finer geography is asserted.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>bi.dim_zone</h2><p>ثلاثة تمثيلات مدن ثابتة. zone_key فريد وcity وصفي وzone_resolution يساوي city_proxy؛ لا ندعي جغرافيا أدق.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>bi.dim_driver</h2><p>Six synthetic drivers. driver_key equals the synthetic source ID; this deliberately simple natural-key dimension has no SCD history. vehicle_type is descriptive, not an automatic AI input.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>bi.dim_driver</h2><p>ستة سائقين اصطناعيين. driver_key يساوي معرف المصدر الاصطناعي؛ وهو بُعد مبسط بمفتاح طبيعي دون سجل SCD. نوع المركبة وصف وليس مدخل AI تلقائيًا.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>bi.dim_date</h2><p>Three observed local start dates, 1–3 June 2026. date_key is YYYYMMDD. This compact teaching dimension is not a complete calendar suitable for every BI time-intelligence function.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>bi.dim_date</h2><p>ثلاثة تواريخ بداية محلية مرصودة، من ١ إلى ٣ يونيو ٢٠٢٦. date_key بصيغة YYYYMMDD. هذا بُعد تعليمي صغير لا تقويم كامل مناسب لكل وظائف التحليل الزمني في BI.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>bi.fact_trips</h2><p>75 unique trip_id rows with dimension keys, UTC start, fare_sar, distance_km, duration_seconds and per-trip gps_event_count. No raw coordinates are exported. Three late trips are retained even without GPS.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>bi.fact_trips</h2><p>75 صفًا بمفاتيح trip_id فريدة، مع مفاتيح الأبعاد وبداية UTC والأجرة والمسافة والمدة وعدد أحداث الرحلة. لا تصدر إحداثيات خام. تبقى الرحلات المتأخرة الثلاث حتى دون GPS.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>ai.zone_hourly_features</h2><p>Three rows: one city proxy at the fixed cutoff. Historical count and duration use completed events in [cutoff−24h, cutoff) and delivery time ≤ cutoff. A missing history has count 0 plus history_available=false and mean NULL, not certified zero activity.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ai.zone_hourly_features</h2><p>ثلاثة صفوف: مدينة لكل لحظة قطع ثابتة. يستخدم العدد والمدة أحداثًا انتهت في [القطع−24ساعة، القطع) ووصلت بحلول القطع. عند غياب التاريخ يكون العدد 0 مع history_available=false ومتوسط NULL، لا تأكيدًا على انعدام النشاط.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>ai.zone_hourly_labels</h2><p>Three entity/horizon rows with target_trip_count=NULL, label_status=UNOBSERVED and label_available_at_utc=NULL. They document missing future ground truth; do not train or evaluate a model on them.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ai.zone_hourly_labels</h2><p>ثلاثة صفوف بمفاتيح المدينة والأفق، مع target_trip_count=NULL وlabel_status=UNOBSERVED ووقت إتاحة NULL. توثق غياب الحقيقة المستقبلية؛ ولا يدرب أو يقيم نموذج عليها.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Read snapshots, not moving targets</h2><p>The release records each Delta table path, version, row count and logical-content SHA-256. Native readback validates the schema, keys, relations and totals before export. A file hash provides integrity checking, not cryptographic proof that a workload executed.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>اقرأ نسخًا ثابتة لا جداول متغيرة</h2><p>يسجل الإصدار مسار كل جدول Delta ونسخته وعدد صفوفه وبصمة SHA-256 للمحتوى المنطقي. تفحص القراءة الفعلية المخطط والمفاتيح والعلاقات والإجماليات قبل التصدير. تتحقق بصمة الملف من سلامته، لكنها ليست إثباتًا تشفيريًا لتنفيذ حمل العمل.</p></td></tr></tbody>
</table>
