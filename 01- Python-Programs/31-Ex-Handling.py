try:
    a = 10
    b = 0

    result = a / b

    print("Result : ", result)

except ValueError as ve:
    print("Exception Occured : ", ve)

except Exception as e:
    print("Please enter only numbers : ", e)


###########################################

try:
    num1 = 10
    num2 = 2
    result = num1 / num2
except ZeroDivisionError as ze:
    print("Cannot divide by zero : ", ze)
else:
    print("Result : ", result)

###########################################

try:
    print(10/2)
except ZeroDivisionError as ze:
    print("Cannot divide by zero : ", ze)
finally:
    print("Program Execution Completed")

###########################################

age = 19

if age >= 18:
    print("You are old enough to vote")
else:
    raise Exception("Age must be 18 or above to vote")


###########################################

class InvalidAgeError(Exception):
    pass

try:
    age = int(input("Enter your age : "))
    if age < 18:
        raise InvalidAgeError("You are not old enough to vote")
    print("You are old enough to vote")
except InvalidAgeError as e:
    print("Invalid Age Error : ", e)
except ValueError as ve:
    print("Invalid Input: ", ve)
finally:
    print("Program Execution Completed")






