from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self,owner,balance =0):
        self.__owner=owner
        self.__balance = balance

    @property
    def owner(self):
        return self.__owner

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, amount):
        if amount >= 0:
            self.__balance = amount
        else:
            print("Invalid balance amount")

    def deposit(self,amount):
        if amount>0:
            self.__balance += amount
            print(f"₹{amount} deposited. Available Balance : ₹{self.__balance}")
        else:
            print("Deposited amount must be greater than 0")

    def withdraw(self,amount):
        if 0<amount<=self.__balance:
            self.__balance=self.balance-amount
            print(f"₹{amount} withdrawn. Available Balnce: ₹{self.__balance}")
        else:
            print("Insuffienct Balance")

@abstractmethod
def account_type(self):
    pass

class SavingsAccount(Account):
    def account_type(self):
        return "Savings Account"

class CurrentAccount(Account):
    def account_type(self):
        return "Current Account"
        
import random

class Account:
    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = balance
        self.account_number = self._generate_account_number()

    def _generate_account_number(self):
        return f"SAV-{random.randint(100000, 999999)}"

    def account_type(self):
        return "Generic"
