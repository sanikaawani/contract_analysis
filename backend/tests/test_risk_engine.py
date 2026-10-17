import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.risk_engine.risk_analyzer import ContractRiskAnalyzer
from backend.utils.report_generator import generate_pdf_report

class TestRiskEngineAndPDF(unittest.TestCase):
    def setUp(self):
        self.analyzer = ContractRiskAnalyzer()
        self.sample_contract = """
        MASTER SERVICE AGREEMENT
        Between Apex Tech Solutions Pvt Ltd and Zenith Digital Services LLP.
        
        1. AUTOMATIC RENEWAL
        This Agreement shall automatically renew for successive terms of 3 (three) years each unless Client gives 180 days notice.
        
        2. UNLIMITED LIABILITY
        Service Provider shall indemnify Client for uncapped and unlimited liability arising out of any breach.
        
        3. NON-COMPETE
        Service Provider shall not engage in competing business in India for 3 years post-termination.
        """

    def test_risk_analysis(self):
        res = self.analyzer.analyze_contract(self.sample_contract, "Test Contract", "Service Agreement")
        self.assertIn("overall_risk_score", res)
        self.assertTrue(res["overall_risk_score"] >= 65, "Expected high risk score for high-risk contract")
        self.assertEqual(res["overall_risk_badge"], "High")
        self.assertTrue(len(res["clauses"]) >= 3)
        self.assertTrue(len(res["red_flags"]) > 0)
        self.assertTrue(len(res["category_breakdown"]) == 8)

    def test_pdf_generation(self):
        res = self.analyzer.analyze_contract(self.sample_contract, "Test Contract", "Service Agreement")
        pdf_buffer = generate_pdf_report(res)
        pdf_bytes = pdf_buffer.getvalue()
        self.assertTrue(len(pdf_bytes) > 1000, "PDF should contain valid bytes")
        self.assertTrue(pdf_bytes.startswith(b'%PDF'), "Should have valid PDF header")

if __name__ == '__main__':
    unittest.main()
