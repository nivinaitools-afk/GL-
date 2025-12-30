from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.config import get_db
from ..database.models import RoleCluster, Skill, Course
from pydantic import BaseModel

router = APIRouter(tags=["reference-data"])

class RoleClusterResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    example_careers: List[str]
    
    class Config:
        from_attributes = True

class SkillResponse(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str]
    
    class Config:
        from_attributes = True

class CourseResponse(BaseModel):
    id: int
    name: str
    course_code: str
    difficulty_level: float
    term_offered: Optional[str]
    description: Optional[str]
    
    class Config:
        from_attributes = True

@router.get("/role-clusters", response_model=List[RoleClusterResponse])
def list_role_clusters(
    tenant_id: int = Query(..., description="Tenant ID"),
    db: Session = Depends(get_db)
):
    """List all role clusters for a tenant."""
    
    clusters = db.query(RoleCluster).filter(
        RoleCluster.tenant_id == tenant_id
    ).all()
    return clusters

@router.get("/skills", response_model=List[SkillResponse])
def list_skills(
    tenant_id: int = Query(..., description="Tenant ID"),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all skills for a tenant."""
    
    query = db.query(Skill).filter(Skill.tenant_id == tenant_id)
    if category:
        query = query.filter(Skill.category == category)
    
    skills = query.all()
    return skills

@router.get("/courses", response_model=List[CourseResponse])
def list_courses(
    tenant_id: int = Query(..., description="Tenant ID"),
    db: Session = Depends(get_db)
):
    """List all courses for a tenant."""
    
    courses = db.query(Course).filter(Course.tenant_id == tenant_id).all()
    return courses

@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "GetLanded Career Intelligence API"}
