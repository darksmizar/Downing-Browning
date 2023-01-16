from Support import stock_screen_support
import sqlite3 as sql3
import tkinter.messagebox
from tkinter import *
import tkinter.ttk as ttk
import main_menu

messagebox = tkinter.messagebox

db_name = "Centra.db"
db = sql3.connect(db_name)

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

    def exit(self):
        confirm = messagebox.askyesno("Stock", "Close Window?")
        if confirm:
            stock_screen_support.destroy_window()

    def main_menu(self):
        confirm = messagebox.askyesno("Stock", "Go Back To Main Menu?")
        if confirm:
            stock_screen_support.destroy_window()
            main_menu.start_gui()

    def add_stock(self):
        stockID = self.stock_id_entry.get()
        name = self.name_entry.get()
        price = self.price_entry.get()
        stockGroupID = self.group_id_entry.get()
        stockLevelsID = self.levels_entry.get()
        supplierID = self.supplier_entry.get()

        if stockID == "" or name == "" or price == "" or stockGroupID == "" or stockLevelsID == "" or supplierID == "":
            messagebox.showerror("Stock", "All Fields Must Be Entered!")
        else:
            if not(stockID.isdigit() or stockGroupID.isdigit() or stockLevelsID.isdigit() or supplierID.isdigit()):
                messagebox.showerror("Stock", "Data Types Of stockID, stockGroupID, stockLevelsID And supplierID Must Be Integer!")

            else:
                cursor = db.cursor()
                cursor.execute(f"INSERT INTO Stock(stockID, name, price, stockGroupID, stockLevelsID, supplierID) VALUES ({stockID}, \"{name}\", {price}, {stockGroupID}, {stockLevelsID}, {supplierID})")
                db.commit()
                messagebox.showinfo("Stock", "Stock Added Successfully!")
                return


    def delete_stock(self):
        stockID = self.ENTRY1_3.get()

        if stockID == "":
            messagebox.showerror("Stock", "All Fields Must Be Entered!")
        else:
            if not stockID.isdigit():
                messagebox.showerror("Stock", "stockID Must Be Integer!")
            else:
                cursor = db.cursor()
                cursor.execute(f"DELETE * FROM Stock WHERE stockID = {stockID}")
                stockID = cursor.fetchall()

                if not stockID:
                    messagebox.showerror("Stock", "Stock Not Found!")
                else:
                    messagebox.showinfo("Stock", "Stock Deleted Successfully!")
                return

    
    def find_stock(self):
        stockID = self.stock_id_entry.get()
        
        if stockID == "":
            messagebox.showerror("Stock", "All Fields Must Be Entered!")
        else:
            if not stockID.isdigit():
                messagebox.showerror("Stock", "stockID Must Be Integer!")
            else:
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM Stock WHERE stockID = {stockID}")
                stock = cursor.fetchall()

                if not stock:
                    messagebox.showerror("Stock", "Stock Not Found!")
                else:
                    messagebox.showinfo("Stock", "Stock Found!")
                

    def print_details(self):
        stockID = self.ENTRY1_3.get()

        if stockID == "":
            messagebox.showerror("Stock", "All Fields Must Be Entered!")
        else:
            if not stockID.isdigit():
                messagebox.showerror("Stock", "stockID Must Be Integer!")
            else:
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM Stock WHERE stockID = {stockID}")
                stock = cursor.fetchall()
                stock = str(stock).replace("'", "")
                messagebox.showinfo("Stock", "Entry Printing!")
                self.LBLStockInfo = Label(self.LBLStockInfo, text=stock)
                self.LBLStockInfo.configure("#ffffff")
                self.LBLStockInfo.place(relx=0.03, rely=0.5, relheight=0.3, relwidth=0.95)
                self.LBLStockInfo.pack()

                return


    def __init__(self, top=None):

        top.title("Stock")
        top.configure(background="#ffffff")

        self.stock_label = Label(top, text="Enter Stock Details", font=("Segoe UI", 12))
        self.stock_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10)

        self.stock_id_label = Label(top, text="Stock ID", font=("Segoe UI", 12))
        self.stock_id_label.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10)

        self.stock_id_entry = Entry(top)
        self.stock_id_entry.grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        self.name_label = Label(top, text="Stock Name", font=("Segoe UI", 12))
        self.name_label.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=10)

        self.name_entry = Entry(top)
        self.name_entry.grid(row=2, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        self.price_label = Label(top, text="Stock Price", font=("Segoe UI", 12))
        self.price_label.grid(row=3, column=0, padx=10, pady=10, ipadx=10, ipady=10)

        self.price_entry = Entry(top)
        self.price_entry.grid(row=3, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        self.group_id_label = Label(top, text="Stock Group ID", font=("Segoe UI", 12))
        self.group_id_label.grid(row=4, column=0, padx=10, pady=10, ipadx=10, ipady=10)

        self.group_id_entry = Entry(top)
        self.group_id_entry.grid(row=4, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        self.levels_label = Label(top, text="Stock Levels ID", font=("Segoe UI", 12))
        self.levels_label.grid(row=5, column=0, padx=10, pady=10, ipadx=10, ipady=10)

        self.levels_entry = Entry(top)
        self.levels_entry.grid(row=5, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        self.supplier_label = Label(top, text="Supplier ID", font=("Segoe UI", 12))
        self.supplier_label.grid(row=6, column=0, padx=10, pady=10, ipadx=10, ipady=10)

        self.supplier_entry = Entry(top)
        self.supplier_entry.grid(row=6, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        self.submit_button = Button(top, text="Submit", font=("Segoe UI", 12))
        self.submit_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10)

        self.submit_button.config(command=self.add_stock)

        self.tree = self.create_stock_table()
        self.tree.grid(row=9, column=0, padx=10, pady=10, ipadx=10, ipady=10)


if __name__ == "__main__":
    start_gui()