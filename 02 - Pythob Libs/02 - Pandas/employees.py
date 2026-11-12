import pandas as pd

employees = {
    "EmpId": [101, 102, 103, 104, 105, 106],
    "Name": ["Ravi", "Sita", "Kiran", "Rahul", "Priya", "Anil"],
    "Department": ["IT", "HR", "IT", "Sales", "HR", "IT"],
    "Salary": [50000, 45000, 70000, 40000, 48000, 65000],
    "Experience": [2, 5, 8, 1, 4, 7]
}

df = pd.DataFrame(employees)

df.to_csv("employees-data.csv", index=False)

print("CSV File Created Successfully")

df = pd.read_csv("employees-data.csv")
print(df)