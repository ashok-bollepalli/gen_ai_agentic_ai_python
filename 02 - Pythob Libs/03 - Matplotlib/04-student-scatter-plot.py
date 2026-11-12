import matplotlib.pyplot as plt

study_hours = [1, 2, 3, 4, 5]
marks = [35, 45, 60, 75, 90]

plt.scatter(study_hours, marks)

plt.title("Study Hours vs Marks")
plt.xlabel("Study Hours")
plt.ylabel("Marks")

plt.grid()

plt.show()