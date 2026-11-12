# Encapsulation

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def set_balance(self, balance):
        self.__balance = balance

account = BankAccount(200)
account.__balance  = 500 # it won't modify private variable data
print(account.get_balance())
print(account.__balance)
