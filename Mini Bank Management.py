import pickle
import os
from datetime import datetime

FILENAME = "BankAccount.dat"
MINIMUM_BALANCE = 3000.00


# ------------------ CLASS ------------------

class BankAccount:
    def __init__(self, acc_no, name, balance, mobile, email):
        self.acc_no = acc_no
        self.name = name
        self.balance = balance
        self.mobile = mobile
        self.email = email
        self.transactions = []  # store transaction history

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(
            f"{datetime.now()} - Deposited ₹{amount}"
        )

    def withdraw(self, amount):
        if self.balance - amount >= MINIMUM_BALANCE:
            self.balance -= amount
            self.transactions.append(
                f"{datetime.now()} - Withdrawn ₹{amount}"
            )
            return True
        return False

    def display(self):
        print("\n--- Account Details ---")
        print(f"Account No : {self.acc_no}")
        print(f"Name       : {self.name}")
        print(f"Balance    : ₹{self.balance:.2f}")
        print(f"Mobile     : {self.mobile}")
        print(f"Email      : {self.email}")
        print("------------------------")

    def show_transactions(self):
        if not self.transactions:
            print("No transactions yet.")
        else:
            print("\n--- Transaction History ---")
            for t in self.transactions:
                print(t)
            print("----------------------------")


# ------------------ FILE HANDLING ------------------

def load_accounts():
    accounts = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "rb") as file:
            while True:
                try:
                    accounts.append(pickle.load(file))
                except EOFError:
                    break
    return accounts


def save_accounts(accounts):
    with open(FILENAME, "wb") as file:
        for acc in accounts:
            pickle.dump(acc, file)


# ------------------ OPERATIONS ------------------

def create_account():
    accounts = load_accounts()
    acc_no = int(input("Enter Account Number: "))

    for acc in accounts:
        if acc.acc_no == acc_no:
            print("Account number already exists!")
            return

    name = input("Enter Name: ")

    while True:
        balance = float(input(f"Enter Initial Balance (Minimum ₹{MINIMUM_BALANCE}): "))
        if balance >= MINIMUM_BALANCE:
            break
        print("Minimum balance not maintained.")

    mobile = input("Enter Mobile Number: ")
    email = input("Enter Email ID: ")

    new_acc = BankAccount(acc_no, name, balance, mobile, email)
    new_acc.transactions.append(
        f"{datetime.now()} - Account Created with ₹{balance}"
    )

    accounts.append(new_acc)
    save_accounts(accounts)
    print("Account created successfully!")


def display_all():
    accounts = load_accounts()
    if not accounts:
        print("No accounts found.")
        return
    for acc in accounts:
        acc.display()


def search_account():
    acc_no = int(input("Enter Account Number: "))
    accounts = load_accounts()

    for acc in accounts:
        if acc.acc_no == acc_no:
            acc.display()
            return

    print("Account not found.")


def adjust_account():
    acc_no = int(input("Enter Account Number: "))
    accounts = load_accounts()

    for acc in accounts:
        if acc.acc_no == acc_no:
            acc.display()
            print("1. Deposit")
            print("2. Withdraw")
            choice = int(input("Enter choice: "))
            amount = float(input("Enter amount: "))

            if choice == 1:
                acc.deposit(amount)
                print("Deposit successful.")
            elif choice == 2:
                if acc.withdraw(amount):
                    print("Withdrawal successful.")
                else:
                    print("Minimum balance must be maintained.")
            else:
                print("Invalid choice.")
                return

            save_accounts(accounts)
            return

    print("Account not found.")


def delete_account():
    acc_no = int(input("Enter Account Number to delete: "))
    accounts = load_accounts()

    updated = [acc for acc in accounts if acc.acc_no != acc_no]

    if len(updated) == len(accounts):
        print("Account not found.")
    else:
        save_accounts(updated)
        print("Account deleted successfully.")


def show_transaction_history():
    acc_no = int(input("Enter Account Number: "))
    accounts = load_accounts()

    for acc in accounts:
        if acc.acc_no == acc_no:
            acc.show_transactions()
            return

    print("Account not found.")


# ------------------ MAIN MENU ------------------

while True:
    print("\n====== BANK MANAGEMENT SYSTEM ======")
    print("1. Create Account")
    print("2. Display All Accounts")
    print("3. Search Account")
    print("4. Deposit / Withdraw")
    print("5. Delete Account")
    print("6. View Transaction History")
    print("7. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input.")
        continue

    if choice == 1:
        create_account()
    elif choice == 2:
        display_all()
    elif choice == 3:
        search_account()
    elif choice == 4:
        adjust_account()
    elif choice == 5:
        delete_account()
    elif choice == 6:
        show_transaction_history()
    elif choice == 7:
        print("Thank you for using the system.")
        break
    else:
        print("Invalid choice.")
        continue

    # Continue option
    cont = input("\nDo you want to continue? (yes/no): ").strip().lower()
    if cont != "yes":
        print("Exiting system.")
        break
