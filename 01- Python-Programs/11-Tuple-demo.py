courses = ("JAVA", "Python", "GEN AI", "DEVOPS", ".Net", "MERN")
print(courses)

print(courses[0])
print(courses[1])
print(courses[-1])

print(courses[1:3])

print(courses[-1:-3:-1]) #start is inclusive, end is exclusive
print(courses[:3])
print(courses[2:])

## courses[1] = "AWS" (not possible)

print(courses.index("GEN AI"))

# tuple packing
student = "Ashok", "Male", 66868686
print(student)





## Tuple functions

# len()
# max ()
# min ()
# sum ()
# sorted ()

numbers = (10, 15, 30, 20, 40, 25)
print(len(numbers))
print(sum(numbers))
print(min(numbers))
print(max(numbers))

### numbers.sorted()  (invalid)

# sorted() returns list, not tuple.

sorted_numbers = sorted(numbers) #it returns new list
print(sorted_numbers)

sorted_numbers = sorted(numbers, reverse=True) #it returns new list
print(sorted_numbers)


courses = ("Python", "Java", "DevOps")

# convert tuple to list
course_list = list(courses) # it gives list
course_list[0] = "GEN AI"
print(course_list)

## Check Value Exists in Tuple

if "GEN AI" in courses:
    print("GEN AI course available in Ashok IT")
else:
    print("GEN AI course not available in Ashok IT")

# Tuple concatnation
frontend = ("HTML", "CSS")
backend = ("Python", "Django")
fullstack = frontend + backend
print(fullstack)

skills_list = list(fullstack)
skills_list.insert(-1,"DevOps")
print(skills_list)


a = ["a", "b", "c"]

# tuple unpacking
student = (a, "Male", 66868686)
name, gender, phone = student
print(name)
print(gender)
print(phone)
a.insert(1, "z")
print(student)