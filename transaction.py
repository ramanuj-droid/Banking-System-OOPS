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
def log_transaction(user, txn_type, amount, balance, session_state):
    import datetime
    txn = {
        "Date/Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Type": txn_type,
        "Amount": amount,
        "Balance": balance
    }
    if user not in session_state["transactions"]:
        session_state["transactions"][user] = []
    session_state["transactions"][user].append(txn)
