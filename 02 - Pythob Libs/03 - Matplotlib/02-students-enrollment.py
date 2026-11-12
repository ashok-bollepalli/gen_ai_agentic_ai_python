import matplotlib.pyplot as plt

courses = ["Python", "Java", "DevOps", "AWS"]
student_enrollments = [50, 40, 30, 35]

#plt.bar(courses, student_enrollments)
plt.barh(courses, student_enrollments)

plt.title("Course Enrollment Report")
plt.xlabel("Course")
plt.ylabel("Student Enrollments")

plt.show()


