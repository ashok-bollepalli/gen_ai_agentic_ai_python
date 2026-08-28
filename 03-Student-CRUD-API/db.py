import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pydb"
    )

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS STUDENTS(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            NAME VARCHAR(100) NOT NULL,
            COURSE VARCHAR(100) NOT NULL,
            FEE DECIMAL(10,2) NOT NULL
        )
    """
    cursor.execute(query)
    cursor.close()
    connection.close()
    print("Student Table is Ready....")

def create_student(student):

    conn = get_connection()
    cursor = conn.cursor()
    query  = "INSERT INTO STUDENTS(name, course, fee) values(%s, %s, %s)"
    cursor.execute(query, (student.name, student.course, student.fee))

    conn.commit()
    cursor.close()
    conn.close()
    return {
        "success" : True,
        "Message": "Student Created",
        "data" : student
    }

def get_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "select * from STUDENTS"

    cursor.execute(query)
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "success": True,
        "Message": "Student fetched successfully",
        "data": students
    }

def get_student_by_id(id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "select * from STUDENTS where ID = %s"
    cursor.execute(query, (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if student:
        return {
            "success": True,
            "message": "Student found",
            "data": student
        }

    else:
        return {
            "success": False,
            "message": "Student not found",
            "data": None
        }


















