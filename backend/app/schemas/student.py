from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    university: Optional[str] = None
    graduation_year: Optional[int] = None

class StudentCreate(StudentBase):
    tenant_id: int

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None

class Student(StudentBase):
    id: int
    tenant_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
