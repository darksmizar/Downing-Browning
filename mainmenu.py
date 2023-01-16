import tkinter as tk

def run():
    root = tk.Tk()
    root.geometry("400x300")
    root.configure(bg="purple")

    booking_button = tk.Button(root, text="Booking", bg="creme")
    booking_button.pack()

    members_button = tk.Button(root, text="Members", bg="creme")
    members_button.pack()

    exit_button = tk.Button(root, text="Exit", bg="creme", command=root.destroy)
    exit_button.pack()

    root.mainloop()
