import sys


# Variables demo
x = 10
print(x)
print(type(x))

name = "Ashok"
print(name)
print(type(name))

_mobile = 68686868
id1 = 101
stud1 = "Rajesh"
course_fee = 4000

# assigning same value to multiple variables
var_1 = var_2 = var_3 = 100

print("Variable 1:", var_1)
print("Variable 2:", var_2)
print("Variable 3:", var_3)

# assigning different values to multiple variables
var_8, var_9, var_10 = 80, 90, 100

print("Variable 8:", var_8)
print("Variable 9:", var_9)
print("Variable 10:", var_10)

# Variable swapping
a = 10
b = a
a,b = b,a
print(a)
print(b)


# Data Types
my_age = 30
print(my_age, type(my_age))
print("size of my_age var in bytes: ", sys.getsizeof(my_age))

my_name = "Ashok Bollepalli"
print(my_name, type(my_name))
print("size of my_name var bytes: ", sys.getsizeof(my_name))


# Flot Data Type
price = 99.99
percentage = 85.5

print(price, type(price))
print("size of price : ", sys.getsizeof(price))
print(percentage, type(percentage))
print("size of percentage : ", sys.getsizeof(percentage))

# complex data type
num = 5 + 3j
print(type(num))

# list data type (ordered + mutable + duplicates allowed)
students = ["Anil", "Sunil", "Gopi", "Anil"]
print(students)
print(type(students))

# tuple data type (ordered + Immutable + Duplicates allowed)
courses = ("Java", "Python", "GEN AI", "Python")
print(courses)
print(type(courses))

# set data type (Un Ordered + Mutable + No Duplicates)
skills = {"Java", "Python", "GEN AI", "DevOps", "Cloud", "Java"}
print(skills)
print(type(skills))

# dictionary data type (key-value pair)
student  = {
    "id" : 101,
    "name" : "Ashok",
    "gender" : "Male"
}
print(student)
print(type(student))

# Student Data
student_id = 101
student_name = "John"
course = "Python"
fee = 5000.00
is_paid = True
imp_concepts  = ["Fundamentals", "Variables", "DSA", "OOPS"]