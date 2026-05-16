import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import re

nlp = spacy.load("en_core_web_sm")

# Words that often get extracted from slides/PDFs but make terrible questions
STOP_KEYWORDS = {
    'contd', 'output', 'input', 'table', 'figure', 'content', 'sets', 
    'page', 'fsa', 'chapter', 'section', 'slide', 'previous', 'next', 'overview'
}

def is_valid_keyword(text):
    """Checks if the keyword passes basic quality rules."""
    text_lower = text.lower()
    
    # Needs to be > 2 chars and shouldn't just be numbers
    if len(text_lower) <= 2 or text_lower.isnumeric():
        return False
        
    # Exclude if it starts with determiners making it redundant
    parts = text_lower.split()
    if not parts: return False
    if parts[0] in {'the', 'a', 'an', 'this', 'that', 'these', 'those', 'some', 'any'}:
        return False
        
    # Exclude common bad slide words
    if any(stop_word in text_lower for stop_word in STOP_KEYWORDS):
        return False
        
    # Exclude keywords that have awkward punctuation floating in them
    if re.search(r'[^\w\s]', text):
        return False
        
    return True

def extract_keywords_spacy(text, top_n=10):
    """
    Extracts keywords based on noun chunks and important nouns using spaCy.
    """
    doc = nlp(text)
    
    # Extract noun chunks, keeping only high quality multi-word concepts
    noun_chunks = [
        chunk.text.strip().lower() 
        for chunk in doc.noun_chunks 
        if not chunk.root.is_stop and 1 < len(chunk.text.split()) <= 3
    ]
    
    # Extract individual important nouns (fallback)
    nouns = [
        token.text.strip().lower() 
        for token in doc 
        if token.pos_ == "NOUN" and not token.is_stop
    ]
    
    # Combine
    all_candidates = noun_chunks + nouns
    
    # Filter using validity rules
    all_candidates = [cand for cand in all_candidates if is_valid_keyword(cand)]
    
    # Count frequencies
    frequency = Counter(all_candidates)
    
    # Boost noun chunks over single nouns to prioritize "Lexicon Analysis" over "Lexicon"
    for chunk in noun_chunks:
        frequency[chunk] += 1
        
    top_keywords = [item[0] for item in frequency.most_common(top_n)]
    return top_keywords

def extract_keywords_tfidf(sentences, top_n=10):
    """
    Extract keywords using TF-IDF across the sentences of the document.
    """
    if len(sentences) < 3:
        return extract_keywords_spacy(" ".join(sentences), top_n)
        
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    try:
        X = vectorizer.fit_transform(sentences)
        indices = X.sum(axis=0).argsort()[-top_n*2:][::-1] # Extract more to leave room for filtering
        feature_names = vectorizer.get_feature_names_out()
        
        raw_keywords = [feature_names[0, idx] for idx in indices.tolist()[0]]
        
        # Filter raw TFIDF keywords
        valid_keywords = [kw for kw in raw_keywords if is_valid_keyword(kw)]
        
        return valid_keywords[:top_n]
        
    except Exception as e:
        # Fallback to spaCy if TF-IDF fails
        return extract_keywords_spacy(" ".join(sentences), top_n)

def get_keywords(text, method="spacy", num_keywords=10):
    """
    Main entry point for getting keywords.
    """
    from utils.preprocessor import extract_sentences
    sentences = extract_sentences(text)
    
    # If the text was parsed strictly into tiny fragments, reconstruct it for generic parsing
    pure_text = " ".join(sentences)
    
    if method == "tfidf":
        return extract_keywords_tfidf(sentences, num_keywords)
    else:
        return extract_keywords_spacy(pure_text, num_keywords)
