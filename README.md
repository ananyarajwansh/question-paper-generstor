# Intelligent Question Paper Generator 🧠📝

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

An enterprise-grade, NLP-based application that automatically synthesizes context-aware examination questions from raw study materials and PDF documents. 

Built with an elegant, glassmorphic UI, it mathematically evaluates keywords and text density to guarantee a balanced mix of High, Medium, and Low exam-importance questions.

---

## ✨ Key Features

- **Automated NLP Synthesis**: Uses `spaCy` and TF-IDF to extract the most relevant core concepts from unstructured text.
- **Dynamic Importance Scoring**: A localized statistical density algorithm categorizes topics by their frequency to guarantee a mix of High, Medium, and Low importance questions.
- **PDF & Text Ingestion**: Seamlessly upload study materials via PDF or paste raw text.
- **Robust PDF Export**: Generates beautifully formatted question papers on-the-fly. Bypasses standard browser download interruptions via raw base64 data URIs.
- **Modern UI/UX**: Premium animated gradient backgrounds, glassmorphism cards, and interactive hover states for a state-of-the-art feel.
- **Customizable Taxonomy**: Control the volume, difficulty (Easy/Medium/Hard), and question type (Definition/Theory/Application/Mixed).

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/ananyarajwansh/question-paper-generstor.git
cd question-paper-generstor
```

### 2. Install Dependencies
Ensure you have Python 3.8+ installed, then install the required packages:
```bash
pip install -r requirements.txt
```

*(Note: The application uses spaCy's `en_core_web_sm` model. It will be downloaded automatically by the preprocessor if not found).*

### 3. Run the Application
Launch the Streamlit server:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (with injected CSS for animations and styling)
- **Backend/Logic**: Python
- **Natural Language Processing**: spaCy, scikit-learn (TF-IDF), NLTK 
- **Document Handling**: PyPDF2 (Reading), fpdf2 (Writing)
- **Data Manipulation**: Pandas

---

## 📂 Project Structure
```
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Project dependencies
├── utils/
│   ├── difficulty_handler.py   # Manages question templates across difficulty tiers
│   ├── importance_scorer.py    # Baseline scoring logic
│   ├── keyword_extractor.py    # spaCy and TF-IDF extraction logic
│   ├── pdf_exporter.py         # fpdf2 generation and byte streaming
│   ├── preprocessor.py         # Text cleaning and model downloading
│   └── question_generator.py   # Core synthesis and distribution logic
```

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
