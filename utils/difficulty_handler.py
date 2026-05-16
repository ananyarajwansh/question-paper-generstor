import json
import os

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'question_templates.json')

def load_templates():
    """Loads the question templates from the JSON file."""
    try:
        with open(TEMPLATES_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback if file doesn't exist
        return {
            "definition": ["What is {keyword}?"],
            "theory": ["Explain {keyword}."],
            "application": ["What are the applications of {keyword}?"]
        }

def get_templates_by_difficulty(q_type, difficulty):
    """
    Returns templates based on question type and limits/adjusts them by difficulty.
    """
    templates = load_templates()
    type_templates = templates.get(q_type, templates["definition"])
    
    # Simple logic: 
    # Easy uses the first template
    # Medium uses the middle templates
    # Hard uses the last template
    
    num_templates = len(type_templates)
    
    if difficulty == "Easy":
        # Usually direct definitions or basic what/define
        return type_templates[:1] if num_templates > 0 else type_templates
    elif difficulty == "Medium":
        # Explanations or discussions
        if num_templates >= 3:
            return type_templates[1:-1]
        else:
            return type_templates
    elif difficulty == "Hard":
        # Detailed notes, impacts, etc.
        return type_templates[-1:] if num_templates > 0 else type_templates
    
    return type_templates
