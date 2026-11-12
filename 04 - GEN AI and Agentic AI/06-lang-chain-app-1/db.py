import sqlite3

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

llm = ChatOllama(model="llama3.2")

def get_course_from_db(input):
    course_name = input["course"]

    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT course_name, duration, fees FROM courses WHERE course_name = ?",
        (course_name,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "course_name": row[0],
            "duration": row[1],
            "fees": row[2]
        }

    return {
        "course_name": course_name,
        "duration": "Not found",
        "fees": "Not found"
    }

prompt = ChatPromptTemplate.from_template(
    """
    Course Name: {course_name}
    Duration: {duration}
    Fees: {fees}

    Explain this course information to a student.
    """
)

chain = RunnableLambda(get_course_from_db) | prompt | llm | StrOutputParser()

response = chain.invoke({
    "course": "Gen AI"
})

print(response)