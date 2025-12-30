from typing import Dict, List

def format_psychometric_explanation(profile: Dict[str, float]) -> Dict[str, str]:
    """Generate human-readable explanations for psychometric dimensions."""
    
    explanations = {}
    
    decision_style = profile.get("decision_style", 0.5)
    if decision_style > 0.7:
        explanations["decision_style"] = "You prefer analytical, data-driven decision making"
    elif decision_style > 0.4:
        explanations["decision_style"] = "You balance intuition and analysis in decisions"
    else:
        explanations["decision_style"] = "You tend to rely on intuition and gut feelings"
    
    risk_tolerance = profile.get("risk_tolerance", 0.5)
    if risk_tolerance > 0.7:
        explanations["risk_tolerance"] = "You're comfortable with uncertainty and taking calculated risks"
    elif risk_tolerance > 0.4:
        explanations["risk_tolerance"] = "You balance risk and stability"
    else:
        explanations["risk_tolerance"] = "You prefer stable, predictable environments"
    
    structure_preference = profile.get("structure_preference", 0.5)
    if structure_preference > 0.7:
        explanations["structure_preference"] = "You thrive with clear processes and structure"
    elif structure_preference > 0.4:
        explanations["structure_preference"] = "You adapt to both structured and flexible environments"
    else:
        explanations["structure_preference"] = "You prefer flexibility and autonomy"
    
    social_preference = profile.get("social_preference", 0.5)
    if social_preference > 0.7:
        explanations["social_preference"] = "You excel in collaborative, team-oriented roles"
    elif social_preference > 0.4:
        explanations["social_preference"] = "You work well independently and in teams"
    else:
        explanations["social_preference"] = "You prefer independent, focused work"
    
    feedback_sensitivity = profile.get("feedback_sensitivity", 0.5)
    if feedback_sensitivity > 0.7:
        explanations["feedback_sensitivity"] = "You actively seek and incorporate feedback"
    elif feedback_sensitivity > 0.4:
        explanations["feedback_sensitivity"] = "You appreciate constructive feedback when needed"
    else:
        explanations["feedback_sensitivity"] = "You prefer self-directed growth and evaluation"
    
    return explanations

def format_skill_gap_explanation(gaps: List[Dict[str, float]]) -> str:
    """Format skill gaps into readable explanation."""
    
    if not gaps:
        return "You meet all the key skill requirements for this role."
    
    high_priority = [g for g in gaps if g.get("priority") == "high"]
    medium_priority = [g for g in gaps if g.get("priority") == "medium"]
    
    explanation = ""
    
    if high_priority:
        skills = [g["skill"] for g in high_priority[:3]]
        explanation += f"High priority skills to develop: {', '.join(skills)}. "
    
    if medium_priority:
        skills = [g["skill"] for g in medium_priority[:2]]
        explanation += f"Secondary focus areas: {', '.join(skills)}."
    
    return explanation.strip()
