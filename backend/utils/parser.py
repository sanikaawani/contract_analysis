import io
import re
import PyPDF2
import docx

def parse_document(file_bytes: bytes, filename: str) -> str:
    """
    Extract text content from uploaded files (.pdf, .docx, .txt).
    """
    filename_lower = filename.lower()
    extracted_text = ""
    
    if filename_lower.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for page in pdf_reader.pages:
            t = page.extract_text()
            if t:
                pages_text.append(t)
        extracted_text = "\n\n".join(pages_text)
        
    elif filename_lower.endswith('.docx'):
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        extracted_text = "\n\n".join(paragraphs)
        
    elif filename_lower.endswith('.txt'):
        try:
            extracted_text = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            extracted_text = file_bytes.decode('latin-1', errors='ignore')
            
    else:
        # Fallback text decoding
        try:
            extracted_text = file_bytes.decode('utf-8')
        except Exception:
            extracted_text = str(file_bytes)

    # Clean redundant whitespace while keeping paragraph / clause splits
    cleaned_text = re.sub(r'\r\n', '\n', extracted_text)
    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    return cleaned_text.strip()
