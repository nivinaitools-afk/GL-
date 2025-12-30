from typing import Dict

class PsychometricEngine:
    """
    Maps scenario-based question responses to 5D psychometric profile.
    Questions are on a 1-5 scale.
    """
    
    QUESTION_MAPPINGS = {
        "Q1": {"dimension": "decision_style", "weight": 0.3, "invert": False},
        "Q2": {"dimension": "decision_style", "weight": 0.3, "invert": True},
        "Q3": {"dimension": "risk_tolerance", "weight": 0.35, "invert": False},
        "Q4": {"dimension": "risk_tolerance", "weight": 0.35, "invert": False},
        "Q5": {"dimension": "structure_preference", "weight": 0.3, "invert": False},
        "Q6": {"dimension": "structure_preference", "weight": 0.3, "invert": True},
        "Q7": {"dimension": "social_preference", "weight": 0.35, "invert": False},
        "Q8": {"dimension": "social_preference", "weight": 0.35, "invert": False},
        "Q9": {"dimension": "feedback_sensitivity", "weight": 0.3, "invert": False},
        "Q10": {"dimension": "feedback_sensitivity", "weight": 0.3, "invert": True},
        "Q11": {"dimension": "decision_style", "weight": 0.4, "invert": False},
        "Q12": {"dimension": "risk_tolerance", "weight": 0.3, "invert": True},
    }
    
    @staticmethod
    def normalize_response(value: int, invert: bool = False) -> float:
        """Normalize 1-5 response to 0-1 scale."""
        normalized = (value - 1) / 4.0
        if invert:
            normalized = 1.0 - normalized
        return normalized
    
    @staticmethod
    def calculate_profile(responses: Dict[str, int]) -> Dict[str, float]:
        """
        Calculate psychometric profile from responses.
        
        Args:
            responses: Dict of question IDs to responses (1-5 scale)
            
        Returns:
            Dict of dimension names to normalized scores (0-1 scale)
        """
        dimension_scores = {
            "decision_style": [],
            "risk_tolerance": [],
            "structure_preference": [],
            "social_preference": [],
            "feedback_sensitivity": [],
        }
        
        for question_id, response in responses.items():
            if question_id in PsychometricEngine.QUESTION_MAPPINGS:
                mapping = PsychometricEngine.QUESTION_MAPPINGS[question_id]
                dimension = mapping["dimension"]
                weight = mapping["weight"]
                invert = mapping["invert"]
                
                normalized = PsychometricEngine.normalize_response(response, invert)
                dimension_scores[dimension].append(normalized * weight)
        
        profile = {}
        for dimension, scores in dimension_scores.items():
            if scores:
                total_weight = sum([
                    PsychometricEngine.QUESTION_MAPPINGS[q]["weight"]
                    for q in responses.keys()
                    if q in PsychometricEngine.QUESTION_MAPPINGS 
                    and PsychometricEngine.QUESTION_MAPPINGS[q]["dimension"] == dimension
                ])
                profile[dimension] = sum(scores) / total_weight if total_weight > 0 else 0.5
            else:
                profile[dimension] = 0.5
        
        return profile
