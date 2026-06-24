from fastapi import Depends, FastAPI , HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.connection import get_db
from app.schemas import StudentCreate
from app import models

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Student API!"
    }


@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    db_student = models.Student(
        name=student.name,
        age=student.age,
        course=student.course
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return {
        "message": "Student created successfully!",
        "student": db_student
    }


@app.get("/students/{student_id}")
def get_students(student_id: int ,db: Session = Depends(get_db)):
    student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int ,student: StudentCreate, db: Session = Depends(get_db)):
    db_student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )
    if db_student is None:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    
    db_student.name = student.name
    db_student.age = student.age
    db_student.course = student.course

    db.commit()
    db.refresh(db_student)

    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student =(

        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if db_student is None:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    db.delete(db_student)
    db.commit()

    return {
        "message" : "Student deleted successfully!"
    }