import tkinter as tk
from tkinter import messagebox
import password_utl as pswd
import db
import config


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=config.BG, width=400, height=300)
        self.controller = controller

        tk.Label(self, text="Login Page", bg=config.BG).pack(pady=30)
        tk.Label(self, text="Username:", bg=config.BG).pack()
        self.user_ent = tk.Entry(self, width=30)
        self.user_ent.pack(pady=5)

        tk.Label(self, text="Password:", bg=config.BG).pack()
        self.pass_ent = tk.Entry(self, show="*", width=30)
        self.pass_ent.pack(pady=5)

        tk.Button(self, text="Login", command=self.login,
                  width=20, bg=config.GREEN, fg="white").pack(pady=20)
        tk.Button(self, text="Register as Student",
                  command=lambda: controller.show_frame("RegistrationFrame"), bg=config.SECONDARY).pack()

    def login(self):
        user = self.user_ent.get()
        password = pswd.hash_password(self.pass_ent.get())

        conn = db.get_connection()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, role FROM Logins WHERE username=%s AND password_hash=%s", (user, password))
        record = cursor.fetchone()
        conn.close()

        if record:
            self.controller.current_user_id = record['user_id']
            dest = "LecturerDashboard" if record['role'] == 'lecturer' else "StudentDashboard"
            self.controller.show_frame(dest)
        else:
            messagebox.showerror("Error", "Invalid Credentials")
