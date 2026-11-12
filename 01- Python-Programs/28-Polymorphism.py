class UpiPayment:
    def pay(self, amount):
        print(f"Paid ₹{amount} using UPI")

class CreditCardPayment:
    def pay(self, amount):
        print(f"Paid ₹{amount} using Credit Card")

class DebitCardPayment:
    def pay(self, amount):
        print(f"Paid ₹{amount} using Debit Card")

class CashPayment:
    def pay(self, amount):
        print(f"Paid ₹{amount} using Hand Cash")

class PaymentService:
    def make_payment(self, payment_method_type, amount):
        payment_method_type.pay(amount)


ps = PaymentService()

ps.make_payment(CreditCardPayment(), 1000)
ps.make_payment(DebitCardPayment(), 2000)
ps.make_payment(CashPayment(), 5000)
ps.make_payment(UpiPayment(), 10000)