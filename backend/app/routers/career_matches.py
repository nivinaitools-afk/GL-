from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.config import get_db
from ..database.models import (
    Student, PsychometricProfile, RoleCluster, 
    StudentSkill, Skill
)
from ..schemas.role_cluster import CareerMatch
from ..engines.role_matcher import RoleMatcher

router = APIRouter(prefix="/students", tags=["career-matches"])

@router.get("/{student_id}/career-matches", response_model=List[CareerMatch])
def get_career_matches(student_id: int, db: Session = Depends(get_db)):
    """Get ranked career matches for a student."""
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    psychometric = db.query(PsychometricProfile).filter(
        PsychometricProfile.student_id == student_id
    ).first()
    
    if not psychometric:
        raise HTTPException(
            status_code=400, 
            detail="Student must complete psychometric assessment first"
        )
    
    psychometric_profile = {
        "decision_style": psychometric.decision_style,
        "risk_tolerance": psychometric.risk_tolerance,
        "structure_preference": psychometric.structure_preference,
        "social_preference": psychometric.social_preference,
        "feedback_sensitivity": psychometric.feedback_sensitivity,
    }
    
    student_skills_query = db.query(StudentSkill, Skill).join(
        Skill, StudentSkill.skill_id == Skill.id
    ).filter(StudentSkill.student_id == student_id).all()
    
    student_skills = {
        skill.name: student_skill.proficiency_level
        for student_skill, skill in student_skills_query
    }
    
    role_clusters = db.query(RoleCluster).filter(
        RoleCluster.tenant_id == student.tenant_id
    ).all()
    
    matches = []
    for role in role_clusters:
        psychometric_fit = RoleMatcher.calculate_psychometric_fit(
            psychometric_profile,
            role.psychometric_ranges
        )
        
        skill_readiness, skill_gaps = RoleMatcher.calculate_skill_readiness(
            student_skills,
            role.skill_weights
        )
        
        fit_score = RoleMatcher.calculate_fit_score(psychometric_fit, skill_readiness)
        
        explanation = RoleMatcher.generate_explanation(
            role.name,
            psychometric_fit,
            skill_readiness,
            fit_score,
            skill_gaps
        )
        
        matches.append(CareerMatch(
            role_cluster_id=role.id,
            name=role.name,
            description=role.description or "",
            fit_score=round(fit_score, 3),
            psychometric_fit=round(psychometric_fit, 3),
            skill_readiness=round(skill_readiness, 3),
            explanation=explanation,
            skill_gaps=skill_gaps,
            example_careers=role.example_careers or []
        ))
    
    matches.sort(key=lambda x: x.fit_score, reverse=True)
    
    return matches
