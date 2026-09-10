<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Prepare once, learn over five days</h1><p>Use a local Python 3.11 environment and Java 17. Check <code>java -version</code> and set <code>JAVA_HOME</code> before launching Jupyter. The small dataset uses CPU only. Keep the full repository together.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>جهّز مرة واحدة وتعلم خلال خمسة أيام</h1><p>استخدم بيئة Python 3.11 محلية وJava 17. تحقق من <code>java -version</code> واضبط <code>JAVA_HOME</code> قبل فتح Jupyter. تعمل البيانات الصغيرة باستخدام CPU. احتفظ بالمستودع كاملًا.</p></td></tr></table>

```bash
git clone https://github.com/almiyead-rgb/masar-modern-data-engineering.git
cd masar-modern-data-engineering
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-course.txt -r requirements-day01.txt
python -m pip check
python -m jupyterlab
```

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><p>On Windows Command Prompt, create the environment with <code>py -3.11 -m venv .venv</code> and activate it with <code>.venv\Scripts\activate</code>. In Jupyter, choose the environment’s Python kernel and open <code>day01/STUDENT.ipynb</code>. Continue with one notebook per day.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><p>في موجه أوامر Windows أنشئ البيئة بأمر <code>py -3.11 -m venv .venv</code> وفعّلها بأمر <code>.venv\Scripts\activate</code>. داخل Jupyter اختر نواة Python الخاصة بالبيئة وافتح <code>day01/STUDENT.ipynb</code>، ثم تابع بدفتر واحد لكل يوم.</p></td></tr></table>

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Day 4 service</h2><p>Before Day 4, start the provided local Kafka broker using <a href="../day04/SETUP.md">the Day 4 setup</a>. You do not need this service for Days 1–3. Use the supplied local addresses; do not expose the broker publicly.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>خدمة اليوم الرابع</h2><p>قبل اليوم الرابع شغّل وسيط Kafka المحلي المرفق وفق <a href="../day04/SETUP.md">إعداد اليوم الرابع</a>. لا تحتاج إلى الخدمة للأيام 1–3. استخدم العناوين المحلية المرفقة ولا تعرض الوسيط للعامة.</p></td></tr></table>

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>Saving work</h2><p>Save each executed notebook and daily handoff ZIP. Restore a handoff at the repository root when moving to a new session. Never overwrite the fixed source data or delete earlier outputs to rerun. See <a href="TROUBLESHOOTING.md">troubleshooting</a> and <a href="VERIFICATION.md">tested environments</a>.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>حفظ العمل</h2><p>احفظ كل دفتر منفذ وملف الانتقال اليومي. استعد ملف الانتقال في جذر المستودع عند تغيير الجلسة. لا تعدّل البيانات الأصلية الثابتة ولا تحذف المخرجات السابقة لإعادة التشغيل. راجع <a href="TROUBLESHOOTING.md">معالجة الأخطاء</a> و<a href="VERIFICATION.md">البيئات المختبرة</a>.</p></td></tr></table>

