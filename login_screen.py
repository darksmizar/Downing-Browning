import tkinter.messagebox
from Support import login_screen_support
import sqlite3 as sql3
import main_menu
from tkinter import *
import tkinter.ttk

messagebox = tkinter.messagebox

global login_attempts
login_attempts = 0

db_name = "Centra.db"
db = sql3.connect(db_name)

def start_gui():
    global root
    root = Tk()
    top = new_Toplevel(root)
    login_screen_support.init(root, top)
    root.mainloop()


w = None
def create_new_topLevel(root, *args, **kwargs):
    global w, w_win
    w = Toplevel(root)
    top = new_Toplevel(root)
    login_screen_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_new_toplevel():
    global w
    w.destroy()
    w = None


class new_Toplevel:
    
    def initiate_login(self):
        username = self.ENTRYusername.get()
        password = self.ENTRYpassword.get()
        accesscode = self.ENTRYaccesscode.get()
        if username == "" or password == "":
            messagebox.showerror("Login", "Required Fields Must Not Be Empty!")
            return
        
        conn = sql3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Access WHERE username = ? AND password = ? AND accesscode = ?', (username, password, accesscode))
        self.user = cursor.fetchone()
        if not self.user:
            messagebox.showerror("Login", "Login Details Invalid!")
            global login_attempts
            login_attempts += 1
            if login_attempts == 3:
                messagebox.showerror("Login", "Too Many Failed Attempts!\nShutting Down!")
                login_screen_support.destroy_window()
        else:
            messagebox.showinfo("Login", "Login Success!")
            f = open("accesscode.txt", "w")
            f.write(accesscode)
            f.close()
            login_screen_support.destroy_window()
            main_menu.start_gui()
        return

    def cancel_login(self):
        f = open("accesscode.txt", "w")
        f.write("")
        f.close()
        confirm = messagebox.askyesno("Login", "Close Window?")
        if confirm:
            login_screen_support.destroy_window()

    def __init__(self, top=None):
        
        top.title("Login Screen")

        self.cancel_button = Button(top, text="Cancel", command=self.cancel_login)
        self.BTNlogin = Button(top, text="Login", command=self.initiate_login)
        self.ENTusername = Entry(top)
        self.ENTpassword = Entry(top, show='•')
        self.ENTaccesscode = Entry(top, show='•')
        self.LBLusername = Label(top, text="Username:")
        self.LBLpassword = Label(top, text="Password:")
        self.LBLaccesscode = Label(top, text="Accesscode:")
        self.LBLlogo = Label(top)

        self.LBLusername.grid(row=0, column=0, sticky="W", pady=10)
        self.ENTusername.grid(row=0, column=1, padx=10)
        self.LBLpassword.grid(row=1, column=0, sticky="W", pady=10)
        self.ENTpassword.grid(row=1, column=1, padx=10)
        self.LBLaccesscode.grid(row=2, column=0, sticky="W", pady=10)
        self.ENTaccesscode.grid(row=2, column=1, padx=10)
        self.LBLlogo.grid(row=0, column=2, rowspan=4)
        self.cancel_button.grid(row=3, column=0, pady=10)
        self.BTNlogin.grid(row=3, column=1)
        self._img1 = PhotoImage(file="Centra_logo.png")
        self.LBLlogo.configure(image=self._img1)

    
if __name__ == "__main__":
    start_gui()