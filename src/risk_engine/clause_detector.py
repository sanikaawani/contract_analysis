"""
Clause Detection & Segmentation Module
Segments contract text into distinct operative clauses and classifies them
into 8 Risk Categories using trained ML models with rule-based fallback.
"""

import os
import re
import joblib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'trained')

# Domain keyword hints for the 8 Risk Categories
CATEGORY_KEYWORDS = {
    'Automatic Renewal': ['automatic renewal', 'renew automatically', 'evergreen', 'successive terms', 'extension', 'roll over', 'renewal date'],
    'Payment Terms': ['payment', 'invoices', 'net 30', 'net 45', 'net 60', 'net 90', 'net 120', 'withhold', 'gst', 'tds', 'remittance', 'disbursement', 'compensation'],
    'Liability Clauses': ['liability', 'indemnify', 'indemnification', 'hold harmless', 'consequential damages', 'loss of profits', 'indirect damages', 'uncapped', 'aggregate liability'],
    'Penalty Clauses': ['liquidated damages', 'penalty', 'forfeit', 'forfeiture', 'security deposit', 'bank guarantee', 'sla credit', 'interest rate 24%', 'downtime'],
    'Termination Clauses': ['terminate', 'termination', 'notice period', 'termination for convenience', 'material breach', 'cure period', 'without cause', 'wind-down', 'lock-in'],
    'Confidentiality Clauses': ['confidential', 'confidentiality', 'non-disclosure', 'trade secret', 'proprietary information', 'perpetual', 'ex-parte injunction', 'nda'],
    'Non-Compete Clauses': ['non-compete', 'compete', 'competing business', 'solicit', 'non-solicitation', 'section 27', 'restraint of trade', 'restrictive covenant'],
    'Restrictive Clauses': ['work made for hire', 'intellectual property', 'assignment of ip', 'background ip', 'audit', 'premises', 'negative covenant', 'brand usage', 'marketing']
}

_model_cache = {}

def get_trained_classifier(model_name: str = 'clause_classifier_rf.joblib'):
    """Loads and caches the trained ML classifier and TF-IDF vectorizer."""
    global _model_cache
    if model_name not in _model_cache:
        model_path = os.path.join(MODELS_DIR, model_name)
        vec_path = os.path.join(MODELS_DIR, 'tfidf_vectorizer.joblib')
        
        if os.path.exists(model_path) and os.path.exists(vec_path):
            try:
                clf = joblib.load(model_path)
                vec = joblib.load(vec_path)
                _model_cache[model_name] = (clf, vec)
            except Exception:
                _model_cache[model_name] = (None, None)
        else:
            _model_cache[model_name] = (None, None)
            
    return _model_cache[model_name]


def segment_contract_into_clauses(text: str) -> list[dict]:
    """
    Segments contract text into individual operative clauses.
    Preserves heading titles, paragraph numbers, and text content.
    """
    if not text:
        return []

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    clauses = []
    current_clause_num = 1
    current_title = "General Clause"
    current_text_lines = []

    # Regex patterns for clause headers
    # e.g., "1. SCOPE OF SERVICES", "Section 4. Termination", "CLAUSE 5:", "ARTICLE III"
    header_pattern = re.compile(
        r'^(?:(?:\d+\.|\d+\.\d+|Section\s+\d+|Clause\s+\d+|ARTICLE\s+[IVXLCDM\d]+)\s*[:.-]?\s*([A-Z\s,/&-]{3,50})|([A-Z\s]{4,40}:?$))'
    )

    for line in lines:
        header_match = header_pattern.match(line)
        if header_match and len(line) < 80 and not line.endswith(('.', ',')):
            # If we had a previous clause accumulated, save it
            if current_text_lines:
                clause_body = " ".join(current_text_lines).strip()
                if len(clause_body) > 25:
                    clauses.append({
                        'clause_number': f"Clause {current_clause_num}",
                        'clause_title': current_title,
                        'clause_text': clause_body
                    })
                    current_clause_num += 1
                current_text_lines = []

            current_title = line
        else:
            current_text_lines.append(line)

    # Add final accumulating clause
    if current_text_lines:
        clause_body = " ".join(current_text_lines).strip()
        if len(clause_body) > 25:
            clauses.append({
                'clause_number': f"Clause {current_clause_num}",
                'clause_title': current_title,
                'clause_text': clause_body
            })

    # If document had no explicit numbered headers, segment by paragraphs / sentences
    if len(clauses) <= 1 and text:
        from ..nlp.preprocessor import tokenize_sentences
        sentences = tokenize_sentences(text)
        
        chunk = []
        c_idx = 1
        for s in sentences:
            chunk.append(s)
            if len(" ".join(chunk)) > 150:
                clauses.append({
                    'clause_number': f"Section {c_idx}",
                    'clause_title': f"Contract Provision {c_idx}",
                    'clause_text': " ".join(chunk)
                })
                c_idx += 1
                chunk = []
        if chunk:
            clauses.append({
                'clause_number': f"Section {c_idx}",
                'clause_title': f"Contract Provision {c_idx}",
                'clause_text': " ".join(chunk)
            })

    return clauses


def classify_clause_category(clause_text: str, model_type: str = 'rf') -> tuple[str, float]:
    """
    Classifies a clause text into one of the 8 Risk Categories.
    Combines ML prediction with keyword heuristic boosting.
    """
    from ..nlp.preprocessor import preprocess_text
    
    clean_text = preprocess_text(clause_text, method='lemmatize')
    model_filename = f'clause_classifier_{model_type}.joblib'
    clf, vec = get_trained_classifier(model_filename)

    ml_predicted_category = None
    confidence = 0.5

    if clf and vec:
        try:
            X = vec.transform([clean_text])
            probs = clf.predict_proba(X)[0]
            max_idx = probs.argmax()
            ml_predicted_category = clf.classes_[max_idx]
            confidence = float(probs[max_idx])
        except Exception:
            pass

    # Keyword rule-based verification / scoring
    text_lower = clause_text.lower()
    keyword_scores = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in text_lower)
        if score > 0:
            keyword_scores[cat] = score

    if keyword_scores:
        top_keyword_category = max(keyword_scores, key=keyword_scores.get)
        # If ML is uncertain (<0.45) or agrees, boost confidence
        if not ml_predicted_category or confidence < 0.45:
            return top_keyword_category, round(max(0.65, confidence), 2)
        elif top_keyword_category == ml_predicted_category:
            return ml_predicted_category, round(min(0.98, confidence + 0.15), 2)

    return ml_predicted_category or 'Restrictive Clauses', round(confidence, 2)


def detect_contract_clauses(contract_text: str, model_type: str = 'rf') -> list[dict]:
    """
    Main detection pipeline:
    1. Segments contract into clauses
    2. Identifies clause category
    3. Returns enriched clause records
    """
    raw_clauses = segment_contract_into_clauses(contract_text)
    detected = []

    for idx, c in enumerate(raw_clauses):
        cat, conf = classify_clause_category(c['clause_text'], model_type=model_type)
        detected.append({
            'id': idx + 1,
            'clause_number': c['clause_number'],
            'clause_title': c['clause_title'],
            'clause_text': c['clause_text'],
            'clause_category': cat,
            'category_confidence': conf
        })

    return detected
