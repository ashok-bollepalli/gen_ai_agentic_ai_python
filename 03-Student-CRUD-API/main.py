from fastapi import FastAPI
from pydantic import BaseModel, Field

import db

app = FastAPI()

base_path = "/api"

# Runs once when the application starts
@app.on_event("startup")
def m1():
    db.create_table()

class Student(BaseModel):
    name: str = Field(..., min_length=3, max_length=15)
    course: str = Field(..., min_length=3, max_length=15)
    fee : float = Field(..., gt=0)

@app.post(f"{base_path}/student", status_code=201)
def create_student(student: Student):
    return db.create_student(student)

@app.get(f"{base_path}/students")
def get_all_students():
    return db.get_students()

@app.get(f"{base_path}/students/{{student_id}}")
def get_student_by_id(student_id: int):
    return db.get_student_by_id(student_id)