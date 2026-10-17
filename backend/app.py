import os
import sys
import json
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.nlp.preprocessing import (
    tokenize_sentences, tokenize_words, remove_stopwords,
    apply_porter_stemmer, apply_lancaster_stemmer, compare_stemmers,
    lemmatize_tokens, full_preprocessing_pipeline
)
from backend.nlp.linguistic_analysis import (
    pos_tag_analysis, chunk_text, extract_named_entities,
    expand_synonyms_wordnet, disambiguate_word_sense
)
from backend.nlp.feature_engineering import LegalFeatureExtractor
from backend.risk_engine.risk_analyzer import ContractRiskAnalyzer
from backend.utils.parser import parse_document
from backend.utils.report_generator import generate_pdf_report

DIST_DIR = os.path.join(PROJECT_ROOT, "frontend", "dist")
app = Flask(__name__, static_folder=DIST_DIR if os.path.exists(DIST_DIR) else None, static_url_path="")
CORS(app)

# Initialize core services
risk_analyzer = ContractRiskAnalyzer()
feature_extractor = risk_analyzer.feature_extractor

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "AI Contract Risk Analysis NLP System",
        "version": "1.0.0"
    })

@app.route('/api/samples', methods=['GET'])
def get_sample_contracts():
    """Return preloaded authentic Indian contracts across all 5 contract types."""
    samples_dir = os.path.join(BASE_DIR, "data", "samples")
    sample_files = {
        "Service Agreement": "service_agreement.txt",
        "Vendor Agreement": "vendor_agreement.txt",
        "Employment Agreement": "employment_agreement.txt",
        "Non-Disclosure Agreement (NDA)": "nda_agreement.txt",
        "Supply Agreement": "supply_agreement.txt"
    }
    
    samples = []
    for c_type, filename in sample_files.items():
        filepath = os.path.join(samples_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            samples.append({
                "contract_type": c_type,
                "filename": filename,
                "title": f"Sample {c_type}",
                "text": content
            })
            
    return jsonify(samples)

@app.route('/api/analyze', methods=['POST'])
def analyze_contract_endpoint():
    """Analyze contract text from raw string or uploaded PDF/DOCX/TXT file."""
    try:
        contract_title = "Uploaded Contract"
        contract_type = "Auto-Detect"
        full_text = ""
        
        if 'file' in request.files:
            file = request.files['file']
            contract_title = request.form.get('contract_title', file.filename)
            contract_type = request.form.get('contract_type', 'Auto-Detect')
            file_bytes = file.read()
            full_text = parse_document(file_bytes, file.filename)
        else:
            data = request.get_json(force=True) if request.is_json else request.form
            full_text = data.get('text', '')
            contract_title = data.get('contract_title', 'Manual Input Contract')
            contract_type = data.get('contract_type', 'Auto-Detect')
            
        if not full_text or not full_text.strip():
            return jsonify({"error": "No contract text or file provided"}), 400
            
        # Execute hybrid AI analysis
        results = risk_analyzer.analyze_contract(
            full_text=full_text,
            contract_title=contract_title,
            contract_type=contract_type
        )
        
        # Include full raw text for UI inspection
        results["raw_text"] = full_text
        return jsonify(results)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/nlp-experiment', methods=['POST'])
def run_nlp_experiment():
    """
    Dedicated interactive laboratory running individual or combined NLP experiments
    on custom input text.
    """
    try:
        data = request.get_json(force=True)
        text = data.get('text', '').strip()
        technique = data.get('technique', 'all')
        query_word = data.get('query_word', '')
        
        if not text:
            return jsonify({"error": "Empty text provided"}), 400
            
        sentences = tokenize_sentences(text)
        sample_s = sentences[0] if sentences else text
        words = tokenize_words(sample_s)
        stop_res = remove_stopwords(words)
        filtered_words = stop_res["filtered_tokens"]
        
        result = {}
        
        # 1. Tokenization
        if technique in ['all', 'tokenization']:
            result['tokenization'] = {
                "sentences": sentences,
                "sentence_count": len(sentences),
                "words": words,
                "word_count": len(words)
            }
            
        # 2. Stopwords
        if technique in ['all', 'stopwords']:
            result['stopwords'] = stop_res
            
        # 3 & 4. Porter vs Lancaster Stemmers
        if technique in ['all', 'stemming']:
            result['stemming'] = {
                "porter": apply_porter_stemmer(filtered_words),
                "lancaster": apply_lancaster_stemmer(filtered_words),
                "comparison": compare_stemmers(filtered_words)
            }
            
        # 5. Lemmatization
        if technique in ['all', 'lemmatization']:
            result['lemmatization'] = lemmatize_tokens(filtered_words)
            
        # 6. POS Tagging
        if technique in ['all', 'pos_tagging']:
            result['pos_tagging'] = pos_tag_analysis(sample_s)
            
        # 7. Chunking
        if technique in ['all', 'chunking']:
            result['chunking'] = chunk_text(sample_s)
            
        # 8. NER
        if technique in ['all', 'ner']:
            result['ner'] = extract_named_entities(text)
            
        # 9. Bag of Words
        if technique in ['all', 'bow']:
            result['bow'] = feature_extractor.extract_bow(text)
            
        # 10. N-Grams
        if technique in ['all', 'ngrams']:
            result['ngrams'] = {
                "unigrams": feature_extractor.extract_ngrams(text, n=1, top_k=10),
                "bigrams": feature_extractor.extract_ngrams(text, n=2, top_k=10),
                "trigrams": feature_extractor.extract_ngrams(text, n=3, top_k=8)
            }
            
        # 11. WordNet Synonym Expansion
        if technique in ['all', 'synonyms']:
            target = query_word if query_word else (filtered_words[0] if filtered_words else "liability")
            result['wordnet_expansion'] = expand_synonyms_wordnet(target)
            
        # 12. Word2Vec Similarity
        if technique in ['all', 'word2vec']:
            target = query_word if query_word else "liability"
            result['word2vec'] = {
                "queried_word": target,
                "similar_terms": feature_extractor.find_similar_words_w2v(target, top_n=6),
                "vector_dimension": feature_extractor.w2v_vector_size
            }
            
        # 13. Word Sense Disambiguation (Lesk)
        if technique in ['all', 'wsd']:
            wsd_target = query_word if query_word else "party"
            result['wsd'] = disambiguate_word_sense(sample_s, wsd_target)
            
        return jsonify(result)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/model-metrics', methods=['GET'])
def get_model_metrics():
    """Return academic evaluation metrics and benchmarking comparisons."""
    metrics_path = os.path.join(BASE_DIR, "ml", "saved_models", "model_benchmarks.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "Benchmarks not yet generated. Please train models first."}), 404

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf_endpoint():
    """Generate and stream downloadable PDF risk report."""
    try:
        data = request.get_json(force=True)
        pdf_stream = generate_pdf_report(data)
        return send_file(
            pdf_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"Contract_Risk_Report_{data.get('contract_title', 'Audit').replace(' ', '_')}.pdf"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend_spa(path):
    """Serve the compiled Vite React frontend or fallback to index.html for SPA routing."""
    if path and os.path.exists(os.path.join(DIST_DIR, path)):
        return send_from_directory(DIST_DIR, path)
    index_file = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_file):
        return send_from_directory(DIST_DIR, "index.html")
    return jsonify({
        "status": "online",
        "service": "AI-Based Contract Risk Analysis NLP API",
        "note": "Frontend UI build not found. Run 'npm run build' inside frontend/ to serve the UI here."
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Legal Contract NLP Risk Engine API on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
