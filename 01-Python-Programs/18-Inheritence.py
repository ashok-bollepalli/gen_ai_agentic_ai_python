class Parent:
    def house(self):
        print("Parent House")

class Child(Parent):
    def bike(self):
        print("Child Bike")

c = Child()
c.bike()
c.house()