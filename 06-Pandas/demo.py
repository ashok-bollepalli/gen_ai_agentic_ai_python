import pandas as pd

employees = {
    "EmpId": [101, 102, 103, 104, 105, 106],
    "Name": ["Ravi", "Sita", "Kiran", "Rahul", "Priya", "Anil"],
    "Department": ["IT", "HR", "IT", "Sales", "HR", "IT"],
    "Salary": [50000, 45000, 70000, 40000, 48000, 65000],
    "Experience": [2, 5, 8, 1, 4, 7]
}

print(type(employees))

df = pd.DataFrame(employees)
print(df)

print(df.head())
print(df.head(3))

print(df.tail())
print(df.tail(2))

print(df.info())

print(df.describe())

print(df["Name"])
print(df[["Name", "Salary"]])

print(df[df["Salary"] > 50000])

print(df[df["Department"] == "IT"])

print(df[(df["Department"] == "IT") & (df["Salary"] > 60000)])

print(df.sort_values("Salary"))

print(df.sort_values("Salary", ascending=False))

print(df.sort_values(["Department", "Salary"]))

df["Bonus"] = df["Salary"] * 0.10
print(df)

df["Revised Salary"] = df["Salary"] + df["Bonus"]
print(df)

df.drop(columns = ["Salary", "Bonus"], inplace=True)
print(df)

df.drop_duplicates(inplace=True)
print(df)

emps = {
    "Name":["Ravi","Sita","Kiran","Rahul","Ashok", "Ashok"],
    "Salary":[50000,None,65000,None, 25000, 25000]
}

df = pd.DataFrame(emps)
print(df)

# Check Duplicate records
print(df.duplicated().sum())
df = df.drop_duplicates()
print(df)

df["Salary"] = df["Salary"].fillna(0)
print(df)