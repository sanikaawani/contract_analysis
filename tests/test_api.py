"""
Integration tests for Flask API Endpoints.
"""

import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_and_pages_status(client):
    assert client.get('/').status_code == 200
    assert client.get('/upload').status_code == 200
    assert client.get('/analysis').status_code == 200
    assert client.get('/nlp-lab').status_code == 200
    assert client.get('/benchmarks').status_code == 200
    assert client.get('/about').status_code == 200


def test_api_samples(client):
    res = client.get('/api/samples')
    assert res.status_code == 200
    data = res.get_json()
    assert 'samples' in data
    assert len(data['samples']) == 5


def test_api_analyze(client):
    payload = {
        'text': '1. PAYMENT TERMS\nClient shall pay in 90 to 120 days. Client may withhold payment.\n2. RENEWAL\nAutomatically renews every 2 years.',
        'contract_type': 'Service Agreement',
        'model_type': 'rf',
        'filename': 'test_contract.txt'
    }
    res = client.post('/api/analyze', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'risk_score' in data
    assert len(data['clauses']) >= 1
    assert 'entities' in data
    assert len(data['recommendations']) > 0


def test_api_nlp_inspect(client):
    payload = {
        'text': 'The Service Provider shall indemnify and hold harmless the Client against all losses without cap under Indian law.',
        'keyword': 'indemnify'
    }
    res = client.post('/api/nlp-inspect', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'nlp_data' in data
    assert 'technique_1_tokenization' in data['nlp_data']
    assert 'technique_8_ner' in data['nlp_data']


def test_api_benchmarks(client):
    res = client.get('/api/models/benchmark')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'benchmarks' in data


def test_api_pdf_report_download(client):
    analysis_payload = {
        'analysis_data': {
            'contract_type': 'Service Agreement',
            'metadata': {'filename': 'test_service.txt', 'detected_title': 'Service Agreement', 'word_count': 120, 'page_count': 1},
            'risk_score': {'overall_score': 82, 'risk_level': 'High', 'recommendation_headline': 'High risk detected', 'total_clauses': 2, 'high_count': 2, 'medium_count': 0, 'low_count': 0, 'risk_percentage_breakdown': {'High': 100, 'Medium': 0, 'Low': 0}},
            'entities': {'organizations': ['Alpha Tech Pvt Ltd'], 'persons': ['Vikram Verma'], 'dates': ['15 Jan 2026'], 'money_amounts': ['INR 5,00,000'], 'durations': ['2 years'], 'governing_acts': ['Indian Contract Act, 1872']},
            'clauses': [
                {'clause_number': 'Clause 1', 'clause_title': 'Liability', 'clause_category': 'Liability Clauses', 'risk_level': 'High', 'risk_score': 85, 'clause_text': 'Unlimited uncapped liability on vendor.', 'explanation': 'Uncapped exposure.', 'recommendation': 'Add 12-month fee cap.'}
            ],
            'recommendations': ['Add a liability cap equal to 12 months fees.']
        }
    }
    res = client.post('/api/report/download', json=analysis_payload)
    assert res.status_code == 200
    assert res.content_type == 'application/pdf'
    assert len(res.data) > 100
