def welcome():
    print("Welcome..")

class Student:

    inst_name  = "Ashok IT"

    def __init__(self, name):
        self.name = name

    def display_result(self):
        print(self.name, "--", Student.inst_name)

s1 = Student("John")
s2 = Student("Michael")

s1.display_result() # s1.display_result(s1)
s2.display_result() # s2.display_result(s2)

welcome() # welcome()
