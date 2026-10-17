"""
Semantics & Lexical Disambiguation Module (Techniques 11 & 13)
11. WordNet Synonym Expansion (Lexical Expansion for Legal Risk Keywords)
13. Word Sense Disambiguation (WSD) using Adapted Lesk Algorithm
"""

import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

# Legal Polysemy Dictionary with Domain-Specific Context Definitions
LEGAL_POLYSEMY_GLOSSARY = {
    'consideration': {
        'legal_sense': 'Something of legal value given by one party in exchange for another party\'s promise or performance (e.g. payment, price, or reciprocal commitment under Section 2(d) of the Indian Contract Act).',
        'lay_sense': 'Thoughtful attention, meditation, or kind regard for others.'
    },
    'execution': {
        'legal_sense': 'The formal signing, sealing, and delivery of a legal contract or instrument to make it legally binding and operative.',
        'lay_sense': 'The carrying out or carrying into effect of a plan, order, or death sentence.'
    },
    'party': {
        'legal_sense': 'A person, corporation, or entity that enters into a legal agreement, contract, or lawsuit.',
        'lay_sense': 'A social gathering of invited guests for conversation and entertainment.'
    },
    'action': {
        'legal_sense': 'A formal legal proceeding, lawsuit, or judicial litigation brought before a court of law.',
        'lay_sense': 'The fact or process of doing something, movement, or exciting activity.'
    },
    'instrument': {
        'legal_sense': 'A formal legal document in writing, such as a deed, contract, bond, or will, that records a formal legal act or agreement.',
        'lay_sense': 'A tool or implement, especially for precision work, or a musical device.'
    },
    'damages': {
        'legal_sense': 'Monetary compensation awarded by a court or agreed in contract for a loss or injury caused by breach of contract.',
        'lay_sense': 'Physical harm that impairs the value, usefulness, or normal function of something.'
    },
    'remedy': {
        'legal_sense': 'The legal means with which a court enforces a right, imposes a penalty, or makes another court order to impose its will.',
        'lay_sense': 'A medicine or treatment for a disease or injury.'
    },
    'covenant': {
        'legal_sense': 'A formal, legally binding promise or commitment in a written contract to do or refrain from doing a specific act.',
        'lay_sense': 'A solemn religious or spiritual agreement.'
    }
}

# Domain-specific legal synonym expansions
LEGAL_DOMAIN_SYNONYMS = {
    'terminate': ['rescind', 'abrogate', 'nullify', 'cancel', 'expire', 'cease', 'dissolve', 'repudiate'],
    'liability': ['indemnity', 'responsibility', 'obligation', 'exposure', 'culpability', 'accountability'],
    'penalty': ['liquidated damages', 'forfeiture', 'punitive charge', 'fine', 'mulct', 'disincentive'],
    'renew': ['extend', 'rollover', 'prolong', 'perpetuate', 'continue', 're-engage'],
    'restrict': ['prohibit', 'forbid', 'bar', 'enjoin', 'inhibit', 'covenant against'],
    'compete': ['rival', 'solicit', 'poach', 'engage in business', 'contend'],
    'confidential': ['proprietary', 'trade secret', 'non-public', 'sensitive', 'classified', 'undisclosed']
}


def expand_wordnet_synonyms(word: str, max_synonyms: int = 10) -> dict:
    """
    Technique 11: WordNet Synonym Expansion.
    Retrieves synsets, definitions, lemmas, hypernyms (broader terms),
    and hyponyms (narrower terms) for a given query or risk keyword.
    """
    word_clean = word.strip().lower()
    synsets = wordnet.synsets(word_clean)

    synonyms = set()
    definitions = []
    hypernyms = set()
    hyponyms = set()

    for syn in synsets:
        definitions.append({
            'synset_name': syn.name(),
            'pos': syn.pos(),
            'definition': syn.definition(),
            'examples': syn.examples()
        })
        for lemma in syn.lemmas():
            name = lemma.name().replace('_', ' ')
            if name.lower() != word_clean:
                synonyms.add(name)

        # Retrieve direct hypernyms (broader concept)
        for hyper in syn.hypernyms():
            for l in hyper.lemmas():
                hypernyms.add(l.name().replace('_', ' '))

        # Retrieve direct hyponyms (narrower concept)
        for hypo in syn.hyponyms():
            for l in hypo.lemmas():
                hyponyms.add(l.name().replace('_', ' '))

    # Augment with legal domain synonyms if applicable
    domain_syns = LEGAL_DOMAIN_SYNONYMS.get(word_clean, [])
    for ds in domain_syns:
        synonyms.add(ds)

    return {
        'query_word': word_clean,
        'synonyms': sorted(list(synonyms))[:max_synonyms],
        'synset_definitions': definitions[:4],
        'hypernyms_broader_concepts': sorted(list(hypernyms))[:6],
        'hyponyms_specific_types': sorted(list(hyponyms))[:6],
        'legal_domain_synonyms': domain_syns
    }


def disambiguate_word_sense(sentence_text: str, target_word: str) -> dict:
    """
    Technique 13: Word Sense Disambiguation (WSD) using the Adapted Lesk Algorithm.
    Computes overlap between the target word's WordNet synset definitions
    and the contextual words in the sentence to select the appropriate sense.
    Also evaluates legal polysemic nuance.
    """
    tokens = word_tokenize(sentence_text.lower())
    target_clean = target_word.strip().lower()

    # NLTK Lesk Disambiguation
    best_synset = lesk(tokens, target_clean)

    lesk_result = {
        'target_word': target_clean,
        'context_sentence': sentence_text,
        'disambiguated_synset': best_synset.name() if best_synset else 'None (No synset match)',
        'pos': best_synset.pos() if best_synset else 'Unknown',
        'definition': best_synset.definition() if best_synset else 'Could not automatically resolve sense.',
        'examples': best_synset.examples() if best_synset else [],
        'is_legal_polysemy': target_clean in LEGAL_POLYSEMY_GLOSSARY,
        'legal_vs_lay_contrast': LEGAL_POLYSEMY_GLOSSARY.get(target_clean, None)
    }

    # Contextual classification for legal polysemy
    if target_clean in LEGAL_POLYSEMY_GLOSSARY:
        legal_indicators = {
            'consideration': ['in exchange for', 'valuable', 'fees', 'rupees', 'sum', 'contract', 'valid', 'payment', 'inr'],
            'execution': ['signed', 'parties', 'agreement', 'delivered', 'in witness', 'executed', 'date', 'seal'],
            'party': ['client', 'vendor', 'service provider', 'contract', 'agreement', 'first party', 'second party'],
            'action': ['court', 'lawsuit', 'legal', 'arbitration', 'proceeding', 'breach', 'damages', 'injunction'],
            'instrument': ['document', 'agreement', 'contract', 'written', 'executed', 'clause', 'terms'],
            'damages': ['liquidated', 'indirect', 'consequential', 'punitive', 'loss', 'inr', 'compensation', 'breach'],
            'remedy': ['injunction', 'legal', 'cure', 'breach', 'relief', 'damages', 'sole', 'exclusive'],
            'covenant': ['agree', 'shall', 'not', 'compete', 'promise', 'clause', 'binding']
        }
        indicators = legal_indicators.get(target_clean, [])
        matched_indicators = [ind for ind in indicators if ind in sentence_text.lower()]
        
        detected_context = 'Legal / Contractual Sense' if matched_indicators else 'General / Colloquial Sense'
        lesk_result['inferred_context_type'] = detected_context
        lesk_result['context_indicator_clues'] = matched_indicators

    return lesk_result


def compute_clause_similarity(clause1: str, clause2: str, word2vec_model=None) -> dict:
    """
    Computes lexical (Jaccard + TF-IDF) and semantic (Word2Vec) similarity between two clauses.
    """
    from .preprocessor import tokenize_words, remove_stopwords
    
    tokens1 = remove_stopwords(tokenize_words(clause1.lower()), preserve_legal_negations=True)
    tokens2 = remove_stopwords(tokenize_words(clause2.lower()), preserve_legal_negations=True)

    set1, set2 = set(tokens1), set(tokens2)
    jaccard = len(set1 & set2) / max(1, len(set1 | set2))

    w2v_sim = 0.0
    if word2vec_model:
        w2v_sim = word2vec_model.compute_similarity(tokens1, tokens2)

    return {
        'jaccard_lexical_similarity': round(float(jaccard), 4),
        'word2vec_semantic_similarity': round(float(w2v_sim), 4),
        'shared_vocabulary': list(set1 & set2)
    }
