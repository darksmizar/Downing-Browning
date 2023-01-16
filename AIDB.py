import sqlite3

# Connect to the database
conn = sqlite3.connect('convenience_store.db')

# Create a cursor
cursor = conn.cursor()

# Create the Order table
cursor.execute('''CREATE TABLE ORDER (
                    OrderID INTEGER PRIMARY KEY,
                    OrderDate DATE NOT NULL,
                    Discount REAL NOT NULL,
                    VAT REAL NOT NULL,
                    MemberID INTEGER,
                    Discount REAL NOT NULL,
                    CostOfOrder REAL NOT NULL,
                    OverallOrderCost REAL NOT NULL
                    )''')

# Create the Order-Product table
cursor.execute('''CREATE TABLE OrderProduct (
                    OrderID INTEGER,
                    ProductID INTEGER,
                    Quantity INTEGER NOT NULL,
                    TotalAmount REAL NOT NULL,
                    PRIMARY KEY (OrderID, ProductID),
                    FOREIGN KEY (OrderID) REFERENCES Order(OrderID),
                    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
                    )''')

# Create the Product table
cursor.execute('''CREATE TABLE Product (
                    ProductID INTEGER PRIMARY KEY,
                    ProductName TEXT NOT NULL,
                    Volume REAL NOT NULL,
                    ItemCost REAL NOT NULL,
                    SupplierID INTEGER,
                    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
                    )''')

# Create the Supplier table
cursor.execute('''CREATE TABLE Supplier (
                    SupplierName TEXT NOT NULL,
                    SupplierID INTEGER PRIMARY KEY,
                    SupplierLocation TEXT NOT NULL,
                    SupplierSupport TEXT NOT NULL,
                    SupplierNo INTEGER NOT NULL
                    )''')

# Create the Member table
cursor.execute('''CREATE TABLE Member (
                    MemberID INTEGER PRIMARY KEY,
                    MemberName TEXT NOT NULL,
                    MemberStatus TEXT NOT NULL,
                    MemberAddress TEXT NOT NULL,
                    RenewDate DATE NOT NULL,
                    PastDue REAL NOT NULL,
                    CurrentDue REAL NOT NULL,
                    Sex CHAR(1) NOT NULL,
                    DOB DATE NOT NULL,
                    MedicalStatus TEXT NOT NULL,
                    JoinDate DATE NOT NULL,
                    Age INTEGER NOT NULL
                    )''')

# Commit the changes and close the connection
conn.commit()
conn.close()
