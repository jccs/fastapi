from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


students = {
    1: {
        "name": "John",
        "age": 17,
        "year": "year 12"
    },
    2: {
        "name": "Kurt Cobain",
        "age": 18,
        "year": "year 12"
    },
    3: {
        "name": "Krist Novoselic",
        "age": 16,
        "year": "year 11"
    },
    4: {
        "name": "Dave Grohl",
        "age": 18,
        "year": "year 12"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/students/")
def index():
    return students #{"name": "First Data"}

@app.get("/students/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0)):

    if student_id not in students:
        return {"Error": f"Couldn't find student with id {student_id}"}
    
    return students[student_id]

@app.get("/students-by-name/{student_id}")
def get_student_by_name(*, student_id: int, name: Optional[str]=None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}

@app.post("/students/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/students/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    if student.name != None:
        students[student_id].name = student.name

    if student.age != None:
        students[student_id].age = student.age

    if student.year != None:
        students[student_id].year = student.year

    return students[student_id]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    del students[student_id]
    return {"Message": "Student deleted successfully"}