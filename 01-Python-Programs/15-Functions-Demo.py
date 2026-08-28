# function with one parameter
def greet(name):
    print(name," Welcome to python")

# calling function
greet("Ashok")
greet("John")
greet("Steve")


# Function with multiple parameters
def print_student_data(name, course):
    print("Student Name is :", name)
    print("Student Course is :", course)

print_student_data("Ashok", "Python")
print_student_data("John", "GEN AI")

# Function with Return Value
def add(i, j):
    return i+j

result = add(10,20)
print(result)

## Function Without Return Value

def greet():
   print("Welcome")

result = greet()
print(result)

# function

def mul(a, b):
    return a*b
    print("completed")

result = mul(10,20)
print(result)


## Function to check even or odd

def check_even_odd(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"

result = check_even_odd(11)
print(f"The given number is {result}")

## Function to Find Biggest Number

def find_biggest(a, b):
    if a > b:
        return a
    else:
        return b

result = find_biggest(20, 35)
print(f"The biggest is {result}")


## Positional Arguments
def student(name, course):
    print("Name:", name)
    print("Course:", course)

student("Ashok", "Python")


## Keyword Arguments
def student(name, course):
    print("Name:", name)
    print("Course:", course)

student(course="JAVA", name="John")

## default arguments
def enroll_student(name="Ashok", course="GEN AI"):
    print("Student Name:", name)
    print("Enrolled Course:", course)

enroll_student("Ashok", "DEVOPS")
enroll_student()


## Variable Length Arguments
def print_numbers(*args, model):
    print(args, model)

print_numbers(10, model="gpt")
print_numbers(20, 30, model="gpt")
print_numbers(30, 40, model="gpt")

# sum of numbers using var args
def add_numbers(*nums):
    total = 0
    for num in nums:
        total = total + num
    return total

print(add_numbers(10, 20))
print(add_numbers(10, 20, 30))
print(add_numbers(10, 20, 30, 40))

# keyword variable length args
def student_details(*a, **kwargs):
    print(kwargs)

student_details(name="Ashok", course="GEN AI")
student_details(name="John", course="Python", fee=1000)
student_details(10, 20, name="John", course="Python", fee=1000, b=30)