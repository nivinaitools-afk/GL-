from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class RoleClusterBase(BaseModel):
    name: str
    description: Optional[str] = None
    skill_weights: Dict[str, float] = {}
    psychometric_ranges: Dict[str, List[float]] = {}
    example_careers: List[str] = []
    typical_pathways: List[str] = []

class RoleClusterCreate(RoleClusterBase):
    tenant_id: int

class RoleCluster(RoleClusterBase):
    id: int
    tenant_id: int
    
    class Config:
        from_attributes = True

class CareerMatch(BaseModel):
    role_cluster_id: int
    name: str
    description: str
    fit_score: float
    psychometric_fit: float
    skill_readiness: float
    explanation: str
    skill_gaps: List[Dict[str, Any]]
    example_careers: List[str]
