# -------- ADMIN DETAILS --------
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

# -------- MENU --------
menu = {
    "espresso": 50,
    "latte": 70,
    "cappuccino": 80
}

orders = {}
subtotal = 0
GST_RATE = 0.05


def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    return username == ADMIN_USER and password == ADMIN_PASS


def show_menu():
    print("\n--- Coffee Menu ---")
    for item, price in menu.items():
        print(f"{item.title()} : ₹{price}")


def take_order():
    global subtotal
    coffee = input("Enter coffee name: ").lower()

    if coffee in menu:
        qty = int(input("Enter quantity: "))
        cost = menu[coffee] * qty
        subtotal += cost
        orders[coffee] = orders.get(coffee, 0) + qty
        print(f"{qty} {coffee}(s) added. ₹{cost}")
    else:
        print("Coffee not available!")


def show_bill():
    while True:
        discount_percent = float(input("Enter discount % (0–50): "))
        if 0 <= discount_percent <= 50:
            break
        print("Invalid discount! Try again.")

    discount = (discount_percent / 100) * subtotal
    gst = subtotal * GST_RATE
    total = subtotal + gst - discount

    print("\n--- FINAL BILL ---")
    bill_text = "\n--- FINAL BILL ---\n"

    for coffee, qty in orders.items():
        line = f"{coffee.title()} x {qty} = ₹{menu[coffee] * qty}"
        print(line)
        bill_text += line + "\n"

    bill_text += f"Subtotal : ₹{subtotal}\n"
    bill_text += f"Discount ({discount_percent}%) : -₹{discount:.2f}\n"
    bill_text += f"GST (5%) : ₹{gst:.2f}\n"
    bill_text += f"Total Payable : ₹{total:.2f}\n"

    print(bill_text)

    with open("bill.txt", "w", encoding="utf-8") as file:
        file.write(bill_text)

    print("Bill saved to bill.txt 🧾")


# -------- MAIN PROGRAM --------
if admin_login():
    print("Login successful ✅")

    while True:
        print("\n1. Show Menu")
        print("2. Take Order")
        print("3. Show Bill")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            show_menu()
        elif choice == "2":
            take_order()
        elif choice == "3":
            show_bill()
        elif choice == "4":
            print("Thank you ☕ Visit again!")
            break
        else:
            print("Invalid choice")
else:
    print("Access denied ❌")
