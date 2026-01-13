import pandas as pd

# إنشاء ملفات Excel الفارغة
pd.DataFrame(columns=["اسم الطالب", "وقت الدخول", "وقت الخروج", "المدة (ساعات)", "مدة محسوبة", "السعر"]).to_excel("sessions.xlsx", index=False)
pd.DataFrame(columns=["اسم الطالب", "نوع الاشتراك", "تاريخ البداية", "تاريخ الانتهاء"]).to_excel("subscriptions.xlsx", index=False)
pd.DataFrame(columns=["رقم الفاتورة", "اسم الطالب", "المدة", "السعر", "وقت الدخول", "وقت الخروج", "تاريخ الاصدار"]).to_excel("invoices.xlsx", index=False)

print("تم إنشاء ملفات Excel بنجاح!")
