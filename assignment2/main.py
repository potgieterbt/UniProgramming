import tkinter as tk

import login
import registration
import dashboards


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Student Management System")
        self.geometry("700x600")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.current_user_id = None
        self.frames = {}

        for F in (login.LoginFrame, registration.RegistrationFrame,
                  dashboards.StudentDashboard, dashboards.LecturerDashboard):
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


if __name__ == "__main__":
    app = Application()
    app.mainloop()
