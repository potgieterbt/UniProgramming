import hashlib
import re
import tkinter as tk
from tkinter import messagebox, ttk

import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "university_db",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def hash_password(plaintext: str) -> str:
    import os
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256", plaintext.encode("utf-8"), salt, 260_000)
    return salt.hex() + ":" + dk.hex()


def verify_password(plaintext: str, stored: str) -> bool:
    try:
        salt_hex, dk_hex = stored.split(":")
        salt = bytes.fromhex(salt_hex)
        dk = hashlib.pbkdf2_hmac(
            "sha256", plaintext.encode("utf-8"), salt, 260_000
        )
        return dk.hex() == dk_hex
    except (ValueError, AttributeError):
        return False


# ===========================================================================
# IDK if I'll keep
# ===========================================================================
def is_valid_username(value: str) -> bool:
    """Return True if value is 3–30 word characters (letters, digits, _)."""
    return bool(re.match(r"^\w{3,30}$", value))


def is_valid_phone(value: str) -> bool:
    """Return True if value looks like a plausible phone number (7–15 chars)."""
    return bool(re.match(r"^[\d\s+\-()]{7,15}$", value))


def is_valid_date(value: str) -> bool:
    """Return True if value is a valid date in DD/MM/YYYY format."""
    from datetime import datetime
    try:
        datetime.strptime(value, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def is_strong_password(value: str) -> tuple[bool, str]:
    """
    Return (True, '') if the password meets complexity rules, otherwise
    return (False, reason).

    Rules: ≥8 chars, at least one uppercase, one lowercase, one digit.
    """
    if len(value) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", value):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", value):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", value):
        return False, "Password must contain at least one digit."
    return True, ""

# ===========================================================================

# ===========================================================================


BG = "#F0F4F8"
PRIMARY = "#1D4E89"
SECONDARY = "#3A86FF"
ACCENT = "#EBF3FF"
WHITE = "#FFFFFF"
TEXT_DARK = "#1A202C"
TEXT_MUTED = "#718096"
DANGER = "#C0392B"
SUCCESS = "#27AE60"
BORDER = "#CBD5E0"
CARD = "#FFFFFF"

F_H1 = ("Segoe UI", 20, "bold")
F_H2 = ("Segoe UI", 14, "bold")
F_BODY = ("Segoe UI", 11)
F_SMALL = ("Segoe UI", 9)
F_BTN = ("Segoe UI", 11, "bold")
F_LABEL = ("Segoe UI", 10)

COURSES = [
    "BSc Computer Science",
    "BSc Software Engineering",
    "BSc Data Science",
    "BSc Cybersecurity",
    "MEng Computer Science",
    "MSc Artificial Intelligence",
    "MSc Data Science",
]

PRONOUNS = [
    "He/Him",
    "She/Her",
    "They/Them",
    "He/They",
    "She/They",
    "Other / Prefer not to say",
]


# ─────────────────────────────────────────────────────────────────────────────
# REUSABLE WIDGET FACTORY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def make_label(parent, text, font=F_BODY, fg=TEXT_DARK, anchor="w", **kw):
    """Create and return a configured Label widget."""
    bg = kw.pop("bg", parent.cget("bg"))
    lbl = tk.Label(
        parent, text=text, font=font, fg=fg, bg=bg, anchor=anchor, **kw
    )
    return lbl


def make_entry(parent, show=None, width=32):
    """Create and return a styled single-line Entry widget."""
    return tk.Entry(
        parent,
        show=show,
        font=F_BODY,
        width=width,
        relief="flat",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=SECONDARY,
        bg=WHITE,
    )


def make_button(parent, text, command, colour=PRIMARY, fg=WHITE, width=18):
    """Create and return a styled Button widget."""
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=F_BTN,
        bg=colour,
        fg=fg,
        relief="flat",
        cursor="hand2",
        width=width,
        padx=10,
        pady=8,
        activebackground=SECONDARY,
        activeforeground=WHITE,
    )


def make_dropdown(parent, variable, choices, width=29):
    """Create and return an OptionMenu dropdown bound to *variable*."""
    menu = tk.OptionMenu(parent, variable, *choices)
    menu.config(
        font=F_BODY,
        bg=WHITE,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        width=width,
        anchor="w",
    )
    menu["menu"].config(font=F_BODY)
    return menu


def add_separator(parent, pady=6):
    """Add a horizontal separator line to *parent*."""
    ttk.Separator(parent, orient="horizontal").pack(
        fill="x", padx=20, pady=pady
    )


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Student Management System")
        self.geometry("760x640")
        self.minsize(680, 560)
        self.configure(bg=BG)

        # Shared state – set after a successful login
        self.current_login_id: int | None = None
        self.current_student_id: int | None = None

        self._frames: dict[str, tk.Frame] = {}
        self._build_all_frames()
        self.show_frame("WelcomePage")

    def _build_all_frames(self):
        """Instantiate all page frames and stack them in the same grid cell."""
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        pages = (
            WelcomePage,
            StudentLoginPage,
            LecturerLoginPage,
            StudentRegisterPage,
            StudentDashboardPage,
            StudentUpdatePage,
            LecturerDashboardPage,
        )
        for PageClass in pages:
            frame = PageClass(container, self)
            self._frames[PageClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name: str):
        """Raise the named page to the top, calling refresh() if available."""
        frame = self._frames[name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.tkraise()

    def logout(self):
        """Clear session state and return to the welcome screen."""
        self.current_login_id = None
        self.current_student_id = None
        self.show_frame("WelcomePage")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: WELCOME
# ─────────────────────────────────────────────────────────────────────────────

class WelcomePage(tk.Frame):
    """
    Landing screen – lets the user choose to log in as a student,
    register as a new student, or log in as the lecturer.
    """

    def __init__(self, parent, controller: App):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Header banner
        banner = tk.Frame(self, bg=PRIMARY, height=100)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        make_label(
            banner, "University Student Portal",
            font=F_H1, fg=WHITE, bg=PRIMARY,
        ).pack(expand=True)

        # Card container
        card = tk.Frame(self, bg=CARD, relief="flat", bd=0)
        card.pack(expand=True, padx=60, pady=30, fill="both")

        make_label(
            card, "Welcome – please choose an option below",
            font=F_H2, fg=TEXT_DARK, bg=CARD,
        ).pack(pady=(30, 6))

        make_label(
            card,
            "This system allows students to manage their personal\n"
            "records and lecturers to view student information.",
            font=F_BODY, fg=TEXT_MUTED, bg=CARD, justify="center",
        ).pack(pady=(0, 30))

        # Navigation buttons
        btn_frame = tk.Frame(card, bg=CARD)
        btn_frame.pack(pady=10)

        make_button(
            btn_frame, "Student Login",
            lambda: self.controller.show_frame("StudentLoginPage"),
        ).grid(row=0, column=0, padx=8, pady=8)

        make_button(
            btn_frame, "Register Account",
            lambda: self.controller.show_frame("StudentRegisterPage"),
            colour=SUCCESS,
        ).grid(row=0, column=1, padx=8, pady=8)

        make_button(
            btn_frame, "Lecturer Login",
            lambda: self.controller.show_frame("LecturerLoginPage"),
            colour=TEXT_MUTED,
        ).grid(row=1, column=0, columnspan=2, padx=8, pady=8)

        # Footer
        make_label(
            self, "SFTW4002 – Principles of Programming  |  Summative 2",
            font=F_SMALL, fg=TEXT_MUTED, bg=BG,
        ).pack(side="bottom", pady=8)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: STUDENT LOGIN  (Requirement 2)
# ─────────────────────────────────────────────────────────────────────────────

class StudentLoginPage(tk.Frame):
    """Allow a registered student to log in with username and password."""

    def __init__(self, parent, controller: App):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        _build_page_header(self, "Student Login", PRIMARY)

        card = _make_card(self)

        make_label(card, "Username", font=F_LABEL, fg=TEXT_MUTED, bg=CARD).pack(
            anchor="w", padx=40, pady=(20, 2)
        )
        self._username_var = tk.StringVar()
        entry_username = make_entry(card)
        entry_username.config(textvariable=self._username_var)
        entry_username.pack(anchor="w", padx=40, pady=(0, 8))

        make_label(card, "Password", font=F_LABEL, fg=TEXT_MUTED, bg=CARD).pack(
            anchor="w", padx=40, pady=(4, 2)
        )
        self._password_var = tk.StringVar()
        entry_password = make_entry(card, show="•")
        entry_password.config(textvariable=self._password_var)
        entry_password.pack(anchor="w", padx=40, pady=(0, 20))

        # Show/hide password toggle
        self._show_pw = tk.BooleanVar(value=False)
        tk.Checkbutton(
            card,
            text="Show password",
            variable=self._show_pw,
            font=F_SMALL,
            bg=CARD,
            fg=TEXT_MUTED,
            command=lambda: entry_password.config(
                show="" if self._show_pw.get() else "•"
            ),
        ).pack(anchor="w", padx=40, pady=(0, 16))

        make_button(card, "Log In", self._attempt_login).pack(
            anchor="w", padx=40, pady=(0, 10)
        )

        add_separator(card)

        _make_back_link(card, "← Back to Welcome", self.controller)

    def _attempt_login(self):
        """Validate credentials and navigate to the student dashboard."""
        username = self._username_var.get().strip()
        password = self._password_var.get()

        if not username or not password:
            messagebox.showerror(
                "Login Failed", "Please enter both username and password.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT login_id, password_hash, role, student_id "
                "FROM login WHERE username = %s",
                (username,),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        if row is None or not verify_password(password, row["password_hash"]):
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password.\nPlease try again.",
            )
            return

        if row["role"] != "student":
            messagebox.showerror(
                "Login Failed",
                "This account is not a student account.\n"
                "Please use the Lecturer Login page.",
            )
            return

        # Successful login – save session and navigate
        self.controller.current_login_id = row["login_id"]
        self.controller.current_student_id = row["student_id"]
        self._username_var.set("")
        self._password_var.set("")
        self.controller.show_frame("StudentDashboardPage")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LECTURER LOGIN  (Requirement 3)
# ─────────────────────────────────────────────────────────────────────────────

class LecturerLoginPage(tk.Frame):
    """Allow the pre-configured lecturer to log in."""

    def __init__(self, parent, controller: App):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        _build_page_header(self, "Lecturer Login", TEXT_MUTED)

        card = _make_card(self)

        make_label(
            card,
            "This login is restricted to authorised teaching staff.",
            font=F_SMALL, fg=TEXT_MUTED, bg=CARD,
        ).pack(padx=40, pady=(16, 0), anchor="w")

        make_label(card, "Username", font=F_LABEL, fg=TEXT_MUTED, bg=CARD).pack(
            anchor="w", padx=40, pady=(14, 2)
        )
        self._username_var = tk.StringVar()
        entry_u = make_entry(card)
        entry_u.config(textvariable=self._username_var)
        entry_u.pack(anchor="w", padx=40)

        make_label(card, "Password", font=F_LABEL, fg=TEXT_MUTED, bg=CARD).pack(
            anchor="w", padx=40, pady=(10, 2)
        )
        self._password_var = tk.StringVar()
        entry_p = make_entry(card, show="•")
        entry_p.config(textvariable=self._password_var)
        entry_p.pack(anchor="w", padx=40, pady=(0, 6))

        self._show_pw = tk.BooleanVar(value=False)
        tk.Checkbutton(
            card,
            text="Show password",
            variable=self._show_pw,
            font=F_SMALL,
            bg=CARD,
            fg=TEXT_MUTED,
            command=lambda: entry_p.config(
                show="" if self._show_pw.get() else "•"
            ),
        ).pack(anchor="w", padx=40, pady=(0, 16))

        make_button(
            card, "Log In", self._attempt_login, colour=TEXT_MUTED
        ).pack(anchor="w", padx=40, pady=(0, 10))

        add_separator(card)
        _make_back_link(card, "← Back to Welcome", self.controller)

    def _attempt_login(self):
        """Validate lecturer credentials and navigate to the lecturer dashboard."""
        username = self._username_var.get().strip()
        password = self._password_var.get()

        if not username or not password:
            messagebox.showerror(
                "Login Failed", "Please enter both username and password.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT login_id, password_hash, role "
                "FROM login WHERE username = %s",
                (username,),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        if row is None or not verify_password(password, row["password_hash"]):
            messagebox.showerror(
                "Login Failed", "Incorrect username or password.")
            return

        if row["role"] != "lecturer":
            messagebox.showerror(
                "Login Failed",
                "This account is not a lecturer account.\n"
                "Please use the Student Login page.",
            )
            return

        self.controller.current_login_id = row["login_id"]
        self._username_var.set("")
        self._password_var.set("")
        self.controller.show_frame("LecturerDashboardPage")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: STUDENT REGISTRATION  (Requirement 1)
# ─────────────────────────────────────────────────────────────────────────────

class StudentRegisterPage(tk.Frame):
    """
    Multi-field registration form.  Collects all required student details,
    validates them, hashes the password, and inserts into the database.
    """

    def __init__(self, parent, controller: App):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        _build_page_header(self, "Create Student Account", SUCCESS)

        scroll = ScrollableFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=30, pady=10)

        card = scroll.inner
        card.configure(bg=CARD)

        def row(label_text, widget_or_var, hint=""):
            """Helper: add a label + widget pair to the form."""
            make_label(card, label_text, font=F_LABEL, fg=TEXT_MUTED, bg=CARD).pack(
                anchor="w", padx=40, pady=(10, 1)
            )
            if isinstance(widget_or_var, tk.Widget):
                widget_or_var.pack(anchor="w", padx=40)
            if hint:
                make_label(
                    card, hint, font=F_SMALL, fg=TEXT_MUTED, bg=CARD
                ).pack(anchor="w", padx=40)

        # ── Personal details ──────────────────────────────────────────
        make_label(
            card, "Personal Details", font=F_H2, fg=PRIMARY, bg=CARD
        ).pack(anchor="w", padx=40, pady=(20, 0))

        self._name = make_entry(card)
        row("Full Name *", self._name)

        self._pronouns_var = tk.StringVar(value=PRONOUNS[0])
        pronouns_menu = make_dropdown(card, self._pronouns_var, PRONOUNS)
        row("Pronouns *", pronouns_menu)

        self._dob = make_entry(card, width=16)
        row("Date of Birth * (DD/MM/YYYY)", self._dob)

        # ── Addresses ─────────────────────────────────────────────────
        add_separator(card, pady=10)
        make_label(
            card, "Addresses", font=F_H2, fg=PRIMARY, bg=CARD
        ).pack(anchor="w", padx=40, pady=(0, 0))

        self._home_addr = make_entry(card)
        row("Home Address *", self._home_addr)

        self._same_addr = tk.BooleanVar(value=False)
        tk.Checkbutton(
            card,
            text="Term-time address is the same as home address",
            variable=self._same_addr,
            font=F_LABEL,
            bg=CARD,
            fg=TEXT_DARK,
            command=self._toggle_term_addr,
        ).pack(anchor="w", padx=40, pady=(10, 2))

        self._term_addr = make_entry(card)
        self._term_addr.pack(anchor="w", padx=40)
        make_label(
            card, "Leave blank if same as home address",
            font=F_SMALL, fg=TEXT_MUTED, bg=CARD
        ).pack(anchor="w", padx=40)

        # ── Emergency contact ─────────────────────────────────────────
        add_separator(card, pady=10)
        make_label(
            card, "Emergency Contact", font=F_H2, fg=PRIMARY, bg=CARD
        ).pack(anchor="w", padx=40, pady=(0, 0))

        self._emg_name = make_entry(card)
        row("Contact Name *", self._emg_name)

        self._emg_number = make_entry(card, width=20)
        row("Contact Phone Number *", self._emg_number, "e.g. 07700 900123")

        # ── Academic ──────────────────────────────────────────────────
        add_separator(card, pady=10)
        make_label(
            card, "Academic", font=F_H2, fg=PRIMARY, bg=CARD
        ).pack(anchor="w", padx=40, pady=(0, 0))

        self._course_var = tk.StringVar(value=COURSES[0])
        course_menu = make_dropdown(card, self._course_var, COURSES)
        row("Course *", course_menu)

        # ── Account credentials ───────────────────────────────────────
        add_separator(card, pady=10)
        make_label(
            card, "Account Credentials", font=F_H2, fg=PRIMARY, bg=CARD
        ).pack(anchor="w", padx=40, pady=(0, 0))

        self._username = make_entry(card, width=24)
        row("Username * (3–30 characters, letters/digits/underscore)",
            self._username)

        self._password = make_entry(card, show="•", width=24)
        row("Password * (min 8 chars, upper, lower, digit)", self._password)

        self._confirm_pw = make_entry(card, show="•", width=24)
        row("Confirm Password *", self._confirm_pw)

        # ── Buttons ───────────────────────────────────────────────────
        add_separator(card, pady=10)
        btn_row = tk.Frame(card, bg=CARD)
        btn_row.pack(anchor="w", padx=40, pady=(0, 20))

        make_button(btn_row, "Register", self._submit, colour=SUCCESS).pack(
            side="left", padx=(0, 10)
        )
        make_button(
            btn_row, "← Back",
            lambda: self.controller.show_frame("WelcomePage"),
            colour=TEXT_MUTED,
            width=10,
        ).pack(side="left")

    def _toggle_term_addr(self):
        """Disable term address field when 'same as home' is checked."""
        if self._same_addr.get():
            self._term_addr.config(state="disabled")
        else:
            self._term_addr.config(state="normal")

    def _submit(self):
        """Validate all fields and write new student + login rows to the DB."""
        # ── Collect values ─────────────────────────────────────────────────
        name = self._name.get().strip()
        pronouns = self._pronouns_var.get()
        dob = self._dob.get().strip()
        home_addr = self._home_addr.get().strip()
        term_addr = (
            None if self._same_addr.get() else self._term_addr.get().strip() or None
        )
        emg_name = self._emg_name.get().strip()
        emg_number = self._emg_number.get().strip()
        course = self._course_var.get()
        username = self._username.get().strip()
        password = self._password.get()
        confirm = self._confirm_pw.get()

        # ── Validate ───────────────────────────────────────────────────────
        errors = []
        if not name:
            errors.append("Full Name is required.")
        if not is_valid_date(dob):
            errors.append("Date of Birth must be in DD/MM/YYYY format.")
        if not home_addr:
            errors.append("Home Address is required.")
        if not emg_name:
            errors.append("Emergency Contact Name is required.")
        if not is_valid_phone(emg_number):
            errors.append("Emergency Contact Number appears invalid.")
        if not is_valid_username(username):
            errors.append(
                "Username must be 3–30 characters "
                "(letters, digits, underscores only)."
            )
        pw_ok, pw_msg = is_strong_password(password)
        if not pw_ok:
            errors.append(pw_msg)
        if password != confirm:
            errors.append("Passwords do not match.")

        if errors:
            messagebox.showerror("Registration Error", "\n".join(errors))
            return

        # ── Database insert ────────────────────────────────────────────────
        from datetime import datetime
        dob_db = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check username is not already taken
            cursor.execute(
                "SELECT login_id FROM login WHERE username = %s", (username,)
            )
            if cursor.fetchone():
                messagebox.showerror(
                    "Registration Error",
                    "That username is already taken. Please choose another.",
                )
                cursor.close()
                conn.close()
                return

            # Insert student record
            cursor.execute(
                """
                INSERT INTO students
                    (name, pronouns, date_of_birth, home_address,
                     term_address, emergency_name, emergency_number, course)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (name, pronouns, dob_db, home_addr,
                 term_addr, emg_name, emg_number, course),
            )
            student_id = cursor.lastrowid

            # Insert login record with hashed password
            cursor.execute(
                """
                INSERT INTO login (username, password_hash, role, student_id)
                VALUES (%s, %s, 'student', %s)
                """,
                (username, hash_password(password), student_id),
            )
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        messagebox.showinfo(
            "Registration Successful",
            f"Welcome, {name}!\nYour account has been created.\n"
            f"You can now log in with username: {username}",
        )
        self._clear_form()
        self.controller.show_frame("StudentLoginPage")

    def _clear_form(self):
        """Reset all form fields to their defaults."""
        for entry in (
            self._name, self._dob, self._home_addr, self._term_addr,
            self._emg_name, self._emg_number, self._username,
            self._password, self._confirm_pw,
        ):
            entry.config(state="normal")
            entry.delete(0, tk.END)
        self._pronouns_var.set(PRONOUNS[0])
        self._course_var.set(COURSES[0])
        self._same_addr.set(False)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: STUDENT DASHBOARD – VIEW  (Requirement 4)
# ─────────────────────────────────────────────────────────────────────────────

class StudentDashboardPage(tk.Frame):
    """
    Display the logged-in student's personal record.
    Refreshed every time the page is raised so edits are immediately visible.
    """

    def __init__(self, parent, controller: App):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        _build_page_header(self, "My Details", PRIMARY)

        # Action bar
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=30, pady=(6, 0))
        make_button(
            bar, "Edit My Details",
            lambda: self.controller.show_frame("StudentUpdatePage"),
            colour=SECONDARY, width=16,
        ).pack(side="left")
        make_button(
            bar, "Log Out", self.controller.logout,
            colour=DANGER, width=10,
        ).pack(side="right")

        # Scrollable card for the detail rows
        scroll = ScrollableFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=30, pady=10)
        self._card = scroll.inner
        self._card.configure(bg=CARD)

    def refresh(self):
        """Re-query the database and repopulate the displayed fields."""
        # Clear previous content
        for widget in self._card.winfo_children():
            widget.destroy()

        sid = self.controller.current_student_id
        if sid is None:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM students WHERE student_id = %s", (sid,))
            row = cursor.fetchone()

            # Also fetch username from login table
            cursor.execute(
                "SELECT username FROM login WHERE student_id = %s", (sid,)
            )
            login_row = cursor.fetchone()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        if row is None:
            make_label(
                self._card, "No record found.", fg=DANGER, bg=CARD
            ).pack(padx=40, pady=20)
            return

        make_label(
            self._card,
            f"Welcome back, {row['name']}!",
            font=F_H2, fg=PRIMARY, bg=CARD,
        ).pack(anchor="w", padx=40, pady=(20, 4))

        add_separator(self._card, pady=4)

        # Build detail rows from a list of (label, value) pairs
        from datetime import date
        dob = row["date_of_birth"]
        dob_str = (
            dob.strftime("%d/%m/%Y") if isinstance(dob, date) else str(dob)
        )
        term_display = row["term_address"] or "Same as home address"

        details = [
            ("Full Name",              row["name"]),
            ("Pronouns",               row["pronouns"]),
            ("Date of Birth",          dob_str),
            ("Home Address",           row["home_address"]),
            ("Term-Time Address",      term_display),
            ("Emergency Contact",      row["emergency_name"]),
            ("Emergency Phone",        row["emergency_number"]),
            ("Course",                 row["course"]),
            ("Username",
             login_row["username"] if login_row else "N/A"),
        ]

        for label, value in details:
            _detail_row(self._card, label, value)

        make_label(
            self._card, " ", bg=CARD
        ).pack()  # bottom padding


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: STUDENT UPDATE  (Requirement 5)
# ─────────────────────────────────────────────────────────────────────────────

class StudentUpdatePage(tk.Frame):
    """
    Pre-populated edit form for the logged-in student's personal record.
    Only changed fields are re-validated; blank password fields mean
    'keep current password'.
    """

    def __init__(self, parent, controller: App):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        _build_page_header(self, "Edit My Details", SECONDARY)

        scroll = ScrollableFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=30, pady=10)
        self._card = scroll.inner
        self._card.configure(bg=CARD)

    def refresh(self):
        """Load current student data into the form fields."""
        for widget in self._card.winfo_children():
            widget.destroy()

        sid = self.controller.current_student_id
        if sid is None:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM students WHERE student_id = %s", (sid,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        if row is None:
            return

        card = self._card

        # ── Pre-populate entries with current values ────────────────────────
        from datetime import date
        dob = row["date_of_birth"]
        dob_str = (
            dob.strftime("%d/%m/%Y") if isinstance(dob, date) else str(dob)
        )

        def labelled_entry(label_text, initial="", show=None):
            make_label(card, label_text, font=F_LABEL, fg=TEXT_MUTED, bg=CARD).pack(
                anchor="w", padx=40, pady=(10, 1)
            )
            e = make_entry(card, show=show)
            e.insert(0, initial)
            e.pack(anchor="w", padx=40)
            return e

        make_label(
            card, "Update Your Details", font=F_H2, fg=SECONDARY, bg=CARD
        ).pack(anchor="w", padx=40, pady=(20, 0))

        self._name = labelled_entry("Full Name *", row["name"])
        self._pronouns_var = tk.StringVar(value=row["pronouns"])
        make_label(card, "Pronouns *", font=F_LABEL, fg=TEXT_MUTED, bg=CARD).pack(
            anchor="w", padx=40, pady=(10, 1)
        )
        make_dropdown(card, self._pronouns_var, PRONOUNS).pack(
            anchor="w", padx=40
        )
        self._dob = labelled_entry("Date of Birth * (DD/MM/YYYY)", dob_str)
        self._home_addr = labelled_entry("Home Address *", row["home_address"])
        self._term_addr = labelled_entry(
            "Term-Time Address (leave blank if same as home)",
            row["term_address"] or "",
        )
        self._emg_name = labelled_entry(
            "Emergency Contact Name *", row["emergency_name"])
        self._emg_number = labelled_entry(
            "Emergency Contact Number *", row["emergency_number"]
        )

        make_label(card, "Course *", font=F_LABEL, fg=TEXT_MUTED, bg=CARD).pack(
            anchor="w", padx=40, pady=(10, 1)
        )
        self._course_var = tk.StringVar(value=row["course"])
        make_dropdown(card, self._course_var, COURSES).pack(
            anchor="w", padx=40)

        add_separator(card, pady=10)
        make_label(
            card,
            "Change Password  (leave blank to keep current password)",
            font=F_H2, fg=SECONDARY, bg=CARD,
        ).pack(anchor="w", padx=40, pady=(0, 0))

        self._new_pw = labelled_entry(
            "New Password (min 8 chars, upper, lower, digit)", show="•"
        )
        self._confirm_pw = labelled_entry("Confirm New Password", show="•")

        add_separator(card, pady=10)
        btn_row = tk.Frame(card, bg=CARD)
        btn_row.pack(anchor="w", padx=40, pady=(0, 20))

        make_button(btn_row, "Save Changes", self._submit, colour=SECONDARY).pack(
            side="left", padx=(0, 10)
        )
        make_button(
            btn_row, "← Cancel",
            lambda: self.controller.show_frame("StudentDashboardPage"),
            colour=TEXT_MUTED, width=10,
        ).pack(side="left")

    def _submit(self):
        """Validate updated fields and commit changes to the database."""
        name = self._name.get().strip()
        pronouns = self._pronouns_var.get()
        dob = self._dob.get().strip()
        home_addr = self._home_addr.get().strip()
        term_addr = self._term_addr.get().strip() or None
        emg_name = self._emg_name.get().strip()
        emg_number = self._emg_number.get().strip()
        course = self._course_var.get()
        new_pw = self._new_pw.get()
        confirm_pw = self._confirm_pw.get()

        errors = []
        if not name:
            errors.append("Full Name is required.")
        if not is_valid_date(dob):
            errors.append("Date of Birth must be in DD/MM/YYYY format.")
        if not home_addr:
            errors.append("Home Address is required.")
        if not emg_name:
            errors.append("Emergency Contact Name is required.")
        if not is_valid_phone(emg_number):
            errors.append("Emergency Contact Number appears invalid.")

        # Only validate password if the user typed something
        if new_pw:
            pw_ok, pw_msg = is_strong_password(new_pw)
            if not pw_ok:
                errors.append(pw_msg)
            if new_pw != confirm_pw:
                errors.append("Passwords do not match.")

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        confirmed = messagebox.askyesno(
            "Confirm Update", "Save these changes to your record?"
        )
        if not confirmed:
            return

        from datetime import datetime
        dob_db = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
        sid = self.controller.current_student_id

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE students SET
                    name = %s, pronouns = %s, date_of_birth = %s,
                    home_address = %s, term_address = %s,
                    emergency_name = %s, emergency_number = %s, course = %s
                WHERE student_id = %s
                """,
                (name, pronouns, dob_db, home_addr, term_addr,
                 emg_name, emg_number, course, sid),
            )

            if new_pw:
                cursor.execute(
                    "UPDATE login SET password_hash = %s WHERE student_id = %s",
                    (hash_password(new_pw), sid),
                )

            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        messagebox.showinfo(
            "Saved", "Your details have been updated successfully.")
        self.controller.show_frame("StudentDashboardPage")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LECTURER DASHBOARD  (Requirement 6)
# ─────────────────────────────────────────────────────────────────────────────

class LecturerDashboardPage(tk.Frame):
    """
    Show a Treeview table of all students and their details.
    Only reachable after a successful lecturer login.
    """

    def __init__(self, parent, controller: App):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        _build_page_header(self, "All Student Records", TEXT_MUTED)

        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=20, pady=(6, 0))

        make_button(bar, "Refresh", self.refresh, colour=SECONDARY, width=10).pack(
            side="left"
        )
        make_button(bar, "Log Out", self.controller.logout, colour=DANGER, width=10).pack(
            side="right"
        )

        # ── Search bar ─────────────────────────────────────────────────────
        search_frame = tk.Frame(self, bg=BG)
        search_frame.pack(fill="x", padx=20, pady=(8, 0))
        make_label(
            search_frame, "Search: ", font=F_LABEL, fg=TEXT_MUTED, bg=BG
        ).pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())
        search_entry = make_entry(search_frame, width=28)
        search_entry.config(textvariable=self._search_var)
        search_entry.pack(side="left", padx=(0, 6))
        make_label(
            search_frame, "(name or course)", font=F_SMALL, fg=TEXT_MUTED, bg=BG
        ).pack(side="left")

        # ── Treeview ───────────────────────────────────────────────────────
        tree_frame = tk.Frame(self, bg=BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "name", "pronouns", "dob", "home_address", "term_address",
            "emg_name", "emg_number", "course",
        )
        col_headers = (
            "Name", "Pronouns", "DOB", "Home Address", "Term Address",
            "Emergency Contact", "Emergency No.", "Course",
        )

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT_DARK,
            rowheight=26,
            fieldbackground=WHITE,
            font=F_SMALL,
        )
        style.configure(
            "Treeview.Heading",
            background=PRIMARY,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", ACCENT)],
                  foreground=[("selected", PRIMARY)])

        self._tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", selectmode="browse"
        )
        for col, header in zip(columns, col_headers):
            self._tree.heading(col, text=header)
            self._tree.column(col, width=110, anchor="w", stretch=True)

        v_scroll = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self._tree.yview
        )
        h_scroll = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self._tree.xview
        )
        self._tree.configure(
            yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set
        )

        self._tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._status_label = make_label(
            self, "", font=F_SMALL, fg=TEXT_MUTED, bg=BG)
        self._status_label.pack(anchor="w", padx=20, pady=(0, 6))

    def refresh(self):
        """Re-query all students and populate the Treeview."""
        # Clear existing rows
        for item in self._tree.get_children():
            self._tree.delete(item)

        search = self._search_var.get().strip().lower(
        ) if hasattr(self, "_search_var") else ""

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM students ORDER BY name"
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        if not rows:
            self._status_label.config(
                text="No student records found in the database.", fg=DANGER
            )
            return

        from datetime import date
        count = 0
        for row in rows:
            # Apply search filter
            if search and search not in row["name"].lower() \
                    and search not in row["course"].lower():
                continue

            dob = row["date_of_birth"]
            dob_str = (
                dob.strftime("%d/%m/%Y") if isinstance(dob, date) else str(dob)
            )
            term = row["term_address"] or "Same as home"
            values = (
                row["name"],
                row["pronouns"],
                dob_str,
                row["home_address"],
                term,
                row["emergency_name"],
                row["emergency_number"],
                row["course"],
            )
            # Alternate row colours for readability
            tag = "even" if count % 2 == 0 else "odd"
            self._tree.insert("", "end", values=values, tags=(tag,))
            count += 1

        self._tree.tag_configure("even", background=WHITE)
        self._tree.tag_configure("odd", background=ACCENT)

        self._status_label.config(
            text=f"Showing {count} of {len(rows)} student record(s).",
            fg=SUCCESS,
        )


# ─────────────────────────────────────────────────────────────────────────────
# SHARED UI HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def _build_page_header(frame: tk.Frame, title: str, colour: str):
    """Add a coloured banner with a title to the top of a page frame."""
    banner = tk.Frame(frame, bg=colour, height=70)
    banner.pack(fill="x")
    banner.pack_propagate(False)
    make_label(banner, title, font=F_H1, fg=WHITE, bg=colour).pack(expand=True)


def _make_card(parent: tk.Frame) -> tk.Frame:
    """Return a white rounded-look card frame packed inside *parent*."""
    card = tk.Frame(parent, bg=CARD, relief="flat", bd=0)
    card.pack(expand=True, padx=80, pady=20, fill="both")
    return card


def _detail_row(parent: tk.Frame, label: str, value: str):
    """Add a two-column label+value row to a detail view card."""
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", padx=40, pady=3)
    make_label(row, f"{label}:", font=F_LABEL, fg=TEXT_MUTED, bg=CARD, width=22).pack(
        side="left"
    )
    make_label(row, value, font=F_BODY, fg=TEXT_DARK,
               bg=CARD).pack(side="left")


def _make_back_link(parent: tk.Frame, text: str, controller: App):
    """Add a clickable 'back' label link to *parent*."""
    lbl = make_label(parent, text, font=F_SMALL,
                     fg=SECONDARY, bg=CARD, cursor="hand2")
    lbl.pack(anchor="w", padx=40, pady=(6, 16))
    lbl.bind(
        "<Button-1>", lambda _: controller.show_frame("WelcomePage")
    )


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
