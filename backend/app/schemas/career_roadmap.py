from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class RoadmapRequest(BaseModel):
    target_role_cluster_id: int
    time_horizon_terms: int = 4

class TermRecommendation(BaseModel):
    term: int
    courses: List[Dict[str, Any]]
    focus_areas: List[str]
    rationale: str

class CareerRoadmap(BaseModel):
    overall_narrative: str
    target_role: str
    current_fit_score: float
    projected_fit_score: float
    skill_gaps: List[Dict[str, Any]]
    term_by_term: List[TermRecommendation]

class CareerRoadmapDB(BaseModel):
    id: int
    student_id: int
    version: int
    role_cluster_id: int
    recommendations: Dict
    generated_at: datetime
    
    class Config:
        from_attributes = True
