from fastapi import Depends, FastAPI
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


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students