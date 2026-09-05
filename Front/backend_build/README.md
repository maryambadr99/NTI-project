# Nile Skies — الباك إند الحقيقي

فرونت متصل فعليًا بسيرفر Flask بيقرا ويكتب في ملفات الـ CSV الموجودة في مجلد `data/`.

## طريقة التشغيل

1. افتح تيرمينال جوه المجلد ده.
2. ثبّت المكتبات المطلوبة:
   ```
   pip install -r requirements.txt
   ```
3. شغّل السيرفر:
   ```
   python app.py
   ```
4. افتح المتصفح على:
   ```
   http://localhost:5000
   ```

## اللي شغال فعليًا (مش demo)

- كل التابات (الرحلات، الأسطول، الحظائر، الطاقم الفني) بتجيب بياناتها بـ `fetch` من الـ API، مش مدمجة جوه الصفحة.
- **الحجز**: لما تحجز رحلة، بينزل فعليًا في `data/flights.csv` (بينقص `available_seats`) وبيتسجل سطر جديد في `data/reservations.csv` (بيتعمل تلقائي أول مرة).
- **دخول الأدمن**: زرار "دخول الأدمن" في الأعلى بيتحقق من `data/admins_pass.csv` على السيرفر (مليش داعي أبعت ملف الباسوردات كامل للمتصفح).
- **تعديل حالة الطائرة/الحظيرة**: بعد الدخول كأدمن، بيظهر لك عنصر تحكم على كل كارت طائرة/حظيرة، والتعديل بيتحفظ فعليًا في نفس ملفات الـ CSV.

## هيكل المشروع

```
app.py                 # سيرفر Flask + كل الـ API endpoints
templates/index.html   # الفرونت (بيكلم الـ API بـ fetch)
data/
  aircraft.csv
  flights.csv
  hangers.csv
  labors.csv
  admins_pass.csv
  reservations.csv     # بيتعمل تلقائي عند أول حجز
requirements.txt
```

## الـ API Endpoints

| Method | Path | الوظيفة |
|---|---|---|
| GET | `/api/aircraft` | كل بيانات الأسطول |
| GET | `/api/flights` | كل الرحلات |
| GET | `/api/hangars` | كل الحظائر |
| GET | `/api/labors` | كل الفنيين |
| POST | `/api/reservations` | حجز رحلة (بيعدّل flights.csv فعليًا) |
| POST | `/api/admin/login` | تسجيل دخول الأدمن |
| PATCH | `/api/aircraft/<serial_number>` | تعديل حالة طائرة (أدمن فقط) |
| PATCH | `/api/hangars/<hanger_id>` | تعديل حالة حظيرة (أدمن فقط) |

## ملاحظة أمان

نظام الأدمن هنا بسيط جدًا (باسورد نص عادي في CSV) زي ما كان في المشروع الأصلي — مناسب للتجربة والتعليم بس، مش لبيئة إنتاج حقيقية.
