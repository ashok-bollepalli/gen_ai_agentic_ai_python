# String operations

name = "Python"
print(len(name))

print(name * 3)

# index based operations
print(name[0])
print(name[-1])

# slicing operations
print(name[0:3]) # Pyt
print(name[3:]) #hon

# name[0] = "J"  # Error

f_name = "Ashok"
l_name = "Bollepalli"

full_name = f_name +" "+ l_name
print(full_name)

# Check character or word exists (True/False)
course = "GEN AI and Agentic AI"
print("AI" in course)
print("Python" in course)

# String with forloop
for letter in course:
    print(letter)

# String methods

# upper() :
# lower() :
# title() : First character of every word converts into upper case
# capitalize() : converts first letter of string into uppercase.
# strip() : removes spaces from beginning and ending of string.
# lsstrip() : lstrip() removes spaces from left side.
# rsstrip() : rstrip() removes spaces from right side.
# replace() : Replace old value with new value and creates new string
# split() : splits string into list of elements
# join() : joins list values into string (we can give delim)
# find() : returns index position of given value.
# count() : returns how many times value is repeated
# startsWith() : checks whether string starts with given value.
# endsWith() : checks whether string ends with given value.
# isdigit() : checks whether all characters are digits.
# isalpha() : checks whether all characters are alphabets.
# isalnum() : checks whether all characters are alphabets or numbers.


msg = "i like gen ai development"
print(msg.title())
print(msg.capitalize())

message = "I like Java"
new_msg = message.replace("Java","Python")
print(new_msg)

courses = "Python,Java,DevOps,AWS"
result = courses.split(",")
print(result)

courses = ["Python", "Java", "DevOps"]
result = "#".join(courses)
print(result)

str = "welcome to c and python"
print(str.find('c')) # 3
print(str.find('z')) # -1
print(str.find('python')) # 11

print(str.index('python')) # 11
## print(str.index('z')) # Error

message = "Python is easy and Python is powerful"
print(message.count("Python"))

print(message.startswith("Python"))
print(message.endswith("Python"))

mobile = "85858658"
print(mobile.isdigit())

name = "AshokIT"
print(name.isalpha())

pwd = "India@123"
print(pwd.isalnum())

# String formatting is used to insert variable values inside a string.
name = "Ashok"
course = "Python"

print("Student name is", name, "and course is", course)
print("Student name is " + name + " and course is " + course)

msg = "Student name is {} and course is {}".format(name, course)
print(msg)

msg  = f"Student name is {name} and course is {course}"
print(msg)

# select * from user_tbl where email={email} and pwd = {pwd}

# Count words in sentence
sentence = "Python is easy to learn"
words = sentence.split()
print(words)
print("Words Count : ", len(words))

# Generate Username based on name and last 4 digits of phno
name = "Ashok"
phno = "868686868"
username = name.lower()+ phno[-4:]
print(username)
