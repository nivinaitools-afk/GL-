from pydantic import BaseModel, Field
from typing import Dict
from datetime import datetime

class PsychometricResponses(BaseModel):
    responses: Dict[str, int] = Field(..., description="Question responses (1-5 scale)")

class PsychometricProfile(BaseModel):
    decision_style: float = Field(..., ge=0.0, le=1.0)
    risk_tolerance: float = Field(..., ge=0.0, le=1.0)
    structure_preference: float = Field(..., ge=0.0, le=1.0)
    social_preference: float = Field(..., ge=0.0, le=1.0)
    feedback_sensitivity: float = Field(..., ge=0.0, le=1.0)

class PsychometricProfileDB(PsychometricProfile):
    id: int
    tenant_id: int
    student_id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True
