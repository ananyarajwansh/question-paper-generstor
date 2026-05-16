from fpdf import FPDF
from io import BytesIO

class PDFExporter(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Intelligent Question Paper', 0, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def sanitize_text(text):
    """
    Replaces common unsupported unicode characters with their latin-1 equivalents,
    and ignores the rest to prevent FPDFUnicodeEncodingException using Arial/Helvetica.
    """
    if not isinstance(text, str):
        return str(text)
    replacements = {
        '•': '-', '“': '"', '”': '"', '‘': "'", '’': "'", 
        '–': '-', '—': '-', '…': '...'
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def create_pdf(questions):
    """
    Creates a detailed PDF in memory of the generated questions natively tagged with Exam Importance.
    Returns the raw bytes of the PDF.
    """
    pdf = PDFExporter()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Process Questions
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Generated Questions', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)
    
    for q in questions:
        # MultiCell handles text wrapping natively
        txt = f"Q{q['id']}. {q['question']}  (Type: {q['type']}, Difficulty: {q['difficulty']}, Importance: {q['importance']})"
        pdf.multi_cell(0, 8, sanitize_text(txt))
        pdf.ln(4)
        
    import tempfile
    
    # Write the compiled PDF directly to a temporary disk array.
    # This prevents any binary coercion glitches in memory during streaming.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            pdf_bytes = f.read()
            
    return pdf_bytes
