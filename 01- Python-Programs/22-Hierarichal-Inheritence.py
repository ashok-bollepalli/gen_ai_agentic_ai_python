class Parent:
    def parent_method(self):
        print("Parent method")

class Child1(Parent):
    def child1_method(self):
        print("Child1 method")

class Child2(Parent):
    def child2_method(self):
        print("Child2 method")

c1 = Child1()
c2 = Child2()

c1.parent_method()
c1.child1_method()
print("------------------")
c2.parent_method()
c2.child2_method()