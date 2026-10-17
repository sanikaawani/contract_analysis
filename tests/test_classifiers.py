"""
Unit tests for ML classifiers, clause detection, and composite risk scoring.
"""

import pytest
from src.risk_engine.clause_detector import detect_contract_clauses, classify_clause_category
from src.risk_engine.risk_classifier import classify_clause_risk
from src.risk_engine.risk_scorer import compute_contract_risk_score
from src.risk_engine.explanation_engine import generate_clause_explanation


def test_classify_clause_category():
    renewal_text = "This agreement shall automatically renew for successive 2 year terms."
    cat, conf = classify_clause_category(renewal_text)
    assert cat == "Automatic Renewal"
    assert conf > 0.5

    liability_text = "Vendor agrees to unlimited liability and holds the client harmless from all damages."
    cat_l, _ = classify_clause_category(liability_text)
    assert cat_l == "Liability Clauses"


def test_classify_clause_risk():
    high_risk_text = "Vendor agrees to unlimited uncapped liability and perpetual indemnity without monetary limit."
    eval_res = classify_clause_risk(high_risk_text)
    assert eval_res['risk_level'] == "High"
    assert eval_res['risk_score'] >= 70

    low_risk_text = "The contract only renews upon mutual written agreement and both parties agree to standard 30-day notice."
    eval_low = classify_clause_risk(low_risk_text)
    assert eval_low['risk_level'] == "Low"
    assert eval_low['risk_score'] <= 35


def test_composite_risk_score():
    sample_clauses = [
        {'clause_category': 'Liability Clauses', 'risk_level': 'High', 'risk_score': 85},
        {'clause_category': 'Automatic Renewal', 'risk_level': 'High', 'risk_score': 85},
        {'clause_category': 'Termination Clauses', 'risk_level': 'High', 'risk_score': 80},
        {'clause_category': 'Payment Terms', 'risk_level': 'Medium', 'risk_score': 55}
    ]
    score_res = compute_contract_risk_score(sample_clauses)
    assert score_res['overall_score'] >= 70
    assert score_res['risk_level'] == "High"
    assert score_res['high_count'] == 3
    assert score_res['total_clauses'] == 4


def test_explanation_and_recommendation():
    exp = generate_clause_explanation('Automatic Renewal', 'High')
    assert "evergreen" in exp['explanation'].lower() or "renew" in exp['explanation'].lower()
    assert "notice" in exp['recommendation'].lower()
