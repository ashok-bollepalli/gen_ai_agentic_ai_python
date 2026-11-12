# assignment operator
a = 100
b = 20

result = a + b
print(result)

result = a - b
print(result)

result = a * b
print(result)

result = a / b
print(result)

# floor division (return quotient without decimal value)
result = a // b
print(result)

# It returns Reminder
result = a % b
print(result)

# additional assignment
balance = 1000
deposit_amount = 500
#balance = balance + deposit_amount
balance += deposit_amount
print("Final balance : ", balance)

withdraw_amount = 200
#balance = balance - withdraw_amount
balance -= withdraw_amount
print("Final balance : ", balance)

uname = "admin"
pwd = "admin@123"
print(uname == "admin" and pwd == "admin@123")
print(uname !="" or pwd !="")

is_logged_in = True
print(not is_logged_in)

###### Membership Operators #####
students = ["Ashok", "Ramesh", "Suresh"]
print("Ashok" in students) # true
print("John" in students) # False
print("Kiran" not in students) # True

a = 10
b = 10

print(a is b)      # True
print(a is not b)  # False