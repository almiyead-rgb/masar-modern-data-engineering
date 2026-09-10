<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Working with Git and GitHub</h1></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>العمل باستخدام Git وGitHub</h1></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p><a href="../README.md">Course home</a> · <a href="../docs/START_HERE.md">Start here</a> · <a href="../STATUS.md">Readiness</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p><a href="../README.md">الرئيسية</a> · <a href="../docs/START_HERE.md">ابدأ هنا</a> · <a href="../STATUS.md">حالة الجاهزية</a></p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>One source of truth</h2><p>Use the course version announced by the instructor. Keep changes on a development branch, review the diff, and merge only after checks pass. The authoring copy currently has a local <code>develop</code> branch, no remote origin and no published release. Future checkpoint tags must refer to real, tested states; none are claimed to exist yet.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>نسخة مرجعية واحدة</h2><p>استخدم نسخة الدورة التي تعلنها المدربة. احتفظ بالتعديلات في فرع تطوير وراجع الفروق ولا تدمج إلا بعد نجاح الفحوص. لنسخة التأليف الحالية فرع <code dir="ltr">develop</code> محلي، بلا أصل بعيد أو إصدار منشور. يجب أن تشير علامات الاستعادة المستقبلية إلى حالات فعلية مختبرة؛ ولا ندعي وجودها الآن.</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Save a meaningful change</h2><p>Keep identifiers, filenames and commit messages in English. Stage only the files you intend to share and inspect the staged diff. Do not run a destructive reset or force-push to solve a notebook problem.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حفظ تعديل مفهوم</h2><p>احتفظ بالمعرفات وأسماء الملفات ورسائل التعديلات بالإنجليزية. جهز الملفات التي تقصد مشاركتها فقط وافحص الفروق. لا تستخدم إعادة ضبط مدمرة أو دفعًا قسريًا لمعالجة مشكلة دفتر.</p></td></tr></tbody>
</table>


<div dir="ltr">

```bash
git status
git diff
# Stage the specific edited files, then inspect them.
git diff --staged
```

</div>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Privacy is not a folder name</h2><p>Do not put instructor-only material in a public repository or any of its branches. A folder named <code>private</code> and a later deletion do not erase public history. The instructor package is stored outside this repository and excluded from the source archive. [GH2]</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>الخصوصية ليست اسم مجلد</h2><p>لا تضع مواد المدربة الخاصة في مستودع عام أو أي فرع منه. اسم مجلد <code dir="ltr">private</code> والحذف اللاحق لا يمحوان التاريخ العام. تحفظ حزمة المدربة خارج هذا المستودع وتستبعد من أرشيف مصدره. [GH2]</p></td></tr></tbody>
</table>

<table dir="ltr" width="100%">
<thead><tr><th width="50%" dir="ltr" lang="en" align="left">English</th><th width="50%" dir="rtl" lang="ar" align="right">العربية</th></tr></thead>
<tbody><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Release checkpoints</h2><p>The intended route is local preparation → review → explicit publication approval → a dedicated course repository → access/render checks → release. Building this source tree does not claim those later stages have happened.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>نقاط الإصدار</h2><p>المسار المقصود: تجهيز محلي ثم مراجعة ثم موافقة نشر صريحة ثم مستودع مستقل للدورة ثم فحص الوصول والعرض ثم إصدار. بناء الشجرة الحالية لا يعني تنفيذ هذه المراحل اللاحقة.</p></td></tr></tbody>
</table>
