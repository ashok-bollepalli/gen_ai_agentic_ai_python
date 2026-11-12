from abc import ABC, abstractmethod

class Payment(ABC):

    def __init__(self):
        print("Payment Class Constructor")

    @abstractmethod
    def pay(self, amount):
        pass

    def payment_success_msg(self):
        print("Payment is successfull")

class UpiPayment(Payment):
    def pay(self, amount):
        print("Paid using UPI : ", amount)
        super().payment_success_msg()

class CreditCardPayment(Payment):
    def __init__(self):
        super().__init__()

    def pay(self, amount):
        print("Paid using CreditCard : ", amount)
        super().payment_success_msg()


upi = UpiPayment()
upi.pay(120)

credit = CreditCardPayment()
credit.pay(35000)