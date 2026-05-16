import streamlit as st
import pandas as pd
import PyPDF2

from utils.keyword_extractor import get_keywords
from utils.question_generator import generate_questions
from utils.pdf_exporter import create_pdf

st.set_page_config(page_title="Intelligent Question Paper Generator", layout="wide")

# Inject Custom CSS for modernized look
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        font-family: 'Inter', 'Roboto', sans-serif;
        background: radial-gradient(circle at top, #636B2F 0%, #3D4127 100%);
    }
    
    /* Hide standard Streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Keyframes for animations */
    @keyframes slideUpFade {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Card styling with hover and animation */
    .question-card {
        background: rgba(61, 65, 39, 0.7); /* #3D4127 */
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(186, 192, 149, 0.2); /* #BAC095 */
        margin-bottom: 20px;
        transition: all 0.3s ease;
        animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .question-card:hover {
        transform: translateY(-4px);
        border-color: rgba(212, 222, 149, 0.6); /* #D4DE95 */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        background: rgba(61, 65, 39, 0.9);
    }
    
    .question-title {
        color: #F8FAFC;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 8px;
        letter-spacing: 0.2px;
    }
    
    .question-meta {
        color: #BAC095;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Formatting Importance Tags natively */
    .importance-badge-High {
        background-color: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #ef4444;    
    }
    .importance-badge-Medium {
        background-color: rgba(245, 158, 11, 0.2);
        color: #fcd34d;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #f59e0b;    
    }
    .importance-badge-Low {
        background-color: rgba(16, 185, 129, 0.2);
        color: #6ee7b7;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #10b981;    
    }
    

    hr {
        border-color: rgba(212, 222, 149, 0.15); /* #D4DE95 */
        margin: 32px 0;
    }
    
    /* Header centering wrapper */
    .main-header-container {
        text-align: center;
        margin-bottom: 3rem;
        margin-top: 1rem;
    }
    
    /* Animated Gradient Title */
    .gradient-title {
        background: linear-gradient(-45deg, #BAC095, #D4DE95, #ffffff, #BAC095);
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    .header-subtitle {
        color: #BAC095;
        font-size: 1.15rem;
        font-weight: 400;
    }
    
    h2, h3 {
        color: #F8FAFC;
        font-weight: 600;
    }
    
    .stButton>button {
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s ease;
        border: 1px solid #BAC095 !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(212, 222, 149, 0.2);
    }
    
    /* Base64 Download Anchor Styling */
    .b64-btn {
        display: inline-block;
        width: 100%;
        text-align: center;
        background-color: transparent;
        color: #F8FAFC !important;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        border: 1px solid #BAC095;
        text-decoration: none;
        margin-top: 5px;
    }
    .b64-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(212, 222, 149, 0.2);
        border-color: #D4DE95;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def main():
    # Centered Header Section
    st.markdown("""
    <div class='main-header-container'>
        <div class='gradient-title'>Intelligent Question Paper Generator</div>
        <div class='header-subtitle'>Automated, context-aware examination synthesis using Natural Language Processing.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout wrapper
    col_input, col_config = st.columns([1.5, 1], gap="large")
    
    with col_input:
        st.markdown("### Source Material", unsafe_allow_html=True)
        
        input_tabs = st.tabs(["Text Input", "PDF Upload"])
        
        input_text = ""
        with input_tabs[0]:
            text_input = st.text_area("Source content", height=250, label_visibility="collapsed", placeholder="Paste study material, notes, or paragraphs here...")
            if text_input:
                input_text = text_input
                
        with input_tabs[1]:
            uploaded_file = st.file_uploader("Upload Document", type="pdf", label_visibility="collapsed")
            if uploaded_file is not None:
                with st.spinner("Processing document..."):
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    input_text = pdf_text
                    st.success("Document processed successfully.")
                    with st.expander("Review Processed Text"):
                        st.write(input_text[:1000] + "..." if len(input_text) > 1000 else input_text)
                    
    with col_config:
        st.markdown("### Synthesis Configuration", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True) # visual spacing
        
        difficulty = st.selectbox("Difficulty Profile", ["Easy", "Medium", "Hard"])
        question_type = st.selectbox("Question Taxonomy", ["Definition", "Theory", "Application", "Mixed"])
        num_questions = st.number_input("Volume of Questions", min_value=1, max_value=20, value=5)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        generate_btn = st.button("Generate Questions", type="primary", use_container_width=True)
        
    st.markdown("<hr>", unsafe_allow_html=True)

    # Core Generation Logic
    if generate_btn:
        if not input_text.strip():
            st.error("Source material is required to generate questions. Please provide text or an uploaded document.")
            return
            
        with st.spinner("Synthesizing questions via NLP pipeline..."):
            type_lower = question_type.lower()
            method = "tfidf" if type_lower in ["theory", "application", "mixed"] else "spacy"
            
            keywords = get_keywords(input_text, method=method, num_keywords=num_questions + 5)
            
            # Pass source_text directly into question_generator to compute importance against the document
            questions = generate_questions(keywords, type_lower, difficulty, input_text, num_questions=num_questions)
            
            if not questions:
                st.warning("Insufficient keyword fidelity for question generation. Provide a more detailed source material.")
                return
                
            st.session_state['generated_questions'] = questions
            st.session_state['pdf_needs_update'] = True
            
    # Output Display
    if 'generated_questions' in st.session_state:
        st.markdown("### Output Generation", unsafe_allow_html=True)
        
        header_actions_col1, header_actions_col2 = st.columns([3, 1], gap="small")
        
        # Generate the PDF payload natively and cache it to prevent Streamlit download interruption
        if 'pdf_bytes' not in st.session_state or st.session_state.get('pdf_needs_update', False):
            st.session_state['pdf_bytes'] = create_pdf(st.session_state['generated_questions'])
            st.session_state['pdf_needs_update'] = False
            
        with header_actions_col2:
            import base64
            # Bypass Streamlit strictly by generating a raw browser-level Data URI string
            b64_pdf = base64.b64encode(st.session_state['pdf_bytes']).decode('utf-8')
            href = f'''<a href="data:application/pdf;base64,{b64_pdf}" download="question_paper.pdf" class="b64-btn">Download PDF</a>'''
            st.markdown(href, unsafe_allow_html=True)
            
        # Display the questions as cards
        st.markdown("<br>", unsafe_allow_html=True)
        for idx, row in pd.DataFrame(st.session_state['generated_questions']).iterrows():
            importance = row['importance']
            
            card_html = f'''<div class="question-card">
<div class="question-title">Q{row['id']}. {row['question']}</div>
<div class="question-meta">Taxonomy: {row['type']} &nbsp;|&nbsp; Profile: {row['difficulty']} &nbsp;|&nbsp; Exam Importance: <span class="importance-badge-{importance}">{importance}</span></div>
</div>
'''
            st.markdown(card_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
