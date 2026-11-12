student = {
    "name": "Ravi",
    "age": 25,
    "course": "Python",
    "marks": 85
}
print(student)
print(student["name"])  # if key not present it gives error
print(student.get("gender"))  # if key not present it gives None
print(student.get("city", "Hyd"))  # If key not present gives default val

## Adding New Key-Value Pair
student["grade"] = "A"
print(student)

student["name"] = "Raj"
print(student)

# Dictionary Operations
print(student.keys())
print(student.values())
print(student.items())

# update() is used to update dictionary values or add new key-value pairs.
student.update({"name": "Ashok"})
print(student)

# pop() removes value based on key.
student.pop("grade")
print(student)

# popItem() removes last inserted key-value pair
student.popitem()
print(student)

# clear : removes all key-value pairs from dictionary
# del : delete entire dictionary from memory

del student["name"]
print(student)

del student

# dictionary with looping

student = {
    "name": "Ravi",
    "age": 25,
    "course": "Python"
}

for key,value in student.items():
    print(key, "--", value)

# Working wit Nested Dictionary

students = {
    "s1": {
        "name": "Raj",
        "age": 25,
        "course": "Python"
    },
    "s2": {
        "name": "Anil",
        "age": 35,
        "course": "GEN AI"
    }
}

print(students["s1"])
print(students["s1"]["name"])
print(students["s1"].get("name"))

print(students["s2"])
print(students["s2"]["name"])

# Looping Nested Dictionary
for student_id, student_data in students.items():
    for key,value in student_data.items():
        print(key, "--", value)

    print("-----------")

places = {}
print(type(places))

print(students, type(students["s2"]))