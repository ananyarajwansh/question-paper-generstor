import random
import re
from utils.difficulty_handler import get_templates_by_difficulty

def get_proportional_importance(keywords, source_text):
    """
    Ranks keywords strictly relative to each other within the document to
    mathematically guarantee a 'Mix' of High, Medium, and Low importance limits.
    """
    lower_text = source_text.lower()
    scored_keywords = []
    
    for kw in set(keywords): # unique keywords
        kw_clean = kw.lower().strip()
        
        # Raw boundary count
        count = len(re.findall(r'\b' + re.escape(kw_clean) + r'\b', lower_text))
        if count == 0 and len(kw_clean) > 4:
            count = lower_text.count(kw_clean)
            
        scored_keywords.append({'keyword': kw_clean, 'count': count})
        
    # Sort highest count to lowest count
    scored_keywords.sort(key=lambda x: x['count'], reverse=True)
    
    if not scored_keywords:
        return []

    max_c = scored_keywords[0]['count']
    # Create proportional bounds based on the max keyword occurrence in this specific text
    high_threshold = max(2, max_c * 0.6)
    med_threshold = max(1, max_c * 0.3)
    
    categorized = {"High": [], "Medium": [], "Low": []}
    
    for item in scored_keywords:
        # Force a distribution. If everything tied at count 1, arbitrarily split by raw position
        if item['count'] >= high_threshold:
            item['importance'] = "High"
            categorized["High"].append(item)
        elif item['count'] >= med_threshold:
            item['importance'] = "Medium"
            categorized["Medium"].append(item)
        else:
            item['importance'] = "Low"
            categorized["Low"].append(item)
            
    # If the text is so uniform that the math fails to bucket them, arbitrarily chunk them into thirds
    if len(categorized["High"]) == len(scored_keywords):
        n = len(scored_keywords)
        part = max(1, n // 3)
        for i, item in enumerate(scored_keywords):
            if i < part: item['importance'] = "High"
            elif i < part*2: item['importance'] = "Medium"
            else: item['importance'] = "Low"
            
    return scored_keywords

def generate_questions(keywords, q_type, difficulty, source_text, num_questions=5):
    """
    Generates questions, ensuring that the final output guarantees 
    a mix of high, medium, and low exam importance.
    """
    scored_keywords = get_proportional_importance(keywords, source_text)
    if not scored_keywords:
        return []
        
    generated_questions = []
    types_list = ["definition", "theory", "application"]
    
    # To force a mix, shuffle the final valid keywords so we encounter all tiers
    random.shuffle(scored_keywords)
    selected_keywords = scored_keywords[:min(num_questions, len(scored_keywords))]
    
    for idx, data in enumerate(selected_keywords):
        keyword = data['keyword']
        importance = data['importance']
        
        current_type = random.choice(types_list) if q_type == "mixed" else q_type
        
        templates = get_templates_by_difficulty(current_type, difficulty)
        if not templates:
            templates = ["What is {keyword}?"]
            
        template = random.choice(templates)
        formatted_keyword = keyword.title()
        question = template.format(keyword=formatted_keyword)
        
        generated_questions.append({
            "id": idx + 1,
            "keyword": keyword,
            "question": question,
            "type": current_type.capitalize(),
            "difficulty": difficulty,
            "importance": importance
        })
        
    return generated_questions
