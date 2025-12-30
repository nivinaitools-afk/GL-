from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    branding_config = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    students = relationship("Student", back_populates="tenant")
    skills = relationship("Skill", back_populates="tenant")
    role_clusters = relationship("RoleCluster", back_populates="tenant")
    courses = relationship("Course", back_populates="tenant")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    university = Column(String)
    graduation_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="students")
    psychometric_profile = relationship("PsychometricProfile", back_populates="student", uselist=False)
    student_skills = relationship("StudentSkill", back_populates="student")
    career_roadmaps = relationship("CareerRoadmap", back_populates="student")

class PsychometricProfile(Base):
    __tablename__ = "psychometric_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, unique=True)
    decision_style = Column(Float, nullable=False)
    risk_tolerance = Column(Float, nullable=False)
    structure_preference = Column(Float, nullable=False)
    social_preference = Column(Float, nullable=False)
    feedback_sensitivity = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = relationship("Student", back_populates="psychometric_profile")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text)
    
    tenant = relationship("Tenant", back_populates="skills")
    skill_relationships = relationship("SkillRelationship", back_populates="skill")
    student_skills = relationship("StudentSkill", back_populates="skill")

class RoleCluster(Base):
    __tablename__ = "role_clusters"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    skill_weights = Column(JSON, default={})
    psychometric_ranges = Column(JSON, default={})
    example_careers = Column(JSON, default=[])
    typical_pathways = Column(JSON, default=[])
    
    tenant = relationship("Tenant", back_populates="role_clusters")
    career_roadmaps = relationship("CareerRoadmap", back_populates="role_cluster")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    course_code = Column(String, nullable=False)
    skills_contributed = Column(JSON, default={})
    difficulty_level = Column(Float, default=0.5)
    term_offered = Column(String)
    description = Column(Text)
    
    tenant = relationship("Tenant", back_populates="courses")
    skill_relationships = relationship("SkillRelationship", back_populates="course")

class SkillRelationship(Base):
    __tablename__ = "skill_relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    confidence_level = Column(Float, default=0.5)
    
    skill = relationship("Skill", back_populates="skill_relationships")
    course = relationship("Course", back_populates="skill_relationships")

class StudentSkill(Base):
    __tablename__ = "student_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency_level = Column(Float, default=0.0)
    source = Column(String, default="inferred")
    
    student = relationship("Student", back_populates="student_skills")
    skill = relationship("Skill", back_populates="student_skills")

class CareerRoadmap(Base):
    __tablename__ = "career_roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    version = Column(Integer, default=1)
    role_cluster_id = Column(Integer, ForeignKey("role_clusters.id"), nullable=False)
    recommendations = Column(JSON, default={})
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="career_roadmaps")
    role_cluster = relationship("RoleCluster", back_populates="career_roadmaps")
