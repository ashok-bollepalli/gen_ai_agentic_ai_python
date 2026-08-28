import sqlite3

#Establishing DB Connection
connection = sqlite3.connect("students.db")

# Create cursor object to execute SQL Queries
cursor = connection.cursor()

# Read student information
student_id = int(input("Enter Student ID: "))

sql = "select * from students where student_id =?"

cursor.execute(sql, (student_id,))

student = cursor.fetchall()
print(student)