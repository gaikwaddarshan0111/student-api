from fastapi import Depends, FastAPI , HTTPException
from sqlalchemy.orm import Session
from app.schemas import StudentResponse, StudentCreate
from app.database import Base, engine
from app.connection import get_db
from app.schemas import StudentCreate
from app import models
from app.routers import students

app = FastAPI()
app.include_router(students.router)

# Create all tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Student API!"
    }

"""
@app.get("/students", response_model = list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students
    
@app.get("/students/{student_id}", response_model = StudentResponse)
def get_student(student_id : int , db : Session = Depends(get_db)):
    students = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if students is None:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    return students
    """


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