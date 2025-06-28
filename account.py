import random

class Account:
    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = balance
        self.account_number = self._generate_account_number()

    def _generate_account_number(self):
        # Generates a random 6-digit number with prefix
        return f"SAV-{random.randint(100000, 999999)}"

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def account_type(self):
        return "Generic Account"


class SavingsAccount(Account):
    def account_type(self):
        return "Savings Account"


class CurrentAccount(Account):
    def account_type(self):
        return "Current Account"
