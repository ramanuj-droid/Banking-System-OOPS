from account import SavingsAccount, CurrentAccount
from transaction import TransactionManager

def main():
    accounts = {}

    while True:
        print("\n==== Welcome to Savitr Bank ====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Balance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            acc_type = input("Choose account type (savings/current): ").lower()
            try:
                balance = float(input("Initial deposit: "))
            except ValueError:
                print(" Invalid amount!")
                continue

            if acc_type == "savings":
                account = SavingsAccount(name, balance)
            elif acc_type == "current":
                account = CurrentAccount(name, balance)
            else:
                print(" Invalid account type!")
                continue

            accounts[name] = account
            print(f"✅ {acc_type.title()} account created for {name}!")

        elif choice == '2':
            name = input("Enter your name: ")
            if name in accounts:
                try:
                    amt = float(input("Enter deposit amount: "))
                    tm = TransactionManager(accounts[name])
                    tm.deposit(amt)
                except ValueError:
                    print(" Invalid amount.")
            else:
                print("❌ Account not found.")

        elif choice == '3':
            name = input("Enter your name: ")
            if name in accounts:
                try:
                    amt = float(input("Enter withdrawal amount: "))
                    tm = TransactionManager(accounts[name])
                    tm.withdraw(amt)
                except ValueError:
                    print(" Invalid amount.")
            else:
                print(" Account not found.")

        elif choice == '4':
            name = input("Enter your name: ")
            if name in accounts:
                acc = accounts[name]
                print(f"\n Name: {acc.owner}")
                print(f" Balance: ₹{acc.balance}")
                print(f" Account Type: {acc.account_type()}")
            else:
                print(" Account not found.")

        elif choice == '5':
            print(" Exiting... Thank you for using Savitr Bank!")
            break

        else:
            print(" Invalid choice. Please select from the menu.")

if __name__ == "__main__":
    main()
