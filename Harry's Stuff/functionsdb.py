import sqlite3

def tabler():
    con = sqlite3.connect("downshire.db")#Connects to/creates database
    con.execute("PRAGMA foreign_keys = 1") #enables use of foreign keys
    cur = con.cursor()

    #Making tables if they don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS
        users(
        UserID INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        department TEXT)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS
        customers(
        CustID INTEGER PRIMARY KEY,
        FirstName TEXT,
        Surname TEXT,
        DOB DATE,
        PhoneNumber TEXT,
        Postcode TEXT)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS
        rooms(
        RoomID INTEGER PRIMARY KEY,
        BookingID INTEGER,
        RoomType TEXT,
        RoomNum TEXT,
        Cleaned BOOLEAN,
        FOREIGN KEY (BookingID) REFERENCES bookings(BookingID))
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS
        bookings(
        BookingID INTEGER PRIMARY KEY,
        CustID INTEGER,
        DateMade TEXT,
        StartDate TEXT,
        EndDate TEXT,
        Cost TEXT,
        FOREIGN KEY (CustID) REFERENCES customers(CustID))
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS
        employees(
        EmployID INTEGER PRIMARY KEY,
        Wage TEXT,
        UserID INTEGER,
        PayslipID INTEGER,
        FOREIGN KEY (UserID) REFERENCES users(UserID),
        FOREIGN KEY (PayslipID) REFERENCES payslips(PayslipID))
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS
        payslips(
        PayslipID INTEGER PRIMARY KEY,
        Wage TEXT,
        HoursWorked TEXT,
        TotalPay TEXT)
    """)
 
    
    con.commit()
    con.close()
    

def view(tree, selectstatement): #displays values in treeview
    tree.delete(*tree.get_children()) #deletes current values in tree
    con = sqlite3.connect("downshire.db")
    cur=con.cursor()
    cur.execute(selectstatement)
    rows = cur.fetchall()
    #fetches relevant values from database and inserts them into a 3d array, rows
    for row in rows:
        tree.insert("", "end", text=row[0], values = row[1:])
        #inserts data for each row into treeview
    con.close()
    
    
def add(addvals, vals):
    con = sqlite3.connect("downshire.db")
    con.execute("pragma foreign_keys = ON")
    cur = con.cursor()
    cur.execute(addvals, vals) #SQLite statement adds values to table
    con.commit()
    con.close()

def search(tree, searchvals, selectstatement):
    tree.delete(*tree.get_children()) #clears treeview
    con = sqlite3.connect("downshire.db")
    con.execute("pragma foreign_keys = ON")
    cur=con.cursor()
    cur.execute(selectstatement) #fetches everything from table
    rows = cur.fetchall()
    searchvals = list(searchvals) #turns searchvals tuple into a list
    reportfile = open("report.txt", "a")#opens reportfile for appending
    for row in rows:
        i=0
        rowlist = list(row) #saves the database row as a list so that it
                            #can be compared to the searchvals list
        for item in searchvals:
            try:
                if searchvals[i] == "" or "#p" in searchvals[i] or "#m" in searchvals[i]:
                    rowlist[i] = searchvals[i]
                    #checks if list value is empty - if so, replaces rowlist value
                    #so that empty space can be ignored when searching
                    #also checks for a #p or #m in case the user wants a price or date range
                i+=1
            except TypeError:
                if searchvals[i] == "" :
                    rowlist[i] = ""
                i+=1
        if rowlist == searchvals: #compares searchvals list to database row list
            tree.insert("", "end", text=row[0], values=row[1:])
            #if they are the same, inserts row into treeview so it can be viewed
            for item in row:
                reportfile.write("%-30s" % (item))
                #formats and writes each item from list to reportfile
            reportfile.write("\n")
            
    reportfile.close()
    #closes reportfile
    con.close()

def delete(delid, tblid, edit):
    con = sqlite3.connect("downshire.db")
    if edit == True:
        con.execute("pragma foreign_keys = OFF")
    else:
        con.execute("pragma foreign_keys = ON")
    #turns off foreign keys when editing a row to allow the row to be deleted
    #even if it's referenced in another table
    cur = con.cursor()
    cur.execute(delid, (tblid,)) #removes row by primary key
    con.commit()
    con.close()