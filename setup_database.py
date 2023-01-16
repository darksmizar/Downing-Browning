import sqlite3

db_name = ('Centra.db')
db = sqlite3.connect(db_name)
cursor = db.cursor()

#  Create Stock Table
def create_stock_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Stock(
            stockID integer,
            name text,
            price real,
            stockGroupID integer,
            stockLevelsID integer,
            supplierID integer,
            primary key(stockID),
            foreign key(stockGroupID) references StockGroup(stockGroupID),
            foreign key(stockLevelsID) references StockLevel(stockLevelsID),
            foreign key(supplierID) references Supplier(supplierID)
        )

        """
    )


#  Create StockGroup Table
def create_stock_group_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS StockGroup(
            stockGroupID integer,
            description text,
            primary key(stockGroupID)
        )

        """
    )


#  Create StockLevel Table
def create_stock_levels_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS StockLevel(
            stockLevelsID integer,
            quantityPresent integer,
            quantitySold integer,
            primary key(stockLevelsID)
        )

        """
    )


#  Create Supplier Table
def create_supplier_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Supplier(
            supplierID integer,
            companyName text,
            location text,
            primary key(supplierID)
        )
        
        """
    )


#  Create Staff Table
def create_staff_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Staff(
            staffID integer,
            lastName text,
            firstName text,
            phoneNumber VARCHAR,
            age integer,
            jobTitle text,
            paycheckID integer,
            accessID integer,
            primary key(staffID),
            foreign key(paycheckID) references Paycheck(paycheckID),
            foreign key(accessID) references Access(accessID)
        )
        
        """
    )


#  Create Paycheck Table
def create_paycheck_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Paycheck(
            paycheckID integer,
            wage real,
            hoursCompleted real,
            primary key(paycheckID)
        )
        
        """
    )


#  Create Access Table
def create_access_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Access(
            accessID integer,
            username text,
            password text,
            accesscode text

        )

        """
    )


#  Add Data to Database
def query(sql):
    cursor.execute("PRAGMA foreign_key = OFF")
    cursor.execute(sql)
    db.commit()


def insert_stock(records):
    for record in records:
        name = record[0]
        price = record[1]
        stockGroupID = record[2]
        stockLevelsID = record[3]
        supplierID = record[4]
        
        sql = f"INSERT INTO Stock (name, price, stockGroupID, stockLevelsID, supplierID) VALUES (\"{name}\", {price}, {stockGroupID}, {stockLevelsID}, {supplierID})"
        query(sql)


def insert_stock_group(records):
    for record in records:
        description = record[0]
        
        sql = f"INSERT INTO StockGroup (description) VALUES (\"{description}\")"
        query(sql)


def insert_stock_levels(records):
    for record in records:
        quantityPresent = record[0]
        quantitySold = record[1]

        sql = f"INSERT INTO StockLevel (quantityPresent, quantitySold) VALUES ({quantityPresent}, {quantitySold})"
        query(sql)

        
def insert_supplier(records):
    for record in records:
        companyName = record[0]
        location = record[1]

        sql = f"INSERT INTO Supplier (companyName, location) VALUES (\"{companyName}\", \"{location}\")"
        query(sql)


def insert_staff(records):
    for record in records:
        lastName = record[0]
        firstName = record[1]
        phoneNumber = record[2]
        age = record[3]
        jobTitle = record[1]

        sql = f"INSERT INTO Staff (lastName, firstName, phoneNumber, age, jobTitle) VALUES (\"{lastName}\", \"{firstName}\", \"{phoneNumber}\", {age}, \"{jobTitle}\")"
        query(sql)


def insert_paycheck(records):
    for record in records:
        wage = record[0]
        hoursCompleted = record[1]

        sql = f"INSERT INTO Paycheck (wage, hoursCompleted) VALUES ({wage}, {hoursCompleted})"
        query(sql)


def insert_access(records):
    for record in records:
        username = record[0]
        password = record[1]

        sql = f"INSERT INTO Access (username, password) VALUES (\"{username}\", \"{password}\")"
        query(sql)


if __name__ == "__main__":
    db_name = "Centra.db"
    create_stock_table()
    create_stock_group_table()
    create_stock_levels_table()
    create_supplier_table()
    create_staff_table()
    create_paycheck_table
    create_access_table()

    stock = [
        ["Beer", 4.40, 5, 1, 1],
        ["Tomato", 2.00, 3, 2, 2],
        ["Bread", 1.40, 4, 3, 3],
        ["Milk", 1.65, 1, 4, 4],
        ["Fish", 2.50, 2, 5, 5],
        ["Soap", 2.70, 6, 6, 6],
        ["Sausage Roll", 2.10, 4, 7, 7],
        ["Mixed Berries", 2.45, 3, 8, 8],
        ["Bleach", 2.95, 6, 9, 9],
        ["Yogurt", 1.95, 1, 10, 10]
    ]
    insert_stock(stock)

    stock_group = [
        ["Chilled"],
        ["Frozen"],
        ["Fruit and Veg"],
        ["Savory"],
        ["Alcohol"],
        ["Household"]
    ]
    insert_stock_group(stock_group)

    stock_levels = [
        [127, 101],
        [140, 68],
        [138, 94],
        [144, 56],
        [96, 87],
        [123, 93],
        [101, 67],
        [132, 91],
        [105, 64],
        [146, 105]
    ]
    insert_stock_levels(stock_levels)

    supplier = [
        ["Guinness", "Ireland"],
        ["Ocado", "Morocco"],
        ["Brennans", "Ireland"],
        ["Tomlinson's Dairy", "Wales"],
        ["Marrfish", "England"],
        ["Carex", "United States"],
        ["Greggs", "England"],
        ["Brakes", "England"],
        ["Easy", "England"],
        ["Müller", "Germany"]
    ]
    insert_supplier(supplier)

    staff = [
        
    ]