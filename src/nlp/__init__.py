# NLP Pipeline Package for Legal Contract Risk Analyzer
from .preprocessor import (
    tokenize_sentences,
    tokenize_words,
    remove_stopwords,
    apply_porter_stemmer,
    apply_lancaster_stemmer,
    apply_lemmatization,
    compare_normalization_techniques,
    preprocess_text
)
from .linguistic import (
    tag_pos,
    perform_chunking,
    extract_named_entities,
    extract_legal_obligations
)
from .feature_engineering import (
    extract_bag_of_words,
    extract_ngrams,
    extract_tfidf_features,
    LegalWord2Vec
)
from .semantics import (
    expand_wordnet_synonyms,
    disambiguate_word_sense,
    compute_clause_similarity
)
from .nlp_inspector import inspect_text_nlp

__all__ = [
    'tokenize_sentences',
    'tokenize_words',
    'remove_stopwords',
    'apply_porter_stemmer',
    'apply_lancaster_stemmer',
    'apply_lemmatization',
    'compare_normalization_techniques',
    'preprocess_text',
    'tag_pos',
    'perform_chunking',
    'extract_named_entities',
    'extract_legal_obligations',
    'extract_bag_of_words',
    'extract_ngrams',
    'extract_tfidf_features',
    'LegalWord2Vec',
    'expand_wordnet_synonyms',
    'disambiguate_word_sense',
    'compute_clause_similarity',
    'inspect_text_nlp'
]
