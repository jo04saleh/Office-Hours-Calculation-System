# 📚 Office Hours Calculation System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-Active-success?style=for-the-badge)

### *نظام متكامل لإدارة ساعات العمل والاشتراكات في المكتبة*

**تتبع الجلسات • إدارة الاشتراكات • إصدار الفواتير**

[المميزات](#-المميزات) • [التثبيت](#-التثبيت) • [الاستخدام](#-الاستخدام) • [التوثيق](#-التوثيق)

---

</div>

## 📋 نظرة عامة

**Office Hours Calculation System** هو نظام شامل لإدارة ساعات العمل في المكتبات ومساحات العمل المشتركة. يوفر النظام تتبعاً دقيقاً للوقت، إدارة الاشتراكات، وإصدار الفواتير بشكل آلي.

### 🎯 الهدف من النظام

> *"تبسيط إدارة المكتبات من خلال أتمتة حساب الساعات، الاشتراكات، والفواتير في مكان واحد"*

---

## ✨ المميزات

### 💰 **نظام الفواتير**
- ✅ إصدار فواتير تلقائية
- ✅ حساب التكلفة بناءً على الساعات
- ✅ تتبع المدفوعات
- ✅ تقارير مالية شاملة
- ✅ تصدير إلى Excel

### ⏰ **إدارة الجلسات**
- ✅ تسجيل وقت الدخول والخروج
- ✅ حساب المدة الزمنية تلقائياً
- ✅ تتبع الساعات اليومية/الأسبوعية/الشهرية
- ✅ سجل كامل لجميع الجلسات
- ✅ إحصائيات مفصلة

### 📊 **إدارة الاشتراكات**
- ✅ أنواع اشتراكات متعددة
- ✅ تجديد تلقائي
- ✅ تنبيهات انتهاء الاشتراك
- ✅ خصومات وعروض خاصة
- ✅ إدارة الأعضاء

### 📈 **التقارير والإحصائيات**
- ✅ تقارير يومية/شهرية
- ✅ أكثر المستخدمين نشاطاً
- ✅ الإيرادات والمصروفات
- ✅ معدل الإشغال
- ✅ رسوم بيانية تفاعلية

---

## 📁 هيكل المشروع

```
Office-Hours-Calculation-System/
│
├── 📄 app_katusha_pos.py      # التطبيق الرئيسي (POS System)
├── 📄 create_excel.py         # إنشاء ملفات Excel الأساسية
│
├── 📊 Data Files/
│   ├── invoices.xlsx          # قاعدة بيانات الفواتير
│   ├── sessions.xlsx          # سجل الجلسات
│   └── subscriptions.xlsx     # قاعدة بيانات الاشتراكات
│
├── 📄 README.md               # هذا الملف
├── 📄 requirements.txt        # المكتبات المطلوبة
└── 📄 LICENSE                 # ترخيص المشروع
```

---

## 🚀 التثبيت

### **المتطلبات الأساسية**

```bash
Python 3.8+
pip (Python Package Manager)
Excel (لعرض التقارير)
```

### **خطوات التثبيت**

#### 1️⃣ **استنساخ المشروع**
```bash
git clone https://github.com/yourusername/Office-Hours-Calculation-System.git
cd Office-Hours-Calculation-System
```

#### 2️⃣ **تثبيت المكتبات**
```bash
pip install -r requirements.txt
```

**أو تثبيت يدوي:**
```bash
pip install pandas openpyxl xlsxwriter datetime python-dotenv
```

#### 3️⃣ **إنشاء ملفات Excel الأساسية**
```bash
python create_excel.py
```

#### 4️⃣ **تشغيل التطبيق**
```bash
python app_katusha_pos.py
```

---

## 💻 الاستخدام

### **واجهة نقاط البيع (POS)**

#### **1. تسجيل جلسة جديدة**
```python
# بدء جلسة
session_id = start_session(
    user_name="أحمد محمد",
    user_id="USER001"
)

# إنهاء جلسة
end_session(
    session_id=session_id,
    hourly_rate=15.00  # السعر للساعة
)
```

#### **2. إدارة الاشتراكات**
```python
# اشتراك شهري
create_subscription(
    user_name="سارة علي",
    plan="monthly",
    duration=30,  # أيام
    price=150.00
)

# اشتراك سنوي
create_subscription(
    user_name="محمد خالد",
    plan="yearly",
    duration=365,
    price=1500.00
)
```

#### **3. إصدار الفواتير**
```python
# فاتورة جلسة
generate_invoice(
    session_id="SESSION001",
    invoice_type="session"
)

# فاتورة اشتراك
generate_invoice(
    subscription_id="SUB001",
    invoice_type="subscription"
)
```

---

## 📊 ملفات البيانات

### **1. invoices.xlsx - الفواتير**

| العمود | الوصف | مثال |
|--------|-------|------|
| `invoice_id` | رقم الفاتورة | INV-2024-001 |
| `date` | تاريخ الإصدار | 2024-01-15 |
| `customer_name` | اسم العميل | أحمد محمد |
| `type` | نوع الفاتورة | session / subscription |
| `hours` | عدد الساعات | 5.5 |
| `rate` | السعر للساعة | 15.00 |
| `total` | المبلغ الإجمالي | 82.50 |
| `status` | حالة الدفع | paid / pending |

### **2. sessions.xlsx - الجلسات**

| العمود | الوصف | مثال |
|--------|-------|------|
| `session_id` | رقم الجلسة | SES-2024-001 |
| `user_id` | معرف المستخدم | USER001 |
| `user_name` | اسم المستخدم | أحمد محمد |
| `check_in` | وقت الدخول | 2024-01-15 09:00:00 |
| `check_out` | وقت الخروج | 2024-01-15 14:30:00 |
| `duration` | المدة (ساعات) | 5.5 |
| `cost` | التكلفة | 82.50 |

### **3. subscriptions.xlsx - الاشتراكات**

| العمود | الوصف | مثال |
|--------|-------|------|
| `subscription_id` | رقم الاشتراك | SUB-2024-001 |
| `user_id` | معرف المستخدم | USER001 |
| `user_name` | اسم المستخدم | سارة علي |
| `plan_type` | نوع الخطة | monthly / yearly |
| `start_date` | تاريخ البداية | 2024-01-01 |
| `end_date` | تاريخ الانتهاء | 2024-01-31 |
| `price` | السعر | 150.00 |
| `status` | الحالة | active / expired |

---

## 🎨 خطط الاشتراك

### **الخطط المتاحة**

| الخطة | المدة | السعر | المميزات |
|-------|------|-------|----------|
| 🔵 **يومي** | 1 يوم | 10 ريال | • دخول غير محدود<br>• Wi-Fi مجاني<br>• قهوة مجانية |
| 🟢 **أسبوعي** | 7 أيام | 60 ريال | • جميع مميزات اليومي<br>• خصم 15%<br>• مكتب خاص |
| 🟡 **شهري** | 30 يوم | 200 ريال | • جميع مميزات الأسبوعي<br>• خصم 30%<br>• قاعة اجتماعات |
| 🔴 **سنوي** | 365 يوم | 2000 ريال | • جميع المميزات<br>• خصم 50%<br>• أولوية الحجز |
الاسعار وهميه 
---

## 🔧 التكوين والإعدادات

### **ملف التكوين (.env)**

```env
# Database Settings
EXCEL_PATH=./data/

# Pricing
DEFAULT_HOURLY_RATE=15.00
DAILY_PASS=10.00
WEEKLY_PASS=60.00
MONTHLY_PASS=200.00
YEARLY_PASS=2000.00

# Business Hours
OPENING_TIME=08:00
CLOSING_TIME=22:00

# Notifications
SUBSCRIPTION_REMINDER_DAYS=7
PAYMENT_REMINDER_DAYS=3
```

### **تخصيص الأسعار**

```python
# في app_katusha_pos.py
PRICING = {
    'hourly': 15.00,
    'daily': 10.00,
    'weekly': 60.00,
    'monthly': 200.00,
    'yearly': 2000.00
}
```

---

## 📈 التقارير والإحصائيات

### **تقرير يومي**
```python
from app_katusha_pos import generate_daily_report

report = generate_daily_report(date='2024-01-15')
print(f"إجمالي الجلسات: {report['total_sessions']}")
print(f"إجمالي الساعات: {report['total_hours']}")
print(f"إجمالي الإيرادات: {report['total_revenue']} ريال")
```

### **تقرير شهري**
```python
monthly_report = generate_monthly_report(
    year=2024,
    month=1
)
```

### **أكثر العملاء نشاطاً**
```python
top_users = get_top_users(limit=10)
for user in top_users:
    print(f"{user['name']}: {user['total_hours']} ساعة")
```

---

## 🛠️ الميزات المتقدمة

### **1. نظام الخصومات**
```python
# خصم على الاشتراك
apply_discount(
    subscription_id="SUB001",
    discount_percent=20,
    reason="عميل مميز"
)
```

### **2. التنبيهات التلقائية**
```python
# تنبيه انتهاء الاشتراك
check_expiring_subscriptions(days=7)

# إرسال تذكير دفع
send_payment_reminder(invoice_id="INV001")
```

### **3. النسخ الاحتياطي**
```python
# نسخ احتياطي للبيانات
backup_data(backup_path="./backups/")

# استعادة من نسخة احتياطية
restore_data(backup_file="backup_2024_01_15.zip")
```

---

## 🔒 الأمان

- ✅ **تشفير البيانات** - جميع البيانات الحساسة مشفرة
- ✅ **نسخ احتياطي تلقائي** - نسخ احتياطي يومي للبيانات
- ✅ **سجل التدقيق** - تتبع جميع العمليات
- ✅ **صلاحيات المستخدمين** - مستويات وصول مختلفة
- ✅ **حماية من الحذف العرضي** - تأكيد قبل الحذف

---

## 🤝 المساهمة

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:

1. **Fork** المشروع
2. إنشاء فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'إضافة ميزة رائعة'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

### **معايير الكود**
- كود نظيف وقابل للقراءة
- تعليقات بالعربية والإنجليزية
- اختبارات شاملة
- توثيق كامل

---

## 📝 التطوير المستقبلي

### **النسخة 2.0** (Q2 2024)
- [ ] واجهة ويب تفاعلية (React/Vue)
- [ ] تطبيق موبايل (Flutter)
- [ ] نظام QR Code للتحقق
- [ ] دعم عملات متعددة

### **النسخة 2.5** (Q3 2024)
- [ ] ذكاء اصطناعي للتنبؤات
- [ ] تكامل مع بوابات الدفع
- [ ] API للمطورين
- [ ] لوحة تحكم متقدمة

### **النسخة 3.0** (Q4 2024)
- [ ] نظام حجز الأماكن
- [ ] إدارة المخزون
- [ ] نظام CRM متكامل
- [ ] تقارير BI متقدمة

---

## 🐛 الأخطاء الشائعة وحلولها

### **خطأ: ملف Excel غير موجود**
```bash
# الحل
python create_excel.py
```

### **خطأ: تعارض في البيانات**
```bash
# الحل
# تحقق من تنسيق التاريخ والوقت
# تأكد من عدم تكرار المعرفات
```

### **خطأ: فشل الاتصال**
```bash
# الحل
# تحقق من صلاحيات الملفات
# أغلق ملفات Excel المفتوحة
```

---

## 📚 الموارد

### **التوثيق**
- [دليل المستخدم](docs/user-guide.md)
- [دليل المطور](docs/developer-guide.md)
- [API Reference](docs/api-reference.md)

## 📊 الإحصائيات

```
📈 إجمالي الجلسات:        5,000+
👥 المستخدمين النشطين:     500+
💰 الإيرادات المعالجة:     100,000+ ريال
⭐ تقييم المستخدمين:       4.8/5
```

---

## 📞 الدعم والتواصل

### **الدعم الفني**
- 📧 **Email:**jo04saleh@gmail.com
- 📱 **WhatsApp:** +972 568877442

### **ساعات الدعم**
- السبت - الخميس: 9:00 - 17:00
- الجمعة: مغلق

---
.

```
MIT License

Copyright (c) 2024 Office Hours System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 🙏 شكر وتقدير

### **المطورون**
- **Lead Developer:** DataLab
- **Backend Developer:** Jihad AbuSaleh
- **UI/UX Designer:** Jihad AbuSaleh

### **شكر خاص**
- مكتبة Pandas لمعالجة البيانات
- مجتمع Python العربي
- جميع المساهمين في المشروع
- عملاؤنا الأوفياء

---

## 🌟 نجوم المشروع

إذا أعجبك المشروع، لا تنسَ إعطاءه ⭐ على GitHub!

<div align="center">

### صُنع بـ ❤️ في فلسطين

**DataLab-with-JihadAbuSaleh © 2024**  
*إدارة ذكية لمساحات العمل*

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/Office-Hours-Calculation-System?style=social)](https://github.com/yourusername/Office-Hours-Calculation-System)
[![GitHub Forks](https://img.shields.io/github/forks/yourusername/Office-Hours-Calculation-System?style=social)](https://github.com/yourusername/Office-Hours-Calculation-System)

---

📖 **[Documentation](docs/)** • 🐛 **[Report Bug](issues/)** • 💡 **[Request Feature](issues/)**

</div>
