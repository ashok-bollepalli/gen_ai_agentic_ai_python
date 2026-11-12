import sqlite3

#Establishing DB Connection
connection = sqlite3.connect("students.db")

# Create cursor object to execute SQL Queries
cursor = connection.cursor()

# Read student information
student_name = input("Enter Student Name: ")
student_email = input("Enter Student Email: ")
student_course   = input("Enter Student Course: ")
student_fee = float(input("Enter Student Fee: "))

sql = "insert into students(student_name, student_email, student_course, student_fee) values(?, ?, ?, ?)"

cursor.execute(sql, (student_name, student_email, student_course, student_fee))

connection.commit()

print("Student inserted Successfully")
connection.close()