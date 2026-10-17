"""
Comprehensive NLP Inspector Module
Orchestrates all 13 NLP techniques on any input text for live interactive exploration:
1. Sentence Tokenization
2. Word Tokenization
3. Stop Word Removal
4. Porter Stemmer
5. Lancaster Stemmer
6. Lemmatization
7. Part-of-Speech (POS) Tagging
8. Chunking (NP, VP, Legal Frames)
9. Named Entity Recognition (NER)
10. Bag of Words (BoW)
11. N-Gram Analysis (Unigrams, Bigrams, Trigrams, Collocations)
12. WordNet Synonym Expansion
13. Word2Vec Embeddings & Similarity
14. Word Sense Disambiguation (WSD - Lesk)
"""

from .preprocessor import (
    tokenize_sentences,
    tokenize_words,
    remove_stopwords,
    apply_porter_stemmer,
    apply_lancaster_stemmer,
    apply_lemmatization,
    compare_normalization_techniques
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
    LegalWord2Vec
)
from .semantics import (
    expand_wordnet_synonyms,
    disambiguate_word_sense
)


# Global Word2Vec instance
_w2v_instance = None

def get_word2vec_model():
    global _w2v_instance
    if _w2v_instance is None:
        _w2v_instance = LegalWord2Vec()
        _w2v_instance.load()
    return _w2v_instance


def inspect_text_nlp(text: str, target_keyword: str = None) -> dict:
    """
    Executes all 13 NLP techniques and generates an interactive, academic inspection payload.
    """
    if not text or not text.strip():
        return {'error': 'No text provided for NLP inspection.'}

    # 1. Sentence Tokenization
    sentences = tokenize_sentences(text)

    # 2. Word Tokenization
    raw_words = tokenize_words(text, remove_punctuation=False)
    clean_words = tokenize_words(text, remove_punctuation=True)

    # 3. Stop Word Removal
    words_without_stopwords = remove_stopwords(clean_words, preserve_legal_negations=True)
    standard_filtered = remove_stopwords(clean_words, preserve_legal_negations=False)

    # 4, 5, 6. Normalization Comparison (Porter vs Lancaster vs Lemmatization)
    normalization_table = compare_normalization_techniques(text, limit=20)

    # 7. POS Tagging
    pos_tags = tag_pos(raw_words[:40])  # Sample first 40 tokens for UI clarity
    pos_distribution = {}
    for item in tag_pos(raw_words):
        tag = item['tag']
        pos_distribution[tag] = pos_distribution.get(tag, 0) + 1

    # 8. Chunking
    chunking_data = perform_chunking(text[:1500])
    legal_obligations = extract_legal_obligations(text)

    # 9. Named Entity Recognition
    entities = extract_named_entities(text)

    # 10. Bag of Words
    bow_data = extract_bag_of_words(text, max_features=30)

    # 11. N-Grams
    ngrams_data = extract_ngrams(text, n_values=[1, 2, 3], top_k=10)

    # 12. WordNet Synonym Expansion
    active_keyword = target_keyword or 'terminate'
    synonym_data = expand_wordnet_synonyms(active_keyword)

    # 13. Word2Vec Representation & Similar Terms
    w2v = get_word2vec_model()
    w2v_similar = w2v.find_most_similar_words(active_keyword, topn=6) if w2v and w2v.model else []
    sample_clause_vector = w2v.get_clause_vector(clean_words[:20]).tolist() if w2v else []

    # 14. Word Sense Disambiguation (Lesk)
    polysemic_word = 'consideration' if 'consideration' in text.lower() else ('party' if 'party' in text.lower() else active_keyword)
    sample_sentence = sentences[0] if sentences else text
    for s in sentences:
        if polysemic_word in s.lower():
            sample_sentence = s
            break
    wsd_data = disambiguate_word_sense(sample_sentence, polysemic_word)

    return {
        'summary': {
            'character_count': len(text),
            'raw_word_count': len(raw_words),
            'clean_word_count': len(clean_words),
            'stopwords_removed_count': len(clean_words) - len(words_without_stopwords),
            'sentence_count': len(sentences)
        },
        'technique_1_tokenization': {
            'sentences': sentences[:15],
            'total_sentences': len(sentences),
            'words_sample': raw_words[:30],
            'total_words': len(raw_words)
        },
        'technique_2_stopwords': {
            'filtered_tokens_sample': words_without_stopwords[:30],
            'preserved_legal_tokens': [w for w in words_without_stopwords if w.lower() in {'shall', 'must', 'may', 'not', 'no', 'unless', 'without', 'except'}][:10],
            'total_retained_tokens': len(words_without_stopwords)
        },
        'techniques_3_4_5_normalization': {
            'comparison_table': normalization_table,
            'porter_sample': apply_porter_stemmer(words_without_stopwords[:15]),
            'lancaster_sample': apply_lancaster_stemmer(words_without_stopwords[:15]),
            'lemmatized_sample': apply_lemmatization(words_without_stopwords[:15], pos_aware=True)
        },
        'technique_6_pos_tagging': {
            'tagged_tokens': pos_tags,
            'pos_distribution': pos_distribution
        },
        'technique_7_chunking': {
            'noun_phrases': chunking_data['noun_phrases'][:8],
            'verb_phrases': chunking_data['verb_phrases'][:8],
            'legal_frames': chunking_data['legal_frames'][:5],
            'tree_str': chunking_data['tree_str'][:500],
            'legal_obligations': legal_obligations[:4]
        },
        'technique_8_ner': {
            'organizations': entities['organizations'],
            'persons': entities['persons'],
            'dates': entities['dates'],
            'money_amounts': entities['money_amounts'],
            'durations': entities['durations'],
            'governing_acts': entities['governing_acts'],
            'jurisdictions': entities['jurisdictions']
        },
        'technique_9_bow': bow_data,
        'technique_10_ngrams': ngrams_data,
        'technique_11_wordnet_synonyms': synonym_data,
        'technique_12_word2vec': {
            'query_word': active_keyword,
            'top_semantic_neighbors': w2v_similar,
            'dense_vector_dimensions': len(sample_clause_vector),
            'sample_vector_slice': sample_clause_vector[:10]  # first 10 floats for visualization
        },
        'technique_13_wsd_lesk': wsd_data
    }
