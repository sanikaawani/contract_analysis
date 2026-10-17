"""
Risk Level Classifier Module
Evaluates individual clause risk level (Low, Medium, High) using trained ML models
augmented with a deterministic Indian Legal Risk Rule Engine.
"""

import os
import re
import joblib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'trained')

# Specific high-risk trigger phrases in Indian commercial agreements
HIGH_RISK_TRIGGERS = [
    r'without\s+(?:any\s+)?(?:monetary\s+)?(?:cap|limit|limitation)',
    r'unlimited.*liability|uncapped.*liability',
    r'perpetual.*indemnity|unlimited.*indemnity',
    r'liable\s+for\s+all\s+direct,\s+indirect.*consequential\s+damages',
    r'automatically\s+renew.*successive\s+terms',
    r'evergreen\s+basis',
    r'administrative\s+exit\s+fee',
    r'withhold\s+any\s+payment\s+at\s+its\s+sole\s+discretion',
    r'ninety\s+\(90\)\s+to\s+one\s+hundred\s+twenty\s+\(120\)\s+days',
    r'120\s+days|180\s+days',
    r'penal\s+interest.*24%',
    r'liquidated\s+damages\s+of\s+2%.*each\s+day',
    r'forfeit\s+the\s+entire\s+security\s+deposit',
    r'terminate.*immediately\s+upon\s+24\s+hours',
    r'locked\s+into\s+a\s+mandatory.*term',
    r'refund\s+all\s+fees\s+received\s+during',
    r'survive\s+perpetually\s+and\s+indefinitely',
    r'liquidated\s+damages\s+of\s+inr\s+50,00,000',
    r'not\s+engage\s+in\s+any\s+competing\s+business.*three\s+\(3\)\s+years',
    r'section\s+27\s+of\s+the\s+indian\s+contract\s+act',
    r'pre-existing\s+background\s+code.*sole\s+and\s+exclusive\s+property',
    r'unrestricted\s+right\s+to\s+enter\s+and\s+audit.*without\s+prior\s+notice',
    r'penal\s+interest.*24%|penalty\s+of\s+inr\s+10,00,000'
]

# Medium risk trigger phrases
MEDIUM_RISK_TRIGGERS = [
    r'renew.*unless.*thirty\s+\(30\)\s+days',
    r'aggregate\s+liability.*capped\s+at\s+three\s+times|capped\s+at\s+2x',
    r'liquidated\s+damages.*0\.5%.*capped\s+at\s+10%',
    r'net\s+45\s+days|forty-five\s+\(45\)\s+days',
    r'interest.*12%\s+per\s+annum',
    r'terminate.*sixty\s+\(60\)\s+days',
    r'cure\s+such\s+breach\s+within\s+thirty\s+\(30\)\s+days',
    r'survive\s+for\s+a\s+period\s+of\s+five\s+\(5\)\s+years',
    r'not\s+to\s+solicit.*twelve\s+\(12\)\s+months',
    r'annual\s+audit.*fifteen\s+\(15\)\s+business\s+days'
]

# Low risk trigger phrases
LOW_RISK_TRIGGERS = [
    r'only\s+be\s+renewed\s+upon.*mutual\s+written\s+agreement',
    r'no\s+automatic\s+renewal',
    r'strictly\s+limited\s+to\s+the\s+total\s+fees\s+actually\s+paid',
    r'neither\s+party\s+shall\s+be\s+liable.*consequential',
    r'reasonable\s+cure\s+period\s+of\s+thirty\s+\(30\)\s+days',
    r'net\s+30\s+days|within\s+thirty\s+\(30\)\s+days',
    r'terminate\s+for\s+convenience\s+upon\s+ninety\s+\(90\)\s+days',
    r'remain\s+in\s+effect\s+for.*two\s+\(2\)\s+years',
    r'service\s+provider\s+retains\s+all\s+right.*background',
    r'no\s+non-compete\s+restrictions'
]

_risk_model_cache = None

def get_trained_risk_classifier():
    """Loads and caches the trained Risk Level ML classifier."""
    global _risk_model_cache
    if _risk_model_cache is None:
        model_path = os.path.join(MODELS_DIR, 'risk_level_classifier.joblib')
        vec_path = os.path.join(MODELS_DIR, 'tfidf_vectorizer.joblib')
        if os.path.exists(model_path) and os.path.exists(vec_path):
            try:
                clf = joblib.load(model_path)
                vec = joblib.load(vec_path)
                _risk_model_cache = (clf, vec)
            except Exception:
                _risk_model_cache = (None, None)
        else:
            _risk_model_cache = (None, None)
    return _risk_model_cache


def classify_clause_risk(clause_text: str, category: str = None) -> dict:
    """
    Evaluates clause risk level (High / Medium / Low).
    Returns risk level, numeric score (1-100), flag factors, and confidence.
    """
    text_clean = clause_text.lower()
    flag_reasons = []

    # 1. Evaluate Rule Triggers
    high_matches = [trig for trig in HIGH_RISK_TRIGGERS if re.search(trig, text_clean)]
    med_matches = [trig for trig in MEDIUM_RISK_TRIGGERS if re.search(trig, text_clean)]
    low_matches = [trig for trig in LOW_RISK_TRIGGERS if re.search(trig, text_clean)]

    # 2. ML Classifier Prediction
    clf, vec = get_trained_risk_classifier()
    ml_risk_level = None
    ml_confidence = 0.5

    if clf and vec:
        try:
            from ..nlp.preprocessor import preprocess_text
            proc_text = preprocess_text(clause_text, method='lemmatize')
            X = vec.transform([proc_text])
            probs = clf.predict_proba(X)[0]
            max_idx = probs.argmax()
            ml_risk_level = clf.classes_[max_idx]
            ml_confidence = float(probs[max_idx])
        except Exception:
            pass

    # 3. Decision Logic Combining Rules & ML
    if high_matches or (ml_risk_level == 'High' and ml_confidence > 0.6):
        risk_level = 'High'
        risk_score = 85 if high_matches else 78
        if 'without monetary cap' in text_clean or 'unlimited' in text_clean:
            flag_reasons.append("Uncapped / Unlimited liability exposure with zero liability ceiling.")
        if 'automatic' in text_clean and 'renew' in text_clean:
            flag_reasons.append("Unfavorable evergreen auto-renewal with exit fee or narrow notice window.")
        if '24 hours' in text_clean or 'immediate' in text_clean:
            flag_reasons.append("Unilateral termination for convenience on extremely short notice.")
        if 'liquidated damages' in text_clean or 'forfeit' in text_clean:
            flag_reasons.append("Punitive liquidated damages exceeding fair compensation thresholds.")
        if 'competing business' in text_clean or 'section 27' in text_clean:
            flag_reasons.append("Overly restrictive non-compete clause (void under Section 27 Indian Contract Act).")
        if not flag_reasons:
            flag_reasons.append("Unbalanced contractual obligations heavily favoring the opposing party.")
    elif med_matches or ml_risk_level == 'Medium':
        risk_level = 'Medium'
        risk_score = 55
        flag_reasons.append("Moderate commercial terms requiring careful monitoring and timeline adherence.")
    elif low_matches or ml_risk_level == 'Low':
        risk_level = 'Low'
        risk_score = 20
        flag_reasons.append("Standard balanced terms with bilateral protections and reasonable notice.")
    else:
        # Default fallback
        risk_level = ml_risk_level or 'Medium'
        risk_score = 50
        flag_reasons.append("Standard commercial clause with average market risk profile.")

    return {
        'risk_level': risk_level,
        'risk_score': risk_score,
        'confidence': round(ml_confidence, 2),
        'flag_reasons': flag_reasons
    }
