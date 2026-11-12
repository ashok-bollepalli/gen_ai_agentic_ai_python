# integer literals
age = 25
student_id = 101

print(age)
print(student_id)

# floating literals
price = 99.99
percentage = 15.55
print(price)
print(percentage)

# String literals
name = 'Ashok'
city = "Hyd"
course = '''It's Python course'''
msg = """
    Welcome to Python Training
    with Realtime projects
"""

# Boolean Literals
is_activated = True
is_completed = False
print(is_activated)
print(is_completed)

# None Literal
result = None
print(result)

# List literal (mutable)
students = ["Ashok", "Ramesh", "Raju", "Ashok"]
print(students)

# Tuple Literal (immutable)
courses = ("Python", "Java", "C++", "Python")
print(courses)

# Set literal (no duplicates, no order)
cities = {"Hyd", "Pune", "Chennai", "Delhi", "Hyd"}
print(cities)

# Dictionary literal
student = {
    "id" : 101,
    "name" : "Ashok",
    "age"   : 35,
    "gender" : "Male",
}
print(student)

students = [
    {
        "id": 101,
        "name": "Ashok",
        "age": 35,
        "gender": "Male",
    },
    {
        "id": 102,
        "name": "John",
        "age": 25,
        "gender": "Male",
    }
]
print(students)
