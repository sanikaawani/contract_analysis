"""
Linguistic Analysis Module (Techniques 6 to 8)
6. Part-of-Speech (POS) Tagging (Penn Treebank + Modal Obligation Analysis)
7. Chunking (Noun Phrases, Verb Phrases, and Legal Obligation Frames)
8. Named Entity Recognition (NER) (Org, Person, Date, Money, Duration, Law)
"""

import re
import nltk
from nltk import pos_tag, RegexpParser
from nltk.tree import Tree
import spacy

# Load spaCy pipeline for robust entity recognition
try:
    nlp_spacy = spacy.load('en_core_web_sm')
except Exception:
    nlp_spacy = None

# Penn Treebank tag descriptive dictionary
POS_DESCRIPTIONS = {
    'CC': 'Coordinating Conjunction',
    'CD': 'Cardinal Number',
    'DT': 'Determiner',
    'EX': 'Existential There',
    'FW': 'Foreign Word',
    'IN': 'Preposition / Subordinating Conjunction',
    'JJ': 'Adjective',
    'JJR': 'Adjective, Comparative',
    'JJS': 'Adjective, Superlative',
    'MD': 'Modal Verb (Obligation/Permission)',
    'NN': 'Noun, Singular or Mass',
    'NNS': 'Noun, Plural',
    'NNP': 'Proper Noun, Singular',
    'NNPS': 'Proper Noun, Plural',
    'PDT': 'Predeterminer',
    'POS': 'Possessive Ending',
    'PRP': 'Personal Pronoun',
    'PRP$': 'Possessive Pronoun',
    'RB': 'Adverb',
    'RBR': 'Adverb, Comparative',
    'RBS': 'Adverb, Superlative',
    'RP': 'Particle',
    'TO': 'to',
    'UH': 'Interjection',
    'VB': 'Verb, Base Form',
    'VBD': 'Verb, Past Tense',
    'VBG': 'Verb, Gerund/Present Participle',
    'VBN': 'Verb, Past Participle',
    'VBP': 'Verb, Non-3rd Person Singular Present',
    'VBZ': 'Verb, 3rd Person Singular Present',
    'WDT': 'Wh-determiner',
    'WP': 'Wh-pronoun',
    'WP$': 'Possessive Wh-pronoun',
    'WRB': 'Wh-adverb'
}

# Modal verb legal severity categorization
MODAL_SEVERITY = {
    'shall': 'Mandatory / Strict Legal Duty (High Weight)',
    'must': 'Mandatory Legal Imperative (High Weight)',
    'will': 'Mandatory Covenant / Future Binding (Medium-High Weight)',
    'agree': 'Mutual Binding Commitment (Medium Weight)',
    'may': 'Discretionary / Permissive Liberty (Low/Optional Weight)',
    'might': 'Conditional Possibility (Low Weight)',
    'should': 'Advisory / Recommended Practice (Low Weight)'
}

# Regex Chunking Grammar for Legal Text
CHUNKING_GRAMMAR = r"""
  NP: {<DT|PRP\$>?<JJ.*>*<NN.*>+}        # Noun Phrase (e.g. "the Service Provider", "valid tax invoice")
  VP: {<MD>?<RB.*>*<VB.*>+<TO>?<VB.*>*}  # Verb Phrase (e.g. "shall indemnify", "agrees to pay")
  PP: {<IN><NP>}                         # Prepositional Phrase (e.g. "in accordance with law")
  CLAUSE: {<NP><VP><NP|PP>*}             # Legal Obligation Frame
"""
chunk_parser = RegexpParser(CHUNKING_GRAMMAR)


def tag_pos(tokens_or_text) -> list[dict]:
    """
    Technique 6: Part-of-Speech (POS) Tagging.
    Tags words with Penn Treebank POS tags and annotates modal legal obligations.
    """
    if isinstance(tokens_or_text, str):
        from .preprocessor import tokenize_words
        tokens = tokenize_words(tokens_or_text, remove_punctuation=False)
    else:
        tokens = list(tokens_or_text)

    if not tokens:
        return []

    tagged_tuples = pos_tag(tokens)
    result = []

    for word, tag in tagged_tuples:
        desc = POS_DESCRIPTIONS.get(tag, 'Punctuation / Symbol')
        word_lower = word.lower()
        is_modal = tag == 'MD' or word_lower in MODAL_SEVERITY
        modal_info = MODAL_SEVERITY.get(word_lower, None)

        result.append({
            'word': word,
            'tag': tag,
            'description': desc,
            'is_modal': is_modal,
            'modal_obligation': modal_info
        })

    return result


def perform_chunking(tokens_or_text) -> dict:
    """
    Technique 7: Chunking (Shallow Parsing).
    Extracts structured Noun Phrases (NP), Verb Phrases (VP), and Legal Obligation Frames.
    """
    if isinstance(tokens_or_text, str):
        from .preprocessor import tokenize_words
        tokens = tokenize_words(tokens_or_text, remove_punctuation=False)
    else:
        tokens = list(tokens_or_text)

    if not tokens:
        return {'noun_phrases': [], 'verb_phrases': [], 'legal_frames': [], 'tree_str': ''}

    tagged = pos_tag(tokens)
    try:
        parsed_tree = chunk_parser.parse(tagged)
    except Exception:
        return {'noun_phrases': [], 'verb_phrases': [], 'legal_frames': [], 'tree_str': ''}

    noun_phrases = []
    verb_phrases = []
    legal_frames = []

    for subtree in parsed_tree.subtrees():
        if isinstance(subtree, Tree):
            phrase_text = " ".join(word for word, tag in subtree.leaves())
            label = subtree.label()
            
            if label == 'NP':
                if phrase_text not in noun_phrases:
                    noun_phrases.append(phrase_text)
            elif label == 'VP':
                if phrase_text not in verb_phrases:
                    verb_phrases.append(phrase_text)
            elif label == 'CLAUSE':
                if phrase_text not in legal_frames:
                    legal_frames.append(phrase_text)

    return {
        'noun_phrases': noun_phrases,
        'verb_phrases': verb_phrases,
        'legal_frames': legal_frames,
        'tree_str': str(parsed_tree)
    }


def extract_named_entities(text: str) -> dict:
    """
    Technique 8: Named Entity Recognition (NER).
    Extracts and normalizes critical legal entities:
    - Organization Names (Companies, LLPs, Pvt Ltd)
    - Person Names (Signatories, Representatives)
    - Dates (Effective dates, renewal dates, expiry dates)
    - Money Amounts (INR, Rs., USD, Lakhs, Crores)
    - Contract Durations (months, years, days)
    - Governing Laws & Acts (Indian Contract Act, Arbitration Act, IT Act)
    """
    entities = {
        'organizations': [],
        'persons': [],
        'dates': [],
        'money_amounts': [],
        'durations': [],
        'governing_acts': [],
        'jurisdictions': [],
        'all_entities_raw': []
    }

    if not text or not text.strip():
        return entities

    # 1. SpaCy Extraction
    if nlp_spacy:
        doc = nlp_spacy(text[:50000])  # Safe limit
        for ent in doc.ents:
            ent_text = ent.text.strip()
            ent_label = ent.label_

            entities['all_entities_raw'].append({
                'text': ent_text,
                'label': ent_label,
                'start': ent.start_char,
                'end': ent.end_char
            })

            if ent_label in ['ORG']:
                if ent_text not in entities['organizations']:
                    entities['organizations'].append(ent_text)
            elif ent_label in ['PERSON']:
                if ent_text not in entities['persons']:
                    entities['persons'].append(ent_text)
            elif ent_label in ['DATE']:
                if ent_text not in entities['dates']:
                    entities['dates'].append(ent_text)
            elif ent_label in ['MONEY']:
                if ent_text not in entities['money_amounts']:
                    entities['money_amounts'].append(ent_text)
            elif ent_label in ['GPE']:
                if ent_text not in entities['jurisdictions']:
                    entities['jurisdictions'].append(ent_text)

    # 2. Rule-based / Regex Boosters for Indian Legal Specifics
    # Indian Currency Patterns: INR 50,000 | Rs. 1,50,000 | ₹ 10,00,000 | 5 Lakhs | 2 Crores
    money_pattern = r'(?i)(?:INR|Rs\.?|₹|\$|USD)\s*[\d,]+(?:\.\d+)?(?:\s*(?:Lakh|Lakhs|Crore|Crores|Million|Billion))?|\b\d+\s*(?:Lakh|Lakhs|Crore|Crores)\b'
    for match in re.finditer(money_pattern, text):
        val = match.group(0).strip()
        if val and val not in entities['money_amounts']:
            entities['money_amounts'].append(val)

    # Duration Patterns: "12 months", "3 years", "90 days", "24 hours"
    duration_pattern = r'(?i)\b(?:\d+|one|two|three|four|five|six|twelve|twenty-four|thirty|sixty|ninety)\s*(?:\([0-9]+\)\s*)?(?:day|days|business days|calendar days|week|weeks|month|months|year|years|hour|hours)\b'
    for match in re.finditer(duration_pattern, text):
        dur = match.group(0).strip()
        if dur and dur not in entities['durations']:
            entities['durations'].append(dur)

    # Indian Statutes / Acts Pattern
    acts_pattern = r'(?i)(?:Indian Contract Act,?\s*1872|Arbitration and Conciliation Act,?\s*1996|Information Technology Act,?\s*2000|Companies Act,?\s*2013|Insolvency and Bankruptcy Code,?\s*2016|Specific Relief Act,?\s*1963|Goods and Services Tax Act|Income Tax Act,?\s*1961)'
    for match in re.finditer(acts_pattern, text):
        act_name = match.group(0).strip()
        if act_name not in entities['governing_acts']:
            entities['governing_acts'].append(act_name)

    # Indian Corporate Entity Suffixes
    org_pattern = r'\b[A-Z][A-Za-z0-9\s,&]+(?:\s+(?:PVT\.?\s*LTD\.?|PRIVATE\s+LIMITED|LIMITED|LTD\.?|LLP|INC\.?|CORP\.?|SERVICES|SOLUTIONS|ENTERPRISES))\b'
    for match in re.finditer(org_pattern, text):
        org_name = match.group(0).strip()
        if org_name and org_name not in entities['organizations']:
            entities['organizations'].append(org_name)

    return entities


def extract_legal_obligations(text: str) -> list[dict]:
    """
    Extracts specific modal-verb driven legal commitments:
    e.g., "[Party] [shall / must / agree to] [Action] [Object / Condition]".
    """
    from .preprocessor import tokenize_sentences
    sentences = tokenize_sentences(text)
    obligations = []

    obligation_keywords = ['shall', 'must', 'agrees to', 'covenants', 'warrants', 'will indemnify', 'may not']

    for s in sentences:
        s_lower = s.lower()
        matched_kw = [kw for kw in obligation_keywords if kw in s_lower]
        if matched_kw:
            chunks = perform_chunking(s)
            obligations.append({
                'sentence': s,
                'obligation_keywords': matched_kw,
                'noun_phrases': chunks['noun_phrases'][:3],
                'verb_phrases': chunks['verb_phrases'][:3]
            })

    return obligations
