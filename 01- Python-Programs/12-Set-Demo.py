courses = {"Python", "JAVA", "DEVOPS", "Python"}
print(hash("Python"))
print(hash("JAVA"))
print(hash("JAVA"))

#### Set Operations ####

# add ( ) : It is used Add one element to set
# update ( ) : It is used Add multiple elements to set
# remove ( ) : It is used to remove specified element from set
# discard ( ) : It is used to remove specified element from set
# pop ( ) : It is used to remove random element from set
# clear ( ) : It is used to remove all elements from set
# del : It is used to delete entire set from memory

courses.add("GEN AI")
print(courses)

courses.update(["GCP", "AWS", "aws", "Azure"])
print(courses)

#courses.remove("HTML")
print(courses)

# If the element is not available, discard() does not give error.

courses.discard("AWS")
print(courses)

courses.pop()
print(courses)

courses.clear()
print(courses)

del courses
## print(courses)


## Set Functions
# len()
# min()
# max()
# sorted()

numbers = {10, 50, 20, 80, 30, 40}
print(len(numbers))
print(min(numbers))
print(max(numbers))
print(sum(numbers))
sorted_numbers = sorted(numbers, reverse=True)
print(sorted_numbers)

# Remove Duplicates from list using set() function
skills = ["JAVA", "Python", "DevOps", "JAVA"]
print(set(skills))