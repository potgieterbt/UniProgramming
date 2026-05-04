import tkinter as tk

# Create the main window
main_window = tk.Tk()
main_window.title("Hello Tkinter")  # Set window title

# Create a StringVar to associate with the label

# Create the label widget with all options
label = tk.Label(main_window,
                 text="Hello Bennett",
                 font=("Calibri", 44)
                 )
label.grid(row=0, column=0)

# Run the main event loop
main_window.mainloop()

# if __name__ == "__main__":
#     print("Hello World")
