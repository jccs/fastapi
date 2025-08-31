from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
import os
import json

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


def read_file(filepath: str) -> dict[int, dict[str, str | int]]:
    if not os.path.exists(filepath):
        return {}
    
    try:
        with open(filepath, 'r') as file:
            content = file.read().strip()
            if not content:
                return {}
            data = json.loads(content)
    except json.JSONDecodeError:
        return {}

    # Convert keys back to int after loading from JSON
    return {int(k): v for k, v in data.items()}


def write_file(filepath: str, data: dict[str, dict[str, str | int]]):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

filepath = "data/students.json"
students: dict[int, dict[str, str | int]] = read_file(filepath)


@app.get("/students/")
def get_students() -> dict[int, dict[str, str | int]]:
    
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0)) -> dict[str, str | int]:
    
    if student_id not in students:
        return {"Error": f"Couldn't find student with id {student_id}"}
    
    return students[student_id]

@app.get("/students-by-name/")
def get_student_by_name(name: str) -> dict[str, str | int]:
    
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}

@app.post("/students/{student_id}")
def create_student(student_id: int, student: Student):
    
    if student_id in students:
        return {"Error": "Student already exists"}
    
    students[student_id] = student.model_dump()
    
    serializable = {str(k): v for k, v in students.items()}
    write_file(filepath, serializable)

    return students[student_id]

@app.put("/students/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    if student.name != None:
        students[student_id]["name"] = student.name

    if student.age != None:
        students[student_id]["age"] = student.age

    if student.year != None:
        students[student_id]["year"] = student.year

    serializable = {str(k): v for k, v in students.items()}
    write_file(filepath, serializable)

    return students[student_id]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    message = f"{students[student_id]['name']} with id {student_id} has been deleted"
    del students[student_id]

    serializable = {str(k): v for k, v in students.items()}
    write_file(filepath, serializable)

    return {"Message": message}