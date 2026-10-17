"""
Unit tests for all 13 NLP techniques in src/nlp/
"""

import pytest
from src.nlp.preprocessor import (
    tokenize_sentences,
    tokenize_words,
    remove_stopwords,
    apply_porter_stemmer,
    apply_lancaster_stemmer,
    apply_lemmatization,
    compare_normalization_techniques
)
from src.nlp.linguistic import (
    tag_pos,
    perform_chunking,
    extract_named_entities,
    extract_legal_obligations
)
from src.nlp.feature_engineering import (
    extract_bag_of_words,
    extract_ngrams,
    LegalWord2Vec
)
from src.nlp.semantics import (
    expand_wordnet_synonyms,
    disambiguate_word_sense
)
from src.nlp.nlp_inspector import inspect_text_nlp


def test_tokenization():
    text = "1.1 The Service Provider shall deliver software. Clause 2(a): The Client agrees to pay INR 50,000 within 30 days."
    sents = tokenize_sentences(text)
    assert len(sents) >= 2

    words = tokenize_words(text, remove_punctuation=True)
    assert len(words) >= 10
    assert "Provider" in words or "Service" in words


def test_stopwords_preserves_legal_negations():
    tokens = ["shall", "not", "be", "liable", "without", "written", "consent", "and", "the", "a"]
    filtered = remove_stopwords(tokens, preserve_legal_negations=True)
    
    # "not", "without", "shall" MUST be preserved in legal context
    assert "not" in filtered
    assert "without" in filtered
    assert "shall" in filtered
    
    # generic stopwords like "and", "the", "a" must be removed
    assert "the" not in filtered
    assert "a" not in filtered


def test_stemming_and_lemmatization():
    tokens = ["indemnified", "obligations", "terminating", "agreements"]
    p_stems = apply_porter_stemmer(tokens)
    l_stems = apply_lancaster_stemmer(tokens)
    lemmas = apply_lemmatization(tokens, pos_aware=True)

    assert len(p_stems) == len(tokens)
    assert len(l_stems) == len(tokens)
    assert len(lemmas) == len(tokens)
    assert "agreement" in lemmas or "obligation" in lemmas


def test_pos_tagging_and_modals():
    text = "The Vendor shall indemnify the Client and may terminate the agreement."
    tagged = tag_pos(text)
    assert len(tagged) > 5

    shall_token = next((t for t in tagged if t['word'].lower() == 'shall'), None)
    assert shall_token is not None
    assert shall_token['is_modal'] is True
    assert "Mandatory" in shall_token['modal_obligation']


def test_chunking_and_legal_frames():
    text = "The Service Provider shall indemnify the Client."
    chunks = perform_chunking(text)
    assert len(chunks['noun_phrases']) >= 1
    assert len(chunks['verb_phrases']) >= 1


def test_ner_extraction():
    text = "ALPHA TECH PVT LTD and Rajesh Sharma executed this agreement on 15th January 2026 for INR 5,00,000 for 2 years in Bengaluru under the Indian Contract Act, 1872."
    entities = extract_named_entities(text)
    
    assert len(entities['money_amounts']) >= 1
    assert any("5,00,000" in m for m in entities['money_amounts'])
    assert len(entities['durations']) >= 1
    assert len(entities['governing_acts']) >= 1


def test_bag_of_words_and_ngrams():
    text = "This contract contains automatic renewal and liquidated damages. Liquidated damages shall apply."
    bow = extract_bag_of_words(text)
    assert bow['total_unique_words'] > 0
    assert len(bow['top_word_frequencies']) > 0

    ngrams = extract_ngrams(text)
    assert len(ngrams['bigrams']) > 0
    assert len(ngrams['detected_risk_collocations']) >= 2


def test_wordnet_synonyms_and_lesk_wsd():
    syns = expand_wordnet_synonyms("terminate")
    assert len(syns['synonyms']) > 0
    assert len(syns['legal_domain_synonyms']) > 0

    sentence = "In consideration of the payment of fees, the parties sign this contract."
    wsd = disambiguate_word_sense(sentence, "consideration")
    assert wsd['is_legal_polysemy'] is True
    assert wsd['inferred_context_type'] == "Legal / Contractual Sense"


def test_master_nlp_inspector():
    text = "The Vendor agrees to unlimited liability and automatic renewal under Indian laws."
    result = inspect_text_nlp(text, target_keyword="terminate")
    
    assert 'technique_1_tokenization' in result
    assert 'technique_2_stopwords' in result
    assert 'techniques_3_4_5_normalization' in result
    assert 'technique_6_pos_tagging' in result
    assert 'technique_7_chunking' in result
    assert 'technique_8_ner' in result
    assert 'technique_9_bow' in result
    assert 'technique_10_ngrams' in result
    assert 'technique_11_wordnet_synonyms' in result
    assert 'technique_12_word2vec' in result
    assert 'technique_13_wsd_lesk' in result
