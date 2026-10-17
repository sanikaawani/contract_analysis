import os
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import joblib

class LegalFeatureExtractor:
    """
    Feature engineering suite encompassing:
    1. Bag of Words (BoW)
    2. TF-IDF Representation
    3. N-Gram Frequency Extractor (1-gram, 2-gram, 3-gram)
    4. Word2Vec Continuous Vector Embeddings
    """
    def __init__(self, model_dir: str = "C:/Users/JIJAU/.gemini/antigravity/scratch/legal_contract_risk_analyzer/backend/ml/saved_models"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.bow_vectorizer = CountVectorizer(
            ngram_range=(1, 1),
            stop_words='english',
            max_features=1000
        )
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            sublinear_tf=True,
            max_features=1500
        )
        self.word2vec_model = None
        self.w2v_vector_size = 100
        
    def fit_corpus(self, documents: list[str]):
        """Fit BoW, TF-IDF and Word2Vec on the contract dataset."""
        # 1. Fit BoW & TF-IDF
        self.bow_vectorizer.fit(documents)
        self.tfidf_vectorizer.fit(documents)
        
        # 2. Train Word2Vec on tokenized corpus
        tokenized_corpus = []
        for doc in documents:
            tokens = [w.lower() for w in word_tokenize(doc) if re.search(r'\w', w)]
            if tokens:
                tokenized_corpus.append(tokens)
                
        # Train domain Word2Vec model
        self.word2vec_model = Word2Vec(
            sentences=tokenized_corpus,
            vector_size=self.w2v_vector_size,
            window=5,
            min_count=1,
            workers=2,
            epochs=50,
            sg=1 # Skip-gram for better representation of rare legal terms
        )
        
        # Save models
        joblib.dump(self.bow_vectorizer, os.path.join(self.model_dir, "bow_vectorizer.joblib"))
        joblib.dump(self.tfidf_vectorizer, os.path.join(self.model_dir, "tfidf_vectorizer.joblib"))
        self.word2vec_model.save(os.path.join(self.model_dir, "legal_word2vec.model"))
        
    def load_models(self):
        """Load pretrained feature extractors."""
        bow_path = os.path.join(self.model_dir, "bow_vectorizer.joblib")
        tfidf_path = os.path.join(self.model_dir, "tfidf_vectorizer.joblib")
        w2v_path = os.path.join(self.model_dir, "legal_word2vec.model")
        
        if os.path.exists(bow_path):
            self.bow_vectorizer = joblib.load(bow_path)
        if os.path.exists(tfidf_path):
            self.tfidf_vectorizer = joblib.load(tfidf_path)
        if os.path.exists(w2v_path):
            self.word2vec_model = Word2Vec.load(w2v_path)

    def extract_bow(self, text: str) -> dict:
        """Extract Bag of Words vector and non-zero feature frequencies."""
        vec = self.bow_vectorizer.transform([text])
        feature_names = self.bow_vectorizer.get_feature_names_out()
        non_zero_indices = vec.nonzero()[1]
        
        word_freqs = []
        for idx in non_zero_indices:
            word_freqs.append({
                "word": feature_names[idx],
                "count": int(vec[0, idx])
            })
        word_freqs.sort(key=lambda x: x["count"], reverse=True)
        return {
            "total_vocab_size": len(feature_names),
            "active_features_count": len(non_zero_indices),
            "word_frequencies": word_freqs
        }

    def extract_tfidf(self, text: str) -> dict:
        """Extract TF-IDF vector with top weighted terms."""
        vec = self.tfidf_vectorizer.transform([text])
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        non_zero_indices = vec.nonzero()[1]
        
        weighted_terms = []
        for idx in non_zero_indices:
            weighted_terms.append({
                "term": feature_names[idx],
                "tfidf_score": round(float(vec[0, idx]), 4)
            })
        weighted_terms.sort(key=lambda x: x["tfidf_score"], reverse=True)
        return {
            "total_features": len(feature_names),
            "top_terms": weighted_terms[:15]
        }

    def extract_ngrams(self, text: str, n: int = 2, top_k: int = 10) -> list[dict]:
        """Extract top n-grams (1, 2, or 3-grams) from text."""
        try:
            vec = CountVectorizer(ngram_range=(n, n), stop_words='english')
            matrix = vec.fit_transform([text])
            feature_names = vec.get_feature_names_out()
            counts = matrix.toarray().flatten()
            
            ngrams = []
            for name, count in zip(feature_names, counts):
                if count > 0:
                    ngrams.append({"ngram": name, "frequency": int(count)})
            ngrams.sort(key=lambda x: x["frequency"], reverse=True)
            return ngrams[:top_k]
        except ValueError:
            return []

    def get_document_w2v_vector(self, text: str) -> np.ndarray:
        """Compute document embedding via mean pooling of Word2Vec word vectors."""
        if self.word2vec_model is None:
            self.load_models()
        tokens = [w.lower() for w in word_tokenize(text) if re.search(r'\w', w)]
        vectors = []
        for t in tokens:
            if t in self.word2vec_model.wv:
                vectors.append(self.word2vec_model.wv[t])
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(self.w2v_vector_size)

    def find_similar_words_w2v(self, word: str, top_n: int = 6) -> list[dict]:
        """Query Word2Vec model for top semantically related legal terms."""
        if self.word2vec_model is None:
            self.load_models()
        word_clean = word.lower().strip()
        if word_clean in self.word2vec_model.wv:
            sims = self.word2vec_model.wv.most_similar(word_clean, topn=top_n)
            return [{"word": w, "similarity": round(float(s), 4)} for w, s in sims]
        else:
            # Fallback for words not directly in vocabulary
            return [{"word": f"'{word}' not in trained domain vocab", "similarity": 0.0}]
