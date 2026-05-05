import tkinter as tk

import login
import registration
import dashboards


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Student Management System")
        self.geometry("400x300")
        self.resizable = False

        self.container = tk.Frame(self, width=400, height=300)
        self.container.pack()
        # self.container.pack(fill="both", expand=False)

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
        try:
            frame.refresh_data()
        except Exception as e:
            print(f"Could not refresh data: {e}")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
