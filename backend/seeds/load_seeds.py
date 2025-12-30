import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.database.config import SessionLocal, engine, Base
from app.database.models import Tenant, Skill, Course, RoleCluster, SkillRelationship

def load_seeds():
    """Load seed data into database."""
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Creating default tenant...")
        tenant = Tenant(
            name="University of Example",
            country="UK",
            branding_config={"primary_color": "#003366", "logo_url": ""}
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        print(f"✓ Created tenant: {tenant.name} (ID: {tenant.id})")
        
        print("\nLoading skills...")
        with open(os.path.join(os.path.dirname(__file__), 'skills.json'), 'r') as f:
            skills_data = json.load(f)
        
        skill_map = {}
        for skill_data in skills_data:
            skill = Skill(
                tenant_id=tenant.id,
                name=skill_data['name'],
                category=skill_data['category'],
                description=skill_data.get('description', '')
            )
            db.add(skill)
            skill_map[skill_data['name']] = skill
        
        db.commit()
        print(f"✓ Loaded {len(skills_data)} skills")
        
        print("\nLoading courses...")
        with open(os.path.join(os.path.dirname(__file__), 'courses.json'), 'r') as f:
            courses_data = json.load(f)
        
        for course_data in courses_data:
            course = Course(
                tenant_id=tenant.id,
                name=course_data['name'],
                course_code=course_data['course_code'],
                difficulty_level=course_data['difficulty_level'],
                term_offered=course_data.get('term_offered', ''),
                description=course_data.get('description', ''),
                skills_contributed={}
            )
            db.add(course)
            db.flush()
            
            for skill_name in course_data.get('skills', []):
                if skill_name in skill_map:
                    skill = skill_map[skill_name]
                    db.flush()
                    relationship = SkillRelationship(
                        skill_id=skill.id,
                        course_id=course.id,
                        confidence_level=0.8
                    )
                    db.add(relationship)
        
        db.commit()
        print(f"✓ Loaded {len(courses_data)} courses")
        
        print("\nLoading role clusters...")
        with open(os.path.join(os.path.dirname(__file__), 'role_clusters.json'), 'r') as f:
            roles_data = json.load(f)
        
        for role_data in roles_data:
            role = RoleCluster(
                tenant_id=tenant.id,
                name=role_data['name'],
                description=role_data.get('description', ''),
                skill_weights=role_data.get('skill_weights', {}),
                psychometric_ranges=role_data.get('psychometric_ranges', {}),
                example_careers=role_data.get('example_careers', []),
                typical_pathways=role_data.get('typical_pathways', [])
            )
            db.add(role)
        
        db.commit()
        print(f"✓ Loaded {len(roles_data)} role clusters")
        
        print("\n✅ Seed data loaded successfully!")
        print(f"\nTenant ID: {tenant.id}")
        print(f"Use this tenant_id when creating students and making API requests.")
        
    except Exception as e:
        print(f"\n❌ Error loading seeds: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    load_seeds()
