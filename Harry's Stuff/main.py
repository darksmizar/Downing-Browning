def Interface(view):
    import tkinter as tk
    from ast import Not
    from pydoc import importfile
    import sqlite3
    import functionsdb
    import tkinter.ttk as ttk
    from tkinter import messagebox
    
    functionsdb.tabler()
    
    class dbsetup(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            self._frame = None
            if view == "Owner/Admin":
                self.replace_frame(User)
                
            else:
                self.replace_frame(Customer)
        #Creates a master frame and asigns users to a frame relevant to their position
                
        def replace_frame(self, frame_class):
            new_frame = frame_class(self)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.grid()
        #Creates a new frame, deletes old one first
        
    class User(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            
            def getvals(mode):
                if mode == True:
                    if identry.get() != "":
                        try:
                            userid = int(identry.get())
                        except ValueError:
                            userid = 0
                    else:
                        userid= str(identry.get())
                    username = str(userentry.get())
                    pword = str(pwordentry.get())
                    if str(deptchoice.get()) == "department":
                        department =""
                    else:
                        department = str(deptchoice.get())
                    loginvals = (userid, username, pword, department)
                    return loginvals
                else:
                    userid = str(identry.get())
                    if userid == "auto":
                        userid = None
                    else:
                        if int(userid)<0:
                            tk.messagebox.showwarning("User ID", "User ID needs to be positive")
                            return
                        if len(str(userid))>4:
                            tk.messagebox.showwarning("User ID", "User ID can't be more than 4 characters")
                            return
                    
                    username = str(userentry.get())
                    pword = str(pwordentry.get())
                    if str(deptchoice.get()) == "department":
                        department =""
                    else:
                        department = str(deptchoice.get())
                    loginvals = (userid, username, pword, department)
                    return loginvals


            def handle_click(event):
                if usertree.identify_region(event.x, event.y) == "separator":
                    return "break"
                #removes ability to stretch columns in treeview

            def getentry(event):
                userentry["state"] = "normal" #enables entry to add text to it
                curitem = usertree.focus()
                itemdict = usertree.item(curitem)
                entrylist = [userentry, pwordentry]
                curid = str(itemdict.get("text"))
                userentry.delete(0, tk.END)
                userentry.insert(0, curid)
                i = 0
                for item in itemdict.get("values"):
                    if i == 2:
                        deptchoice.set(item)
                    else:
                        entrylist[i].delete(0, tk.END)
                        entrylist[i].insert(0, item)
                    i += 1
                #puts selected row into entries
                userentry["state"] = "disabled"
                #disables primary/foreign key entry to prevent editing

            def addrow():
                addvals = getvals(False)
                if not addvals==None:
                    try:
                        newrow = """INSERT INTO users (UserID, username, password, department) VALUES (?,?,?,?)"""
                        functionsdb.add(newrow, addvals)
                        functionsdb.view(usertree, userselect)
                        #uses add function to insert record and resets view
                    except sqlite3.IntegrityError:
                        tk.messagebox.showerror("User ID", "Error: User ID, username or password is not unique or referential integrity of database breached")
                        #checks for primary/foreign key errors


            def search():
                loginsearchvals = getvals(True)
                #fetches entry values
                reportfile = open("report.txt", "w")
                #clears reportfile by opening it in write mode
                headings = ["User ID", "Username", "Password", "Department"]
                for text in headings:
                    reportfile.write("%-30s" % (text))
                reportfile.write("\n"+4*("------------------------------")+"\n")
                #formats reportfile with headings
                reportfile.close()
                functionsdb.search(usertree, loginsearchvals, userselect)
                #executes search with current values in the entries

            def delrow(messagename1, messagetext1, messagename2, messagetext2, editdel):
                curitem = usertree.focus()
                itemdict = usertree.item(curitem)
                try:
                    if itemdict.get("text") == "":
                        errormessage(messagename1, messagetext1)
                        #checks if user has selected a row
                    else:
                        accountid = str(itemdict.get("text"))
                        result = messagebox.askokcancel(messagename2, messagetext2)
                        #makes sure user wants to edit/delete row
                        if result == True:
                            loginiddel = """DELETE FROM users WHERE UserID = ?"""
                            if editdel == True:
                                functionsdb.delete(loginiddel, accountid, edit = True)
                            else:
                                functionsdb.delete(loginiddel, accountid, edit = False)
                            functionsdb.view(usertree, userselect)
                            #uses delete function to remove row and resets view
                        return result
                except sqlite3.IntegrityError:
                    tk.messagebox.showerror("User ID",
                                            "Error: Referential integrity of database breached")
                    return False
                    #checks for primary/foreign key errors

            def edit():
                curitem = usertree.focus()
                itemdict = usertree.item(curitem)
                if itemdict.get("text") == "":
                    errormessage("Edit Row", "Please select a row before editing")
                else:
                    searchbutton["state"] = "disabled"
                    addbutton["state"] = "disabled"
                    delbutton["state"] = "disabled"
                    editbutton["state"] = "disabled"
                    refreshbutton["state"] = "disabled"
                    savebutton["state"] = "normal"
                    exitbutton["state"] = "normal"
                    userbutton["state"] = "disabled"
                    customerbutton["state"] = "disabled"
                    roomsbutton["state"] = "disabled"
                    bookingsbutton["state"] = "disabled"
                    employeesbutton["state"] = "disabled"
                    paybutton["state"] = "disabled"
                    #disables and enables buttons as necessary for editing
                    event = None
                    getentry(event)
                    usertree.bind("<<TreeviewSelect>>", getentry)
                    #getentry function bound to selecting a cell in the treeview

            def save():
                if getvals(False) != None:
                    #makes sure inputs are valid
                    result = delrow("Edit Error", "Please select a row before editing", "Edit Row", "Are you sure you want to edit the selected row?", editdel = True)
                    if result == True:
                        addrow()

                    
            def refresh():
                identry["state"] = "normal"
                searchbutton["state"] = "normal"
                addbutton["state"] = "normal"
                delbutton["state"] = "normal"
                editbutton["state"] = "normal"
                refreshbutton["state"] = "normal"
                savebutton["state"] = "disabled"
                exitbutton["state"] = "disabled"
                userbutton["state"] = "disabled"
                customerbutton["state"] = "normal"
                roomsbutton["state"] = "normal"
                bookingsbutton["state"] = "normal"
                employeesbutton["state"] = "normal"
                paybutton["state"] = "normal"
                entrylist = [identry, userentry, pwordentry]
                for entry in entrylist:
                    entry.delete(0, tk.END)
                deptchoice.set("Department")
                functionsdb.view(usertree, userselect)
                
            def unbind():
                usertree.unbind("<<TreeviewSelect>>")
                
            def errormessage(title, text):
                messagebox.showerror(title, text)
        
            userselect = """SELECT * FROM users"""
            
            searchbutton = tk.Button(self, text="Search", width=14, height=1, command=search)
            searchbutton.grid(row=6, column=1011, columnspan=2)
            
            addbutton = tk.Button(self, text="Add", width=7, height=1, command=addrow)
            addbutton.grid(row=7, column=1011)
            
            delbutton = tk.Button(self, text="Delete", width=7, height=1,
                                  command=lambda: delrow("Delete Row", "Please select a row to delete.",
                                                         "Delete Row", "Are you sure?", editdel = False))
            delbutton.grid(row=7, column=1012)
            
            editbutton = tk.Button(self, text="Edit", width=7, height=1, command=edit)
            editbutton.grid(row=11, column=1011)

            refreshbutton = tk.Button(self, text="Refresh", width=14, height=1, command=refresh)
            refreshbutton.grid(row=8, column=1011, columnspan=2)

            savebutton = tk.Button(self, text="Save", width=7, height=1, command=save)
            savebutton.grid(row=11, column=1012, padx=(20, 0))

            exitbutton = tk.Button(self, text="Exit", width=7, height=1, command=lambda: [refresh(), unbind()])
            exitbutton.grid(row=11, column=1013, padx=(20, 0))
            
            userbutton = tk.Button(self, text="Users", width=10, height=1, command=lambda: master.replace_frame(User))
            userbutton.grid(row=1, column=4)
            
            customerbutton = tk.Button(self, text="Customers", width=10, height=1, command=lambda: master.replace_frame(Customer))
            customerbutton.grid(row=1, column=5)
            
            roomsbutton = tk.Button(self, text="Rooms", width=10, height=1, command=lambda: master.replace_frame(Room))
            roomsbutton.grid(row=1, column=6)
            
            bookingsbutton = tk.Button(self, text="Bookings", width=10, height=1)
            bookingsbutton.grid(row=1, column=7)
            
            employeesbutton = tk.Button(self, text="Employees", width=10, height=1)
            employeesbutton.grid(row=1, column=8)
            
            paybutton = tk.Button(self, text="Payslips", width=10, height=1)
            paybutton.grid(row=1, column=9)
            
            self.emptylabel = tk.Label(self)
            self.emptylabel.grid(row=1, columnspan = 20)
            
            identry = tk.Entry(self)
            identry.grid(row=2, column=1011, columnspan=2)
            
            userentry = tk.Entry(self)
            userentry.grid(row=3, column=1011, columnspan=2)
            
            pwordentry = tk.Entry(self)
            pwordentry.grid(row=4, column=1011, columnspan=2)
            
            idlabel = tk.Label(self, text = "User ID")
            idlabel.grid(row=2, column=1010)
            
            userlabel = tk.Label(self, text = "Username")
            userlabel.grid(row=3, column=1010)
            
            pwordlabel = tk.Label(self, text = "Password")
            pwordlabel.grid(row=4, column=1010)
            
            deptchoice = tk.StringVar(self)
            deptchoice.set("Department")
            self.statuschoice = tk.OptionMenu(self, deptchoice, "Floor", "Receptionist", "Manager", "Owner/Admin")
            self.statuschoice.grid(row=5, column=1011, columnspan=2)
        
            usertree = ttk.Treeview(self, height= 15, columns=("username", "password", "department"))
            usertree.heading('#0', text="UserID", anchor=tk.CENTER)
            usertree.heading('#1', text="username", anchor=tk.CENTER)
            usertree.heading('#2', text="password", anchor=tk.CENTER)
            usertree.heading('#3', text="department", anchor=tk.CENTER)
            
            functionsdb.view(usertree, userselect)
            
            usertree.column('#0', width=120)
            usertree.column('#1', width=150)
            usertree.column('#2', width=150)
            usertree.column('#3', width=150)
            
            usertree.bind('<Button-1>', handle_click)
            usertree.bind('<Motion>', handle_click)
            
            usertree.grid(row=2, column=1, columnspan=1000, rowspan=10)
            
            refresh()
            
            
    class Customer(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master)

            def handle_click(event):
                if usertree.identify_region(event.x, event.y) == "separator":
                    return "break"
                #removes ability to stretch columns in treeview
            
            def getvals():
                if custidentry.get() != "":
                    try:
                        custid = int(custidentry.get())
                    except ValueError:
                        custid = 0
                else:
                    custid= str(custidentry.get())
                firstname = str(firstnameentry.get())
                surname = str(surnameentry.get())
                loginvals = (custid, firstname, surname)
                return loginvals
                    

            def search():
                loginsearchvals = getvals()
                #fetches entry values
                reportfile = open("report.txt", "w")
                #clears reportfile by opening it in write mode
                headings = ["Customer ID", "First Name", "Surname"]
                for text in headings:
                    reportfile.write("%-30s" % (text))
                reportfile.write("\n"+4*("------------------------------")+"\n")
                #formats reportfile with headings
                reportfile.close()
                functionsdb.search(usertree, loginsearchvals, userselect)
                #executes search with current values in the entries

            def delrow(messagename1, messagetext1, messagename2, messagetext2, editdel):
                curitem = usertree.focus()
                itemdict = usertree.item(curitem)
                try:
                    if itemdict.get("text") == "":
                        errormessage(messagename1, messagetext1)
                        #checks if user has selected a row
                    else:
                        custid = str(itemdict.get("text"))
                        result = messagebox.askokcancel(messagename2, messagetext2)
                        #makes sure user wants to edit/delete row
                        if result == True:
                            loginiddel = """DELETE FROM users WHERE CustID = ?"""
                            if editdel == True:
                                functionsdb.delete(loginiddel, custid, edit = True)
                            else:
                                functionsdb.delete(loginiddel, custid, edit = False)
                            functionsdb.view(usertree, userselect)
                            #uses delete function to remove row and resets view
                        return result
                except sqlite3.IntegrityError:
                    tk.messagebox.showerror("Customer ID",
                                            "Error: Referential integrity of database breached")
                    return False
                    #checks for primary/foreign key errors

                    
            def refresh():
                searchbutton["state"] = "normal"
                refreshbutton["state"] = "normal"
                customerbutton["state"] = "disabled"
                if view == "Owner/Admin":
                    userbutton["state"] = "normal"
                    employeesbutton["state"] = "normal"
                    roomsbutton["state"] = "normal"
                    bookingsbutton["state"] = "normal"
                    paybutton["state"] = "normal"
                if view == "Receptionist":
                    userbutton["state"] = "disabled"
                    employeesbutton["state"] = "disabled"
                    roomsbutton["state"] = "normal"
                    bookingsbutton["state"] = "normal"
                    paybutton["state"] = "disabled"
                if view == "Manager":
                    userbutton["state"] = "disabled"
                    employeesbutton["state"] = "normal"
                    roomsbutton["state"] = "normal"
                    bookingsbutton["state"] = "normal"
                    paybutton["state"] = "normal"
                if view == "Floor":
                    userbutton["state"] = "disabled"
                    employeesbutton["state"] = "normal"
                    roomsbutton["state"] = "normal"
                    bookingsbutton["state"] = "disabled"
                    paybutton["state"] = "disabled"
                    
                    
                
                entrylist = [custidentry, firstnameentry, surnameentry]
                for entry in entrylist:
                    entry.delete(0, tk.END)
                    
                functionsdb.view(usertree, userselect)
                
            def unbind():
                usertree.unbind("<<TreeviewSelect>>")
                
            def errormessage(title, text):
                messagebox.showerror(title, text)
        
            userselect = """SELECT * FROM customers"""
            #A select statement that will be used later to select the whole customers tab
            
            searchbutton = tk.Button(self, text="Search", width=14, height=1, command=search)
            searchbutton.grid(row=6, column=1011, columnspan=2)

            refreshbutton = tk.Button(self, text="Refresh", width=14, height=1, command=refresh)
            refreshbutton.grid(row=8, column=1011, columnspan=2)
            
            userbutton = tk.Button(self, text="Users", width=10, height=1, command=lambda: master.replace_frame(User))
            userbutton.grid(row=1, column=4)
            
            customerbutton = tk.Button(self, text="Customers", width=10, height=1,)
            customerbutton.grid(row=1, column=5)
            
            roomsbutton = tk.Button(self, text="Rooms", width=10, height=1, command=lambda: master.replace_frame(Room))
            roomsbutton.grid(row=1, column=6)
            
            bookingsbutton = tk.Button(self, text="Bookings", width=10, height=1)
            bookingsbutton.grid(row=1, column=7)
            
            employeesbutton = tk.Button(self, text="Employees", width=10, height=1)
            employeesbutton.grid(row=1, column=8)
            
            paybutton = tk.Button(self, text="Payslips", width=10, height=1)
            paybutton.grid(row=1, column=9)
            
            self.emptylabel = tk.Label(self)
            self.emptylabel.grid(row=1, columnspan = 20)
            
            custidentry = tk.Entry(self)
            custidentry.grid(row=2, column=1011, columnspan=2)
            
            firstnameentry = tk.Entry(self)
            firstnameentry.grid(row=3, column=1011, columnspan=2)
            
            surnameentry = tk.Entry(self)
            surnameentry.grid(row=4, column =1011, columnspan=2)
            
            idlabel = tk.Label(self, text = "Customer ID")
            idlabel.grid(row=2, column=1010)
            
            firstnamelabel = tk.Label(self, text = "Forename")
            firstnamelabel.grid(row=3, column=1010)
            
            surnamelabel = tk.Label(self, text= "Surname")
            surnamelabel.grid(row=4, column=1010)

            
            usertree = ttk.Treeview(self, height= 15, columns=("FirstName", "Surname", "DOB", "PhoneNumber", "Postcode"))
            usertree.heading('#0', text="Customer ID", anchor=tk.CENTER)
            usertree.heading('#1', text="First Name", anchor=tk.CENTER)
            usertree.heading('#2', text="Surname", anchor=tk.CENTER)
            usertree.heading('#3', text="DOB", anchor=tk.CENTER)
            usertree.heading('#4', text="Phone No.", anchor=tk.CENTER)
            usertree.heading('#5', text="Postcode", anchor=tk.CENTER)
            
            functionsdb.view(usertree, userselect)
            
            usertree.column('#0', width=120)
            usertree.column('#1', width=120)
            usertree.column('#2', width=150)
            usertree.column('#3', width=150)
            usertree.column('#4', width=110)
            usertree.column('#5', width=130)
            
            usertree.bind('<Button-1>', handle_click)
            usertree.bind('<Motion>', handle_click)
            
            usertree.grid(row=2, column=1, columnspan=1000, rowspan=10)
            
            refresh()
            
                      
    class Room(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            
            def handle_click(event):
                if usertree.identify_region(event.x, event.y) == "separator":
                    return "break"
                #removes ability to stretch columns in treeview
            
            
            def getvals(mode):
                if mode == True:
                    if roomidentry.get() != "":
                        try:
                            roomid = int(roomidentry.get())
                        except ValueError:
                            roomid = 0
                    else:
                        roomid= str(roomidentry.get())
                    bookingid = str(bookingidentry.get())
                    if str(typechoice.get()) == "RoomType":
                        roomtype =""
                    else:
                        roomtype = str(typechoice.get())
                    if str(cleanchoice.get()) == "Cleaned":
                        cleaned =""
                    else:
                        cleaned = str(cleanchoice.get())
                    roomnum = str(roomnumentry.get())
                    loginvals = (roomid, bookingid, roomtype, cleaned, roomnum)
                    return loginvals
                else:
                    roomid = str(roomidentry.get())
                    if roomid == "auto":
                        roomid = None
                    else:
                        if int(roomid)<0:
                            tk.messagebox.showwarning("User ID", "User ID needs to be positive")
                            return
                        if len(str(roomid))>4:
                            tk.messagebox.showwarning("User ID", "User ID can't be more than 4 characters")
                            return
                    
                    bookingid = str(bookingidentry.get())
                    if str(typechoice.get()) == "RoomType":
                        roomtype =""
                    else:
                        roomtype = str(typechoice.get())
                    if str(cleanchoice.get()) == "Cleaned":
                        cleaned =""
                    else:
                        cleaned = str(cleanchoice.get())
                    roomnum = str(roomnumentry.get())
                    loginvals = (roomid, bookingid, roomtype, roomnum, cleaned)
                    return loginvals
            
            
            
            
            def search():
                g
    
            def getentry(event):
                roomidentry["state"] = "normal" #enables entry to add text to it
                curitem = usertree.focus()
                itemdict = usertree.item(curitem)
                entrylist = [bookingidentry,]
                curid = str(itemdict.get("text"))
                userentry.delete(0, tk.END)
                userentry.insert(0, curid)
                i = 0
                for item in itemdict.get("values"):
                    if i == 2:
                        deptchoice.set(item)
                    else:
                        entrylist[i].delete(0, tk.END)
                        entrylist[i].insert(0, item)
                    i += 1
                #puts selected row into entries
                userentry["state"] = "disabled"
                #disables primary/foreign key entry to prevent editing

            def addrow():
                addvals = getvals(False)
                if not addvals==None:
                    try:
                        newrow = """INSERT INTO rooms (RoomID, BookingID, RoomType, RoomNum, Cleaned) VALUES (?,?,?,?,?)"""
                        functionsdb.add(newrow, addvals)
                        functionsdb.view(usertree, userselect)
                        #uses add function to insert record and resets view
                    except sqlite3.IntegrityError:
                        tk.messagebox.showerror("Room ID", "Error: Room ID, BookingID or RoomNum is not unique or referential integrity of database breached")
                        #checks for primary/foreign key errors


            def search():
                loginsearchvals = getvals(True)
                #fetches entry values
                reportfile = open("report.txt", "w")
                #clears reportfile by opening it in write mode
                headings = ["Room ID", "Booking ID", "Room Type", "Room Num", "Cleaned?"]
                for text in headings:
                    reportfile.write("%-30s" % (text))
                reportfile.write("\n"+4*("------------------------------")+"\n")
                #formats reportfile with headings
                reportfile.close()
                functionsdb.search(usertree, loginsearchvals, userselect)
                #executes search with current values in the entries

            def delrow(messagename1, messagetext1, messagename2, messagetext2, editdel):
                curitem = usertree.focus()
                itemdict = usertree.item(curitem)
                try:
                    if itemdict.get("text") == "":
                        errormessage(messagename1, messagetext1)
                        #checks if user has selected a row
                    else:
                        accountid = str(itemdict.get("text"))
                        result = messagebox.askokcancel(messagename2, messagetext2)
                        #makes sure user wants to edit/delete row
                        if result == True:
                            loginiddel = """DELETE FROM rooms WHERE RoomID = ?"""
                            if editdel == True:
                                functionsdb.delete(loginiddel, accountid, edit = True)
                            else:
                                functionsdb.delete(loginiddel, accountid, edit = False)
                            functionsdb.view(usertree, userselect)
                            #uses delete function to remove row and resets view
                        return result
                except sqlite3.IntegrityError:
                    tk.messagebox.showerror("Room ID",
                                            "Error: Referential integrity of database breached")
                    return False
                    #checks for primary/foreign key errors

            def edit():
                curitem = usertree.focus()
                itemdict = usertree.item(curitem)
                if itemdict.get("text") == "":
                    errormessage("Edit Row", "Please select a row before editing")
                else:
                    searchbutton["state"] = "disabled"
                    addbutton["state"] = "disabled"
                    delbutton["state"] = "disabled"
                    editbutton["state"] = "disabled"
                    refreshbutton["state"] = "disabled"
                    savebutton["state"] = "normal"
                    exitbutton["state"] = "normal"
                    userbutton["state"] = "disabled"
                    customerbutton["state"] = "disabled"
                    roomsbutton["state"] = "disabled"
                    bookingsbutton["state"] = "disabled"
                    employeesbutton["state"] = "disabled"
                    paybutton["state"] = "disabled"
                    #disables and enables buttons as necessary for editing
                    event = None
                    getentry(event)
                    usertree.bind("<<TreeviewSelect>>", getentry)
                    #getentry function bound to selecting a cell in the treeview

            def save():
                if getvals(False) != None:
                    #makes sure inputs are valid
                    result = delrow("Edit Error", "Please select a row before editing", "Edit Row", "Are you sure you want to edit the selected row?", editdel = True)
                    if result == True:
                        addrow()

       
            def refresh():
                searchbutton["state"] = "normal"
                refreshbutton["state"] = "normal"
                roomsbutton["state"] = "disabled"
                if view == "Owner/Admin":
                    userbutton["state"] = "normal"
                    employeesbutton["state"] = "normal"
                    customerbutton["state"] = "normal"
                    bookingsbutton["state"] = "normal"
                    paybutton["state"] = "normal"
                if view == "Receptionist":
                    userbutton["state"] = "disabled"
                    employeesbutton["state"] = "disabled"
                    customerbutton["state"] = "normal"
                    bookingsbutton["state"] = "normal"
                    paybutton["state"] = "disabled"
                if view == "Manager":
                    userbutton["state"] = "disabled"
                    employeesbutton["state"] = "normal"
                    customerbutton["state"] = "normal"
                    bookingsbutton["state"] = "normal"
                    paybutton["state"] = "normal"
                if view == "Floor":
                    userbutton["state"] = "disabled"
                    employeesbutton["state"] = "normal"
                    customerbutton["state"] = "disabled"
                    bookingsbutton["state"] = "disabled"
                    paybutton["state"] = "disabled"
                    
            def unbind():
                usertree.unbind("<<TreeviewSelect>>")
                
            def errormessage(title, text):
                messagebox.showerror(title, text)
            
            userselect = """SELECT * FROM rooms"""
            #A select statement that will be used later to select the whole customers tab
            
            searchbutton = tk.Button(self, text="Search", width=14, height=1, command=search)
            searchbutton.grid(row=7, column=1011, columnspan=2)
            
            addbutton = tk.Button(self, text="Add", width=7, height=1, command=addrow)
            addbutton.grid(row=8, column=1011)
            
            delbutton = tk.Button(self, text="Delete", width=7, height=1,
                                  command=lambda: delrow("Delete Row", "Please select a row to delete.",
                                                         "Delete Row", "Are you sure?", editdel = False))
            delbutton.grid(row=8, column=1012)
            
            editbutton = tk.Button(self, text="Edit", width=7, height=1, command=edit)
            editbutton.grid(row=12, column=1011)

            refreshbutton = tk.Button(self, text="Refresh", width=14, height=1, command=refresh)
            refreshbutton.grid(row=9, column=1011, columnspan=2)

            savebutton = tk.Button(self, text="Save", width=7, height=1, command=save)
            savebutton.grid(row=12, column=1012, padx=(20, 0))

            exitbutton = tk.Button(self, text="Exit", width=7, height=1, command=lambda: [refresh(), unbind()])
            exitbutton.grid(row=12, column=1013, padx=(20, 0))
            
            userbutton = tk.Button(self, text="Users", width=10, height=1, command=lambda: master.replace_frame(User))
            userbutton.grid(row=1, column=4)
            
            customerbutton = tk.Button(self, text="Customers", width=10, height=1, command=lambda: master.replace_frame(Customer))
            customerbutton.grid(row=1, column=5)
            
            roomsbutton = tk.Button(self, text="Rooms", width=10, height=1)
            roomsbutton.grid(row=1, column=6)
            
            bookingsbutton = tk.Button(self, text="Bookings", width=10, height=1)
            bookingsbutton.grid(row=1, column=7)
            
            employeesbutton = tk.Button(self, text="Employees", width=10, height=1)
            employeesbutton.grid(row=1, column=8)
            
            paybutton = tk.Button(self, text="Payslips", width=10, height=1)
            paybutton.grid(row=1, column=9)
            
            self.emptylabel = tk.Label(self)
            self.emptylabel.grid(row=1, columnspan = 20)
            
            roomidentry = tk.Entry(self)
            roomidentry.grid(row=2, column=1011, columnspan=2)
            
            bookingidentry = tk.Entry(self)
            bookingidentry.grid(row=3, column=1011, columnspan=2)
            
            typechoice = tk.StringVar(self)
            typechoice.set("RoomType")
            self.statuschoice = tk.OptionMenu(self, typechoice, "Single", "Double", "Quad", "Suite")
            self.statuschoice.grid(row=4, column=1011, columnspan=2)
            
            roomnumentry = tk.Entry(self)
            roomnumentry.grid(row=5, column =1011, columnspan=2)
            
            cleanchoice = tk.StringVar(self)
            cleanchoice.set("Cleaned")
            self.statuschoice = tk.OptionMenu(self, cleanchoice, "TRUE", "FALSE")
            self.statuschoice.grid(row=6, column=1011, columnspan=2)
            
            idlabel = tk.Label(self, text = "Room ID")
            idlabel.grid(row=2, column=1010)
            
            bookingidlabel = tk.Label(self, text = "Booking ID")
            bookingidlabel.grid(row=3, column=1010)
            
            roomtypelabel = tk.Label(self, text= "Type")
            roomtypelabel.grid(row=4, column=1010)
            
            roomnumlabel = tk.Label(self, text = "Room Num")
            roomnumlabel.grid(row=5, column=1010)
            
            cleanlabel = tk.Label(self, text="Cleaned?")
            cleanlabel.grid(row=6, column=1010)

            
            usertree = ttk.Treeview(self, height= 15, columns=("Booking ID", "Type", "Room Num", "Cleaned?"))
            usertree.heading('#0', text="Room ID", anchor=tk.CENTER)
            usertree.heading('#1', text="Booking ID", anchor=tk.CENTER)
            usertree.heading('#2', text="Type", anchor=tk.CENTER)
            usertree.heading('#3', text="Room Num", anchor=tk.CENTER)
            usertree.heading('#4', text="Cleaned?", anchor=tk.CENTER)
            
            
            functionsdb.view(usertree, userselect)
            
            usertree.column('#0', width=120)
            usertree.column('#1', width=120)
            usertree.column('#2', width=150)
            usertree.column('#3', width=150)
            usertree.column('#4', width=110)
            
            
            usertree.bind('<Button-1>', handle_click)
            usertree.bind('<Motion>', handle_click)
            
            usertree.grid(row=2, column=1, columnspan=1000, rowspan=10)
            
            refresh()

            
            
    app = dbsetup()
    app.geometry("1000x500+100+100")
    app.title("Downshire Arms")
    app.mainloop()
    
    