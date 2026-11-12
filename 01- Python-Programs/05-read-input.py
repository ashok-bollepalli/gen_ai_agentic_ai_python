
a = input("Enter first number : ")
b = input("Enter second number : ")

print(type(a), type(b))

print("Result Before Typecasting : ", (a+b))

a = int(a)
b = int(b)

print("Result After Typecasting : ", (a+b))
