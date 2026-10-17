import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.nlp.preprocessing import (
    tokenize_sentences, tokenize_words, remove_stopwords,
    apply_porter_stemmer, apply_lancaster_stemmer, compare_stemmers,
    lemmatize_tokens
)
from backend.nlp.linguistic_analysis import (
    pos_tag_analysis, chunk_text, extract_named_entities,
    expand_synonyms_wordnet, disambiguate_word_sense
)
from backend.nlp.feature_engineering import LegalFeatureExtractor

class TestNLPComponents(unittest.TestCase):
    
    def setUp(self):
        self.sample_clause = (
            "The Service Provider shall indemnify Apex Tech Solutions Pvt Ltd "
            "for a penalty sum of INR 5,00,000 within 30 days of Effective Date 15th October 2024."
        )
        self.fe = LegalFeatureExtractor()
        self.fe.load_models()

    def test_tokenization(self):
        sentences = tokenize_sentences(self.sample_clause)
        self.assertTrue(len(sentences) >= 1)
        words = tokenize_words(sentences[0])
        self.assertTrue(len(words) >= 10)
        self.assertIn("Service", words)

    def test_stopwords(self):
        words = tokenize_words(self.sample_clause)
        res = remove_stopwords(words)
        self.assertIn("The", res["removed_stopwords"])
        self.assertIn("Service", res["filtered_tokens"])

    def test_stemmers(self):
        words = ["indemnification", "services", "agreements", "prohibited"]
        p_stems = apply_porter_stemmer(words)
        l_stems = apply_lancaster_stemmer(words)
        comparison = compare_stemmers(words)
        self.assertEqual(len(p_stems), 4)
        self.assertEqual(len(l_stems), 4)
        self.assertEqual(len(comparison), 4)

    def test_lemmatization(self):
        words = ["indemnified", "obligations", "terminates", "parties"]
        lemmas = lemmatize_tokens(words)
        self.assertTrue(len(lemmas) >= 3)

    def test_pos_tagging(self):
        res = pos_tag_analysis(self.sample_clause)
        self.assertIn("tagged_tokens", res)
        self.assertIn("shall", res["modal_obligations"])

    def test_chunking(self):
        res = chunk_text(self.sample_clause)
        self.assertTrue(len(res["chunks"]["noun_phrases"]) > 0)
        self.assertTrue("shall indemnify" in res["chunks"]["legal_obligations"] or len(res["chunks"]["verb_phrases"]) > 0)

    def test_named_entity_recognition(self):
        entities = extract_named_entities(self.sample_clause)
        self.assertTrue(len(entities["organizations"]) > 0)
        self.assertTrue(any("5,00,000" in m or "INR" in m for m in entities["money_amounts"]))
        self.assertTrue(any("30 days" in d for d in entities["contract_durations"]))

    def test_wordnet_synonyms(self):
        res = expand_synonyms_wordnet("liability")
        self.assertEqual(res["word"], "liability")
        self.assertTrue(len(res["definitions"]) > 0)

    def test_word_sense_disambiguation(self):
        sentence = "The agreement requires adequate legal consideration to be valid."
        wsd = disambiguate_word_sense(sentence, "consideration")
        self.assertIn(wsd["target_word"], ["consideration"])
        self.assertTrue(wsd["chosen_sense"] != "None")

    def test_feature_engineering_bow_tfidf_w2v(self):
        bow = self.fe.extract_bow(self.sample_clause)
        self.assertTrue(bow["active_features_count"] > 0)
        tfidf = self.fe.extract_tfidf(self.sample_clause)
        self.assertTrue(len(tfidf["top_terms"]) > 0)
        ngrams = self.fe.extract_ngrams(self.sample_clause, n=2)
        self.assertTrue(len(ngrams) > 0)
        sim_words = self.fe.find_similar_words_w2v("liability")
        self.assertTrue(len(sim_words) > 0)

if __name__ == '__main__':
    unittest.main()
