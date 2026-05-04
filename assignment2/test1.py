import tkinter as tk
from tkinter import messagebox, ttk
# import mysql.connector
import mariadb
import hashlib

# --- DATABASE CONFIGURATION ---
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "user",
    "password": "password",
    "database": "test",
}


def get_db_connection():
    try:
        return mariadb.connect(**DB_CONFIG)
    except mariadb.Error as err:
        messagebox.showerror("Database Error", f"Connection failed: {err}")
        return None


def hash_password(password):
    """Securely hashes passwords using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Digital Transformation System")
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

# --- REQUIREMENTS 2 & 3: LOGIN ---


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        tk.Label(self, text="Campus Data Portal", font=(
            "Arial", 20, "bold"), bg="#f0f0f0").pack(pady=30)

        tk.Label(self, text="Username:", bg="#f0f0f0").pack()
        self.user_ent = tk.Entry(self, width=30)
        self.user_ent.pack(pady=5)

        tk.Label(self, text="Password:", bg="#f0f0f0").pack()
        self.pass_ent = tk.Entry(self, show="*", width=30)
        self.pass_ent.pack(pady=5)

        tk.Button(self, text="Login", command=self.login,
                  width=20, bg="#4CAF50", fg="white").pack(pady=20)
        tk.Button(self, text="Register as Student",
                  command=lambda: controller.show_frame("RegistrationFrame")).pack()

    def login(self):
        user = self.user_ent.get()
        pw = hash_password(self.pass_ent.get())

        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, role FROM Logins WHERE username=%s AND password_hash=%s", (user, pw))
        record = cursor.fetchone()
        conn.close()

        if record:
            self.controller.current_user_id = record['user_id']
            dest = "LecturerDashboard" if record['role'] == 'lecturer' else "StudentDashboard"
            self.controller.show_frame(dest)
        else:
            messagebox.showerror("Error", "Invalid Credentials")

# --- REQUIREMENT 1: REGISTRATION ---


class RegistrationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Student Registration",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Form Container
        self.form = tk.Frame(self)
        self.form.pack(pady=10)

        # Fields mapping: (Label, attr_name)
        self.fields = [
            ("Username", "reg_user"), ("Password",
                                       "reg_pass"), ("Full Name", "reg_name"),
            ("Pronouns", "reg_pro"), ("DOB (YYYY-MM-DD)",
                                      "reg_dob"), ("Home Address", "reg_home"),
            ("Term Address", "reg_term"), ("Emergency Name", "reg_e_name"),
            ("Emergency Phone", "reg_e_num"), ("Course", "reg_course")
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
                  command=self.submit, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self, text="Cancel",
                  command=lambda: controller.show_frame("LoginFrame")).pack()

    def submit(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Warning", "All fields are required.")
            return

        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Logins (username, password_hash, role) VALUES (%s, %s, 'student')",
                           (data['reg_user'], hash_password(data['reg_pass'])))
            u_id = cursor.lastrowid

            cursor.execute("""INSERT INTO Students (student_id, name, pronouns, dob, home_address,
                              term_address, emergency_contact_name, emergency_contact_number, course)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (u_id, data['reg_name'], data['reg_pro'], data['reg_dob'], data['reg_home'],
                            data['reg_term'], data['reg_e_name'], data['reg_e_num'], data['reg_course']))
            conn.commit()
            messagebox.showinfo("Success", "Account Created!")
            self.controller.show_frame("LoginFrame")
        except Exception as e:
            messagebox.showerror("Error", f"Could not register: {e}")
        finally:
            conn.close()

# --- REQUIREMENTS 4 & 5: STUDENT DISPLAY & UPDATE ---


class StudentDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Your Profile", font=(
            "Arial", 16, "bold")).pack(pady=10)

        self.form = tk.Frame(self)
        self.form.pack()

        self.fields = [
            ("Full Name", "name"), ("Pronouns", "pronouns"), ("DOB", "dob"),
            ("Home Address", "home_address"), ("Term Address", "term_address"),
            ("Emergency Name", "emergency_contact_name"), ("Emergency Phone",
                                                           "emergency_contact_number"),
            ("Course", "course")
        ]

        self.entries = {}
        for i, (label, key) in enumerate(self.fields):
            tk.Label(self.form, text=label).grid(
                row=i, column=0, sticky="e", padx=5, pady=2)
            ent = tk.Entry(self.form, width=40)
            ent.grid(row=i, column=1, padx=5, pady=2)
            self.entries[key] = ent

        tk.Button(self, text="Update Information", command=self.save,
                  bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self, text="Logout",
                  command=lambda: controller.show_frame("LoginFrame")).pack()

    def refresh_data(self):
        conn = get_db_connection()
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

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Students SET name=%s, pronouns=%s, dob=%s, home_address=%s,
                          term_address=%s, emergency_contact_name=%s, emergency_contact_number=%s,
                          course=%s WHERE student_id=%s""", tuple(vals))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", "Profile Updated Successfully[cite: 1].")

# --- REQUIREMENT 6: LECTURER VIEW ---


class LecturerDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Student Records Master List",
                 font=("Arial", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=(
            "ID", "Name", "Course", "Phone"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Phone", text="Emergency #")
        self.tree.pack(fill="both", expand=True, padx=10)

        tk.Button(self, text="Refresh List",
                  command=self.refresh_data).pack(pady=5)
        tk.Button(self, text="Logout", command=lambda: controller.show_frame(
            "LoginFrame")).pack(pady=10)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT student_id, name, course, emergency_contact_number FROM Students")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=(
                row['student_id'], row['name'], row['course'], row['emergency_contact_number']))
        conn.close()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
