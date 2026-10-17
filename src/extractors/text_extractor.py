"""
Text Extraction Module for Legal Contracts.
Supports PDF (PyPDF2), DOCX (python-docx), and TXT formats with robust error handling
and text cleaning for Indian and international legal agreements.
"""

import os
import re
import io
import PyPDF2
from docx import Document


def clean_contract_text(raw_text: str) -> str:
    """
    Cleans raw contract text:
    - Normalizes unicode characters (quotes, dashes, non-breaking spaces)
    - Strips recurring header/footer artifacts
    - Normalizes paragraph and clause line breaks
    - Preserves legal numbering (e.g., 1.1, Clause 4(a), Section 2)
    """
    if not raw_text:
        return ""

    # Replace smart quotes and dashes
    text = raw_text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2013', '-').replace('\u2014', '--')
    text = text.replace('\u00a0', ' ').replace('\ufeff', '')
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove repeated page numbers like "Page 1 of 5", "--- Page 2 ---"
    text = re.sub(r'(?i)page\s+\d+\s+(?:of\s+\d+)?', '', text)
    text = re.sub(r'[-=]{3,}\s*page\s*\d+\s*[-=]{3,}', '', text)

    # Collapse multiple blank lines into two
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Collapse multiple inline spaces into one
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
    cleaned = '\n'.join(lines).strip()

    return cleaned


def extract_from_txt(file_bytes: bytes) -> str:
    """Extracts text from raw TXT bytes using multi-encoding fallbacks."""
    for enc in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
        try:
            return file_bytes.decode(enc)
        except UnicodeDecodeError:
            continue
    return file_bytes.decode('utf-8', errors='ignore')


def extract_from_pdf(file_bytes: bytes) -> tuple[str, int]:
    """Extracts text from PDF bytes using PyPDF2."""
    pdf_file = io.BytesIO(file_bytes)
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    text_chunks = []

    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text_chunks.append(page_text)

    full_text = "\n\n".join(text_chunks)
    return full_text, num_pages


def extract_from_docx(file_bytes: bytes) -> tuple[str, int]:
    """Extracts text from DOCX bytes using python-docx."""
    docx_file = io.BytesIO(file_bytes)
    doc = Document(docx_file)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    
    # Also extract any tables
    table_texts = []
    for table in doc.tables:
        for row in table.rows:
            row_text = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
            if row_text:
                table_texts.append(row_text)

    full_text = "\n\n".join(paragraphs + table_texts)
    return full_text, len(paragraphs)


def extract_text_from_file(file_storage_or_path, filename: str = None) -> dict:
    """
    Unified extraction entrypoint.
    Accepts a Werkzeug FileStorage object, file path string, or bytes buffer.
    Returns a dictionary with raw text, cleaned text, and metadata.
    """
    if isinstance(file_storage_or_path, str):
        filepath = file_storage_or_path
        filename = filename or os.path.basename(filepath)
        with open(filepath, 'rb') as f:
            file_bytes = f.read()
    elif hasattr(file_storage_or_path, 'read'):
        filename = filename or getattr(file_storage_or_path, 'filename', 'unknown_document.txt')
        file_bytes = file_storage_or_path.read()
    else:
        file_bytes = bytes(file_storage_or_path)
        filename = filename or 'document.txt'

    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'txt'
    page_count = 1

    if ext == 'pdf':
        raw_text, page_count = extract_from_pdf(file_bytes)
    elif ext in ['docx', 'doc']:
        raw_text, page_count = extract_from_docx(file_bytes)
    else:
        raw_text = extract_from_txt(file_bytes)
        page_count = max(1, len(raw_text.split('\n\n')))

    cleaned_text = clean_contract_text(raw_text)
    words = cleaned_text.split()
    word_count = len(words)
    char_count = len(cleaned_text)
    est_reading_time_mins = max(1, round(word_count / 200))

    # Detect contract title / header
    first_lines = [l.strip() for l in cleaned_text.split('\n') if l.strip()][:5]
    detected_title = first_lines[0] if first_lines else "Contract Document"
    for line in first_lines:
        if any(term in line.upper() for term in ['AGREEMENT', 'CONTRACT', 'NDA', 'STATEMENT OF WORK', 'MOU']):
            detected_title = line
            break

    return {
        'filename': filename,
        'file_extension': ext,
        'raw_text': raw_text,
        'cleaned_text': cleaned_text,
        'detected_title': detected_title,
        'page_count': page_count,
        'word_count': word_count,
        'character_count': char_count,
        'reading_time_minutes': est_reading_time_mins
    }
