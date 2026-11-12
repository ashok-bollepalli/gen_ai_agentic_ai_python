class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, course):
        super().__init__(name)
        self.course = course

    def display(self):
        print(self.name)
        print(self.course)

s1 = Student("Ashok", "Python")
s1.display()