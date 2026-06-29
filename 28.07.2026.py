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

name_var = tk.StringVar()
receipt_var = tk.StringVar()
item_var = tk.StringVar()
qty_var = tk.StringVar()

name_entry = None
receipt_entry = None
qty_entry = None
price_label = None
tree = None

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
    name_var.set("")
    receipt_var.set("")
    item_var.set(list(ITEMS.keys())[0])
    qty_var.set("")

def build_form(parent):
    global name_entry, receipt_entry, qty_entry
    row = 0

    tk.Label(parent, text ="Customer full name", anchor = "w").grid(row = row, column = 0, sticky = "w", pady = 3)
    row +=1
    name_entry = tk.Entry(parent, textvariable = name_var, width = 30)
    name_entry.grid(row = row, column = 0, stickey = "ew", pady = (0,8))
    row +=1

    tk.Label(parent, text = "Receipt Number:", anchor = "w").grid(row = row, column = 0, sticky = "w", pady = 3)
    row += 1
    receipt_entry = tk.Entry(parent, textvariable = receipt_var, width = 30)
    receipt_entry.grid(row = row, column = 0, sticky = "ew", pady = (0,8))
    row += 1

    tk.Label(parent, text = "Item to hire:", anchor = "w").grid(row = row, column = 0, sticky = "w", pady = 3)
    row += 1
    item_var.set(list(ITEMS.keys())[0])
    item_dropdown = ttk.Combobox(parent, textvariable = item_var, values = list(ITEMS.keys()), state = "read only", width = "28")
    item_dropdown.grid(row = row, column = 0, sticky = "ew", pady = (0,8))
    row += 1
    
    tk.Label(parent, text = "quantity (1-500)", anchor = "w").grid(row = row, column = 0, sticky = "w", pady = 3)
    row += 1
    qty_entry = tk.Entry(parent, textvariable = receipt_var, width = 30)
    qty_entry.grid(row = row, column = 0, sticky = "ew", pady = (0,8))
    row += 1

    tk.Label(parent, text = "Add rental", bg = "#4CAF50", fg = "white", font = ("Arial", 10, "bold"), width = 26, 
            command = add_rental).grid(row = row, column = 0, pady = 4)
    row += 1
    tk.Button(parent, text = "Mark as Returned", bg = "#f44336", fg = "white", font = ("Arial", 10, "bold"), width = 26,
            command = delete_rental).grid(row = row, column = 0, pady = 4)
    row += 1
    tk.Button(parent, text = "Clear Form", font = ("Arial", 10), width = 26, 
            command = clear_form).grid(row = row, column = 4)

# build the table

def build_table(parent):
    global tree

    tree = ttk.Treeview(parent, columns = COLUMNS, show = "headings", height = 16)

    widths = [90, 175, 130, 60, 110]
    for col, width in zip(COLUMNS, widths):
        tree.heading(col, text = col)
        tree.column(col, width = width, anchor = "center")

    
    scrollbar = ttk.Scrollbar(parent, orient = "vertical", command = tree.yview)
    tree.configure(yscrollcommand = scrollbar.set)
    tree.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
    scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

    tk.Label(parent, text = "Select a row then click 'Mark as Returned' to remove it.",
             font = ("Arial", 9), fg = "grey").pack(pady = (6,0))


def build_ui():
    tk.Label(root, text = "Callum's Party Rental Corp", font = ("Arial", 18, "bold")).pack(pady =
                                                                                        (12,6))  
    
    container = tk.Frame(root)
    container.pack(fill = tk.BOTH, expand = True, padx = 12, pady = 6)

    left = tk.LabelFrame(container, text = "New Rental", font = ("Arial", 11, "bold"), padx = 10, pady = 10)
    right = tk.LabelFrame(container, text = "Active Rentals", font = ("Arial", 11, "bold"), padx = 10, pady = 10)

    build_form(left)
    build_table(right)

# keep the code running

build_ui()
root.mainloop()