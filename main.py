import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

FILE_NAME = "expenses.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Notes"])


# Add Expense
def add_expense():
    date = date_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()
    notes = notes_entry.get().strip()

    if date == "" or category == "" or amount == "":
        messagebox.showerror("Error", "Please fill all required fields")
        return

    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, notes])

    tree.insert("", tk.END, values=(date, category, amount, notes))

    messagebox.showinfo("Success", "Expense Added Successfully")
    clear_fields()


# Load Expenses
def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    try:
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header

            for row in reader:
                tree.insert("", tk.END, values=row)

    except FileNotFoundError:
        pass


# Export Expenses
def export_expenses():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if save_path:
        with open(FILE_NAME, "r", encoding="utf-8") as source:
            data = source.read()

        with open(save_path, "w", encoding="utf-8") as target:
            target.write(data)

        messagebox.showinfo("Success", "Expenses Exported Successfully")


# Clear Fields
def clear_fields():
    date_entry.delete(0, tk.END)
    category_entry.set("")
    amount_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)


# ================= GUI =================

root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("850x600")
root.config(bg="#E8F5E9")

# Title
title = tk.Label(
    root,
    text="Personal Finance Tracker",
    font=("Arial", 22, "bold"),
    bg="#E8F5E9",
    fg="#1B5E20"
)
title.pack(pady=15)

# Decorative Text
decor = tk.Label(
    root,
    text="Shopping • Food • Travel • Savings • Bills",
    font=("Arial", 12),
    bg="#E8F5E9",
    fg="#2E7D32"
)
decor.pack()

# Input Frame
frame = tk.Frame(
    root,
    bg="#C8E6C9",
    bd=3,
    relief="ridge"
)
frame.pack(pady=15)

# Date
tk.Label(
    frame,
    text="Date",
    bg="#C8E6C9",
    font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=10, pady=8)

date_entry = tk.Entry(frame, width=25)
date_entry.grid(row=0, column=1, padx=10)

# Category
tk.Label(
    frame,
    text="Category",
    bg="#C8E6C9",
    font=("Arial", 10, "bold")
).grid(row=1, column=0, padx=10, pady=8)

category_entry = ttk.Combobox(
    frame,
    width=22,
    values=[
        "Shopping",
        "Fruits",
        "Vegetables",
        "Clothes",
        "Savings",
        "Bills",
        "Travel"
    ]
)
category_entry.grid(row=1, column=1, padx=10)

# Amount
tk.Label(
    frame,
    text="Amount",
    bg="#C8E6C9",
    font=("Arial", 10, "bold")
).grid(row=2, column=0, padx=10, pady=8)

amount_entry = tk.Entry(frame, width=25)
amount_entry.grid(row=2, column=1, padx=10)

# Notes
tk.Label(
    frame,
    text="Notes",
    bg="#C8E6C9",
    font=("Arial", 10, "bold")
).grid(row=3, column=0, padx=10, pady=8)

notes_entry = tk.Entry(frame, width=25)
notes_entry.grid(row=3, column=1, padx=10)

# Buttons
button_frame = tk.Frame(root, bg="#E8F5E9")
button_frame.pack(pady=10)

add_btn = tk.Button(
    button_frame,
    text="Add Expense",
    command=add_expense,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
    width=18
)
add_btn.grid(row=0, column=0, padx=10)

export_btn = tk.Button(
    button_frame,
    text="Export Expenses",
    command=export_expenses,
    bg="#2196F3",
    fg="white",
    font=("Arial", 10, "bold"),
    width=18
)
export_btn.grid(row=0, column=1, padx=10)

# Table Style
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#F1F8E9",
    foreground="black",
    rowheight=28,
    fieldbackground="#F1F8E9"
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold")
)

# Table
columns = ("Date", "Category", "Amount", "Notes")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=14
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)

tree.pack(pady=15)

# Load Existing Expenses
load_expenses()

root.mainloop()