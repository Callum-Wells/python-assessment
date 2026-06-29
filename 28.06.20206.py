# All imports that are required for this system to run
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


items_for_rent = {         
    "Bouncy Castle" : 125, 
    "Table" : 10,
    "Chair" : 3,
    "Table wear" : 1,
    "Party lights" : 75
}


columns = ("Receipt #", "Customer Nam", "Item", "Qty",  "Total")

#list to store rentals

rentals = []

root = tk.Tk()
root.title("Callum's Party Rental Corp") # app title 
root.geometry("1050x580") # app size

#input variables

name_var    = tk.StringVar()
receipt_var = tk.StringVar()
item_var    = tk.StringVar()
qty_var     = tk.StringVar()

name_entry    = None
receipt_entry = None
qty_entry     = None
price_label   = None
tree          = None

#add a rental to the list

def add_rental():
    name = name_var.get().strip()
    receipt = receipt_var.get().strip()
    item = item_var.get()
    qty_str = qty_var.get().strip()

    # check fields aren't empty

    if not name:
        messagebox.showerror("Error", "Name is required")
        return
    
    if not receipt:
        messagebox.showerror("Error", "Receipt is required.")
        return
    
    if not receipt.isdigit():
        messagebox.showerror("Error", "Reciept must be a number")
        return
    
    if not qty_str:
        messagebox.showerror("Error", "Quantity is required.")
        return
    
    if not qty_str.isdigit():
        messagebox.showerror("Error", "Quantity must be a number")
        return
    
    # check quantity is in range

    if not (1 <= int(qty_str) <= 500):
        messagebox.showerror("Error", "Quantity must be between 1 and 500.")
        return
    
    qty = int(qty_str)
    total = ITEM.get(item, 0) * qty

    rental = {
        "Reciept": receipt,
        "Name": name,
        "Item": item,
        "qty": qty,
        "Total": total
    }
    rentals.append(rental)

    # save to file

    line = f" Receipt: {receipt} | Customer: {name} | Item: {item} | Qty: {qty} | Total: ${total:.2f}\n"
    with open("rentals.txt", "a") as f:
        f.write(line)

    refresh_table()
    clear_form()
    messagebox.showinfo("Added", f"Rental for {name} added.")


# delete selected rental

def delete_rental():
    selected = tree.selection()
    if not selected():
        messagebox.showwarning("Nothing selected", "Select a rental first.")
        return
    
    confirmed = messagebox.askyesno("Confirm", "Remove this rental")

    index = tree.index(selected[0])
    removed = rentals.pop(index)
    refresh_table()
    messagebox.showinfo("Returned", f"{removed['name']}'s rental has been returned")


# update this table

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    for rental in rentals:
        tree.insert("", tk.END, values = (
            rental["receipt"]
            rental["name"]
            rental["item"]
            rental["qty"]
            f"${rental['total']:.2f}"
        ))

def clear_form():

    
# keep the code running

root.mainloop()
