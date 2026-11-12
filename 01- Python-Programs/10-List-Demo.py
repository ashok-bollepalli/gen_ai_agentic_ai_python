# list creation
courses = ["JAVA", "Python", "DevOps", "GEN AI"]

## access list elments
print(courses[0])
print(courses[1])
print(courses[2])
print(courses[3])

items = ["Laptop", "Mouse", "Keyboard", "Monitor"]

# Positive Indexing (starts from left to right)
print(items[0])

#negative index (starts from right to left)
print(items[-1])


# List Slicing :: used to get a part of list
# syntax : list_name[start:end]

numbers = [10, 20, 30, 40, 50, 60]
print(numbers) # print all elements

print(numbers[1:4]) #start index inclusive, end index exclusive

print(numbers[:3]) # print from 0th index to 2nd index

print(numbers[2:]) # print from 2nd to last

print(numbers[::2]) # step by 2

print(numbers[::-1]) # print in reverse order


#######################################################
# List Operations
#######################################################

# append : append() adds an element at the end of the list
# insert : insert() adds and element at specified index
# extends : extend() adds multiple elements to the list.
# remove : remove() removes the specified value
# pop : pop() removes element based on index. If index is not given, pop() removes the last element
# clear : clear() removes all elements from the list.
# del : del can delete an element or entire list.

courses = ["Python", "Java"]
courses.append("DevOps")
print(courses)

courses.insert(1, "GEN AI")
print(courses)


frontend = ["HTML", "CSS"]
backend = ["Python", "Django"]
frontend.extend(backend)
print(frontend)


courses.remove("Java")
print(courses)

courses.pop()
print(courses)

courses.clear()
print(courses)

courses = ["Python", "Java", "DevOps"]
del courses


# list with for loop
courses = ["Python", "Java", "DevOps"]
for course in courses:
    print(course)

# List functions

print(len(courses))

numbers = [1, 3, 6, 9, 2]
print(len(numbers))
print(min(numbers))
print(max(numbers))
print(sum(numbers))

numbers.sort() #it modifies existing list
print(numbers)

numbers.sort(reverse=True)
print(numbers)


#################################

# normal way
numbers = []
for i in range(1,6):
    numbers.append(i)

print(numbers)

# list comprehension
numbers = [i for i in range(1,6)]
print(numbers)

# square of numbers in normal way
squares = []
for i in range(1,6):
    squares.append(i*i)
print(squares)

# square of numbers using comprehension
squares = [i * i for i in range(1,6)]
print(squares)

# Even Numbers normal way
even_numbers = []
for i in range(1,11):
    if i % 2 == 0:
     even_numbers.append(i)
print(even_numbers)

# comprehension
even_numbers = [i for i in range(1,11) if i % 2 ==0]
print(even_numbers)

# convert to uppercase
names = ["ravi", "sita", "kiran"]
for name in names:
    print(name.upper())

upper_names = [name.upper() for name in names]
print(upper_names)

# students grade
marks = [80, 30, 90, 45, 20]
results = ["Pass" if mark>=35 else "Fail" for mark in marks]
print(results)

# GST
prices = [1000, 2000, 5000, 10000]
price_with_gst = [price + (price * 18 /100) for price in prices]
print(price_with_gst)


numbers = [10,20,30,40]
print(numbers)
numbers.insert(0,5)
print(numbers)

numbers_tuple = tuple(numbers)
print(numbers_tuple)