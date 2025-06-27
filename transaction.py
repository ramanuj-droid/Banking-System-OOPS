class TransactionManager:
    def __init__(self, account):
        self.account = account

    def deposit(self, amount):
        if amount > 0:
            self.account.deposit(amount)
            return f"✅ ₹{amount} deposited successfully."
        else:
            return "❌ Deposit must be greater than zero."

    def withdraw(self, amount):
        if amount <= 0:
            return "❌ Withdrawal must be greater than zero."
        elif amount > self.account.balance:
            return "❌ Insufficient balance."
        else:
            self.account.withdraw(amount)
            return f"✅ ₹{amount} withdrawn successfully."
