import unittest
import json
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")

    def test_get_samples(self):
        response = self.app.get('/api/samples')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 5)
        types = [s["contract_type"] for s in data]
        self.assertIn("Service Agreement", types)
        self.assertIn("Vendor Agreement", types)
        self.assertIn("Employment Agreement", types)
        self.assertIn("Non-Disclosure Agreement (NDA)", types)
        self.assertIn("Supply Agreement", types)

    def test_analyze_endpoint(self):
        payload = {
            "text": "This Agreement shall automatically renew for successive terms of 3 (three) years each unless the Client provides written notice 180 days prior.",
            "contract_title": "Test Renewal Agreement",
            "contract_type": "Service Agreement"
        }
        response = self.app.post('/api/analyze', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("overall_risk_score", data)
        self.assertTrue(len(data["clauses"]) >= 1)

    def test_nlp_experiment_endpoint(self):
        payload = {
            "text": "The Service Provider shall indemnify Apex Tech Solutions Pvt Ltd within 30 days.",
            "technique": "all",
            "query_word": "indemnify"
        }
        response = self.app.post('/api/nlp-experiment', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("tokenization", data)
        self.assertIn("stemming", data)
        self.assertIn("lemmatization", data)
        self.assertIn("pos_tagging", data)
        self.assertIn("chunking", data)
        self.assertIn("ner", data)
        self.assertIn("bow", data)
        self.assertIn("ngrams", data)
        self.assertIn("wordnet_expansion", data)
        self.assertIn("word2vec", data)
        self.assertIn("wsd", data)

    def test_model_metrics_endpoint(self):
        response = self.app.get('/api/model-metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("best_category_model_metrics", data)
        self.assertIn("feature_comparison_category", data)

    def test_spa_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"html", response.data.lower())

if __name__ == '__main__':
    unittest.main()
