from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.config import get_db
from ..database.models import Student, PsychometricProfile as PsychometricProfileModel
from ..schemas.psychometric import PsychometricResponses, PsychometricProfile, PsychometricProfileDB
from ..engines.psychometric_engine import PsychometricEngine

router = APIRouter(prefix="/students", tags=["psychometrics"])

@router.post("/{student_id}/psychometrics", response_model=PsychometricProfile)
def submit_psychometric_assessment(
    student_id: int,
    responses: PsychometricResponses,
    db: Session = Depends(get_db)
):
    """Submit psychometric assessment responses and generate profile."""
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    profile_data = PsychometricEngine.calculate_profile(responses.responses)
    
    existing_profile = db.query(PsychometricProfileModel).filter(
        PsychometricProfileModel.student_id == student_id
    ).first()
    
    if existing_profile:
        for key, value in profile_data.items():
            setattr(existing_profile, key, value)
        db.commit()
        db.refresh(existing_profile)
        return PsychometricProfile(**profile_data)
    else:
        db_profile = PsychometricProfileModel(
            tenant_id=student.tenant_id,
            student_id=student_id,
            **profile_data
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return PsychometricProfile(**profile_data)

@router.get("/{student_id}/psychometrics", response_model=PsychometricProfileDB)
def get_psychometric_profile(student_id: int, db: Session = Depends(get_db)):
    """Get student's psychometric profile."""
    
    profile = db.query(PsychometricProfileModel).filter(
        PsychometricProfileModel.student_id == student_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Psychometric profile not found")
    
    return profile
