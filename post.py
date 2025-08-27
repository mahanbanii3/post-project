from gettext import install
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB = "users_post.db"

# --- DATABASE ---
def create_users_table():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# --- MAIN APP ---
class PostApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("برنامه خدمات پستی ایران")
        self.geometry("650x480")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure(bg='#e5ebf7')
        create_users_table()
        self.show_login()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        LoginFrame(self)

    def show_signup(self):
        self.clear()
        SignupFrame(self)

    def show_dashboard(self, username):
        self.clear()
        DashboardFrame(self, username)

# --- LOGIN ---
class LoginFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=30)
        self.master = master
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        ttk.Label(self, text="ورود به سامانه پست ایران", font=("Vazirmatn", 18, "bold")).pack(pady=(0,18))
        self.username = ttk.Entry(self, font=("Vazirmatn", 14), width=22)
        self.username.pack(pady=6)
        self.username.insert(0, "نام کاربری")
        self.password = ttk.Entry(self, font=("Vazirmatn", 14), show="*", width=22)
        self.password.pack(pady=6)
        self.password.insert(0, "رمز عبور")
        ttk.Button(self, text="ورود", command=self.login, style="Accent.TButton").pack(pady=10)
        ttk.Button(self, text="ثبت‌نام", command=master.show_signup).pack()
        self.username.bind("<FocusIn>", lambda e: self._clear_placeholder(self.username, "نام کاربری"))
        self.password.bind("<FocusIn>", lambda e: self._clear_placeholder(self.password, "رمز عبور"))

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def login(self):
        u = self.username.get()
        p = self.password.get()
        if not u or not p or u == "نام کاربری" or p == "رمز عبور":
            messagebox.showwarning("خطا", "نام کاربری و رمز عبور را وارد کنید.")
            return
        if check_user(u, p):
            self.master.show_dashboard(u)
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است!")

# --- SIGNUP ---
class SignupFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=30)
        self.master = master
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        ttk.Label(self, text="ثبت‌نام کاربر جدید", font=("Vazirmatn", 18, "bold")).pack(pady=(0,18))
        self.username = ttk.Entry(self, font=("Vazirmatn", 14), width=22)
        self.username.pack(pady=6)
        self.username.insert(0, "نام کاربری")
        self.password = ttk.Entry(self, font=("Vazirmatn", 14), show="*", width=22)
        self.password.pack(pady=6)
        self.password.insert(0, "رمز عبور")
        ttk.Button(self, text="ثبت‌نام", command=self.signup, style="Accent.TButton").pack(pady=10)
        ttk.Button(self, text="بازگشت به ورود", command=master.show_login).pack()
        self.username.bind("<FocusIn>", lambda e: self._clear_placeholder(self.username, "نام کاربری"))
        self.password.bind("<FocusIn>", lambda e: self._clear_placeholder(self.password, "رمز عبور"))

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def signup(self):
        u = self.username.get()
        p = self.password.get()
        if not u or not p or u == "نام کاربری" or p == "رمز عبور":
            messagebox.showwarning("خطا", "نام کاربری و رمز عبور را وارد کنید.")
            return
        if add_user(u, p):
            messagebox.showinfo("موفقیت", "ثبت‌نام با موفقیت انجام شد. حالا وارد شوید.")
            self.master.show_login()
        else:
            messagebox.showerror("خطا", "این نام کاربری قبلا ثبت شده است.")

# --- DASHBOARD & POST SERVICES ---
class DashboardFrame(ttk.Frame):
    def __init__(self, master, username):
        super().__init__(master, padding=30)
        self.master = master
        self.username = username
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        ttk.Label(self, text=f"خوش آمدید {username}", font=("Vazirmatn", 16)).pack(pady=(0,15))
        ttk.Label(self, text="سرویس‌های پستی:", font=("Vazirmatn", 14, "bold")).pack(pady=(0,15))
        ttk.Button(self, text="رهگیری مرسوله", width=22, command=lambda: self.show_service('tracking')).pack(pady=6)
        ttk.Button(self, text="محاسبه هزینه پست", width=22, command=lambda: self.show_service('cost')).pack(pady=6)
        ttk.Button(self, text="دفاتر پستی نزدیک", width=22, command=lambda: self.show_service('branch')).pack(pady=6)
        ttk.Button(self, text="خروج", width=22, command=master.show_login).pack(pady=20)
        self.service_frame = None

    def show_service(self, service_type):
        if self.service_frame:
            self.service_frame.destroy()
        if service_type == 'tracking':
            self.service_frame = TrackingFrame(self)
        elif service_type == 'cost':
            self.service_frame = CostFrame(self)
        elif service_type == 'branch':
            self.service_frame = BranchFrame(self)
        self.service_frame.pack(pady=20)

# --- SERVICE: TRACKING ---
class TrackingFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="کد رهگیری مرسوله را وارد کنید:", font=("Vazirmatn", 13)).pack(pady=6)
        self.code_entry = ttk.Entry(self, font=("Vazirmatn", 13), width=24)
        self.code_entry.pack(pady=6)
        ttk.Button(self, text="رهگیری", command=self.track).pack(pady=6)
        self.result = ttk.Label(self, text="", font=("Vazirmatn", 12))
        self.result.pack(pady=6)

    def track(self):
        code = self.code_entry.get().strip()
        if not code:
            messagebox.showwarning("خطا", "کد رهگیری را وارد کنید.")
            return

        # --- سرویس واقعی (در صورت داشتن API) ---
        # url = "https://api.post.ir/v1/track"
        # headers = {"Authorization": "Bearer [YOUR_API_KEY]"}
        # resp = requests.post(url, json={"barcode": code}, headers=headers)
        # if resp.status_code == 200:
        #     data = resp.json()
        #     self.result.config(text=f"وضعیت: {data['state']}\nآخرین مکان: {data['last_location']}")
        # else:
        #     self.result.config(text="کد رهگیری یافت نشد یا خطا در ارتباط با سرور.")
        
        # --- شبیه‌سازی برای نمونه ---
        if code == "1234567890":
            self.result.config(text="وضعیت: ارسال شده\nآخرین مکان: تهران - مرکز تجزیه و مبادلات\nتاریخ: 1403/05/12")
        elif code == "9876543210":
            self.result.config(text="وضعیت: تحویل داده شد\nآخرین مکان: شیراز - پست منطقه ۴\nتاریخ: 1403/05/10")
        else:
            self.result.config(text="کد رهگیری یافت نشد یا هنوز وارد سیستم نشده است.")

# --- SERVICE: COST ---
class CostFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        cities = ['تهران', 'مشهد', 'شیراز', 'اصفهان', 'تبریز', 'اهواز']
        services = ['پیشتاز', 'سفارشی', 'ویژه']
        ttk.Label(self, text="محاسبه هزینه پست:", font=("Vazirmatn", 13)).pack(pady=6)
        frm = ttk.Frame(self)
        frm.pack(pady=3)
        ttk.Label(frm, text="مبدا:").grid(row=0, column=0, padx=3)
        self.src = ttk.Combobox(frm, values=cities, font=("Vazirmatn", 12), width=10)
        self.src.grid(row=0, column=1, padx=3)
        ttk.Label(frm, text="مقصد:").grid(row=0, column=2, padx=3)
        self.dst = ttk.Combobox(frm, values=cities, font=("Vazirmatn", 12), width=10)
        self.dst.grid(row=0, column=3, padx=3)
        ttk.Label(frm, text="وزن (گرم):").grid(row=1, column=0, padx=3)
        self.weight = ttk.Entry(frm, font=("Vazirmatn", 12), width=12)
        self.weight.grid(row=1, column=1, padx=3)
        ttk.Label(frm, text="سرویس:").grid(row=1, column=2, padx=3)
        self.service = ttk.Combobox(frm, values=services, font=("Vazirmatn", 12), width=10)
        self.service.grid(row=1, column=3, padx=3)
        ttk.Button(self, text="محاسبه", command=self.calc_cost).pack(pady=10)
        self.result = ttk.Label(self, text="", font=("Vazirmatn", 12))
        self.result.pack()

    def calc_cost(self):
        src = self.src.get()
        dst = self.dst.get()
        try:
            weight = int(self.weight.get())
        except ValueError:
            weight = 0
        service = self.service.get()
        if not src or not dst or not weight or not service:
            self.result.config(text="تمام اطلاعات را کامل وارد کنید.")
            return

        # --- در صورت وجود API واقعی، از آن استفاده کنید ---
        # url = "https://api.post.ir/v1/cost"
        # resp = requests.post(url, json={"src": src, "dst": dst, "weight": weight, "service": service})
        # if resp.status_code == 200:
        #     data = resp.json()
        #     self.result.config(text=f"هزینه: {data['cost']} تومان")
        # else:
        #     self.result.config(text="خطا در ارتباط با سرور.")
        
        # --- شبیه‌سازی هزینه ---
        base = 35000 if service == 'پیشتاز' else 25000 if service == 'سفارشی' else 55000
        extra = ((weight-500)//500)*5000 if weight > 500 else 0
        city_factor = 10000 if src != dst else 0
        cost = base + extra + city_factor
        self.result.config(text=f"هزینه ارسال: {cost:,} تومان")

# --- SERVICE: NEAREST POST OFFICE ---
class BranchFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        cities = ['تهران', 'مشهد', 'شیراز', 'اصفهان', 'تبریز', 'اهواز']
        ttk.Label(self, text="شهر مورد نظر را انتخاب کنید:", font=("Vazirmatn", 13)).pack(pady=6)
        self.city = ttk.Combobox(self, values=cities, font=("Vazirmatn", 12), width=14)
        self.city.pack(pady=4)
        ttk.Button(self, text="جستجوی دفاتر", command=self.search).pack(pady=5)
        self.result = ttk.Label(self, text="", font=("Vazirmatn", 12), wraplength=400)
        self.result.pack(pady=6)

    def search(self):
        city = self.city.get()
        if not city:
            self.result.config(text="نام شهر را انتخاب کنید.")
            return
        # --- اگر API واقعی داشتی، اینجا استفاده کن ---
        # url = f"https://api.post.ir/v1/branches?city={city}"
        # resp = requests.get(url)
        # if resp.status_code == 200:
        #     data = resp.json()
        #     self.result.config(text="\n".join([f"{b['name']} - {b['address']}" for b in data['branches']]))
        # else:
        #     self.result.config(text="خطا در ارتباط با سرور یا دفتر پیدا نشد.")
        
        # --- شبیه‌سازی دفاتر ---
        branches = {
            'تهران': ["دفتر مرکزی: میدان ونک - ۸۸۷۶۵۴۳۲", "دفتر غرب: خیابان آزادی - ۶۶۵۴۳۲۱۰"],
            'مشهد': ["دفتر مرکزی: بلوار وکیل آباد - ۳۸۷۶۵۴۳۲"],
            'شیراز': ["دفتر مرکزی: خیابان زند - ۷۱۲۳۴۵۶۷"],
            'اصفهان': ["دفتر مرکزی: خیابان چهارباغ - ۳۲۶۵۴۳۲۱"],
            'تبریز': ["دفتر مرکزی: خیابان امام - ۴۱۳۵۶۷۸۹"],
            'اهواز': ["دفتر مرکزی: خیابان نادری - ۳۳۵۶۷۸۹۰"]
        }
        self.result.config(text="\n".join(branches.get(city, ["دفتر پیدا نشد."])))

# --- RUN ---
if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    PostApp().mainloop()
