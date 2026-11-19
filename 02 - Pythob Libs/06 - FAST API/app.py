from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from courses import courses

app = FastAPI()

@app.get("/courses")
def get_course():
  return courses

@app.get("/courses/{course_id}")
def get_course(course_id: int):
   course = courses.get(course_id)
   if course is None:
       raise HTTPException(
           status_code=404,
           detail="Course not found"
       )
   return course

@app.get("/course-search")
def search_course(search: str):
    result  = []
    for course_id, course in courses.items():
        if search.lower() in course["course_name"].lower():
            result.append({
                "course_id": course_id,
                **course
            })
    return result


class Course(BaseModel):
    course_id: int
    course_name: str
    course_price: int

@app.post("/course", status_code=201)
def create_course(course: Course):
    # logic to insert data into db
    return {
        "message" : "Course created",
        "course" : course
    }
