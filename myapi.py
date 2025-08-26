from fastapi import FastAPI, Path
from typing import Optional

app = FastAPI()


students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 12"
    },
    2: {
        "name": "Kurt Cobain",
        "age": 18,
        "class": "year 12"
    },
    3: {
        "name": "Krist Novoselic",
        "age": 16,
        "class": "year 11"
    },
    4: {
        "name": "Dave Grohl",
        "age": 18,
        "class": "year 12"
    }
}

@app.get("/students/")
def index():
    return students#{"name": "First Data"}

@app.get("/students/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0, lt=5)):
    return students[student_id]

@app.get("/students/by-name/")
def get_student_by_name(*, name: Optional[str]=None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}