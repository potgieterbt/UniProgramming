import tkinter as tk
from tkinter import messagebox, ttk
import db
import config


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
                  command=self.save, bg=config.GREEN, fg="white").pack(pady=10)
        tk.Button(self, text="Logout",
                  command=lambda: controller.show_frame("LoginFrame"), bg=config.DANGER).pack()

    def refresh_data(self):
        conn = db.get_connection()
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

        conn = db.get_connection()
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

        vertscrlbar = ttk.Scrollbar(
            self, orient='vertical', command=self.tree.yview)

        vertscrlbar.pack(side='right', fill='x')

        self.tree.configure(xscrollcommand=vertscrlbar.set)

        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Phone", text="Phone")
        self.tree.pack(fill="both", expand=False, padx=5, side='right')

        tk.Button(self, text="Refresh List",
                  command=self.refresh_data).pack(pady=5)
        tk.Button(self, text="Logout",
                  command=lambda: controller.show_frame("LoginFrame")).pack(pady=10)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT student_id, first_name, last_name, course, emergency_contact_number FROM Students")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=(
                row['student_id'], row['first_name'], row['last_name'], row['course'], row['emergency_contact_number']))
            conn.close()
