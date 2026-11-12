import sqlite3

#Establishing DB Connection
connection = sqlite3.connect("students.db")

# Create cursor object to execute SQL Queries
cursor = connection.cursor()

# Using cursor we can execute SQL queries

cursor.execute("""
    create table if not exists students(
        student_id integer primary key autoincrement,
        student_name text,
        student_email text unique,
        student_course text,
        student_fee real
    )
""")

print("Student Table Created Successfully....")

connection.commit()
connection.close()