"""
Feature Engineering Module (Techniques 9, 10, 12)
9. Bag of Words (BoW)
10. N-Gram Analysis (Unigrams, Bigrams, Trigrams & Legal Collocations)
12. Word2Vec Embeddings (Gensim Word2Vec trained on legal contracts corpus)
"""

import os
import re
import joblib
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'trained')

# High-risk legal n-gram collocation markers
HIGH_RISK_COLOCATIONS = {
    'automatic renewal': 'Auto-Renewal Risk',
    'evergreen basis': 'Perpetual Term Risk',
    'sole discretion': 'Unilateral Power Risk',
    'hold harmless': 'Broad Indemnity Risk',
    'indemnify and hold': 'Uncapped Indemnity Risk',
    'unlimited liability': 'Uncapped Liability Risk',
    'liquidated damages': 'Liquidated Penalty Risk',
    'consequential damages': 'Consequential Loss Risk',
    'loss of profits': 'Indirect Damage Risk',
    'work made for hire': 'IP Forfeiture Risk',
    'prior written notice': 'Strict Notice Requirement',
    'ex-parte injunction': 'Immediate Injunction Risk',
    'lock-in period': 'Lock-in Commitment Risk',
    'non-refundable': 'Financial Forfeiture Risk',
    'forfeit security deposit': 'Security Forfeiture Risk',
    'section 27': 'Restraint of Trade Statutory Risk',
    'section 74': 'Liquidated Damages Statutory Risk'
}


def extract_bag_of_words(texts: list[str] or str, max_features: int = 50) -> dict:
    """
    Technique 9: Bag of Words (BoW).
    Constructs a vocabulary and frequency count matrix for the provided contract text.
    """
    if isinstance(texts, str):
        texts = [texts]

    if not texts or not any(t.strip() for t in texts):
        return {'vocabulary': {}, 'word_counts': [], 'total_unique_words': 0}

    # Vectorize with CountVectorizer
    vectorizer = CountVectorizer(
        lowercase=True,
        stop_words='english',
        max_features=max_features,
        token_pattern=r'(?u)\b[a-zA-Z]{3,}\b'
    )
    
    try:
        bow_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        counts = bow_matrix.toarray().sum(axis=0)

        word_freq = []
        for word, count in zip(feature_names, counts):
            word_freq.append({'word': word, 'count': int(count)})

        # Sort descending by frequency
        word_freq.sort(key=lambda x: x['count'], reverse=True)

        return {
            'vocabulary': {k: int(v) for k, v in vectorizer.vocabulary_.items()},
            'top_word_frequencies': word_freq[:max_features],
            'total_unique_words': len(feature_names),
            'feature_names': list(feature_names)
        }
    except Exception as e:
        return {'vocabulary': {}, 'top_word_frequencies': [], 'total_unique_words': 0, 'error': str(e)}


def extract_ngrams(text: str, n_values: list[int] = [1, 2, 3], top_k: int = 15) -> dict:
    """
    Technique 10: N-Gram Analysis (Unigrams, Bigrams, Trigrams).
    Extracts multi-word contiguous sequences and detects high-risk legal collocations.
    """
    from .preprocessor import tokenize_words, remove_stopwords
    
    tokens = tokenize_words(text.lower(), remove_punctuation=True)
    filtered_tokens = remove_stopwords(tokens, preserve_legal_negations=True)

    result = {
        'unigrams': [],
        'bigrams': [],
        'trigrams': [],
        'detected_risk_collocations': []
    }

    # 1. Extract N-Grams using CountVectorizer
    for n in n_values:
        label = 'unigrams' if n == 1 else ('bigrams' if n == 2 else 'trigrams')
        try:
            vec = CountVectorizer(ngram_range=(n, n), stop_words='english', token_pattern=r'(?u)\b[a-zA-Z]{3,}\b')
            matrix = vec.fit_transform([text])
            features = vec.get_feature_names_out()
            counts = matrix.toarray()[0]

            pairs = [{'ngram': f, 'frequency': int(c)} for f, c in zip(features, counts)]
            pairs.sort(key=lambda x: x['frequency'], reverse=True)
            result[label] = pairs[:top_k]
        except Exception:
            result[label] = []

    # 2. Match against High-Risk Legal Collocations
    text_lower = text.lower()
    for colocation, risk_type in HIGH_RISK_COLOCATIONS.items():
        if colocation in text_lower:
            count = text_lower.count(colocation)
            result['detected_risk_collocations'].append({
                'collocation': colocation,
                'risk_type': risk_type,
                'occurrences': count
            })

    return result


def extract_tfidf_features(texts: list[str], max_features: int = 3000):
    """
    Extracts TF-IDF matrices (Unigram + Bigram) with sublinear term frequency scaling.
    """
    tfidf = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=max_features,
        sublinear_tf=True,
        stop_words='english'
    )
    matrix = tfidf.fit_transform(texts)
    return tfidf, matrix


class LegalWord2Vec:
    """
    Technique 12: Word2Vec Continuous Vector Representation for Legal Text.
    Trained on legal contract sentences with 100-dimension CBOW/Skip-gram embeddings.
    """
    def __init__(self, vector_size: int = 100, window: int = 5, min_count: int = 2):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.model = None

    def train_on_corpus(self, tokenized_sentences: list[list[str]], epochs: int = 30):
        """Trains Word2Vec model on pre-tokenized sentences."""
        self.model = Word2Vec(
            sentences=tokenized_sentences,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            workers=4,
            sg=1,  # Skip-gram for better infrequent legal term representations
            epochs=epochs
        )
        return self.model

    def save(self, filepath: str = None):
        """Saves Word2Vec model to disk."""
        os.makedirs(MODELS_DIR, exist_ok=True)
        path = filepath or os.path.join(MODELS_DIR, 'word2vec_legal.model')
        if self.model:
            self.model.save(path)
            return path
        return None

    def load(self, filepath: str = None):
        """Loads Word2Vec model from disk."""
        path = filepath or os.path.join(MODELS_DIR, 'word2vec_legal.model')
        if os.path.exists(path):
            self.model = Word2Vec.load(path)
            return self.model
        return None

    def get_word_vector(self, word: str) -> np.ndarray:
        """Returns 100-dim vector for a single word."""
        if self.model and word.lower() in self.model.wv:
            return self.model.wv[word.lower()]
        return np.zeros(self.vector_size)

    def get_clause_vector(self, tokens: list[str]) -> np.ndarray:
        """Computes dense average sentence/clause embedding."""
        if not self.model or not tokens:
            return np.zeros(self.vector_size)

        vectors = [self.model.wv[w.lower()] for w in tokens if w.lower() in self.model.wv]
        if not vectors:
            return np.zeros(self.vector_size)
        return np.mean(vectors, axis=0)

    def find_most_similar_words(self, word: str, topn: int = 8) -> list[dict]:
        """Finds top semantic neighbors using cosine similarity in embedding space."""
        if not self.model or word.lower() not in self.model.wv:
            return []

        similar = self.model.wv.most_similar(word.lower(), topn=topn)
        return [{'word': w, 'similarity_score': round(float(s), 4)} for w, s in similar]

    def compute_similarity(self, tokens1: list[str], tokens2: list[str]) -> float:
        """Computes cosine similarity between two clauses using Word2Vec embeddings."""
        v1 = self.get_clause_vector(tokens1)
        v2 = self.get_clause_vector(tokens2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(v1, v2) / (norm1 * norm2))
