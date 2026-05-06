import tkinter as tk
from tkinter import messagebox, ttk
import db


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

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10)

        self.fields = [
            "First Name",
            "Last Name",
            "Pronouns",
            "DOB",
            "Home Address",
            "Term-Time Address",
            "Emergency Name",
            "Emergency Number",
            "Course",
        ]

        self.tree = ttk.Treeview(
            tree_frame, columns=self.fields, show="headings")

        h_scroll = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scroll.set)

        for col in self.fields:
            self.tree.heading(col, text=col)

        self.tree.pack(side="top", fill="both", expand=True)
        h_scroll.pack(side="bottom", fill="x")

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
            "SELECT * FROM Students")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=(
                row['first_name'], row['last_name'], row['pronouns'],
                row['dob'], row['home_address'], row['term_address'],
                row['emergency_contact_name'], row['emergency_contact_number'],
                row['course']))
        conn.close()
