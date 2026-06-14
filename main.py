import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import os
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# Create CSV file if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Notes"])


def calculate_total():
    total = 0

    try:
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                try:
                    total += float(row[2])
                except:
                    pass

    except FileNotFoundError:
        pass

    total_label.config(text=f"Total Expenses: ₹{total:,.2f}")


def save_all_rows():
    with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Notes"])

        for item in tree.get_children():
            writer.writerow(tree.item(item)["values"])


def add_expense():
    date = date_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()
    notes = notes_entry.get().strip()

    if date == "" or category == "" or amount == "":
        messagebox.showerror("Error", "Please fill all required fields")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Invalid Date",
            "Use format: YYYY-MM-DD\nExample: 2026-06-15"
        )
        return

    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, notes])

    tree.insert("", tk.END, values=(date, category, amount, notes))

    calculate_total()
    clear_fields()

    messagebox.showinfo("Success", "Expense Added Successfully")


def delete_expense():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an expense to delete"
        )
        return

    for item in selected:
        tree.delete(item)

    save_all_rows()
    calculate_total()

    messagebox.showinfo(
        "Deleted",
        "Expense deleted successfully"
    )


def search_expenses():
    search_text = search_entry.get().strip().lower()

    for row in tree.get_children():
        tree.delete(row)

    try:
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if (
                    search_text in row[0].lower()
                    or search_text in row[1].lower()
                ):
                    tree.insert("", tk.END, values=row)

    except FileNotFoundError:
        pass


def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    try:
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                tree.insert("", tk.END, values=row)

    except FileNotFoundError:
        pass

    calculate_total()


def show_pie_chart():
    category_totals = {}

    try:
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                category = row[1]

                try:
                    amount = float(row[2])
                except:
                    continue

                category_totals[category] = (
                    category_totals.get(category, 0) + amount
                )

        if not category_totals:
            messagebox.showwarning(
                "No Data",
                "No expenses available"
            )
            return

        plt.figure(figsize=(6, 6))
        plt.pie(
            category_totals.values(),
            labels=category_totals.keys(),
            autopct="%1.1f%%"
        )
        plt.title("Expense Distribution")
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))


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

        messagebox.showinfo(
            "Success",
            "Expenses Exported Successfully"
        )


def clear_fields():
    date_entry.delete(0, tk.END)
    category_entry.set("")
    amount_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)


# ================= GUI =================

root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("1000x700")
root.config(bg="#E8F5E9")

title = tk.Label(
    root,
    text="Personal Finance Tracker",
    font=("Arial", 22, "bold"),
    bg="#E8F5E9",
    fg="#1B5E20"
)
title.pack(pady=15)

decor = tk.Label(
    root,
    text="Shopping • Food • Travel • Savings • Bills",
    font=("Arial", 12),
    bg="#E8F5E9",
    fg="#2E7D32"
)
decor.pack()

frame = tk.Frame(root, bg="#C8E6C9", bd=3, relief="ridge")
frame.pack(pady=15)

tk.Label(frame, text="Date", bg="#C8E6C9",
         font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=8)

date_entry = tk.Entry(frame, width=25)
date_entry.grid(row=0, column=1)

tk.Label(
    frame,
    text="Format: YYYY-MM-DD",
    bg="#C8E6C9",
    fg="gray",
    font=("Arial", 8)
).grid(row=0, column=2)

tk.Label(frame, text="Category", bg="#C8E6C9",
         font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=8)

category_entry = ttk.Combobox(
    frame,
    width=22,
    values=[
        "Food",
        "Shopping",
        "Travel",
        "Savings",
        "Beauty",
        "Bills",
        "Clothes"
    ]
)
category_entry.grid(row=1, column=1)

tk.Label(frame, text="Amount", bg="#C8E6C9",
         font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=8)

amount_entry = tk.Entry(frame, width=25)
amount_entry.grid(row=2, column=1)

tk.Label(frame, text="Notes", bg="#C8E6C9",
         font=("Arial", 10, "bold")).grid(row=3, column=0, padx=10, pady=8)

notes_entry = tk.Entry(frame, width=25)
notes_entry.grid(row=3, column=1)

button_frame = tk.Frame(root, bg="#E8F5E9")
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Expense",
    command=add_expense,
    bg="#4CAF50",
    fg="white",
    width=15
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Delete Expense",
    command=delete_expense,
    bg="#F44336",
    fg="white",
    width=15
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Export CSV",
    command=export_expenses,
    bg="#2196F3",
    fg="white",
    width=15
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Pie Chart",
    command=show_pie_chart,
    bg="#9C27B0",
    fg="white",
    width=15
).grid(row=0, column=3, padx=5)

summary_frame = tk.Frame(root, bg="#E8F5E9")
summary_frame.pack()

total_label = tk.Label(
    summary_frame,
    text="Total Expenses: ₹0.00",
    font=("Arial", 12, "bold"),
    bg="#E8F5E9",
    fg="#D32F2F"
)
total_label.pack()

search_frame = tk.Frame(root, bg="#E8F5E9")
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search:",
    bg="#E8F5E9",
    font=("Arial", 10, "bold")
).grid(row=0, column=0)

search_entry = tk.Entry(search_frame, width=25)
search_entry.grid(row=0, column=1, padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_expenses,
    bg="#FF9800",
    fg="white"
).grid(row=0, column=2)

tk.Button(
    search_frame,
    text="Show All",
    command=load_expenses,
    bg="#607D8B",
    fg="white"
).grid(row=0, column=3, padx=5)

columns = ("Date", "Category", "Amount", "Notes")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=220)

tree.pack(pady=15)

load_expenses()

root.mainloop()