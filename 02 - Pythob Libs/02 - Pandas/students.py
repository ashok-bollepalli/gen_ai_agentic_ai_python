import pandas as pd

students = {
    "name": ["Ravi", "Sita", "Kiran"],
    "course": ["Python", "Java", "DevOps"],
    "marks": [80, 90, 75]
}

df = pd.DataFrame(students)

df.to_excel("students-data.xlsx", index=False)

print("Excel File created.....")

df = pd.read_excel("students-data.xlsx")

print(df)
