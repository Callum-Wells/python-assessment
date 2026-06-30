# Callum's Pary rental corp
# gui based rental tracking system that i built with tkinter

# importing all files from python that will be neccassary for my code
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# A dictionary outside of the functions. This works for both
# item dropdown options and price calculation in add_rental
# Keeping price in one place means change only needs to happen
# here not duplicated throughout the anywhere else in the program
items_for_rent = {         
    "Bouncy Castle" : 125, 
    "Table" : 10,
    "Chair" : 3,
    "Table wear" : 1,
    "Party lights" : 75
}

# Column headers for the treeveiw table, defined once 
# so build_table and any future code referencing the structure
# can stay consistent even if a column is added later on
columns = ("Receipt #", "Customer Name", "Item", "Qty",  "Total")

# Store of all active rentals. Each entry is a dictionary, not 
# a class instance, because the data is simple and a class would 
# add some unnecessary complexity. All inputs in one session are in this
rentals = []

root = tk.Tk()
root.title("Callum's Party Rental Corp") # app title 
root.geometry("1050x580") # starting size large enought to show everything displayed

# StrinVars bound to entry widgets. Using a stringVar instead of 
# widget.get() directly means the GUI and and the actual value stay 
# synchronised automatically. This alllows clear_form() to reset inputs
# by setting the variable rather than all widgets individually
name_var = tk.StringVar()
receipt_var = tk.StringVar()
item_var = tk.StringVar()
qty_var = tk.StringVar()

# widgets are stated as none here and are assigned inside build_form/build_table
# They are a global so that add_rental, delete_rental and refresh_table
# read from them without each widget needing to be passed as an argument through all functons
name_entry = None
receipt_entry = None
qty_entry = None
price_label = None
tree = None


def add_rental():
    """
    Validates user input, calculates the rental total, and 
    appends a new rental record created to the memory list, and append
    a matching line to rentals.txt
    
    Each error line has a different message rather than one universal
    Wrong input. This is so that its easier for users to find thier mistake
    """
    # reads the current value of each StringVar at the moment the button is
    # clicked, rather than relying on a stored value. This means we are checking
    # exactly what the user sees
    name = name_var.get().strip()
    receipt = receipt_var.get().strip()
    item = item_var.get()
    qty_str = qty_var.get().strip()
    # .strip() removes white space accidentally created by the user
    # Incase they type " Callum " .strip() makes it not break

    # Empty name check. This comes first because a rental with no customer
    # is no rental at all and they would like to see errors from what they enter first to last
    if not name:
        messagebox.showerror("Error", "Name is required")
        return
    
    # checks if receipt is blank
    if not receipt:
        messagebox.showerror("Error", "Receipt is required.")
        return
    
    # isdigit() makes sure that receipt is only numeric. 
    # We need this so that it can match real life where receipts are purely numeric
    if not receipt.isdigit():
        messagebox.showerror("Error", "Receipt must be a number")
        return
    
    # checking quantity has been entered and isdigit()
    # checks if it is number. Checking emptiness first is
    # structered better
    if not qty_str:
        messagebox.showerror("Error", "Quantity is required.")
        return
    
    if not qty_str.isdigit():
        messagebox.showerror("Error", "Quantity must be a number")
        return
    
    # Ensures input is in range of items available to rent
    # makes sure typos like 10 000 or 0 can't get entered 
    if not (1 <= int(qty_str) <= 500):
        messagebox.showerror("Error", "Quantity must be between 1 and 500.")
        return
    
    # Converst qty_str to an int once all checks have been cleared
    # converting earlier would risk a value eroor if a non digit 
    # string slipped through.
    qty = int(qty_str)

    # .get() is a lookup to ensure the item is in items_for_rent
    # This should never hapen as ive used a dropdown
    # Total defualts to 0 insted of making a keyerror and crashing the app
    total = items_for_rent.get(item, 0) * qty

    # build a record dictionary matching the structure every functions expects
    # These keys must stay consistent throughout the whole program or else functions break
    rental = {
        "receipt": receipt,
        "name": name,
        "item": item,
        "qty": qty,
        "total": total
    }
    rentals.append(rental) # this is the point where a rental enters the memory system

    # Writes a record of this file in append mode. It will
    # be used as a persistent storage, but currently only "add" is implemented
    # The file is never read back in on. 
    # delete_rental does not remove the line
    # this means file and memory list are not kept in sync
    line = f" Receipt: {receipt} | Customer: {name} | Item: {item} | Qty: {qty} | Total: ${total:.2f}\n"
    with open("rentals.txt", "a") as f: # "a" = append, so existing file contents are present between runs
        f.write(line)

    # refresh the visible table first so the new row appears
    # then clear the form so user can immediately start entering the new rental.
    refresh_table()
    clear_form()
    messagebox.showinfo("Added", f"Rental for {name} added.")



def delete_rental():
    '''
    This function removes the selected rental from the memory list and 
    refreshes the table. Relies on row's position in the treeview mathing
    its index in the rentals list.
    '''
    # tree.selection() returns a tuple of selected row IDs
    # this means its empty if nothing is selected. which is why this is checked 
    # before anything else
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Nothing selected", "Select a rental first.")
        return
    
    # Confirmation is here because deletion is immediate. so if they
    # accidentally click on it then theres no taking it back.
    confirmed = messagebox.askyesno("Confirm", "Remove this rental")
    if not confirmed:
        return # user backed out, leave everything untouched

    # tee.index() converts the selected row's widget ID into
    # its positional index in the table. This is used to pop the matching
    # entry out of the rentals list at the same position
    index = tree.index(selected[0])

    #.pop(index) both removes the entry from rentals and returns it in one step
    # it is in the confirmation message below without needing to look it up again
    removed = rentals.pop(index)
    refresh_table()
    messagebox.showinfo("Returned", f"{removed['name']}'s rental has been returned")
    # it give a pop up window so users won't miss it



def refresh_table():
    '''
    Rebuilds the treeview from scratch using the current content of rentals.
    It wipes and reinserts information instead of indiviually doing rows
    because it garentees the table matches the list.
    '''
    # 
    for row in tree.get_children():
        tree.delete(row)

    # reinsert one row per rentil, in list order.
    # this keeps tree position and list index aligned for delete_rental
    for rental in rentals:
        tree.insert("", tk.END, values = (
            rental["receipt"],
            rental["name"],
            rental["item"],
            rental["qty"],
            f"${rental['total']:.2f}" # 2 decimal places for currency
        ))

def clear_form():
    '''
    Resets all input fields after a successful add or 
    immediatly through the clear form button. Resetting the 
    item dropdown to the first key. this leaves a predictable start state
    '''
    name_var.set("")
    receipt_var.set("")
    
    # reset dropdown to first in dictionary rather than blank
    # cant leave blank as items_for_rent is a readonly dropdown
    item_var.set(list(items_for_rent.keys())[0])
    qty_var.set("")

def build_form(parent):
    '''
    makes the left side panel. Uses grid layout with a
    running row counter so that inserting or removing a field
    later only requires adding or removing one label and widget pair.
    rather than remembering every row 
    '''
    global name_entry, receipt_entry, qty_entry
    row = 0 # starts row at 0 and tracks the next free grid row

    tk.Label(parent, text ="Customer full name", anchor = "w").grid(row = row, column = 0, sticky = "w", pady = 3)
    row +=1
    name_entry = tk.Entry(parent, textvariable = name_var, width = 30)
    name_entry.grid(row = row, column = 0, sticky = "ew", pady = (0,8)) # stickey = "ew" lets the entry stretch to fill the column width
    row +=1

    tk.Label(parent, text = "Receipt Number:", anchor = "w").grid(row = row, column = 0, sticky = "w", pady = 3)
    row += 1
    receipt_entry = tk.Entry(parent, textvariable = receipt_var, width = 30)
    receipt_entry.grid(row = row, column = 0, sticky = "ew", pady = (0,8))
    row += 1

    tk.Label(parent, text = "Item to hire:", anchor = "w").grid(row = row, column = 0, sticky = "w", pady = 3)
    row += 1
    # dropdown is set to readonly so the user can only select an existing item
    # from the items_for_rent. this makes price lookup consistent and successful
    item_var.set(list(items_for_rent.keys())[0]) # default to first itesm so the dropdown never starts blank
    item_dropdown = ttk.Combobox(parent, textvariable = item_var, values = list(items_for_rent.keys()), state = "readonly", width = 28)
    item_dropdown.grid(row = row, column = 0, sticky = "ew", pady = (0,8))
    row += 1
    
    tk.Label(parent, text = "quantity (1-500)", anchor = "w").grid(row = row, column = 0, sticky = "w", pady = 3)
    row += 1
    qty_entry = tk.Entry(parent, textvariable = qty_var, width = 30)
    qty_entry.grid(row = row, column = 0, sticky = "ew", pady = (0,8))
    row += 1

    # buttons allow a function to be called when it is clicker 
    # rather than immediatly when the GUI is built
    tk.Button(parent, text = "Add rental", bg = "#4CAF50", fg = "white", font = ("Arial", 10, "bold"), width = 26, 
            command = add_rental).grid(row = row, column = 0, pady = 4) # green to visually signal positive/ confiming action
    row += 1
    tk.Button(parent, text = "Mark as Returned", bg = "#f44336", fg = "white", font = ("Arial", 10, "bold"), width = 26,
            command = delete_rental).grid(row = row, column = 0, pady = 4) # red to visually signal negative/ destructive action
    row += 1
    tk.Button(parent, text = "Clear Form", font = ("Arial", 10), width = 26, 
            command = clear_form).grid(row = row, column = 0) # neutral colour to show no risk

# build the table

def build_table(parent):
    """
    builds the right hand treeview table and its scrollbar.
    The srollbar and tree are linked in both directions so that 
    dragging the scrollbar drage the table. without the link it 
    would visually desync
    """
    global tree

    # show = "headings" hides the tkinter defualt blank first column 
    tree = ttk.Treeview(parent, columns = columns, show = "headings", height = 16)

    # widths is paired with columns position using zip()
    # both tuples must stay the same length an in the same order or 
    # columns will be done incorrectly
    widths = [90, 175, 130, 60, 110]
    for col, width in zip(columns, widths):
        tree.heading(col, text = col)
        tree.column(col, width = width, anchor = "center") # centered text reads more clearly in a short table

    
    scrollbar = ttk.Scrollbar(parent, orient = "vertical", command = tree.yview)
    tree.configure(yscrollcommand = scrollbar.set) # links scrollbar position to tree's current scroll position
    tree.pack(side = tk.LEFT, fill = tk.BOTH, expand = True) # table takes up all remaining space in its frame
    scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

    tk.Label(parent, text = "Select a row then click 'Mark as Returned' to remove it.",
    font = ("Arial", 9), fg = "grey").pack(pady = (6,0)) # smaller font and grey so read as a hint


def build_ui():
    '''
    the overall window layout. the table, splitting layout build, widget construction
    build_ui decides where things go, the other two decide what does there. 
    '''
    tk.Label(root, text = "Callum's Party Rental Corp", font = ("Arial", 18, "bold")).pack(pady =
    (12,6))  
    
    # container holds both panels side by side and expands with the window
    # so rezising the window rezises table accordingly
    container = tk.Frame(root)
    container.pack(fill = tk.BOTH, expand = True, padx = 12, pady = 6)

    #left panel: fixed width only grows vertically
    # does not need to be wider because window is
    left = tk.LabelFrame(container, text = "New Rental", font = ("Arial", 11, "bold"), padx = 10, pady = 10)
    left.pack(side = tk.LEFT, fill = tk.Y, padx = (0,10))

    # right panel expands in both directions so table does grow to fill
    # whatever space is left form panel takes place
    right = tk.LabelFrame(container, text = "Active Rentals", font = ("Arial", 11, "bold"), padx = 10, pady = 10)
    right.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)


    build_form(left)
    build_table(right)

# build the interface once then handle the control to 
# tkinter user inputs and interactions.
# uses relevant callback functions until window closes
build_ui()
root.mainloop()