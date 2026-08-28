import threading
import time

balance = 1000

lock = threading.Lock()

def withdraw(amount):
    global balance

    with lock:
        if balance >= amount:
            print(
                threading.current_thread().name,
                "is processing withdrawl"
            )
            current_balance = balance
            time.sleep(1)
            balance = current_balance - amount
            print("Remaining Balance:", balance)
        else:
            print( threading.current_thread().name, "- Insufficient balance" )


t1 = threading.Thread(target=withdraw, args=(700,), name="Customer-1")
t2 = threading.Thread(target=withdraw, args=(700,), name="Customer-2")

t1.start()
t2.start()

t1.join()
t2.join()

print("Final Balance:", balance)