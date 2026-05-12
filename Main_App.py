import webbrowser
import customtkinter as ctk
from tkinter import messagebox, ttk
import random
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import sys
import os
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# --- KONFIGURATSIYA ---
TOKEN = ""
CHAT_ID = ""

# --- UMUMIY SOZLAMALAR ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Vizual standartlar
MAIN_BG = "#EBF2FF"  # Siz tanlagan Mavjli moviy fon
CARD_BG = "#FFFFFF"
FONT_TITLE = ("Helvetica", 32, "bold")
FONT_QUESTION = ("Helvetica", 24, "bold")
FONT_BUTTON = ("Helvetica", 18, "bold")
FONT_UI = ("Helvetica", 16)


class PedagogApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Pedagog Monitoring Pro")
        self.geometry("1200x850")

        # Umumiy fonni o'rnatish
        self.configure(fg_color=MAIN_BG)

        self.init_db()
        self.quiz_bank = []
        self.admin_login_cred = "admin"
        self.admin_pass_cred = "123"
        self.show_pass = False

        self.load_quiz_bank_local()
        self.load_admin_config_from_sheets()
        self.start_screen()

    def init_db(self):
        conn = sqlite3.connect('quiz_results.db')
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS results (name TEXT, groups TEXT, topic TEXT, score INTEGER, percent INTEGER)")
        conn.commit()
        conn.close()

    def load_quiz_bank_local(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        try:
            if getattr(sys, 'frozen', False):
                BASE_DIR = sys._MEIPASS
            else:
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
            # Xatolik tuzatildi: client obyektini to'g'ri yaratish
            self.gc_client = gspread.authorize(creds)
            self.sheet = self.gc_client.open("Pedagog_Baza").sheet1
            self.quiz_bank = self.sheet.get_all_records()
        except Exception as e:
            messagebox.showerror("Xato", f"Google Sheets yuklashda xato: {e}")

    def load_admin_config_from_sheets(self):
        try:
            admin_sheet = self.gc_client.open("AdminConfig").sheet1
            data = admin_sheet.get_all_records()
            if data:
                last_row = data[-1]
                self.admin_login_cred = str(last_row.get("Login", "admin"))
                self.admin_pass_cred = str(last_row.get("Password", "123"))
        except:
            pass

    def save_admin_config_to_sheets(self):
        try:
            admin_sheet = self.gc_client.open("AdminConfig").sheet1
            admin_sheet.append_row([self.admin_login_cred, self.admin_pass_cred])
            return True
        except:
            return False

    def clear(self):
        for w in self.winfo_children(): w.destroy()

    def start_screen(self):
        self.clear()
        # Markaziy karta
        main_card = ctk.CTkFrame(self, corner_radius=35, fg_color=CARD_BG, border_width=1, border_color="#D1D5DB")
        main_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.7)

        header = ctk.CTkFrame(main_card, fg_color="transparent")
        header.pack(pady=(40, 20))
        ctk.CTkLabel(header, text="🎓", font=("Helvetica", 75)).pack()
        ctk.CTkLabel(header, text="AI Pedagog", font=FONT_TITLE, text_color="#111827").pack()
        ctk.CTkFrame(header, height=3, width=120, fg_color="#3B82F6").pack(pady=10)
        ctk.CTkLabel(header, text="Monitoring System Pro", font=("Helvetica", 16, "italic"),
                     text_color="#6B7280").pack()

        btn_container = ctk.CTkFrame(main_card, fg_color="transparent")
        btn_container.pack(expand=True, fill="both", padx=60)

        self.student_btn = ctk.CTkButton(btn_container, text="👨‍🎓  TALABA SIFATIDA KIRISH", height=65, font=FONT_BUTTON,
                                         corner_radius=15, fg_color="#2563EB", hover_color="#1E40AF",
                                         command=self.student_login_ui)
        self.student_btn.pack(fill="x", pady=12)

        self.admin_btn = ctk.CTkButton(btn_container, text="👨‍🏫  O'QITUVCHI SIFATIDA KIRISH", height=65,
                                       font=FONT_BUTTON,
                                       corner_radius=15, fg_color="#059669", hover_color="#047857",
                                       command=self.admin_login_ui)
        self.admin_btn.pack(fill="x", pady=12)

        footer = ctk.CTkFrame(main_card, fg_color="transparent")
        footer.pack(side="bottom", pady=20)
        ctk.CTkLabel(footer, text="© 2026 AI Pedagog Team", font=("Helvetica", 11), text_color="#9CA3AF").pack()
        ctk.CTkLabel(footer, text=" v2.0.1 ", fg_color="#F3F4F6", corner_radius=5, font=("Helvetica", 10, "bold")).pack(
            pady=5)

    def admin_login_ui(self):
        self.clear()
        f = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=30, border_width=1, border_color="#D1D5DB")
        f.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.6)

        ctk.CTkLabel(f, text="Admin Kirish", font=FONT_QUESTION).pack(pady=(35, 20))
        self.l_e = ctk.CTkEntry(f, placeholder_text="Login", width=380, height=55, font=FONT_UI, corner_radius=12)
        self.l_e.pack(pady=10)

        p_frame = ctk.CTkFrame(f, fg_color="transparent")
        p_frame.pack(pady=10)
        self.p_e = ctk.CTkEntry(p_frame, placeholder_text="Parol", show="*", width=380, height=55, font=FONT_UI,
                                corner_radius=12)
        self.p_e.pack(side="left")

        self.eye_btn = ctk.CTkButton(p_frame, text="👁️", width=40, height=40, fg_color="transparent", text_color="grey",
                                     command=self.toggle_password)
        self.eye_btn.place(relx=0.9, rely=0.5, anchor="center")

        ctk.CTkButton(f, text="KIRISH", height=65, width=380, font=FONT_BUTTON, corner_radius=12,
                      command=self.check_admin).pack(pady=20)

        # Parolni o'zgartirish uslubini yumshatish
        ctk.CTkButton(f, text="Parolni o'zgartirish 🔑", height=50, width=380, font=("Helvetica", 15, "bold"),
                      fg_color="#F59E0B", corner_radius=12, command=self.change_password_ui).pack(pady=5)

        ctk.CTkButton(f, text="Parolni unutdingizmi?", font=("Helvetica", 13, "underline"), fg_color="transparent",
                      text_color="#3B82F6", command=self.contact_developer).pack()
        ctk.CTkButton(f, text="Orqaga", font=FONT_UI, fg_color="transparent", text_color="grey",
                      command=self.start_screen).pack(pady=10)

    def toggle_password(self):
        self.show_pass = not self.show_pass
        self.p_e.configure(show="" if self.show_pass else "*")
        self.eye_btn.configure(text="🔒" if self.show_pass else "👁️")

    def check_admin(self):
        if self.l_e.get() == self.admin_login_cred and self.p_e.get() == self.admin_pass_cred:
            self.admin_panel()
        else:
            messagebox.showerror("Xato", "Login yoki parol noto'g'ri!")

    def student_login_ui(self):
        self.clear()
        card = ctk.CTkFrame(self, corner_radius=30, fg_color=CARD_BG, border_width=1, border_color="#D1D5DB")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.55)

        ctk.CTkLabel(card, text="Talaba Ma'lumotlari", font=FONT_QUESTION).pack(pady=(40, 20))
        self.n_e = ctk.CTkEntry(card, placeholder_text="F.I.SH", width=400, height=60, font=FONT_UI, corner_radius=12)
        self.n_e.pack(pady=12)
        self.g_e = ctk.CTkEntry(card, placeholder_text="Guruh", width=400, height=60, font=FONT_UI, corner_radius=12)
        self.g_e.pack(pady=12)

        ctk.CTkButton(card, text="Mavzularga o'tish", height=65, width=400, font=FONT_BUTTON, corner_radius=15,
                      fg_color="#3B82F6", command=self.show_topics).pack(pady=15)
        ctk.CTkButton(card, text="Orqaga", font=FONT_UI, fg_color="transparent", text_color="grey",
                      command=self.start_screen).pack()

    def show_topics(self):
        self.u_name, self.u_group = self.n_e.get(), self.g_e.get()
        if not self.u_name or not self.u_group:
            messagebox.showwarning("!", "Ma'lumotni kiriting!")
            return
        self.clear()
        ctk.CTkLabel(self, text="Mavzuni tanlang", font=FONT_TITLE).pack(pady=30)
        topics = list(set([q['Mavzu'] for q in self.quiz_bank if q.get('Mavzu')]))
        scroll = ctk.CTkScrollableFrame(self, width=1000, height=550, fg_color="transparent")
        scroll.pack()
        for t in topics:
            ctk.CTkButton(scroll, text=t, height=80, width=950, font=FONT_BUTTON, corner_radius=15,
                          fg_color=CARD_BG, text_color="black", border_width=1, border_color="#D1D5DB",
                          hover_color="#F3F4F6", command=lambda m=t: self.start_test(m)).pack(pady=8)

    def start_test(self, topic):
        qs = [q for q in self.quiz_bank if q['Mavzu'] == topic]
        self.quiz_data = random.sample(qs, min(len(qs), 20))
        self.cur_topic, self.q_idx, self.score = topic, 0, 0
        self.remaining_time = 600
        self.test_ui()
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            if hasattr(self, 'timer_label'): self.timer_label.configure(text=f"⏳ {mins:02d}:{secs:02d}")
            self.remaining_time -= 1
            self.timer_after = self.after(1000, self.update_timer)
        else:
            self.finish_test(forced=True)

    def test_ui(self):
        self.clear()
        q = self.quiz_data[self.q_idx]
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=60, pady=20)
        ctk.CTkLabel(top, text=f"Savol: {self.q_idx + 1}/{len(self.quiz_data)}", font=FONT_UI).pack(side="left")
        self.timer_label = ctk.CTkLabel(top, text="⏳ 10:00", font=FONT_QUESTION, text_color="#EF4444")
        self.timer_label.pack(side="right")

        q_card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=30, border_width=1, border_color="#D1D5DB")
        q_card.pack(pady=10, padx=60, fill="both", expand=True)
        ctk.CTkLabel(q_card, text=q['Savol'], font=FONT_QUESTION, wraplength=900).pack(pady=40, padx=20)

        opts = [q['A'], q['B'], q['C'], q['D']]
        random.shuffle(opts)
        for opt in opts:
            ctk.CTkButton(q_card, text=opt, height=70, width=850, font=FONT_BUTTON, fg_color="#F9FAFB",
                          text_color="black", hover_color="#EBF2FF", corner_radius=12,
                          command=lambda a=opt: self.check_ans(a, q['Javob'])).pack(pady=7)

        ctk.CTkButton(self, text="Testni yakunlash", height=50, width=250, font=FONT_UI, fg_color="#EF4444",
                      corner_radius=12, command=self.finish_test).pack(pady=20)

    def check_ans(self, ans, correct):
        if str(ans).strip() == str(correct).strip(): self.score += 1
        self.q_idx += 1
        if self.q_idx < len(self.quiz_data):
            self.test_ui()
        else:
            self.finish_test(forced=True)

    def finish_test(self, forced=False):
        try:
            self.after_cancel(self.timer_after)
        except:
            pass
        percent = int((self.score / len(self.quiz_data)) * 100)
        conn = sqlite3.connect('quiz_results.db')
        conn.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?)",
                     (self.u_name, self.u_group, self.cur_topic, self.score, percent))
        conn.commit()
        conn.close()
        self.send_telegram(self.u_name, self.u_group, self.cur_topic, self.score, percent)
        self.save_to_google_sheets(self.u_name, self.u_group, self.cur_topic, self.score, percent)
        self.show_final_result(percent)

    def show_final_result(self, percent):
        self.clear()
        res = ctk.CTkFrame(self, corner_radius=35, fg_color=CARD_BG, border_width=2, border_color="#10B981")
        res.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.65)
        ctk.CTkLabel(res, text="🏆 NATIJA", font=FONT_TITLE, text_color="#10B981").pack(pady=(40, 10))
        ctk.CTkLabel(res, text=f"{self.u_name}", font=FONT_BUTTON).pack()
        ctk.CTkLabel(res, text=f"{percent}%", font=("Helvetica", 120, "bold"), text_color="#3B82F6").pack(pady=20)
        ctk.CTkLabel(res, text=f"To'g'ri javoblar: {self.score} / {len(self.quiz_data)}", font=FONT_UI).pack()
        ctk.CTkButton(res, text="ASOSIY MENYUGA QAYTISH", height=65, width=350, font=FONT_BUTTON, corner_radius=15,
                      command=self.start_screen).pack(pady=40)

    def admin_panel(self):
        self.clear()
        ctk.CTkLabel(self, text="👨‍🏫 Boshqaruv paneli", font=FONT_TITLE).pack(pady=50)
        p = ctk.CTkFrame(self, fg_color="transparent")
        p.pack(expand=True)
        ctk.CTkButton(p, text="📊 NATIJALARNI KO'RISH", height=80, width=500, font=FONT_BUTTON, corner_radius=15,
                      command=self.show_results).pack(pady=12)
        ctk.CTkButton(p, text="📝 SAVOLLARNI TAHRIRLASH", height=80, width=500, font=FONT_BUTTON, corner_radius=15,
                      fg_color="#F59E0B", command=self.edit_questions_ui).pack(pady=12)
        ctk.CTkButton(p, text="🏠 CHIQISH", height=80, width=500, font=FONT_BUTTON, corner_radius=15,
                      fg_color="#4B5563", command=self.start_screen).pack(pady=12)

    def show_results(self):
        self.clear()
        ctk.CTkLabel(self, text="📊 Imtihon Natijalari", font=FONT_TITLE).pack(pady=25)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40)
        ctk.CTkButton(btn_frame, text="🔙 Orqaga", height=50, width=180, font=FONT_UI, corner_radius=12,
                      command=self.admin_panel).pack(side="left")
        ctk.CTkButton(btn_frame, text="🗑️ Tozalash", height=50, width=180, font=FONT_UI, corner_radius=12,
                      fg_color="#EF4444", command=self.clear_all_results).pack(side="right")

        f = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=20)
        f.pack(fill="both", expand=True, padx=40, pady=20)

        style = ttk.Style()
        style.configure("Results.Treeview", font=("Helvetica", 13), rowheight=35)
        self.result_tree = ttk.Treeview(f, columns=("N", "G", "M", "B", "P"), show="headings", style="Results.Treeview")
        for c, h in zip(("N", "G", "M", "B", "P"), ("F.I.SH", "Guruh", "Mavzu", "Ball", "Foiz")):
            self.result_tree.heading(c, text=h)
            self.result_tree.column(c, anchor="center", width=180)
        self.result_tree.pack(fill="both", expand=True, padx=10, pady=10)

        conn = sqlite3.connect('quiz_results.db')
        for r in conn.execute("SELECT * FROM results"): self.result_tree.insert("", "end", values=r)
        conn.close()

    # --- BOSHQA METODLAR (Kodingizdagi mantiq o'zgarishsiz qoldi) ---
    def contact_developer(self):
        webbrowser.open("https://t.me/Jumayev_Asliddin")

    def send_telegram(self, name, group, topic, score, percent):
        text = f"✅ **Test Yakunlandi**\n\n👤 **Talaba:** {name}\n👥 **Guruh:** {group}\n🎯 **Natija:** {score}/20 ({percent}%)"
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=5)
        except:
            pass

    def save_to_google_sheets(self, name, group, topic, score, percent):
        try:
            res_sh = self.gc_client.open("Natijalar").sheet1
            res_sh.append_row([name, group, topic, score, f"{percent}%"])
        except:
            pass

    def clear_all_results(self):
        if messagebox.askyesno("Tasdiqlash", "Barcha natijalar o'chirilsinmi?"):
            try:
                conn = sqlite3.connect('quiz_results.db')
                conn.execute("DELETE FROM results");
                conn.commit();
                conn.close()
                self.gc_client.open("Natijalar").sheet1.batch_clear(['A2:E100'])
                for item in self.result_tree.get_children(): self.result_tree.delete(item)
                messagebox.showinfo("Tayyor", "Barcha ma'lumotlar o'chirildi!")
            except Exception as e:
                messagebox.showerror("Xato", str(e))

    # Edit questions va change password qismlari ham yangi dizaynda...
    def edit_questions_ui(self):
        self.clear()
        ctk.CTkLabel(self, text="Savollarni tahrirlash", font=FONT_TITLE).pack(pady=20)
        ctk.CTkButton(self, text="🔙 Orqaga", height=45, width=150, font=FONT_UI, command=self.admin_panel).pack(pady=5)
        f = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        f.pack(fill="both", expand=True, padx=40, pady=20)
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Helvetica", 14), rowheight=38)
        cols = ("ID", "Mavzu", "Savol", "Javob")
        self.tree = ttk.Treeview(f, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center", width=100 if c == "ID" else 300)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.open_edit_window)
        for i, q in enumerate(self.quiz_bank, start=2):
            self.tree.insert("", "end", values=(i, q.get('Mavzu'), q.get('Savol'), q.get('Javob')))

    def open_edit_window(self, event):
        # Bu oyna CTkToplevel bo'lgani uchun fonini moslaymiz
        selection = self.tree.selection()
        if not selection: return
        item = selection[0];
        vals = self.tree.item(item)['values'];
        row_id = vals[0]
        full_row = self.sheet.row_values(row_id)

        edit_win = ctk.CTkToplevel(self)
        edit_win.title(f"Tahrirlash - {row_id}")
        edit_win.geometry("950x850")
        edit_win.configure(fg_color=MAIN_BG)
        edit_win.attributes("-topmost", True)

        scroll = ctk.CTkScrollableFrame(edit_win, width=900, height=750, fg_color=CARD_BG, corner_radius=20)
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        fields = {}
        labels = ["Mavzu (A)", "Savol (B)", "A variant (C)", "B variant (D)", "C variant (E)", "D variant (F)",
                  "To'g'ri Javob (G)"]
        for i, label in enumerate(labels):
            ctk.CTkLabel(scroll, text=label, font=("Helvetica", 16, "bold")).pack(pady=(10, 2))
            if i == 1:
                ent = ctk.CTkTextbox(scroll, width=800, height=100, font=FONT_UI, border_width=2)
                ent.insert("1.0", full_row[i] if len(full_row) > i else "")
            else:
                ent = ctk.CTkEntry(scroll, width=800, height=50, font=FONT_UI, border_width=2)
                ent.insert(0, full_row[i] if len(full_row) > i else "")
            ent.pack();
            fields[label] = ent

        def save():
            new = [fields["Mavzu (A)"].get(), fields["Savol (B)"].get("1.0", "end-1c"), fields["A variant (C)"].get(),
                   fields["B variant (D)"].get(), fields["C variant (E)"].get(), fields["D variant (F)"].get(),
                   fields["To'g'ri Javob (G)"].get()]
            self.sheet.update(range_name=f"A{row_id}:G{row_id}", values=[new])
            messagebox.showinfo("OK", "Saqlandi!", parent=edit_win)
            edit_win.destroy();
            self.edit_questions_ui()

        ctk.CTkButton(scroll, text="💾 SAQLASH", height=65, width=400, font=FONT_BUTTON, command=save).pack(pady=25)

    def change_password_ui(self):
        self.clear()
        f = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=30, border_width=1, border_color="#D1D5DB")
        f.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.7)
        ctk.CTkLabel(f, text="Login va parolni o'zgartirish", font=FONT_QUESTION).pack(pady=30)
        self.old_login = ctk.CTkEntry(f, placeholder_text="Eski login", width=400, height=50, font=FONT_UI)
        self.old_login.pack(pady=8)
        self.old_pass = ctk.CTkEntry(f, placeholder_text="Eski parol", show="*", width=400, height=50, font=FONT_UI)
        self.old_pass.pack(pady=8)
        self.new_login = ctk.CTkEntry(f, placeholder_text="Yangi login", width=400, height=50, font=FONT_UI,
                                      state="disabled")
        self.new_login.pack(pady=8)
        self.new_pass = ctk.CTkEntry(f, placeholder_text="Yangi parol", width=400, height=50, font=FONT_UI,
                                     state="disabled")
        self.new_pass.pack(pady=8)
        ctk.CTkButton(f, text="TEKSHIRISH ✅", height=55, width=400, font=FONT_BUTTON, fg_color="#10B981",
                      command=self.verify_old_credentials).pack(pady=10)
        ctk.CTkButton(f, text="SAQLASH 💾", height=55, width=400, font=FONT_BUTTON, fg_color="#F59E0B",
                      command=self.save_new_credentials).pack(pady=5)
        ctk.CTkButton(f, text="Orqaga", font=FONT_UI, fg_color="transparent", text_color="grey",
                      command=self.admin_login_ui).pack(pady=10)

    def verify_old_credentials(self):
        if self.old_login.get() == self.admin_login_cred and self.old_pass.get() == self.admin_pass_cred:
            self.new_login.configure(state="normal");
            self.new_pass.configure(state="normal")
            messagebox.showinfo("OK", "To'g'ri! Endi yangi ma'lumotlarni kiriting.")
        else:
            messagebox.showerror("Xato", "Eski ma'lumotlar noto'g'ri!")

    def save_new_credentials(self):
        if self.new_login.get() and self.new_pass.get():
            self.admin_login_cred, self.admin_pass_cred = self.new_login.get(), self.new_pass.get()
            if self.save_admin_config_to_sheets():
                messagebox.showinfo("OK", "Saqlandi!");
                self.admin_login_ui()
        else:
            messagebox.showwarning("!", "Ma'lumotlarni to'liq kiriting!")


if __name__ == "__main__":
    app = PedagogApp()
    app.mainloop()