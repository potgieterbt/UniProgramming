# import mysql
import mariadb
import sys
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk


DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "user",
    "password": "password",
    "database": "test",
}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection():
    return mariadb.connect(**DB_CONFIG)


class User:
    name: str
    pronouns: str
    DoB: str
    Address: str


class Lecturer(User):
    lectuer_id: int


class Student(User):
    student_id: int
    TTAddress: str
    EContactName: str
    EContractNuber: str
    CourseID: str


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Student Management System")
        self.geometry("700x600")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.current_user_id = None
        self.frames = {}

        for F in (LoginFrame, RegistrationFrame, StudentDashboard, LecturerDashboard):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'refresh_data'):
            frame.refresh_data()


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        tk.Label(self, text="Login Page").pack(pady=30)
        tk.Label(self, text="Username:").pack()
        self.user_ent = tk.Entry(self, width=30)
        self.user_ent.pack(pady=5)

        tk.Label(self, text="Password:").pack()
        self.pass_ent = tk.Entry(self, show="*", width=30)
        self.pass_ent.pack(pady=5)

        tk.Button(self, text="Login", command=self.login,
                  width=20).pack(pady=20)
        tk.Button(self, text="Register as Student",
                  command=lambda: controller.show_frame("RegistrationFrame")).pack()

    def login(self):
        user = self.user_ent.get()
        password = hash_password(self.pass_ent.get())

        conn = get_connection()
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
                  command=self.submit).pack(pady=10)
        tk.Button(self, text="Cancel",
                  command=lambda: controller.show_frame("LoginFrame")).pack()

    def submit(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Warning", "All fields are required.")
            return
        conn = get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Logins (username, password_hash, role) VALUES (%s, %s, 'student')", (data['reg_user'], hash_password(data['reg_pass'])))
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


class StudentDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Your Profile").pack(pady=10)

        self.form = tk.Frame(self)
        self.form.pack()

        self.fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Pronouns", "pronouns"),
            ("DOB", "dob"),
            ("Home Address", "home_address"),
            ("Term-Time Address", "term_address"),
            ("Emergency Name", "emergency_contact_name"),
            ("Emergency Number", "emergency_contact_number"),
            ("Course", "course"),
        ]

        self.entries = {}
        for i, (label, key) in enumerate(self.fields):
            tk.Label(self.form, text=label).grid(
                row=i, column=0, sticky="e", padx=5, pady=2)
            ent = tk.Entry(self.form, width=40)
            ent.grid(row=i, column=1, padx=5, pady=2)
            self.entries[key] = ent

        tk.Button(self, text="Update Information",
                  command=self.save).pack(pady=10)
        tk.Button(self, text="Logout",
                  command=lambda: controller.show_frame("LoginFrame")).pack()

    def refresh_data(self):
        conn = get_connection()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Students WHERE student_id=%s",
                       (self.controller.current_user_id,))
        student = cursor.fetchone()
        conn.close()

        if student:
            for key, entry in self.entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, str(student[key]) if student[key] else "")

    def save(self):
        vals = [self.entries[k].get() for _, k in self.fields]
        vals.append(self.controller.current_user_id)

        conn = get_connection()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """UPDATE Students SET first_name=%s, last_name=%s, pronouns=%s,
            dob=%s, home_address=%s, term_address=%s, emergency_contact_name=%s,
            emergency_contact_number=%s, course=%s WHERE student_id=%s""",
            tuple(vals))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", "Profile Updated Successfully!")


class LecturerDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Student Record Lecturer View").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=(
            "ID", "First Name", "Last Name", "Course", "Phone"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Phone", text="Phone")
        self.tree.pack(fill="both", expand=True, padx=10)

        tk.Button(self, text="Refresh List",
                  command=self.refresh_data).pack(pady=5)
        tk.Button(self, text="Logout",
                  command=lambda: controller.show_frame("LoginFrame")).pack(pady=10)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT student_id, first_name, last_name, course, emergency_contact_number FROM Students")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=(
                row['student_id'], row['first_name'], row['last_name'], row['course'], row['emergency_contact_number']))
            conn.close()


if __name__ == "__main__":
    print(hashlib.sha256("lecturer123".encode()).hexdigest())
    app = Application()
    app.mainloop()
