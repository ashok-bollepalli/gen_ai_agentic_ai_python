import matplotlib.pyplot as plt

courses = ["Python", "Java", "DevOps", "AWS"]
students = [50, 40, 30, 35]

plt.pie(students, labels = courses, autopct="%1.1f%%")

plt.title("Course Enrollment Share")

plt.show()