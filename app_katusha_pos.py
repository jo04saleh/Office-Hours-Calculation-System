# app_katusha_pos.py
# Katusha POS - GUI library session manager
# - Saves invoices to invoices.xlsx (one row per invoice)
# - Keeps sessions.xlsx and subscriptions.xlsx for records
# - Prints to thermal printer (Rongta) when Vendor/Product IDs are provided and python-escpos installed
# - Otherwise prints a receipt preview and still saves to Excel
# - Receipt header is ASCII boxed "KATUSHA"
# - Time printed in 12-hour format with AM/PM
# - Footer contains: "تم التطوير من قبل DataLab.ps"
# - Designed with a modern DataLab-like color scheme and large buttons for POS use

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pandas as pd
import os, sys

# --- Resource path for PyInstaller compatibility ---
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Files (next to exe/script)
sessions_file = resource_path("sessions.xlsx")
subs_file = resource_path("subscriptions.xlsx")
invoices_file = resource_path("invoices.xlsx")

# Ensure data files exist
def ensure_files():
    if not os.path.exists(sessions_file):
        pd.DataFrame(columns=["اسم الطالب", "وقت الدخول", "وقت الخروج", "المدة (ساعات)", "مدة محسوبة", "السعر"]).to_excel(sessions_file, index=False)
    if not os.path.exists(subs_file):
        pd.DataFrame(columns=["اسم الطالب", "نوع الاشتراك", "تاريخ البداية", "تاريخ الانتهاء"]).to_excel(subs_file, index=False)
    if not os.path.exists(invoices_file):
        pd.DataFrame(columns=["رقم الفاتورة", "اسم الطالب", "المدة", "السعر", "وقت الدخول", "وقت الخروج", "تاريخ الاصدار"]).to_excel(invoices_file, index=False)

ensure_files()

# Pricing table (hours rounded to nearest 0.5)
prices = {
    1.0: 6, 1.5: 8, 2.0: 10, 2.5: 12, 3.0: 14, 3.5: 15,
    4.0: 16, 4.5: 18, 5.0: 20, 5.5: 21, 6.0: 22, 6.5: 23,
    7.0: 24, 7.5: 25, 8.0: 26, 8.5: 27, 9.0: 28, 9.5: 29,
    10.0: 30, 10.5: 31, 11.0: 32, 11.5: 33, 12.0: 34
}
sessions = {}  # active sessions {name: datetime}

# Try to import escpos for thermal printing; if not available, disable printing until user enables/installs
try:
    from escpos.printer import Usb
    ESC_POS_AVAILABLE = True
except Exception:
    ESC_POS_AVAILABLE = False

# Where to store vendor/product ids (user adds them later)
PRINTER_CONFIG = {
    "vendor_id": None,   # e.g., 0x1fc9
    "product_id": None   # e.g., 0x2016
}

# Utilities
def round_to_half(hour_float):
    return round(hour_float * 2) / 2

def read_subscriptions_df():
    df = pd.read_excel(subs_file)
    if "تاريخ الانتهاء" in df.columns:
        df["تاريخ الانتهاء"] = pd.to_datetime(df["تاريخ الانتهاء"], errors="coerce")
    return df

def has_active_subscription(name):
    df = read_subscriptions_df()
    if name not in df["اسم الطالب"].values:
        return False
    student_rows = df[df["اسم الطالب"] == name]
    for _, row in student_rows.iterrows():
        end = row.get("تاريخ الانتهاء")
        if pd.notnull(end) and datetime.now() <= pd.to_datetime(end):
            return True
    return False

# --- Invoice / printing functions ---
def save_invoice_to_excel(name, duration, price, start_time, end_time):
    df = pd.read_excel(invoices_file)
    invoice_no = 1
    if not df.empty:
        invoice_no = int(df["رقم الفاتورة"].max()) + 1 if "رقم الفاتورة" in df.columns and pd.notnull(df["رقم الفاتورة"]).any() else len(df) + 1
    new_row = {
        "رقم الفاتورة": invoice_no,
        "اسم الطالب": name,
        "المدة": duration,
        "السعر": price,
        "وقت الدخول": start_time.strftime("%Y-%m-%d %I:%M %p"),
        "وقت الخروج": end_time.strftime("%Y-%m-%d %I:%M %p"),
        "تاريخ الاصدار": datetime.now().strftime("%Y-%m-%d %I:%M %p")
    }
    df = df._append(new_row, ignore_index=True)
    df.to_excel(invoices_file, index=False)
    return invoice_no

def get_receipt_text(invoice_no, name, duration, price, start_time, end_time):
    header = "╔══════════════════════╗\n║       KATUSHA        ║\n╚══════════════════════╝\n"
    body = f"فاتورة رقم: {invoice_no}\n"
    body += f"الاسم: {name}\n"
    body += f"وقت الدخول: {start_time.strftime('%Y-%m-%d %I:%M %p')}\n"
    body += f"وقت الخروج: {end_time.strftime('%Y-%m-%d %I:%M %p')}\n"
    body += f"المدة (محسوبة): {duration} ساعة\n"
    body += f"السعر: {price}\n"
    footer = "\n-----------------------------\nتم التطوير من قبل DataLab.ps\n\n"
    return header + body + footer

def print_receipt(name, duration, price, start_time, end_time):
    invoice_no = save_invoice_to_excel(name, duration, price, start_time, end_time)
    receipt = get_receipt_text(invoice_no, name, duration, price, start_time, end_time)
    if ESC_POS_AVAILABLE and PRINTER_CONFIG.get("vendor_id") and PRINTER_CONFIG.get("product_id"):
        try:
            p = Usb(PRINTER_CONFIG["vendor_id"], PRINTER_CONFIG["product_id"])
            for line in receipt.splitlines():
                p.text(line + "\n")
            p.cut()
            messagebox.showinfo("تمت الطباعة", f"تم طباعة الفاتورة #{invoice_no} بنجاح")
            return
        except Exception as e:
            messagebox.showwarning("تحذير طباعة", f"فشل الاتصال بالطابعة: {e}\nسيتم حفظ الفاتورة محلياً وعرض معاينة.")
    else:
        print_note = "" if ESC_POS_AVAILABLE else "[ملاحظة: python-escpos غير مثبت]\n"
        if ESC_POS_AVAILABLE and (not PRINTER_CONFIG.get("vendor_id") or not PRINTER_CONFIG.get("product_id")):
            print_note = "[ملاحظة: لم تُضف Vendor/Product ID للطابعة بعد]\n"
        preview = print_note + receipt
        PreviewWindow(preview)
        messagebox.showinfo("تم الحفظ", f"تم حفظ الفاتورة #{invoice_no} في {os.path.basename(invoices_file)}")

# --- GUI and POS logic ---
def append_session_record(name, start, end, duration, duration_calc, price):
    df = pd.read_excel(sessions_file)
    new_row = {
        "اسم الطالب": name,
        "وقت الدخول": start.strftime("%Y-%m-%d %I:%M %p"),
        "وقت الخروج": end.strftime("%Y-%m-%d %I:%M %p"),
        "المدة (ساعات)": duration,
        "مدة محسوبة": duration_calc,
        "السعر": price
    }
    df = df._append(new_row, ignore_index=True)
    df.to_excel(sessions_file, index=False)
    refresh_history()

def register_entry():
    name = entry_name.get().strip()
    if not name:
        messagebox.showerror("خطأ", "الرجاء إدخال اسم الطالب")
        return
    if name in sessions:
        messagebox.showwarning("مكرر", f"{name} مسجل فعلاً داخل المكتبة")
        return
    sessions[name] = datetime.now()
    refresh_active_sessions()
    entry_name.delete(0, tk.END)

def register_exit(print_and_save=True):
    name = entry_name.get().strip()
    if not name:
        messagebox.showerror("خطأ", "الرجاء إدخال اسم الطالب")
        return
    if name not in sessions:
        messagebox.showerror("خطأ", "هذا الطالب غير مسجل دخوله")
        return
    start = sessions[name]
    end = datetime.now()
    if has_active_subscription(name):
        duration = round((end - start).total_seconds() / 3600, 2)
        price = "مشمول بالاشتراك"
        append_session_record(name, start, end, duration, round_to_half(duration), price)
        del sessions[name]
        refresh_active_sessions()
        if print_and_save:
            print_receipt(name, round_to_half(duration), price, start, end)
        return
    duration = round((end - start).total_seconds() / 3600, 2)
    duration_calc = round_to_half(duration)
    price = prices.get(duration_calc, "غير محدد")
    append_session_record(name, start, end, duration, duration_calc, price)
    del sessions[name]
    refresh_active_sessions()
    if print_and_save:
        print_receipt(name, duration_calc, price, start, end)

def register_subscription():
    name = entry_name.get().strip()
    sub_type = sub_var.get()
    if not name or sub_type == "":
        messagebox.showerror("خطأ", "الرجاء إدخال الاسم واختيار نوع الاشتراك")
        return
    start = datetime.now()
    if sub_type == "يوم":
        end = start + timedelta(days=1)
    elif sub_type == "أسبوع":
        end = start + timedelta(weeks=1)
    else:
        end = start + timedelta(days=30)
    df = pd.read_excel(subs_file)
    new_row = {"اسم الطالب": name, "نوع الاشتراك": sub_type, "تاريخ البداية": start.strftime("%Y-%m-%d %I:%M %p"), "تاريخ الانتهاء": end.strftime("%Y-%m-%d %I:%M %p")}
    df = df._append(new_row, ignore_index=True)
    df.to_excel(subs_file, index=False)
    messagebox.showinfo("تم", f"تم تفعيل اشتراك {sub_type} للطالب {name}")
    entry_name.delete(0, tk.END)
    refresh_subscriptions()

# --- GUI helpers ---
def PreviewWindow(text):
    w = tk.Toplevel(root)
    w.title("معاينة الفاتورة - Preview")
    txt = tk.Text(w, width=50, height=20, font=("Courier", 10))
    txt.pack(padx=10, pady=10)
    txt.insert("1.0", text)
    txt.config(state="disabled")

def refresh_history(search_name=None):
    for row in tree_hist.get_children():
        tree_hist.delete(row)
    df = pd.read_excel(sessions_file)
    if search_name:
        df = df[df["اسم الطالب"].astype(str).str.contains(search_name)]
    for _, r in df.iterrows():
        tree_hist.insert("", "end", values=(
            r.get("اسم الطالب"),
            r.get("وقت الدخول"),
            r.get("وقت الخروج"),
            r.get("المدة (ساعات)"),
            r.get("مدة محسوبة"),
            r.get("السعر")
        ))

def refresh_active_sessions():
    list_active.delete(0, tk.END)
    for name, start in sessions.items():
        list_active.insert(tk.END, f"{name} — دخل في {start.strftime('%I:%M %p')}")

def refresh_subscriptions():
    for row in tree_sub.get_children():
        tree_sub.delete(row)
    df = read_subscriptions_df()
    for _, r in df.iterrows():
        tree_sub.insert("", "end", values=(
            r.get("اسم الطالب"),
            r.get("نوع الاشتراك"),
            r.get("تاريخ البداية"),
            r.get("تاريخ الانتهاء")
        ))

def on_search_history():
    term = entry_search.get().strip()
    refresh_history(term if term else None)

# --- Build GUI ---
root = tk.Tk()
root.title("Katusha POS - DataLab Edition")
root.geometry("1100x640")
root.configure(bg="#0f172a")  # dark navy background

# Left panel
frame_left = tk.Frame(root, bg="#0b1220", padx=16, pady=16)
frame_left.pack(side=tk.LEFT, fill=tk.Y)

lbl_title = tk.Label(frame_left, text="KATUSHA — DataLab POS", font=("Segoe UI", 18, "bold"), fg="#E6F0FF", bg="#0b1220")
lbl_title.pack(pady=(0,8))

tk.Label(frame_left, text="اسم الطالب:", font=("Segoe UI", 14), fg="#CFE6FF", bg="#0b1220").pack(anchor="w")
entry_name = tk.Entry(frame_left, font=("Segoe UI", 18), justify='center', width=20)
entry_name.pack(pady=8)

btn_in = tk.Button(frame_left, text="تسجيل دخول", font=("Segoe UI", 14, "bold"), width=20, height=2, command=register_entry, bg="#06b6d4", fg="white")
btn_in.pack(pady=6)

btn_out = tk.Button(frame_left, text="تسجيل خروج + طباعة", font=("Segoe UI", 13, "bold"), width=20, height=2, command=lambda: register_exit(True), bg="#ef4444", fg="white")
btn_out.pack(pady=6)

btn_out_no_print = tk.Button(frame_left, text="تسجيل خروج (بدون طباعة)", font=("Segoe UI", 12, "bold"), width=20, height=1, command=lambda: register_exit(False), bg="#f59e0b", fg="white")
btn_out_no_print.pack(pady=6)

tk.Label(frame_left, text="اشتراك سريع:", font=("Segoe UI", 12), fg="#CFE6FF", bg="#0b1220").pack(pady=(12,0), anchor="w")
sub_var = tk.StringVar(value="يوم")
sub_menu = ttk.Combobox(frame_left, values=["يوم", "أسبوع", "شهر"], textvariable=sub_var, state="readonly", width=18, font=("Segoe UI", 12))
sub_menu.pack(pady=6)
btn_sub = tk.Button(frame_left, text="تفعيل اشتراك", font=("Segoe UI", 12, "bold"), width=20, height=1, command=register_subscription, bg="#3b82f6", fg="white")
btn_sub.pack(pady=6)

tk.Label(frame_left, text="الجلسات النشطة:", font=("Segoe UI", 12), fg="#CFE6FF", bg="#0b1220").pack(pady=(18,4), anchor="w")
list_active = tk.Listbox(frame_left, width=28, height=8, font=("Segoe UI", 11))
list_active.pack()
refresh_active_sessions()

# Right panel
frame_right = tk.Frame(root, bg="#e6eef8", padx=12, pady=12)
frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

search_frame = tk.Frame(frame_right, bg="#e6eef8")
search_frame.pack(fill=tk.X, pady=(0,8))
entry_search = tk.Entry(search_frame, font=("Segoe UI", 12), width=30)
entry_search.pack(side=tk.LEFT, padx=(0,8))
btn_search = tk.Button(search_frame, text="بحث", font=("Segoe UI", 11), command=on_search_history, bg="#06b6d4", fg="white")
btn_search.pack(side=tk.LEFT)
btn_refresh = tk.Button(search_frame, text="تحديث السجل", font=("Segoe UI", 11), command=lambda: refresh_history(), bg="#06b6d4", fg="white")
btn_refresh.pack(side=tk.LEFT, padx=8)

cols = ("الاسم", "وقت الدخول", "وقت الخروج", "المدة الحقيقية", "المدة المحسوبة", "السعر")
tree_hist = ttk.Treeview(frame_right, columns=cols, show="headings", height=14)
for c in cols:
    tree_hist.heading(c, text=c)
    tree_hist.column(c, width=140, anchor="center")
tree_hist.pack(fill=tk.BOTH, expand=True, pady=(0,8))
refresh_history()

lbl_subs = tk.Label(frame_right, text="قائمة الاشتراكات", font=("Segoe UI", 12, "bold"), bg="#e6eef8")
lbl_subs.pack(pady=(6,0))
cols2 = ("الاسم", "نوع الاشتراك", "بداية", "انتهاء")
tree_sub = ttk.Treeview(frame_right, columns=cols2, show="headings", height=6)
for c in cols2:
    tree_sub.heading(c, text=c)
    tree_sub.column(c, width=160, anchor="center")
tree_sub.pack(fill=tk.X, pady=(4,8))
refresh_subscriptions()

# Bottom actions
bottom_frame = tk.Frame(root, bg="#0b1220", padx=12, pady=8)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

def export_invoices():
    messagebox.showinfo("ملف الفواتير", f"الفواتير محفوظة في: {invoices_file}")

def clear_all_records():
    if messagebox.askyesno("تأكيد", "هل تريد حذف جميع سجلات الجلسات؟"):
        pd.DataFrame(columns=[ "اسم الطالب", "وقت الدخول", "وقت الخروج", "المدة (ساعات)", "مدة محسوبة", "السعر"]).to_excel(sessions_file, index=False)
        refresh_history()

btn_invoice = tk.Button(bottom_frame, text="عرض ملف الفواتير", command=export_invoices, bg="#06b6d4", fg="white")
btn_invoice.pack(side=tk.LEFT, padx=8)
btn_clear = tk.Button(bottom_frame, text="حذف السجلات", command=clear_all_records, bg="#ef4444", fg="white")
btn_clear.pack(side=tk.LEFT, padx=8)

root.mainloop()
