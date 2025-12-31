import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

# ---------- DATA ----------
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

menu = {
    "Espresso": 50,
    "Latte": 70,
    "Cappuccino": 80
}

orders = {}
subtotal = 0
GST_RATE = 0.05

# ---------- PERSISTENT BILL NUMBER ----------
bill_number = 1
if os.path.exists("all_bills.txt"):
    with open("all_bills.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in reversed(lines):
            if line.startswith("Bill No:"):
                try:
                    bill_number = int(line.strip().split(":")[1]) + 1
                except:
                    bill_number = 1
                break

# ---------- FUNCTIONS ----------
def login():
    if user_entry.get() == ADMIN_USER and pass_entry.get() == ADMIN_PASS:
        login_frame.pack_forget()
        app_frame.pack()
    else:
        messagebox.showerror("Error", "Invalid login")


def add_order():
    global subtotal
    coffee = coffee_var.get()
    qty = qty_var.get()

    if coffee == "" or qty <= 0:
        messagebox.showerror("Error", "Select coffee & quantity")
        return

    cost = menu[coffee] * qty
    subtotal += cost
    orders[coffee] = orders.get(coffee, 0) + qty
    subtotal_label.config(text=f"Subtotal: ₹{subtotal}")


def generate_bill():
    global subtotal, orders, bill_number

    if subtotal == 0:
        messagebox.showerror("Error", "No orders placed")
        return

    try:
        discount_percent = float(discount_entry.get())
        if not (0 <= discount_percent <= 50):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Discount must be 0–50")
        return

    discount = subtotal * (discount_percent / 100)
    gst = subtotal * GST_RATE
    total = subtotal + gst - discount

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    bill = "\n=============================\n"
    bill += f"Bill No: {bill_number}\n"
    bill += f"Date: {now}\n"
    bill += "--- FINAL BILL ---\n"

    for item, qty in orders.items():
        bill += f"{item} x {qty} = ₹{menu[item] * qty}\n"

    bill += f"\nSubtotal: ₹{subtotal}"
    bill += f"\nDiscount ({discount_percent}%): -₹{discount:.2f}"
    bill += f"\nGST (5%): ₹{gst:.2f}"
    bill += f"\nTotal: ₹{total:.2f}\n"
    bill += "=============================\n"

    # Save bill to file (append mode)
    with open("all_bills.txt", "a", encoding="utf-8") as f:
        f.write(bill)

    messagebox.showinfo("Bill Generated", bill)

    # ----- RESET FOR NEXT CUSTOMER -----
    orders.clear()
    subtotal = 0
    bill_number += 1
    subtotal_label.config(text="Subtotal: ₹0")
    discount_entry.delete(0, tk.END)


# ---------- GUI ----------
root = tk.Tk()
root.title("Coffee Management System")
root.geometry("400x450")

# ----- LOGIN FRAME -----
login_frame = tk.Frame(root)
login_frame.pack(pady=50)

tk.Label(login_frame, text="Admin Login", font=("Arial", 16)).pack(pady=10)

tk.Label(login_frame, text="Username").pack()
user_entry = tk.Entry(login_frame)
user_entry.pack()

tk.Label(login_frame, text="Password").pack()
pass_entry = tk.Entry(login_frame, show="*")
pass_entry.pack()

tk.Button(login_frame, text="Login", command=login).pack(pady=10)

# ----- MAIN APP FRAME -----
app_frame = tk.Frame(root)

tk.Label(app_frame, text="Coffee Management", font=("Arial", 16)).pack(pady=10)

coffee_var = tk.StringVar()
qty_var = tk.IntVar()

tk.Label(app_frame, text="Select Coffee").pack()
tk.OptionMenu(app_frame, coffee_var, *menu.keys()).pack()

tk.Label(app_frame, text="Quantity").pack()
tk.Entry(app_frame, textvariable=qty_var).pack()

tk.Button(app_frame, text="Add Order", command=add_order).pack(pady=5)

subtotal_label = tk.Label(app_frame, text="Subtotal: ₹0")
subtotal_label.pack(pady=5)

tk.Label(app_frame, text="Discount % (0–50)").pack()
discount_entry = tk.Entry(app_frame)
discount_entry.pack()

tk.Button(app_frame, text="Generate Bill", command=generate_bill).pack(pady=10)

root.mainloop()
