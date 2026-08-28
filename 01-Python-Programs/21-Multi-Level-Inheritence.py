class GrandParent:
    def grandparent_method(self):
        print("Grand Parent method")

class Parent(GrandParent):
    def parent_method(self):
        print("Parent method")

class Child(Parent):
    def child_method(self):
        print("Child Method")

obj = Child()
obj.child_method()
obj.parent_method()
obj.grandparent_method()

