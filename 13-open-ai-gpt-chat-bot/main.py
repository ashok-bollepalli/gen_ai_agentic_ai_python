from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "Welcome to FAST API"}

@app.get("/course")
def get_course():
    return {
        "course" : "GEN AI & Agentic AI with Python",
        "duration" : "3 Months",
        "trainer" : "Mr. Ashok"
    }

class Student(BaseModel):
    name: str
    email: str
    phno: int

@app.post("/student")
def add_student(student: Student):
    return {
        "message" : "Student added successfully",
        "student_data" : student
    }
