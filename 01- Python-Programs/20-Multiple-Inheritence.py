class Father:
    def father_property(self):
        print("Father property")
    def m1(self):
        print("Father m1 method")

class Mother:
    def mother_property(self):
        print("Mother property")
    def m1(self):
        print("Mother m1 method")

class Child(Father, Mother):
    def child_property(self):
        print("Child property")
    def m1(self):
        print("Child m1 method")


obj = Child()
obj.father_property()
obj.mother_property()
obj.child_property()
obj.m1()