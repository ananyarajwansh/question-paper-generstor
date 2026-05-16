import re
from collections import Counter

def calculate_importance(keyword, input_text):
    """
    Measures how often a concept/keyword appears throughout the total text 
    to gauge its 'Exam Importance' weight (Low, Medium, High).
    """
    if not input_text or not keyword:
        return "Medium"
        
    lower_text = input_text.lower()
    
    # Simple unigram/bigram token count simulation
    kw = keyword.lower().strip()
    word_count = len(lower_text.split())
    if word_count == 0:
        return "Medium"
        
    # Strictly boundary check to avoid counting "net" inside "network"
    occurrences = len(re.findall(r'\b' + re.escape(kw) + r'\b', lower_text))
    
    # If boundaries fail (usually due to bad PDF gluing), only use explicit count
    # if the keyword is extremely distinct (length > 4) to prevent substring overlap explosions.
    if occurrences == 0 and len(kw) > 4:
         occurrences = lower_text.count(kw)
         
    effective_word_count = max(word_count, 350) 
    
    frequency = (occurrences / effective_word_count) * 1000 
    
    # Extremely strict distribution mapping 
    if occurrences <= 1 or frequency <= 5.0:
        return "Low"
    elif occurrences >= 5 or frequency > 15.0:
        return "High"
    else:
        return "Medium"
