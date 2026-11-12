age = 20
if age >=18:
    print("Eligible for vote")


print("1. Add Student")
print("2. View Student")
print("3. Update Student")
print("4. Delete Student")

choice = int(input("Enter your choice: "))

match choice:
    case 1:
        print("Student add operation selected")
    case 2:
        print("Student View Operation selected")
    case 3:
        print("Student Update Operation selected")
    case 4:
        print("Student Delete Operation selected")
    case _:
        print("Invalid Choice")

