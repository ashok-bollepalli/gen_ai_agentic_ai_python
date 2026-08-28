import json

student = {
    "id": 101,
    "name": "Ravi",
    "course": "Python",
    "fee": 15000
}

student_json = json.dumps(student, sort_keys=True, indent=4)
print(student_json)
print(type(student_json))

print("--------------------------------")

student = json.loads(student_json)
print(student)
print(type(student))

print("--------------------------------")

with open("student.json", "w") as file:
    json.dump(student, file, indent=10)

print("JSON file created successfully")

print("--------------------------------")

with open("student.json", "r") as file:
    student = json.load(file)
    print(student)
