from typing import Dict, List, Any
from sqlalchemy.orm import Session
from ..database.models import Course, Skill, SkillRelationship

class RoadmapGenerator:
    """
    Generates personalized career roadmaps with course recommendations.
    """
    
    @staticmethod
    def identify_skill_gaps(
        student_skills: Dict[str, float],
        required_skills: Dict[str, float],
        threshold: float = 0.15
    ) -> List[Dict[str, Any]]:
        """Identify skills that need development."""
        gaps = []
        
        for skill_name, required_level in required_skills.items():
            current_level = student_skills.get(skill_name, 0.0)
            gap = required_level - current_level
            
            if gap > threshold:
                gaps.append({
                    "skill": skill_name,
                    "current": round(current_level, 2),
                    "required": round(required_level, 2),
                    "gap": round(gap, 2),
                    "priority": "high" if gap > 0.5 else "medium" if gap > 0.3 else "low"
                })
        
        gaps.sort(key=lambda x: x["gap"], reverse=True)
        return gaps
    
    @staticmethod
    def recommend_courses(
        db: Session,
        tenant_id: int,
        skill_gaps: List[Dict[str, Any]],
        time_horizon_terms: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Recommend courses to fill skill gaps.
        
        Returns list of terms with recommended courses.
        """
        skill_names = [gap["skill"] for gap in skill_gaps]
        
        skills = db.query(Skill).filter(
            Skill.tenant_id == tenant_id,
            Skill.name.in_(skill_names)
        ).all()
        
        skill_id_map = {skill.name: skill.id for skill in skills}
        
        course_skill_contributions = {}
        for gap in skill_gaps:
            skill_name = gap["skill"]
            skill_id = skill_id_map.get(skill_name)
            
            if not skill_id:
                continue
            
            relationships = db.query(SkillRelationship, Course).join(
                Course, SkillRelationship.course_id == Course.id
            ).filter(
                SkillRelationship.skill_id == skill_id,
                Course.tenant_id == tenant_id
            ).all()
            
            for rel, course in relationships:
                if course.id not in course_skill_contributions:
                    course_skill_contributions[course.id] = {
                        "course": course,
                        "skills_addressed": [],
                        "total_value": 0.0
                    }
                
                course_skill_contributions[course.id]["skills_addressed"].append({
                    "skill": skill_name,
                    "contribution": rel.confidence_level,
                    "gap": gap["gap"]
                })
                course_skill_contributions[course.id]["total_value"] += gap["gap"] * rel.confidence_level
        
        ranked_courses = sorted(
            course_skill_contributions.values(),
            key=lambda x: x["total_value"],
            reverse=True
        )
        
        term_plan = []
        courses_per_term = 3
        
        for term in range(1, time_horizon_terms + 1):
            start_idx = (term - 1) * courses_per_term
            end_idx = start_idx + courses_per_term
            term_courses = ranked_courses[start_idx:end_idx]
            
            if not term_courses:
                break
            
            term_recommendations = []
            focus_areas = set()
            
            for course_data in term_courses:
                course = course_data["course"]
                skills = course_data["skills_addressed"]
                
                term_recommendations.append({
                    "course_code": course.course_code,
                    "course_name": course.name,
                    "skills_developed": [s["skill"] for s in skills],
                    "impact": round(course_data["total_value"], 2),
                    "difficulty": course.difficulty_level
                })
                
                focus_areas.update([s["skill"] for s in skills])
            
            term_plan.append({
                "term": term,
                "courses": term_recommendations,
                "focus_areas": list(focus_areas),
                "rationale": RoadmapGenerator._generate_term_rationale(term, list(focus_areas))
            })
        
        return term_plan
    
    @staticmethod
    def _generate_term_rationale(term: int, focus_areas: List[str]) -> str:
        """Generate explanation for term recommendations."""
        if term == 1:
            return f"Build foundational skills in {', '.join(focus_areas[:2])} to establish a strong base."
        elif term == 2:
            return f"Deepen expertise in {', '.join(focus_areas[:2])} while maintaining momentum."
        elif term == 3:
            return f"Advance to intermediate-level competencies in {', '.join(focus_areas[:2])}."
        else:
            return f"Consolidate learning and specialize in {', '.join(focus_areas[:2])}."
    
    @staticmethod
    def calculate_projected_improvement(
        skill_gaps: List[Dict[str, Any]],
        term_plan: List[Dict[str, Any]]
    ) -> float:
        """Estimate skill improvement from following the roadmap."""
        if not skill_gaps:
            return 0.0
        
        total_gap = sum(gap["gap"] for gap in skill_gaps)
        
        addressed_skills = set()
        for term in term_plan:
            addressed_skills.update(term["focus_areas"])
        
        addressed_gap = sum(
            gap["gap"] for gap in skill_gaps 
            if gap["skill"] in addressed_skills
        )
        
        improvement_rate = 0.7
        return (addressed_gap / total_gap) * improvement_rate if total_gap > 0 else 0.0
    
    @staticmethod
    def generate_narrative(
        student_name: str,
        role_name: str,
        current_fit: float,
        projected_fit: float,
        skill_gaps: List[Dict[str, Any]]
    ) -> str:
        """Generate overall roadmap narrative."""
        
        narrative = f"Based on your profile, you're currently at {current_fit:.0%} fit for {role_name}. "
        
        if current_fit > 0.7:
            narrative += "You're already well-positioned for this career path. "
        elif current_fit > 0.5:
            narrative += "You have a solid foundation to build upon. "
        else:
            narrative += "There's significant opportunity for growth. "
        
        if skill_gaps:
            top_gaps = [gap["skill"] for gap in skill_gaps[:3]]
            narrative += f"Your primary focus areas are: {', '.join(top_gaps)}. "
        
        improvement = projected_fit - current_fit
        if improvement > 0:
            narrative += f"Following this roadmap can increase your fit to {projected_fit:.0%}, "
            narrative += f"a {improvement:.0%} improvement over {len(skill_gaps)} key skill areas."
        
        return narrative
