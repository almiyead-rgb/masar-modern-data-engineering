<table dir="ltr" width="100%"><tr><td width="50%" valign="top" dir="ltr" lang="en" align="left"><h1>Day 1 setup</h1></td><td width="50%" valign="top" dir="rtl" lang="ar" align="right"><h1>إعداد اليوم الأول</h1></td></tr></table>

<table dir="ltr" width="100%"><tr><td width="50%" valign="top" dir="ltr" lang="en" align="left"><h2>Recommended: Colab CPU</h2><p>Open <a href="https://colab.research.google.com/github/almiyead-rgb/masar-modern-data-engineering/blob/main/DAY01_STUDENT.ipynb">the notebook</a>, save a copy to your Drive, and run the setup cell. It fetches this public repository, installs the pinned PySpark/Delta packages and selects Java 17. No GPU, Docker, Kafka, dbt, token or paid account is needed for Day 1. Internet is required for the initial package and JAR downloads. Save your executed notebook and download the generated handoff ZIP before ending a Colab session.</p></td><td width="50%" valign="top" dir="rtl" lang="ar" align="right"><h2>المسار المقترح: Colab بمعالج CPU</h2><p>افتح <a href="https://colab.research.google.com/github/almiyead-rgb/masar-modern-data-engineering/blob/main/DAY01_STUDENT.ipynb">الدفتر</a> واحفظ نسخة في Drive وشغل خلية الإعداد. تجلب هذا المستودع العام وتثبت إصدارات PySpark وDelta المحددة وتختار Java 17. لا يحتاج اليوم الأول GPU أو Docker أو Kafka أو dbt أو رمز وصول أو حسابًا مدفوعًا. يلزم الإنترنت للتنزيل الأول للحزم وملفات JAR. احفظ الدفتر المنفذ ونزّل ZIP المخرجات قبل إنهاء جلسة Colab.</p></td></tr></table>

<table dir="ltr" width="100%"><tr><td width="50%" valign="top" dir="ltr" lang="en" align="left"><h2>Local Jupyter alternative</h2><p>Use Python 3.11 and Java 17; clone the repository and run these commands from its root. On Windows replace the activation line with <code>.venv\Scripts\activate</code>.</p></td><td width="50%" valign="top" dir="rtl" lang="ar" align="right"><h2>بديل Jupyter المحلي</h2><p>استخدم Python 3.11 وJava 17 واستنسخ المستودع ثم نفذ الأوامر من جذره. في Windows استبدل سطر التفعيل بـ<code>.venv\Scripts\activate</code>.</p></td></tr></table>

```bash
git clone https://github.com/almiyead-rgb/masar-modern-data-engineering.git
cd masar-modern-data-engineering
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-day01.txt
python -m jupyterlab
```

<table dir="ltr" width="100%"><tr><td width="50%" valign="top" dir="ltr" lang="en" align="left"><p>Open <code>DAY01_STUDENT.ipynb</code>. To run without a notebook use <code>python scripts/run_day01.py</code>. The tested environment and actual verification result are listed in <a href="../STATUS.md">Status</a>; Colab itself is a separate hosted environment and is not certified by a GitHub test.</p></td><td width="50%" valign="top" dir="rtl" lang="ar" align="right"><p>افتح <code>DAY01_STUDENT.ipynb</code>. وللتشغيل دون دفتر استخدم <code>python scripts/run_day01.py</code>. البيئة المختبرة ونتيجة التحقق الفعلية في <a href="../STATUS.md">الحالة</a>؛ خدمة Colab بيئة مستقلة ولا يعد اختبار GitHub اعتمادًا لخدمتها.</p></td></tr></table>

