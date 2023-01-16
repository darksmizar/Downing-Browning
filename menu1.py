import tkinter as tk
import subprocess

def run():
    root = tk.Tk()
    root.geometry("800x400")
    root.configure(bg = "#9b59b6")

    def open_file(file_name):
        subprocess.call(["python", file_name + ".py"])

    booking_button = tk.Button(root, text = "Booking", bg = "#ecf0f1", height = 2, width = 20, command = lambda: open_file("Booking"))
    booking_button.place(relx = 0.5, rely = 0.3, anchor = "center")

    members_button = tk.Button(root, text = "Members", bg = "#ecf0f1", height = 2, width = 20, command = lambda: open_file("Members"))
    members_button.place(relx = 0.5, rely = 0.5, anchor = "center")

    exit_button = tk.Button(root, text = "Exit", bg = "#ecf0f1", height = 2, width = 20, command = root.destroy)
    exit_button.place(relx = 0.5, rely = 0.7, anchor = "center")

    root.mainloop()

run()
