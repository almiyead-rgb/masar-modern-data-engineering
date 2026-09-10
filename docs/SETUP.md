<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h1>Prepare your learning environment</h1><p>Use Python 3.11, Java 17 and a CPU. Keep the complete repository together: the five daily notebooks share the supplied data and code. The full course’s recorded execution used GitHub Actions on Ubuntu; see <a href="VERIFICATION.md">the execution record</a>. Colab hosting has not been separately tested.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h1>جهّز بيئة تعلمك</h1><p>استخدم Python 3.11 وJava 17 ومعالج CPU. احتفظ بالمستودع كاملًا؛ تشترك دفاتر الأيام الخمسة في البيانات والكود المرفقين. تم التنفيذ المسجل للدورة على Ubuntu داخل GitHub Actions؛ راجع <a href="VERIFICATION.md">سجل التنفيذ</a>. لم تُختبر استضافة Colab بصورة مستقلة.</p></td></tr></table>

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>1. Clone your own fork</h2><p>Follow <a href="GIT_WORKFLOW.md">the Git guide</a> to create a Fork in your account. Copy its HTTPS clone URL from <strong>Code</strong>. In the command below, replace <code>YOUR_FORK_URL</code> with that copied URL. The final <code>masar-modern-data-engineering</code> argument sets the local folder name even if you renamed your fork.</p><p>Use only the fixed synthetic dataset. Initial setup needs internet access to download packages and Delta dependencies. No paid API or GPU is required.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>1. استنسخ نسختك الخاصة</h2><p>اتبع <a href="GIT_WORKFLOW.md">دليل Git</a> لإنشاء Fork داخل حسابك، ثم انسخ رابط HTTPS من زر <strong>Code</strong>. استبدل <code>YOUR_FORK_URL</code> في الأمر التالي بالرابط الذي نسخته. يحدد الجزء الأخير <code>masar-modern-data-engineering</code> اسم المجلد المحلي حتى لو غيّرت اسم نسختك.</p><p>استخدم البيانات الاصطناعية الثابتة فقط. يلزم الإنترنت عند الإعداد لتنزيل الحزم ومكتبات Delta. لا تحتاج إلى API مدفوع أو GPU.</p></td></tr></table>

```bash
git clone YOUR_FORK_URL masar-modern-data-engineering
cd masar-modern-data-engineering
git remote -v
java -version
```

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>2. Create a Python environment</h2><p>Confirm that Java reports version 17 and that <code>JAVA_HOME</code> points to that installation before starting Jupyter. Use the commands for your operating system below. Create the environment once; activate it again when returning to your project.</p><h3>Linux / macOS</h3></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>2. أنشئ بيئة Python</h2><p>تحقق من أن إصدار Java هو 17، وأن <code>JAVA_HOME</code> يشير إلى مجلد تثبيته قبل تشغيل Jupyter. اختر الأوامر المناسبة لنظام جهازك أدناه. أنشئ البيئة مرة واحدة، ثم فعّلها مجددًا عند العودة إلى مشروعك.</p><h3>Linux / macOS</h3></td></tr></table>

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h3>Windows Command Prompt</h3><p>Use Command Prompt for these activation commands. Do not run the Linux activation command on Windows.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h3>موجه أوامر Windows</h3><p>استخدم موجه الأوامر Command Prompt لتنفيذ أوامر التفعيل التالية. لا تستخدم أمر التفعيل الخاص بـLinux على Windows.</p></td></tr></table>

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
```

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>3. Install and open Jupyter</h2><p>Run these commands with the environment activated. The requirements files specify the course package versions. Resolve any installation error before opening the notebooks; do not upgrade individual packages independently.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>3. ثبّت الحزم وافتح Jupyter</h2><p>نفّذ الأوامر التالية بعد تفعيل البيئة. تحدد ملفات المتطلبات إصدارات الحزم المستخدمة في الدورة. عالج أي خطأ تثبيت قبل فتح الدفاتر، ولا تحدّث الحزم منفردة إلى إصدارات مختلفة.</p></td></tr></table>

```bash
python --version
python -m pip install -r requirements-course.txt -r requirements-day01.txt
python -m pip check
python -m jupyterlab
```

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>4. Follow the daily notebooks</h2><p>Choose the Python kernel from this environment. Start with <code>day01/STUDENT.ipynb</code>, run its cells in order and save the outputs. Continue with <code>day02/STUDENT.ipynb</code> through <code>day05/STUDENT.ipynb</code>. Each day’s page links its concepts, labs, glossary and completion checks.</p><p>Before Day 4, follow <a href="../day04/SETUP.md">the Day 4 setup</a> to start the supplied local Kafka service. Days 1–3 do not require that service. Keep the broker on the local addresses provided; do not expose it publicly.</p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>4. اتبع دفاتر الأيام</h2><p>اختر نواة Python الخاصة بهذه البيئة. ابدأ بـ<code>day01/STUDENT.ipynb</code> وشغّل خلاياه بالترتيب واحفظ المخرجات. تابع بعد ذلك من <code>day02/STUDENT.ipynb</code> إلى <code>day05/STUDENT.ipynb</code>. تربط صفحة كل يوم مفاهيمه ولاباته ومصطلحاته وفحوص اكتماله.</p><p>قبل اليوم الرابع اتبع <a href="../day04/SETUP.md">إعداد اليوم الرابع</a> لتشغيل خدمة Kafka المحلية المرفقة. لا تحتاج الأيام 1–3 إلى هذه الخدمة. التزم بالعناوين المحلية المحددة ولا تعرض الوسيط للعامة.</p></td></tr></table>

<table dir="ltr" width="100%"><tr><td width="50%" dir="ltr" lang="en" align="left" valign="top"><h2>5. Keep your progress</h2><p>Save each executed notebook, lab notes and the generated daily handoff ZIP. When changing machines or sessions, follow the day’s completion instructions to restore the handoff at the repository root while preserving relative paths. Use your own archives; do not extract an unknown ZIP over your work. Keep the fixed source files unchanged.</p><p><a href="GIT_WORKFLOW.md">Commit and upload your work</a> · <a href="TROUBLESHOOTING.md">Resolve errors</a> · <a href="../project/SUBMISSION.md">Submit the cumulative project</a> · <a href="../README.md">Course home</a></p></td><td width="50%" dir="rtl" lang="ar" align="right" valign="top"><h2>5. احتفظ بتقدمك</h2><p>احفظ كل دفتر منفذ وملاحظات اللابات وملف ZIP اليومي المولد. عند تغيير الجهاز أو الجلسة، اتبع تعليمات اكتمال اليوم لاستعادة الملف في جذر المستودع مع الحفاظ على المسارات النسبية. استخدم أرشيفاتك الخاصة ولا تفك ملف ZIP مجهولًا فوق عملك. اترك ملفات المصدر الثابتة دون تعديل.</p><p><a href="GIT_WORKFLOW.md">احفظ عملك وارفعه</a> · <a href="TROUBLESHOOTING.md">عالج الأخطاء</a> · <a href="../project/SUBMISSION.md">سلّم المشروع التراكمي</a> · <a href="../README.md">الرئيسية</a></p></td></tr></table>
