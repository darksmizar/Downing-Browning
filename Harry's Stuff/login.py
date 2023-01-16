import tkinter as tk
from ast import Not
from pydoc import importfile
import sqlite3
import main
from functionsdb import tabler
from tkinter import messagebox
from PIL import ImageTk, Image
import keyboard



con = sqlite3.connect("downshire.db")#Connects to/creates database
cur = con.cursor()

class logindb(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame=None
        self.replace_frame(Menu)
        #Creates the master frame and sets the starting frame
    
    def replace_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.grid()
        #Creates a new frame, deletes old one first
        
class Menu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        path = "downshire.jpg"
        pic = Image.open(path)
        pic = pic.resize((300, 300),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(pic) 
        panel = tk.Label(self, image = img)
        panel.image = img
        panel.grid(row=1, column=2)
        
        loginbutton = tk.Button(self, text="Log in", width=7, command=lambda: master.replace_frame(Login))
        loginbutton.grid(row=2, column=2, pady=(5,0))
        
        regbutton = tk.Button(self, text="Register",width=7, command=lambda: master.replace_frame(Register))
        regbutton.grid(row=3, column=2,pady=(5,0))
        
class Login(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        def boom():
            tabler()
            inp_user = str(self.Userentry.get())
            inp_password = str(self.Passwordentry.get())
            con.execute("pragma foreign_keys = ON") #enables use of foreign keys
            cur.execute(f"SELECT username from users WHERE username='{inp_user}' AND password = '{inp_password}';")
            if cur.fetchall():
                query = "SELECT department from users WHERE username=? AND password = ?"
                result = cur.execute(query, (inp_user, inp_password)) 

                # or you could unpack the tuple immediately (note the trailing comma)
                view, = result.fetchone()
                tk.messagebox.showinfo("Login", "Login Successful.")
                con.close()
                self.master.destroy()
                main.Interface(view)
                
                
            else:
                tk.messagebox.showinfo("Login", "Login failed.")
            
        loginbutton = tk.Button(self, text="Log In", width=7, command=boom)
        loginbutton.grid(row=2, column=2, pady=(5,0))
        
        cancelbutton = tk.Button(self, text="Cancel",width=7, command=lambda: master.replace_frame(Menu))
        cancelbutton.grid(row=2, column=1, pady=(5,0))

        #creates buttons for registering and logging in

        self.Userentry = tk.Entry(self)
        self.Userentry.grid(row=0, column=1, columnspan=2, padx=(5,0), pady=(20,0))

        self.Passwordentry = tk.Entry(self, show="•")
        self.Passwordentry.grid(row=1, column=1, columnspan=2, padx=(5,0), pady=(5,0))
    
        userlabel = tk.Label(self, text="Username: ")
        userlabel.grid(row=0,column=0, padx=(50,0), pady=(20,0))

        pwordlabel = tk.Label(self, text="Password: ")
        pwordlabel.grid(row=1,column=0, padx=(50,0), pady=(5,0))
        #creates entries and corresponding labels
        
class Register(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        def reg():
            tabler()
            con.execute("pragma foreign_keys = ON")
            inp_user = str(self.Userentry.get())
            inp_password = str(self.Passwordentry.get())

            key = str(self.Keyentry.get())
            rows = cur.fetchall()
            for row in rows:
                if row[1] == inp_user:
                    print("Username already registered")
                    return 
            if len(inp_user)<6:
                tk.messagebox.showwarning("Registration", "Username too short")
            if len(inp_password)<8:
                tk.messagebox.showwarning("Registration", "Password too short.")
            if dept.get() == "Department":
                tk.messagebox.showwarning("Registration", "Please select a department")
                return
    
            if key == open("KEY.txt").read():
                cur.execute("""
                    INSERT INTO users(
                        username,
                        password,
                        department
                    )
                    VALUES(
                        ?,
                        ?,
                        ?
                    )
                            """, 
                            (inp_user, inp_password, dept.get())
                )
                tk.messagebox.showinfo("Register", "Registration Successful.")

                
            else:
                tk.messagebox.showinfo("Register", "Registration Failed.")
            con.commit()
            self.master.destroy()
            con.close()
            master.replace_frame(Menu)
            
        regbutton = tk.Button(self, text="Register",width=7, command=reg)
        regbutton.grid(row=4, column=2, pady=(5,0))
        
        cancelbutton = tk.Button(self, text="Cancel",width=7, command=lambda: master.replace_frame(Menu))
        cancelbutton.grid(row=4, column=1, pady=(5,0))
        
        self.Userentry = tk.Entry(self)
        self.Userentry.grid(row=0, column=1, columnspan=2, padx=(5,0), pady=(20,0))

        self.Passwordentry = tk.Entry(self, show="•")
        self.Passwordentry.grid(row=1, column=1, columnspan=2, padx=(5,0), pady=(5,0))
        
        dept = tk.StringVar(self)
        dept.set("Department")
        self.deptchoice = tk.OptionMenu(self, dept, "Floor", "Receptionist", "Manager", "Owner/Admin")
        self.deptchoice.grid(row=3, column=1, columnspan=5, pady=(5, 0))
        
        self.Keyentry = tk.Entry(self, show="•")
        self.Keyentry.grid(row=2, column=1, columnspan=2, padx=(5,0) )

        userlabel = tk.Label(self, text="Username: ")
        userlabel.grid(row=0,column=0, padx=(50,0), pady=(20,0))

        pwordlabel = tk.Label(self, text="Password: ")
        pwordlabel.grid(row=1,column=0, padx=(50,0), pady=(5,0))
        
        keylabel = tk.Label(self, text="Key: ")
        keylabel.grid(row=2, column=0, padx=(50,0), pady= (5,0) )
       
        
        

    

        

app =logindb()
app.title("Login Page")
app.mainloop()

    
