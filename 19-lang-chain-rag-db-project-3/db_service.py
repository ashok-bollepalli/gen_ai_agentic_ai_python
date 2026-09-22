import sqlite3
from pathlib import Path


DB_PATH = Path("data/student.db")


def get_connection():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            course_code TEXT UNIQUE NOT NULL,

            course_name TEXT NOT NULL,

            description TEXT,

            duration TEXT,

            fee REAL,

            eligibility TEXT,

            mode TEXT
        )
    """)

    courses = [

        (
            "PY101",
            "Python Programming",
            "Python programming from beginner to advanced level.",
            "3 Months",
            15000,
            "Basic computer knowledge",
            "Online"
        ),

        (
            "DS101",
            "Data Science",
            "Python, statistics, machine learning and data visualization.",
            "6 Months",
            35000,
            "Basic Python knowledge",
            "Online + Classroom"
        ),

        (
            "AI101",
            "Generative AI",
            "LLMs, RAG, LangChain, vector databases and AI applications.",
            "4 Months",
            30000,
            "Python programming knowledge",
            "Online"
        )
    ]

    for course in courses:

        cursor.execute(
            """
            INSERT OR IGNORE INTO courses
            (
                course_code,
                course_name,
                description,
                duration,
                fee,
                eligibility,
                mode
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            course
        )

    connection.commit()

    connection.close()


def get_all_courses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM courses
        ORDER BY course_name
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def search_courses(keyword):

    connection = get_connection()

    cursor = connection.cursor()

    keyword = f"%{keyword}%"

    cursor.execute(
        """
        SELECT *
        FROM courses

        WHERE course_code LIKE ?
        OR course_name LIKE ?
        OR description LIKE ?
        OR eligibility LIKE ?
        """,
        (
            keyword,
            keyword,
            keyword,
            keyword
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]
