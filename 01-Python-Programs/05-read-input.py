# list type casting
course_name = "Python"
letters = list(course_name)
print(letters)

# Tuple Type Casting
numbers = [10, 20, 30]
result = tuple(numbers)
print(result)

# Set Type Casting
numbers = [10, 20, 10, 30, 20]
unique_numbers = set(numbers)
print(unique_numbers)

# dict type casting
data = [("name", "Ashok"), ("course", "Python")]
student = dict(data)
print(student)

# Implicit casting
a = 10
b = 2.5
result = a + b
print("Result : ", result)
print(type(result))

# Explicit Casting
i = "10"
j = "20"
result = int(i) + int(j)
print("Result : ", result)
print(type(result))

