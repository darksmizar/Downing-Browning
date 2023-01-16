from tkinter import *
import sqlite3 as sql3
import tkinter.messagebox
import tkinter.ttk as ttk
from Support import stock_screen_support

db_name = 'Centra.db'
db = sql3.connect(db_name)
global cursor
cursor = db.cursor()

def start_gui():
    global root
    root = Tk()
    top = new_Toplevel(root)
    stock_screen_support.init(root, top)
    root.mainloop()


w = None
def create_new_toplevel(root, *args, **kwargs):
    global w, w_win
    w = Toplevel(root)
    top = new_Toplevel(root)
    stock_screen_support(w, top, *args, **kwargs)
    return (w, top)


def destroy_new_toplevel():
    global w
    w.destroy()
    w = None

class new_Toplevel:
    
    def create_stock_table(self):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Stock")
        rows = cursor.fetchall()
        
        tree = ttk.Treeview(root, columns=("StockID", "Name", "Price", "StockGroupID", "StockLevelID", "SupplierID"))
        tree.heading("#0", text="StockID")
        tree.heading("#1", text="Name")
        tree.heading("#2", text="Price")
        tree.heading("#3", text="StockGroupID")
        tree.heading("#4", text="StockLevelID")
        tree.heading("#5", text="SupplierID")

        for i, row in enumerate(rows):
            tree.insert('', 'end', text=i, values=row)

        return tree

    
    def __init__(self, top=None):
        top.title("Stock Table")
        top.configure(background='#ffffff')

        self.table = self.create_stock_table()
        self.table.grid()


if __name__ == '__main__':
    start_gui()