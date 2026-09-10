<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Runtime acceptance boundaries</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>حدود قبول التشغيل</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><a href="../README.md">Course home</a> · <a href="START_HERE.md">Start here</a> · <a href="../STATUS.md">Readiness</a></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><a href="../README.md">الرئيسية</a> · <a href="START_HERE.md">ابدأ هنا</a> · <a href="../STATUS.md">الجاهزية</a></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Three separate decisions</h2><p>Source authoring QA checks code structure, documentation and saved reference outputs. Native acceptance requires real engines and readback evidence. Publication is a separate authorization and live-site check. Success in one category does not imply success in another.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ثلاثة قرارات منفصلة</h2><p>يفحص تدقيق البناء بنية الكود والتوثيق والمخرجات المرجعية المحفوظة. ويتطلب قبول التشغيل محركات فعلية وأدلة قراءة للمخرجات. أما النشر فإذن مستقل وفحص للموقع المنشور. النجاح في أحدها لا يعني النجاح في الآخر.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>What the actual pipeline must prove</h2><p>Two independent native runs must use the fixed dataset and unchanged implementation, distinct workspaces and processes, and all ten ordered stages of the eight labs. The comparison uses the eight Gold/serving content digests, not nondeterministic Parquet byte equality. Each run retains stage reports, measured plans, Delta data/log files, Kafka checkpoint evidence and GX Data Docs.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما يجب أن يثبته المسار الفعلي</h2><p>يستخدم تشغيلان أصليان مستقلان البيانات الثابتة والكود نفسه، وبمساحتي عمل وعمليتين منفصلتين، وينفذان المراحل العشر المرتبة للابات الثمانية. تقارن بصمات محتوى جداول Gold والتقديم الثمانية، لا تطابق بايتات Parquet الذي قد يختلف. يحتفظ كل تشغيل بتقارير المراحل وخطط القياس وملفات بيانات Delta ومعاملاتها وأدلة نقاط تحقق Kafka وData Docs الخاصة بـGX.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Evidence is checked, not just declared</h2><p>The final source checks require named successful checks and the correct scope/dataset. A successful integration run seals an inventory after Spark shutdown. A native acceptance index must point to actual run reports and inventories by relative path and SHA256. Missing, altered or copied run evidence is rejected. Local hashes check consistency; they are not cryptographic attestation against a person who can rewrite every file.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>يفحص الدليل ولا يكتفى بإعلانه</h2><p>تشترط الفحوص أسماء فحوص ناجحة ونطاقًا وبيانات صحيحين. يحفظ التكامل الناجح حصر بصمات الملفات بعد إيقاف Spark. ويجب أن يشير فهرس القبول إلى تقارير التشغيل والحصر الفعلية بمسارات نسبية وبصمات SHA256. يرفض نقص الأدلة أو تغييرها أو نسخ هوية التشغيل. تفحص البصمات المحلية الاتساق، وليست تصديقًا مشفرًا يمنع شخصًا يتحكم بجميع الملفات من إعادة كتابتها.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>dbt has a separate execution gap</h2><p>The native Spark pipeline does not execute dbt. The session profile and runner are now configured in source; they still need an actual verified build. Acceptance needs matching <code>run_results.json</code> and <code>manifest.json</code>, successful model/test nodes and coverage of the supplied six models and seven singular tests. A hand-written PASSED status cannot replace these artifacts.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>لـdbt فجوة تنفيذ مستقلة</h2><p>لا ينفذ مسار Spark الأصلي أداة dbt. أُعد موصل الجلسة وملف اتصاله والمشغّل، ويلزم تنفيذ البناء فعليًا والتحقق منه. يتطلب القبول ملفي <code dir="ltr">run_results.json</code> و<code dir="ltr">manifest.json</code> متطابقي هوية التنفيذ، ونجاح النماذج والاختبارات وتغطية النماذج الستة والاختبارات المفردة السبعة المرفقة. لا تعوض كتابة كلمة PASSED هذه الملفات.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Run the checks without publishing</h2><p>The following commands inspect source or request native execution; none creates a GitHub repository or publishes. A missing prerequisite must stop before the first native stage. The second command is expected to fail while runtime evidence is missing.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الفحوص لا تنشر المستودع</h2><p>تفحص الأوامر التالية المصدر أو تطلب التشغيل الأصلي، ولا تنشئ مستودع GitHub أو تنشره. يجب أن يتوقف التشغيل عند نقص المتطلبات قبل المرحلة الأصلية الأولى. من المتوقع أن يرفض الأمر الثاني اعتماد التدريس ما دامت أدلة المحرك ناقصة.</p></td></tr></tbody>
</table>

```bash
python scripts/check_repository.py
python scripts/check_repository.py --release
python scripts/run_day05.py --part integration --preflight
python scripts/run_day05.py --part integration
```

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Execution versus assessment</h2><p>These acceptance rules protect the course build. They do not add grades, attendance conditions, paid accounts or extra projects. Formal student assessment remains subject to the organizer’s confirmed policy. The owner is not asked to debug code or provision the assistant’s environment.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>التشغيل ليس سياسة تقييم</h2><p>تحمي هذه الشروط بناء الدورة، ولا تضيف درجات أو نسب حضور أو حسابات مدفوعة أو مشاريع إضافية. يبقى تقييم الطالب الرسمي وفق سياسة الجهة المؤكدة. لا تطلب هذه المراجعة من صاحبة المشروع تصحيح الكود أو تجهيز بيئة المساعد.</p></td></tr></tbody>
</table>

