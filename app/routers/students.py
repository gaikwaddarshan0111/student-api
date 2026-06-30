from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.connection import get_db
from app.schemas import StudentCreate, StudentResponse

router = APIRouter(
    prefix="/students",
    tags=["students"]
)

@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@router.get("/{student_id}",response_model = StudentResponse)
def get_student(
    student_id : int,
    db: Session = Depends(get_db)):
    student = crud.get_student(db , student_id)

    if student is None:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    return student


@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(db, student)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id : int , student: StudentCreate, db: Session = Depends(get_db)):
    update_student = crud.update_student(db, student_id, student)

    if update_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    return update_student


@router.delete("/{student_id}")
def delete_student(student_id: int, db:Session = Depends(get_db)):
    
    delete_student = crud.delete_student(db , student_id)
    

    if delete_student is None:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
  
    return {"message": "Student deleted successfully!"}