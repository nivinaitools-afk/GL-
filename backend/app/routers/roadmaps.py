from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.config import get_db
from ..database.models import (
    Student, RoleCluster, StudentSkill, Skill,
    CareerRoadmap as CareerRoadmapModel
)
from ..schemas.career_roadmap import RoadmapRequest, CareerRoadmap, CareerRoadmapDB
from ..engines.roadmap_generator import RoadmapGenerator
from ..engines.role_matcher import RoleMatcher

router = APIRouter(prefix="/students", tags=["roadmaps"])

@router.post("/{student_id}/roadmap", response_model=CareerRoadmap)
def generate_roadmap(
    student_id: int,
    request: RoadmapRequest,
    db: Session = Depends(get_db)
):
    """Generate a personalized career roadmap."""
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    role_cluster = db.query(RoleCluster).filter(
        RoleCluster.id == request.target_role_cluster_id
    ).first()
    if not role_cluster:
        raise HTTPException(status_code=404, detail="Role cluster not found")
    
    student_skills_query = db.query(StudentSkill, Skill).join(
        Skill, StudentSkill.skill_id == Skill.id
    ).filter(StudentSkill.student_id == student_id).all()
    
    student_skills = {
        skill.name: student_skill.proficiency_level
        for student_skill, skill in student_skills_query
    }
    
    skill_readiness, _ = RoleMatcher.calculate_skill_readiness(
        student_skills,
        role_cluster.skill_weights
    )
    
    current_fit = skill_readiness
    
    skill_gaps = RoadmapGenerator.identify_skill_gaps(
        student_skills,
        role_cluster.skill_weights
    )
    
    term_plan = RoadmapGenerator.recommend_courses(
        db,
        student.tenant_id,
        skill_gaps,
        request.time_horizon_terms
    )
    
    improvement = RoadmapGenerator.calculate_projected_improvement(
        skill_gaps,
        term_plan
    )
    projected_fit = min(1.0, current_fit + improvement)
    
    narrative = RoadmapGenerator.generate_narrative(
        student.name,
        role_cluster.name,
        current_fit,
        projected_fit,
        skill_gaps
    )
    
    roadmap_data = {
        "overall_narrative": narrative,
        "target_role": role_cluster.name,
        "current_fit_score": round(current_fit, 3),
        "projected_fit_score": round(projected_fit, 3),
        "skill_gaps": skill_gaps,
        "term_by_term": term_plan
    }
    
    latest_version = db.query(CareerRoadmapModel).filter(
        CareerRoadmapModel.student_id == student_id
    ).count()
    
    db_roadmap = CareerRoadmapModel(
        student_id=student_id,
        version=latest_version + 1,
        role_cluster_id=role_cluster.id,
        recommendations=roadmap_data
    )
    db.add(db_roadmap)
    db.commit()
    db.refresh(db_roadmap)
    
    return CareerRoadmap(**roadmap_data)

@router.get("/{student_id}/roadmap/{version}", response_model=CareerRoadmap)
def get_roadmap(student_id: int, version: int, db: Session = Depends(get_db)):
    """Retrieve a specific version of a student's roadmap."""
    
    roadmap = db.query(CareerRoadmapModel).filter(
        CareerRoadmapModel.student_id == student_id,
        CareerRoadmapModel.version == version
    ).first()
    
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    return CareerRoadmap(**roadmap.recommendations)

@router.get("/{student_id}/roadmaps", response_model=list[CareerRoadmapDB])
def list_roadmaps(student_id: int, db: Session = Depends(get_db)):
    """List all roadmap versions for a student."""
    
    roadmaps = db.query(CareerRoadmapModel).filter(
        CareerRoadmapModel.student_id == student_id
    ).order_by(CareerRoadmapModel.version.desc()).all()
    
    return roadmaps
