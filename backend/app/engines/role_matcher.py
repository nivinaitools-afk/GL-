from typing import Dict, List, Tuple
import math

class RoleMatcher:
    """
    Matches students to role clusters based on psychometric fit and skill readiness.
    Fit Score = 0.4 * psychometric_fit + 0.6 * skill_readiness
    """
    
    @staticmethod
    def calculate_psychometric_fit(
        student_profile: Dict[str, float],
        role_ranges: Dict[str, List[float]]
    ) -> float:
        """
        Calculate how well student's psychometric profile fits role requirements.
        
        Args:
            student_profile: Dict of dimension names to scores (0-1)
            role_ranges: Dict of dimension names to [min, max] acceptable ranges
            
        Returns:
            Fit score between 0 and 1
        """
        if not role_ranges:
            return 0.5
        
        fits = []
        for dimension, value in student_profile.items():
            if dimension in role_ranges:
                min_val, max_val = role_ranges[dimension]
                
                if min_val <= value <= max_val:
                    center = (min_val + max_val) / 2
                    range_width = max_val - min_val
                    distance_from_center = abs(value - center)
                    fit = 1.0 - (distance_from_center / (range_width / 2)) * 0.3
                    fits.append(fit)
                else:
                    if value < min_val:
                        distance = min_val - value
                    else:
                        distance = value - max_val
                    
                    penalty = min(distance * 2, 1.0)
                    fits.append(max(0.0, 1.0 - penalty))
        
        return sum(fits) / len(fits) if fits else 0.5
    
    @staticmethod
    def calculate_skill_readiness(
        student_skills: Dict[str, float],
        required_skills: Dict[str, float]
    ) -> Tuple[float, List[Dict[str, float]]]:
        """
        Calculate student's skill readiness for a role.
        
        Args:
            student_skills: Dict of skill names to proficiency levels (0-1)
            required_skills: Dict of skill names to required weights (0-1)
            
        Returns:
            Tuple of (readiness_score, skill_gaps)
        """
        if not required_skills:
            return 1.0, []
        
        total_weighted_score = 0.0
        total_weight = 0.0
        skill_gaps = []
        
        for skill_name, required_weight in required_skills.items():
            student_proficiency = student_skills.get(skill_name, 0.0)
            
            contribution = student_proficiency * required_weight
            total_weighted_score += contribution
            total_weight += required_weight
            
            gap = required_weight - student_proficiency
            if gap > 0.1:
                skill_gaps.append({
                    "skill": skill_name,
                    "current": round(student_proficiency, 2),
                    "required": round(required_weight, 2),
                    "gap": round(gap, 2)
                })
        
        readiness = total_weighted_score / total_weight if total_weight > 0 else 0.0
        
        skill_gaps.sort(key=lambda x: x["gap"], reverse=True)
        
        return readiness, skill_gaps
    
    @staticmethod
    def calculate_fit_score(
        psychometric_fit: float,
        skill_readiness: float
    ) -> float:
        """
        Calculate overall fit score.
        
        Args:
            psychometric_fit: Psychometric fit score (0-1)
            skill_readiness: Skill readiness score (0-1)
            
        Returns:
            Overall fit score (0-1)
        """
        return 0.4 * psychometric_fit + 0.6 * skill_readiness
    
    @staticmethod
    def generate_explanation(
        role_name: str,
        psychometric_fit: float,
        skill_readiness: float,
        fit_score: float,
        skill_gaps: List[Dict[str, float]]
    ) -> str:
        """Generate human-readable explanation of match."""
        
        psych_desc = "excellent" if psychometric_fit > 0.8 else "strong" if psychometric_fit > 0.65 else "moderate" if psychometric_fit > 0.5 else "developing"
        skill_desc = "excellent" if skill_readiness > 0.8 else "strong" if skill_readiness > 0.65 else "moderate" if skill_readiness > 0.5 else "developing"
        
        explanation = f"You have a {psych_desc} personality fit ({psychometric_fit:.0%}) and {skill_desc} skill readiness ({skill_readiness:.0%}) for {role_name}. "
        
        if skill_gaps:
            top_gaps = skill_gaps[:3]
            gap_names = [g["skill"] for g in top_gaps]
            explanation += f"Key areas to develop: {', '.join(gap_names)}."
        else:
            explanation += "You meet the skill requirements for this role cluster."
        
        return explanation
