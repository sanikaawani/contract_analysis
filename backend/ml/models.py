import os
import numpy as np
import joblib
from backend.nlp.feature_engineering import LegalFeatureExtractor

class LegalContractMLPipeline:
    """
    Inference wrapper for trained Clause Classifier & Risk Predictor models.
    """
    def __init__(self, model_dir: str = "C:/Users/JIJAU/.gemini/antigravity/scratch/legal_contract_risk_analyzer/backend/ml/saved_models"):
        self.model_dir = model_dir
        self.feature_extractor = LegalFeatureExtractor(model_dir=model_dir)
        self.category_model = None
        self.risk_model = None
        self.category_classes = []
        self.risk_classes = []
        self.load()

    def load(self):
        """Load trained models and vectorizers."""
        self.feature_extractor.load_models()
        
        cat_model_path = os.path.join(self.model_dir, "clause_category_model.joblib")
        risk_model_path = os.path.join(self.model_dir, "risk_level_model.joblib")
        
        if os.path.exists(cat_model_path):
            self.category_model = joblib.load(cat_model_path)
            self.category_classes = list(self.category_model.classes_)
            
        if os.path.exists(risk_model_path):
            self.risk_model = joblib.load(risk_model_path)
            self.risk_classes = list(self.risk_model.classes_)

    def predict_clause(self, clause_text: str) -> dict:
        """
        Classify clause category and risk level.
        """
        if self.category_model is None or self.risk_model is None:
            self.load()
            
        tfidf_vec = self.feature_extractor.tfidf_vectorizer.transform([clause_text])
        
        # 1. Predict Category
        cat_pred = self.category_model.predict(tfidf_vec)[0]
        cat_confidence = 0.90
        if hasattr(self.category_model, "predict_proba"):
            probs = self.category_model.predict_proba(tfidf_vec)[0]
            cat_confidence = round(float(np.max(probs)), 3)
        elif hasattr(self.category_model, "decision_function"):
            df = self.category_model.decision_function(tfidf_vec)[0]
            # Softmax approximation
            exp_df = np.exp(df - np.max(df))
            cat_confidence = round(float(np.max(exp_df / np.sum(exp_df))), 3)
            
        # 2. Predict Risk Level
        risk_pred = self.risk_model.predict(tfidf_vec)[0]
        risk_confidence = 0.85
        if hasattr(self.risk_model, "predict_proba"):
            r_probs = self.risk_model.predict_proba(tfidf_vec)[0]
            risk_confidence = round(float(np.max(r_probs)), 3)
        elif hasattr(self.risk_model, "decision_function"):
            r_df = self.risk_model.decision_function(tfidf_vec)[0]
            exp_rdf = np.exp(r_df - np.max(r_df))
            risk_confidence = round(float(np.max(exp_rdf / np.sum(exp_rdf))), 3)

        return {
            "category": cat_pred,
            "category_confidence": cat_confidence,
            "risk_level": risk_pred,
            "risk_confidence": risk_confidence
        }
