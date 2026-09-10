<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Day 4 · Streaming and trust</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>اليوم الرابع · التدفق وموثوقية البيانات</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Build on the same project</h2><p>LO5 and LO6, with LO8 integration. Labs 05 and 06 extend the corrected 75-trip Silver table from Day 3. No new dataset or separate assignment is introduced. Instructor: Meaad Al-Marri · SDA-DSC-214.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>إضافة إلى المشروع نفسه</h2><p>يرتبط اليوم بالهدفين LO5 وLO6، ويدعم التكامل LO8. يضيف اللابان 05 و06 إلى جدول Silver المصحح ذي 75 رحلة من اليوم الثالث. لا نضيف مجموعة بيانات أو تكليفًا مستقلًا. المدربة: ميعاد المري · SDA-DSC-214.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Current status: authored, not engine-verified</h2><p>An executed source-reference notebook is available. The Kafka/Spark/Delta and GX notebooks are authored with visible ENGINE_NOT_EXECUTED status. Their outputs are intentionally empty. Local source tests are not a substitute for native lab execution.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الحالة: محتوى مكتوب دون اعتماد تشغيل المحركات</h2><p>يوجد دفتر مرجعي منفذ من المصدر. دفاتر Kafka وSpark وDelta وGX مكتوبة وموسومة ENGINE_NOT_EXECUTED، ومخرجاتها فارغة عمدًا. اختبارات المصدر المحلية لا تستبدل التنفيذ الفعلي للابات.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Reading and practice route</h2><ul><li><a href="CONCEPTS.md">1. Understand streaming and trust</a></li><li><a href="STREAM_CONTRACT.md">2. Read the streaming contract</a></li><li><a href="../labs/lab05/WALKTHROUGH.md">3. Lab 05: actual streaming route</a></li><li><a href="QUALITY_POLICY.md">4. Read the quality policy</a></li><li><a href="../labs/lab06/WALKTHROUGH.md">5. Lab 06: GX and quarantine</a></li><li><a href="GOVERNANCE.md">6. Document governance</a></li><li><a href="OBSERVABILITY.md">7. Interpret run evidence</a></li><li><a href="PRACTICE.md">8. Explain your results</a></li><li><a href="COMPLETION.md">9. Continue to Day 5</a></li><li><a href="GLOSSARY.md">Terminology and pronunciation</a></li><li><a href="SOURCES.md">Official references</a></li></ul></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>مسار القراءة والتطبيق</h2><ul><li><a href="CONCEPTS.md">1. فهم التدفق وموثوقية البيانات</a></li><li><a href="STREAM_CONTRACT.md">2. عقد التدفق</a></li><li><a href="../labs/lab05/WALKTHROUGH.md">3. اللاب 05: مسار التدفق الأصلي</a></li><li><a href="QUALITY_POLICY.md">4. سياسة الجودة</a></li><li><a href="../labs/lab06/WALKTHROUGH.md">5. اللاب 06: الجودة والعزل</a></li><li><a href="GOVERNANCE.md">6. توثيق الحوكمة</a></li><li><a href="OBSERVABILITY.md">7. تفسير أدلة المراقبة</a></li><li><a href="PRACTICE.md">8. تفسير نتائجك</a></li><li><a href="COMPLETION.md">9. الانتقال لليوم الخامس</a></li><li><a href="GLOSSARY.md">المصطلحات والنطق</a></li><li><a href="SOURCES.md">المراجع الأصلية</a></li></ul></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>The concrete question</h2><p>Can we distinguish a resumed read from a newly sent duplicate event, and stop seven bad trip rows from entering trusted outputs? The expected answer is auditable counts and explicit decisions, not a green label alone.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>سؤال اليوم</h2><p>هل نفرّق بين استئناف القراءة وإعادة إرسال حدث مكرر، ونمنع دخول سبعة صفوف معيبة إلى المخرجات الموثوقة؟ الإجابة المطلوبة أعداد قابلة للتسوية وقرارات واضحة، لا علامة خضراء وحدها.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Suggested six-hour learning sequence</h2><p>30 min recap and reference → 45 min streaming concepts → 75 min Lab 05 → 15 min break → 35 min quality concepts → 80 min Lab 06 → 15 min break → 40 min observability and governance → 25 min evidence and handoff. This is a pacing proposal, not an attendance or grading rule.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>تسلسل مقترح ضمن الساعات الست</h2><p>30 دقيقة للمراجعة والمرجع ← 45 لمفاهيم التدفق ← 75 للاب 05 ← 15 استراحة ← 35 لمفاهيم الجودة ← 80 للاب 06 ← 15 استراحة ← 40 للمراقبة والحوكمة ← 25 للأدلة والانتقال. هذا توزيع مقترح للتقديم، وليس شرط حضور أو درجات.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Outputs to carry forward</h2><p>A raw event Delta table, a deduplicated event snapshot, restart evidence, a failed-candidate report, a seven-row quarantine table, GX Data Docs, a separately revalidated 75-trip snapshot, and governance notes. Paths are generated only after a successful native run.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>ما ينتقل معك</h2><p>جدول Delta للأحداث الخام، ونسخة أحداث منزوعة التكرار، وأدلة الاستئناف، وتقرير دفعة فاشلة، وجدول عزل من سبعة صفوف، وتقارير GX، ونسخة 75 رحلة أُعيد فحصها مستقلة، وملاحظات الحوكمة. لا تُولد المسارات الفعلية إلا بعد نجاح التشغيل الأصلي.</p></td></tr></tbody>
</table>
