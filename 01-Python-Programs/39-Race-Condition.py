import threading
import time

balance = 1000

def withdraw(amount):
    global balance
    if balance >= amount:
        current_balance = balance
        time.sleep(1)
        balance = current_balance - amount
        print("Withdraw successfully")
        print("Remaining Balance:", balance)
    else:
        print("Insufficient Balance")

t1 = threading.Thread(target=withdraw, args=(700,))
t2 = threading.Thread(target=withdraw, args=(700,))

t1.start()
t2.start()

t1.join()
t2.join()

print("Final Balance :", balance)