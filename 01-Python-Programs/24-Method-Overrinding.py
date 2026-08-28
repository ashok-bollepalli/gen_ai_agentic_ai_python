class Parent:
    def display(self):
        print("Parent display method")

class Child(Parent):
    def display(self):
        super().display()
        print("Child display method")

obj = Child()
obj.display()


