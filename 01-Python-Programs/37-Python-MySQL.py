import mysql.connector
from mysql.connector import Error


def get_connection():
    """
    Creates and returns a MySQL database connection.
    Update the username and password according to your MySQL configuration.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="student"
        )

        return connection

    except Error as error:
        print("Database connection failed:", error)
        return None


def create_table():
    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS students (
                student_id INT PRIMARY KEY AUTO_INCREMENT,
                student_name VARCHAR(100) NOT NULL,
                student_email VARCHAR(100) UNIQUE NOT NULL,
                student_course VARCHAR(100) NOT NULL,
                student_fee DECIMAL(10, 2) NOT NULL
            )
        """

        cursor.execute(sql)
        connection.commit()

        print("Students table created successfully.")

    except Error as error:
        print("Error while creating table:", error)

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# CREATE operation
def add_student():
    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        student_name = input("Enter student name: ").strip()
        student_email = input("Enter student email: ").strip()
        student_course = input("Enter student course: ").strip()
        student_fee = float(input("Enter student fee: "))

        sql = """
            INSERT INTO students
            (student_name, student_email, student_course, student_fee)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            student_name,
            student_email,
            student_course,
            student_fee
        )

        cursor = connection.cursor()
        cursor.execute(sql, values)
        connection.commit()

        print("Student added successfully.")
        print("Generated Student ID:", cursor.lastrowid)

    except ValueError:
        print("Student fee must be a valid number.")

    except Error as error:
        print("Error while adding student:", error)

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# READ operation - all students
def view_all_students():
    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        sql = "SELECT * FROM students ORDER BY student_id"

        cursor.execute(sql)
        students = cursor.fetchall()

        if not students:
            print("No student records found.")
            return

        print("\n" + "=" * 90)
        print(
            f"{'ID':<8}"
            f"{'Name':<20}"
            f"{'Email':<30}"
            f"{'Course':<20}"
            f"{'Fee':>10}"
        )
        print("=" * 90)

        for student in students:
            print(
                f"{student['student_id']:<8}"
                f"{student['student_name']:<20}"
                f"{student['student_email']:<30}"
                f"{student['student_course']:<20}"
                f"{float(student['student_fee']):>10.2f}"
            )

        print("=" * 90)

    except Error as error:
        print("Error while reading students:", error)

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# READ operation - one student
def view_student_by_id():
    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        student_id = int(input("Enter student ID: "))

        sql = """
            SELECT *
            FROM students
            WHERE student_id = %s
        """

        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, (student_id,))

        student = cursor.fetchone()

        if student:
            print("\nStudent Details")
            print("------------------------------")
            print("Student ID     :", student["student_id"])
            print("Student Name   :", student["student_name"])
            print("Student Email  :", student["student_email"])
            print("Student Course :", student["student_course"])
            print("Student Fee    :", student["student_fee"])
        else:
            print("Student not found.")

    except ValueError:
        print("Student ID must be a number.")

    except Error as error:
        print("Error while reading student:", error)

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# UPDATE operation
def update_student():
    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        student_id = int(input("Enter student ID to update: "))

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
            return

        print("Press Enter to keep the existing value.")

        student_name = input(
            f"Enter name [{student['student_name']}]: "
        ).strip()

        student_email = input(
            f"Enter email [{student['student_email']}]: "
        ).strip()

        student_course = input(
            f"Enter course [{student['student_course']}]: "
        ).strip()

        student_fee_input = input(
            f"Enter fee [{student['student_fee']}]: "
        ).strip()

        if not student_name:
            student_name = student["student_name"]

        if not student_email:
            student_email = student["student_email"]

        if not student_course:
            student_course = student["student_course"]

        if student_fee_input:
            student_fee = float(student_fee_input)
        else:
            student_fee = student["student_fee"]

        sql = """
            UPDATE students
            SET student_name = %s,
                student_email = %s,
                student_course = %s,
                student_fee = %s
            WHERE student_id = %s
        """

        values = (
            student_name,
            student_email,
            student_course,
            student_fee,
            student_id
        )

        cursor.execute(sql, values)
        connection.commit()

        print("Student updated successfully.")

    except ValueError:
        print("Student ID and fee must contain valid numbers.")

    except Error as error:
        print("Error while updating student:", error)

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# DELETE operation
def delete_student():
    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        student_id = int(input("Enter student ID to delete: "))

        cursor = connection.cursor()

        cursor.execute(
            "SELECT student_name FROM students WHERE student_id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
            return

        confirmation = input(
            f"Are you sure you want to delete {student[0]}? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("Delete operation cancelled.")
            return

        sql = "DELETE FROM students WHERE student_id = %s"

        cursor.execute(sql, (student_id,))
        connection.commit()

        print("Student deleted successfully.")

    except ValueError:
        print("Student ID must be a number.")

    except Error as error:
        print("Error while deleting student:", error)

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


def display_menu():
    print("\n================================")
    print(" Student Management System")
    print("================================")
    print("1. Add Student")
    print("2. View All Students")
    print("3. View Student by ID")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")
    print("================================")


def main():
    create_table()

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_all_students()

        elif choice == "3":
            view_student_by_id()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Thank you for using Student Management System.")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 6.")


main()