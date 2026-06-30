from sqlalchemy.orm import Session
from app import models
from app.schemas import StudentCreate

def get_students(db: Session):
    return db.query(models.Student).all()


def get_student(db: Session, student_id: int):
    return (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

def create_student(db :Session, student: StudentCreate):
    db_student = models.Student(
        name = student.name,
        age = student.age,
        course = student.course 
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student

def update_student(db: Session, student_id: int, student: StudentCreate):
    db_student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if db_student is None:
        return None

    db_student.name = student.name
    db_student.age = student.age
    db_student.course = student.course

    db.commit()
    db.refresh(db_student)

    return db_student

def delete_student(db : Session , student_id: int):
    db_student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )
    

    if db_student is None:
        return None
    
    db.delete(db_student)
    db.commit()

    return db_student