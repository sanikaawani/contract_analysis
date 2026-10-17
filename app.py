"""
Main Flask Web Application & REST API
AI-Based Contract Risk Analysis and Clause Detection System for SMBs using NLP
"""

import os
import sys
import json
import io
from flask import (
    Flask, render_template, request, jsonify, send_file, redirect, url_for, session
)
from werkzeug.utils import secure_filename

# Ensure root is on path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config
from src.extractors import extract_text_from_file, clean_contract_text
from src.nlp import (
    inspect_text_nlp,
    expand_wordnet_synonyms,
    disambiguate_word_sense,
    extract_named_entities
)
from src.risk_engine import (
    detect_contract_clauses,
    classify_clause_risk,
    compute_contract_risk_score,
    generate_clause_explanation,
    generate_contract_recommendations
)
from src.reports import generate_pdf_report
from models.benchmark import get_benchmark_data

app = Flask(__name__)
app.config.from_object(Config)

# Ensure essential directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_DIR'], exist_ok=True)
os.makedirs(app.config['SAMPLE_CONTRACTS_DIR'], exist_ok=True)


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ==========================================
# Frontend HTML Page Routes
# ==========================================

@app.route('/')
def index():
    """Home landing page with system overview and SMB value proposition."""
    return render_template('index.html')


@app.route('/upload')
def upload_page():
    """Upload & Sample Contract selector page."""
    return render_template('upload.html', contract_types=Config.CONTRACT_TYPES)


@app.route('/analysis')
def analysis_page():
    """Interactive Contract Risk Analysis Dashboard."""
    return render_template('analysis.html')


@app.route('/nlp-lab')
def nlp_lab_page():
    """Live 13-Technique NLP Playground & Inspector."""
    return render_template('nlp_lab.html')


@app.route('/benchmarks')
def benchmarks_page():
    """ML Model Benchmark & Evaluation page."""
    return render_template('benchmarks.html')


@app.route('/about')
def about_page():
    """System Architecture, UML Diagrams, ER Schema & Viva FAQ."""
    return render_template('about.html')


# ==========================================
# REST API Endpoints
# ==========================================

@app.route('/api/samples', methods=['GET'])
def list_samples():
    """Returns available sample Indian contracts."""
    sample_files = [
        {
            'id': 'service_agreement.txt',
            'name': 'Master Service Agreement',
            'type': 'Service Agreement',
            'description': 'High-risk IT services contract with evergreen auto-renewal, uncapped liability, and 24-hr termination.',
            'risk_preview': 'High Risk (Evergreen, Uncapped Indemnity)'
        },
        {
            'id': 'vendor_agreement.txt',
            'name': 'Commercial Vendor Agreement',
            'type': 'Vendor Agreement',
            'description': 'Balanced manufacturing component supply agreement with Net 45 terms and liability capped at 1x contract value.',
            'risk_preview': 'Moderate Risk (Capped Liabilities)'
        },
        {
            'id': 'employment_agreement.txt',
            'name': 'Executive Employment Agreement',
            'type': 'Employment Agreement',
            'description': 'Employment contract with 2-year post-termination non-compete (Section 27 Indian Contract Act analysis).',
            'risk_preview': 'High Risk (Restraint of Trade)'
        },
        {
            'id': 'nda_agreement.txt',
            'name': 'Mutual Non-Disclosure Agreement',
            'type': 'Non-Disclosure Agreement (NDA)',
            'description': 'Standard mutual 2-year non-disclosure agreement with clear exclusions and reasonable liability caps.',
            'risk_preview': 'Low Risk (Mutual Protections)'
        },
        {
            'id': 'supply_agreement.txt',
            'name': 'Raw Material Supply Agreement',
            'type': 'Supply Agreement',
            'description': 'Low-risk annual commodity supply contract with 90-day bilateral termination and zero liquidated damages.',
            'risk_preview': 'Low Risk (Bilateral Terms)'
        }
    ]
    return jsonify({'samples': sample_files})


@app.route('/api/sample/<filename>', methods=['GET'])
def get_sample_contract(filename):
    """Retrieves text of a specific sample contract."""
    clean_name = secure_filename(filename)
    filepath = os.path.join(app.config['SAMPLE_CONTRACTS_DIR'], clean_name)
    if not os.path.exists(filepath):
        # Fallback to dataset generator if not yet created
        from data.dataset_generator import create_sample_contracts
        create_sample_contracts()

    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({
            'filename': clean_name,
            'content': content
        })
    return jsonify({'error': 'Sample contract not found'}), 404


@app.route('/api/upload', methods=['POST'])
def upload_contract():
    """
    Handles file upload (PDF, DOCX, TXT) and returns extracted text & metadata.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'Unsupported file type. Allowed: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'}), 400

    try:
        filename = secure_filename(file.filename)
        extraction = extract_text_from_file(file, filename=filename)
        return jsonify({
            'success': True,
            'metadata': extraction
        })
    except Exception as e:
        return jsonify({'error': f'Failed to extract text from document: {str(e)}'}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_contract():
    """
    Core Risk Analysis Pipeline:
    1. Extracts/cleans contract text
    2. Runs Clause Detection & Category Classification (8 categories)
    3. Runs Risk Level Classifier (High/Med/Low) & Flags
    4. Computes Composite Risk Score (0-100)
    5. Extracts Named Entities (NER: Org, Person, Date, Money, Duration, Law)
    6. Generates AI Explanations & Actionable Recommendations
    """
    data = request.get_json() or {}
    contract_text = data.get('text', '').strip()
    contract_type = data.get('contract_type', 'Service Agreement')
    model_type = data.get('model_type', 'rf')  # 'rf', 'lr', 'nb'
    filename = data.get('filename', 'contract_document.txt')

    if not contract_text:
        return jsonify({'error': 'No contract text provided for analysis.'}), 400

    try:
        # 1. Clean & compute document metadata
        cleaned_text = clean_contract_text(contract_text)
        words = cleaned_text.split()
        metadata = {
            'filename': filename,
            'contract_type': contract_type,
            'detected_title': data.get('title', 'Commercial Contract'),
            'word_count': len(words),
            'character_count': len(cleaned_text),
            'page_count': max(1, round(len(words) / 350)),
            'reading_time_minutes': max(1, round(len(words) / 200))
        }

        # 2. Clause Detection & Segmentation
        detected_clauses = detect_contract_clauses(cleaned_text, model_type=model_type)

        # 3. Risk Level Classification & AI Explanations for each clause
        analyzed_clauses = []
        for c in detected_clauses:
            cat = c['clause_category']
            risk_eval = classify_clause_risk(c['clause_text'], category=cat)
            risk_level = risk_eval['risk_level']
            
            exp_rec = generate_clause_explanation(cat, risk_level, custom_clause_text=c['clause_text'])
            
            analyzed_clauses.append({
                'id': c['id'],
                'clause_number': c['clause_number'],
                'clause_title': c['clause_title'],
                'clause_text': c['clause_text'],
                'clause_category': cat,
                'category_confidence': c['category_confidence'],
                'risk_level': risk_level,
                'risk_score': risk_eval['risk_score'],
                'risk_confidence': risk_eval['confidence'],
                'flag_reasons': risk_eval['flag_reasons'],
                'explanation': exp_rec['explanation'],
                'recommendation': exp_rec['recommendation']
            })

        # 4. Composite Risk Scoring
        risk_score_summary = compute_contract_risk_score(analyzed_clauses)

        # 5. Extract Named Entities
        entities = extract_named_entities(cleaned_text)

        # 6. Overall SMB Recommendations
        overall_recommendations = generate_contract_recommendations(
            analyzed_clauses, risk_score_summary['overall_score']
        )

        response_payload = {
            'success': True,
            'contract_type': contract_type,
            'metadata': metadata,
            'risk_score': risk_score_summary,
            'clauses': analyzed_clauses,
            'entities': entities,
            'recommendations': overall_recommendations
        }

        return jsonify(response_payload)

    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500


@app.route('/api/nlp-inspect', methods=['POST'])
def nlp_inspect_endpoint():
    """
    Executes all 13 NLP techniques on the given text and returns comprehensive inspection data.
    """
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    keyword = data.get('keyword', 'terminate')

    if not text:
        return jsonify({'error': 'No text provided for NLP inspection.'}), 400

    try:
        inspection_results = inspect_text_nlp(text, target_keyword=keyword)
        return jsonify({'success': True, 'nlp_data': inspection_results})
    except Exception as e:
        return jsonify({'error': f'NLP inspection error: {str(e)}'}), 500


@app.route('/api/models/benchmark', methods=['GET'])
def get_benchmarks():
    """Retrieves ML classification benchmark comparison metrics."""
    try:
        data = get_benchmark_data()
        return jsonify({'success': True, 'benchmarks': data})
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve benchmarks: {str(e)}'}), 500


@app.route('/api/synonyms', methods=['POST'])
def get_synonyms():
    """Technique 11: WordNet Synonym Expansion."""
    data = request.get_json() or {}
    word = data.get('word', 'terminate').strip()
    if not word:
        return jsonify({'error': 'No word provided'}), 400

    syns = expand_wordnet_synonyms(word)
    return jsonify({'success': True, 'synonyms_data': syns})


@app.route('/api/wsd', methods=['POST'])
def get_wsd():
    """Technique 13: Lesk Word Sense Disambiguation."""
    data = request.get_json() or {}
    sentence = data.get('sentence', '').strip()
    word = data.get('word', 'consideration').strip()

    if not sentence or not word:
        return jsonify({'error': 'Sentence and target word are required.'}), 400

    wsd_result = disambiguate_word_sense(sentence, word)
    return jsonify({'success': True, 'wsd_data': wsd_result})


@app.route('/api/report/download', methods=['POST'])
def download_pdf_report():
    """Generates and downloads the PDF risk report."""
    data = request.get_json() or {}
    analysis_data = data.get('analysis_data', {})
    
    if not analysis_data or 'clauses' not in analysis_data:
        return jsonify({'error': 'Invalid analysis data for PDF report generation.'}), 400

    try:
        filename = analysis_data.get('metadata', {}).get('filename', 'contract')
        base_name = os.path.splitext(filename)[0]
        pdf_filename = f"Risk_Report_{base_name}.pdf"
        
        pdf_bytes = generate_pdf_report(analysis_data)
        
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=pdf_filename
        )
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500


if __name__ == '__main__':
    print("Starting AI Legal Contract Risk Analyzer Web Server on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
