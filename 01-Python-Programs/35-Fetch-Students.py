import sqlite3

#Establishing DB Connection
connection = sqlite3.connect("students.db")

# Create cursor object to execute SQL Queries
cursor = connection.cursor()

sql = "select * from students"

cursor.execute(sql)

students  = cursor.fetchall()

print(type(students))

for student in students:
    print(student)