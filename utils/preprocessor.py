import spacy
import re

# Load the spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """
    Cleans text aggressively to handle bad PDF extraction.
    Forcefully separates joined words and converts visual breaks to punctuation.
    """
    # Separate joined words (e.g., "parsedOutput" -> "parsed Output")
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Convert bullets, newlines, and tabs into periods to force spaCy to see them as sentence boundaries
    text = re.sub(r'[\n\r\t•▪\-\*]+', '. ', text)
    
    # Remove multiple periods and clean spaces
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_sentences(text):
    """
    Splits the text into sentences using spaCy, ensuring realistic lengths.
    """
    text = clean_text(text)
    doc = nlp(text)
    
    sentences = []
    for sent in doc.sents:
        cleaned_sent = sent.text.strip()
        # Filter out garbage short fragments and massive unbroken blocks (bad PDF tables)
        if 20 < len(cleaned_sent) < 400:
            sentences.append(cleaned_sent)
            
    return sentences

def tokenize_and_lemmatize(text):
    """
    Tokenizes the text, removes stopwords, and lemmatizes the tokens.
    """
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return tokens
