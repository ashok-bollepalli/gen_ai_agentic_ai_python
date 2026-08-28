class A:
    def method_a(self):
        print("Method from class A")

class B(A):
    def method_b(self):
        print("Method from class B")

class C(A):
    def method_c(self):
        print("Method from class C")

class D(B, C):
    def method_d(self):
        print("Method from class D")

obj = D()
obj.method_a()
obj.method_b()
obj.method_c()
obj.method_d()
