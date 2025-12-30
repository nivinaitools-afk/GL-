from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.config import get_db
from ..database.models import Student as StudentModel
from ..schemas.student import Student, StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])

@router.post("", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student."""
    
    existing = db.query(StudentModel).filter(StudentModel.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_student = StudentModel(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get student by ID."""
    
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, update: StudentUpdate, db: Session = Depends(get_db)):
    """Update student information."""
    
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    
    db.commit()
    db.refresh(student)
    return student

@router.get("", response_model=List[Student])
def list_students(tenant_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List students, optionally filtered by tenant."""
    
    query = db.query(StudentModel)
    if tenant_id:
        query = query.filter(StudentModel.tenant_id == tenant_id)
    
    students = query.offset(skip).limit(limit).all()
    return students
