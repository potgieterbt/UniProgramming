import tkinter as tk
from tkinter import messagebox
import password_utl as pswd
import db
import config


class RegistrationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Student Registration").pack(pady=10)

        self.form = tk.Frame(self)
        self.form.pack(pady=10)

        self.fields = [
            ("Username", "reg_user"),
            ("Password", "reg_pass"),
            ("Pronouns", "reg_pro"),
            ("First Name", "reg_fname"),
            ("Last Name", "reg_lname"),
            ("DOB (YYYY-MM-DD)", "reg_dob"),
            ("Home Address", "reg_home"),
            ("Term-Time Address", "reg_term"),
            ("Emergency Name", "reg_e_name"),
            ("Emergency Number", "reg_e_number"),
            ("Course", "reg_course"),
        ]

        self.entries = {}
        for i, (label, attr) in enumerate(self.fields):
            tk.Label(self.form, text=label).grid(
                row=i, column=0, sticky="e", padx=5, pady=2)
            show_char = "*" if "Password" in label else ""
            ent = tk.Entry(self.form, width=40, show=show_char)
            ent.grid(row=i, column=1, padx=5, pady=2)
            self.entries[attr] = ent

        tk.Button(self, text="Complete Registration",
                  command=self.submit, bg=config.GREEN).pack(pady=10)
        tk.Button(self, text="Cancel",
                  command=lambda: controller.show_frame("LoginFrame"), bg=config.DANGER).pack()

    def submit(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Warning", "All fields are required.")
            return
        conn = db.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Logins (username, password_hash, role) VALUES (%s, %s, 'student')", (data['reg_user'], pswd.hash_password(data['reg_pass'])))
            u_id = cursor.lastrowid

            cursor.execute(
                """INSERT INTO Students (student_id, first_name, last_name, pronouns, dob,
                home_address, term_address, emergency_contact_name,
                emergency_contact_number, course)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (u_id, data['reg_fname'], data['reg_lname'], data['reg_pro'],
                 data['reg_dob'], data['reg_home'], data['reg_term'],
                 data['reg_e_name'], data['reg_e_number'], data['reg_course']))
            conn.commit()
            messagebox.showinfo("Success", "Account Created!")
            self.controller.show_frame("LoginFrame")

        except Exception as e:
            messagebox.showerror("Error", f"Could not register: {e}")
        finally:
            conn.close()
