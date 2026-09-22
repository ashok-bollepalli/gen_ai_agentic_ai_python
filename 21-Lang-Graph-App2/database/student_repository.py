import sqlite3
from config.settings import DB_NAME


def find_student(student_id):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    data = cur.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )

    return data.fetchone()