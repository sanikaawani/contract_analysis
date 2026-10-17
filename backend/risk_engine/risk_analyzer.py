import re
from backend.nlp.preprocessing import tokenize_sentences, tokenize_words, remove_stopwords, full_preprocessing_pipeline
from backend.nlp.linguistic_analysis import pos_tag_analysis, chunk_text, extract_named_entities, expand_synonyms_wordnet, disambiguate_word_sense
from backend.nlp.feature_engineering import LegalFeatureExtractor
from backend.ml.models import LegalContractMLPipeline
from backend.risk_engine.legal_knowledge import LEGAL_STATUTES, RISK_HEURISTIC_RULES

class ContractRiskAnalyzer:
    """
    Hybrid AI Contract Risk Engine integrating ML Clause Classification,
    Statistical NLP Feature Extraction, and Indian Statutory Heuristics.
    """
    def __init__(self):
        self.ml_pipeline = LegalContractMLPipeline()
        self.feature_extractor = self.ml_pipeline.feature_extractor
        
    def analyze_contract(self, full_text: str, contract_title: str = "Uploaded Contract", contract_type: str = "Auto-Detect") -> dict:
        """
        End-to-end analysis of full contract text.
        """
        if not full_text or not full_text.strip():
            return {"error": "Empty contract text provided"}
            
        # 1. Segment into clauses / sentences
        raw_clauses = tokenize_sentences(full_text)
        
        # 2. Extract Contract-Wide Named Entities
        extracted_entities = extract_named_entities(full_text)
        
        # 3. Analyze each clause
        analyzed_clauses = []
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        category_risk_scores = {
            "Automatic Renewal": 0,
            "Payment Terms": 0,
            "Liability Clauses": 0,
            "Penalty Clauses": 0,
            "Termination Clauses": 0,
            "Confidentiality Clauses": 0,
            "Non-Compete Clauses": 0,
            "Restrictive Clauses": 0
        }
        category_clause_counts = {k: 0 for k in category_risk_scores}
        
        red_flags = []
        
        for idx, clause in enumerate(raw_clauses):
            clause_clean = clause.strip()
            if len(clause_clean) < 15:
                continue
                
            # ML Prediction
            pred = self.ml_pipeline.predict_clause(clause_clean)
            category = pred["category"]
            risk_level = pred["risk_level"]
            confidence = pred["category_confidence"]
            
            # Legal Rule-based heuristic verification
            heuristic_reasons = []
            for rule in RISK_HEURISTIC_RULES:
                if re.search(rule["pattern"], clause_clean, re.IGNORECASE):
                    if rule["category"] == category or category == "General / Boilerplate":
                        category = rule["category"]
                        risk_level = rule["boost_risk"]
                        heuristic_reasons.append(rule["reason"])
                        
            # Numerical risk weight
            if risk_level == "High":
                risk_score_item = 90
                high_risk_count += 1
            elif risk_level == "Medium":
                risk_score_item = 55
                medium_risk_count += 1
            else:
                risk_score_item = 20
                low_risk_count += 1
                
            if category in category_risk_scores:
                category_risk_scores[category] += risk_score_item
                category_clause_counts[category] += 1
                
            # Detailed Legal Guidance & Counter Clause
            legal_info = LEGAL_STATUTES.get(category, {
                "statute": "Indian Contract Act, 1872",
                "legal_principle": "General contractual fairness and mutual consent principles.",
                "case_law": "Standard commercial precedent",
                "sme_impact": "Requires careful review against business operational requirements.",
                "counter_clause": "Standard balanced bilateral terms as negotiated."
            })
            
            # Key trigger phrases in this clause
            words = tokenize_words(clause_clean)
            pos_info = pos_tag_analysis(clause_clean)
            
            clause_result = {
                "clause_id": idx + 1,
                "clause_text": clause_clean,
                "category": category,
                "risk_level": risk_level,
                "risk_score": risk_score_item,
                "confidence": confidence,
                "modal_obligations": pos_info["modal_obligations"],
                "statute": legal_info["statute"],
                "legal_principle": legal_info["legal_principle"],
                "sme_impact": legal_info["sme_impact"],
                "recommended_counter_clause": legal_info["counter_clause"],
                "heuristic_flags": heuristic_reasons
            }
            
            analyzed_clauses.append(clause_result)
            
            if risk_level == "High" and len(red_flags) < 5:
                red_flags.append({
                    "clause_id": idx + 1,
                    "category": category,
                    "summary": heuristic_reasons[0] if heuristic_reasons else f"High risk {category} detected.",
                    "snippet": clause_clean[:140] + "..." if len(clause_clean) > 140 else clause_clean
                })
                
        # 4. Compute Overall Contract Risk Score (0-100)
        total_clauses = len(analyzed_clauses)
        if total_clauses > 0:
            # Weighted calculation heavily penalizing High risk traps
            raw_risk = (high_risk_count * 90 + medium_risk_count * 50 + low_risk_count * 15) / total_clauses
            # Additional penalty if critical non-compete or uncapped liability exists
            if high_risk_count >= 3:
                raw_risk = min(100, raw_risk + 15)
            overall_risk_score = round(min(100, max(10, raw_risk)), 1)
        else:
            overall_risk_score = 0
            
        if overall_risk_score >= 65:
            overall_risk_grade = "High Risk"
            overall_risk_badge = "High"
            risk_summary_text = "Critical legal and financial vulnerabilities detected under Indian Law. Immediate renegotiation is strongly advised before signing."
        elif overall_risk_score >= 40:
            overall_risk_grade = "Moderate Risk"
            overall_risk_badge = "Medium"
            risk_summary_text = "Contains moderate commercial risks requiring renegotiation of notice periods, liability caps, or payment terms."
        else:
            overall_risk_grade = "Low Risk / Standard"
            overall_risk_badge = "Low"
            risk_summary_text = "Contract follows standard commercial norms with balanced rights and minimal unconscionable risk for SMBs."

        # Normalize category risk scores (0-100)
        category_breakdown = []
        for cat, total_s in category_risk_scores.items():
            count = category_clause_counts[cat]
            avg_s = round(total_s / count, 1) if count > 0 else 0
            category_breakdown.append({
                "category": cat,
                "risk_score": avg_s,
                "clause_count": count,
                "severity": "High" if avg_s >= 65 else ("Medium" if avg_s >= 40 else "Low")
            })

        # 5. Extract Top N-Grams and Key Terms
        top_bigrams = self.feature_extractor.extract_ngrams(full_text, n=2, top_k=8)
        top_trigrams = self.feature_extractor.extract_ngrams(full_text, n=3, top_k=6)
        tfidf_features = self.feature_extractor.extract_tfidf(full_text)

        # 6. Ambiguous Legal Words WSD Test
        wsd_samples = []
        test_wsd_words = ["consideration", "party", "interest", "execution", "covenant", "damages", "title"]
        for w in test_wsd_words:
            if re.search(r'\b' + w + r'\b', full_text, re.IGNORECASE):
                # find sentence containing word
                for s in raw_clauses:
                    if re.search(r'\b' + w + r'\b', s, re.IGNORECASE):
                        wsd_res = disambiguate_word_sense(s, w)
                        wsd_samples.append(wsd_res)
                        break
                        
        return {
            "contract_title": contract_title,
            "contract_type": contract_type,
            "overall_risk_score": overall_risk_score,
            "overall_risk_grade": overall_risk_grade,
            "overall_risk_badge": overall_risk_badge,
            "risk_summary_text": risk_summary_text,
            "clause_counts": {
                "total": total_clauses,
                "high_risk": high_risk_count,
                "medium_risk": medium_risk_count,
                "low_risk": low_risk_count
            },
            "entities": extracted_entities,
            "category_breakdown": category_breakdown,
            "red_flags": red_flags,
            "clauses": analyzed_clauses,
            "ngram_analysis": {
                "top_bigrams": top_bigrams,
                "top_trigrams": top_trigrams
            },
            "tfidf_top_terms": tfidf_features["top_terms"],
            "wsd_samples": wsd_samples
        }
