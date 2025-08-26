from fastapi import FastAPI, Path

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