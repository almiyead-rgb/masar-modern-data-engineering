<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Save your work with Git</h1><p>Keep one repository for the cumulative project. Use a development branch for your changes, inspect the diff and commit meaningful learning steps. Keep file names and commit messages in English.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>احفظ عملك باستخدام Git</h1><p>احتفظ بمستودع واحد للمشروع التراكمي. استخدم فرع تطوير لتعديلاتك وراجع الفروق واحفظ مراحل التعلم برسائل واضحة. استخدم الإنجليزية لأسماء الملفات ورسائل التعديل.</p></td></tr></table>

```bash
git switch -c develop
git status
git diff
git add day01/STUDENT.ipynb LAB01_NOTES.md LAB02_NOTES.md
git diff --staged
git commit -m "Complete Day 1 Bronze and scan experiments"
```

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p>Use the files you actually changed in git add. Keep outputs/, handoff ZIP files, virtual environments and credentials out of ordinary commits. Save the output archive through the approved submission channel; retain bounded results inside notebooks.</p><p>A private-looking folder name does not protect information in a public repository. Do not force-push or delete earlier work to repair a notebook error. See <a href="../project/SUBMISSION.md">submission</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p>حدد في git add الملفات التي عدلتها فعلًا. استبعد outputs/ وملفات الانتقال والبيئات الافتراضية وبيانات الدخول من التعديلات الاعتيادية. احفظ ملف المخرجات عبر قناة التسليم المعتمدة واحتفظ بالنتائج الصغيرة داخل الدفاتر.</p><p>اسم المجلد لا يحمي المعلومات في مستودع عام. لا تستخدم الدفع القسري أو تحذف عملك السابق لإصلاح خطأ في دفتر. راجع <a href="../project/SUBMISSION.md">التسليم</a>.</p></td></tr></table>

