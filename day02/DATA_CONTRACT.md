<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 2 · Silver data contract</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الثاني · عقد بيانات Silver</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../README.md">Course home</a> · <a href="../STATUS.md">Execution record</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">سجل التنفيذ</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Scope and grain</h2><p>Exactly one row per trip_id. Source revision is 1 for the Day 2 base and late fixtures. Fields describe completed trips and do not by themselves form a leakage-safe ML feature set.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>النطاق ومستوى الصف</h2><p>صف واحد فقط لكل trip_id. مراجعة المصدر 1 للبيانات الأساسية والمتأخرة في اليوم الثاني. تصف الحقول رحلات مكتملة، ولا تشكل وحدها خصائص تعلم آلي آمنة من تسرب المعلومات.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>trip_id</code></h2><p>string · Non-empty unique business identity.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>trip_id</code></h2><p>string · هوية أعمال غير فارغة وفريدة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>driver_id</code></h2><p>string · Must match one unique driver.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>driver_id</code></h2><p>string · يطابق سائقًا واحدًا بمفتاح فريد.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>city</code></h2><p>string · Riyadh, Jeddah or Dammam.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>city</code></h2><p>string · إحدى Riyadh أو Jeddah أو Dammam.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>start_utc / end_utc</code></h2><p>timestamp · Offset-aware input; UTC session; end strictly after start.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>start_utc / end_utc</code></h2><p>timestamp · مدخلات تتضمن إزاحة زمنية؛ جلسة UTC؛ النهاية بعد البداية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>trip_date_local</code></h2><p>date · Start date in Asia/Riyadh, not ingestion date.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>trip_date_local</code></h2><p>date · تاريخ البداية في Asia/Riyadh وليس تاريخ الاستقبال.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>fare_sar</code></h2><p>decimal(12,2) · Non-negative SAR, two source decimals at most; no silent rounding.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>fare_sar</code></h2><p>decimal(12,2) · ريال غير سالب، منزلتان عشريتان بالمصدر كحد أقصى، دون تقريب صامت.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>distance_km</code></h2><p>decimal(12,2) · Strictly positive kilometers.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>distance_km</code></h2><p>decimal(12,2) · مسافة موجبة بالكيلومتر.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>duration_seconds</code></h2><p>long · Full timestamp difference in whole seconds, strictly positive.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>duration_seconds</code></h2><p>long · فرق التوقيتين الكاملين بالثواني الصحيحة، موجب.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>vehicle_type</code></h2><p>string · sedan or suv, from the unique driver dimension.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>vehicle_type</code></h2><p>string · sedan أو suv من جدول السائقين ذي المفاتيح الفريدة.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>driver_rating</code></h2><p>decimal(3,1) · Between 0 and 5; descriptive fixture attribute, not point-in-time history.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>driver_rating</code></h2><p>decimal(3,1) · من 0 إلى 5؛ صفة وصفية في العينة وليست تاريخًا محفوظًا عند كل نقطة زمنية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>source_revision</code></h2><p>integer · 1 today; do not derive from ingestion time.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>source_revision</code></h2><p>integer · 1 اليوم؛ لا تشتقها من وقت الاستقبال.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>_source_file / _source_sha256</code></h2><p>string · Stable source provenance retained in native Silver.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>_source_file / _source_sha256</code></h2><p>string · معلومات المصدر الثابتة المحفوظة في Silver الأصلية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2><code>_payload_hash</code></h2><p>string · Native hash used for conflict detection; business comparison excludes operational metadata.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2><code>_payload_hash</code></h2><p>string · بصمة أصلية لكشف التعارض؛ تستبعد مقارنة الأعمال المعلومات التشغيلية.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Rejection policy</h2><p>Reject unknown cities, missing keys, orphan drivers, invalid times, non-positive duration/distance, negative/non-finite/overflowing fares and excessive decimal precision. Stop before publishing an invalid native table; do not conceal failures by dropping rows. The seven quality fixture records are inspected in reference tests only today.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>سياسة الرفض</h2><p>ارفض المدن غير المعروفة والمفاتيح المفقودة والسائقين غير المطابقين والتوقيتات غير الصالحة والمدة أو المسافة غير الموجبة والأجور السالبة أو غير المنتهية أو المتجاوزة للحد والدقة العشرية الزائدة. توقف قبل نشر جدول أصلي معيب؛ لا تخف الفشل بحذف الصفوف. تفحص سجلات عينة الجودة السبعة في الاختبارات المرجعية فقط اليوم.</p></td></tr></tbody>
</table>
