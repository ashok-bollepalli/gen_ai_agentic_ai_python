for i in range(1, 11):
    if i == 5:
        break
    print(i)
###################

for i in range(1, 11):
    if i == 5:
        continue
    print(i)
###################

students = ["Raju", "john", "Steve", "Ashok", "Rani"]
search_name  = "Ashok"

for student in students:
    print("Checking :", student)
    if search_name == student:
        print("Student Found :", student)
        break
########################################
students = [
    {"name": "Ravi", "marks": 80},
    {"name": "Kiran", "marks": 30},
    {"name": "Sita", "marks": 90}
]

for student in students:
    if student["marks"] < 35:
        continue
    print("Certificate Sent for :", student["name"])