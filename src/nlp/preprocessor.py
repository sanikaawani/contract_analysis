"""
NLP Preprocessing Module (Techniques 1 to 5)
1. Sentence Tokenization
2. Word Tokenization
3. Stop Word Removal (Domain-tuned with negation preservation)
4. Porter Stemmer
5. Lancaster Stemmer
6. Lemmatization (WordNet with POS context)
"""

import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk import pos_tag

# Ensure required NLTK resources are available
for resource in ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng']:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

# Initialize stemmers and lemmatizer
porter_stemmer = PorterStemmer()
lancaster_stemmer = LancasterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

# Standard NLTK English Stopwords
STANDARD_STOPWORDS = set(stopwords.words('english'))

# Crucial legal negation/conditional words that MUST NOT be removed in legal context
PRESERVED_LEGAL_TOKENS = {
    'not', 'no', 'nor', 'never', 'none', 'neither',
    'without', 'unless', 'except', 'until', 'against',
    'shall', 'must', 'may', 'cannot', 'under', 'between'
}

# Domain-adapted legal stop words
LEGAL_STOPWORDS = STANDARD_STOPWORDS - PRESERVED_LEGAL_TOKENS


def tokenize_sentences(text: str) -> list[str]:
    """
    Technique 1 (Part A): Sentence Tokenization.
    Combines NLTK sent_tokenize with legal clause boundary detection
    (e.g., Section 1.1, Clause 4(a), numbered sub-clauses).
    """
    if not text or not text.strip():
        return []

    # First split by numbered legal paragraphs if present
    # e.g., "\n1. ", "\n1.1 ", "\n(a) ", "\nSection 2: "
    raw_paragraphs = re.split(r'\n(?=(?:\d+\.|\d+\.\d+|\([a-z0-9]+\)|Section\s+\d+|Clause\s+\d+|ARTICLE\s+[IVXLCDM\d]+)\s+)', text)

    sentences = []
    for para in raw_paragraphs:
        para_clean = para.strip()
        if not para_clean:
            continue
        
        # If the paragraph has multiple grammatical sentences, tokenize them
        nltk_sents = sent_tokenize(para_clean)
        for s in nltk_sents:
            s_clean = s.strip()
            if len(s_clean) > 5:
                sentences.append(s_clean)

    # Fallback to direct sent_tokenize if no legal numbering split occurred
    if not sentences:
        sentences = [s.strip() for s in sent_tokenize(text) if s.strip()]

    return sentences


def tokenize_words(text: str, remove_punctuation: bool = True) -> list[str]:
    """
    Technique 1 (Part B): Word Tokenization.
    Extracts individual token words while respecting hyphens, currency markers, and percentages.
    """
    if not text:
        return []

    tokens = word_tokenize(text)
    if remove_punctuation:
        # Keep alphanumeric tokens and currency symbols
        tokens = [t for t in tokens if re.search(r'[a-zA-Z0-9]', t)]
    return tokens


def remove_stopwords(tokens: list[str], preserve_legal_negations: bool = True) -> list[str]:
    """
    Technique 2: Stop Word Removal.
    Filters out common conversational stopwords while preserving legal conditional negations.
    """
    stop_list = LEGAL_STOPWORDS if preserve_legal_negations else STANDARD_STOPWORDS
    return [t for t in tokens if t.lower() not in stop_list]


def apply_porter_stemmer(tokens: list[str]) -> list[str]:
    """
    Technique 3: Porter Stemmer.
    Applies Martin Porter's classic algorithmic suffix stripping.
    """
    return [porter_stemmer.stem(t) for t in tokens]


def apply_lancaster_stemmer(tokens: list[str]) -> list[str]:
    """
    Technique 4: Lancaster Stemmer.
    Applies the more aggressive Paice/Husk Lancaster stemming algorithm.
    """
    return [lancaster_stemmer.stem(t) for t in tokens]


def _get_wordnet_pos(treebank_tag: str):
    """Maps NLTK Treebank POS tags to WordNet POS constants."""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def apply_lemmatization(tokens: list[str], pos_aware: bool = True) -> list[str]:
    """
    Technique 5: Lemmatization.
    Reduces words to true morphological lemma base forms using WordNet dictionary lookup.
    """
    if not tokens:
        return []

    if pos_aware:
        tagged = pos_tag(tokens)
        lemmas = []
        for word, tag in tagged:
            wn_pos = _get_wordnet_pos(tag)
            lemma = wordnet_lemmatizer.lemmatize(word, pos=wn_pos)
            lemmas.append(lemma)
        return lemmas
    else:
        return [wordnet_lemmatizer.lemmatize(t) for t in tokens]


def compare_normalization_techniques(text: str, limit: int = 25) -> list[dict]:
    """
    Generates a comparative side-by-side analysis of:
    Raw Word -> Porter Stem -> Lancaster Stem -> WordNet Lemma.
    Demonstrates linguistic normalization differences for academic viva & reports.
    """
    words = tokenize_words(text, remove_punctuation=True)
    filtered = remove_stopwords(words, preserve_legal_negations=True)
    
    unique_words = list(dict.fromkeys(filtered))[:limit]
    tagged = pos_tag(unique_words)
    
    comparison = []
    for word, tag in tagged:
        p_stem = porter_stemmer.stem(word)
        l_stem = lancaster_stemmer.stem(word)
        wn_pos = _get_wordnet_pos(tag)
        lemma = wordnet_lemmatizer.lemmatize(word, pos=wn_pos)
        
        comparison.append({
            'original_word': word,
            'pos_tag': tag,
            'porter_stem': p_stem,
            'lancaster_stem': l_stem,
            'wordnet_lemma': lemma,
            'stem_vs_lemma_difference': bool(p_stem.lower() != lemma.lower())
        })
        
    return comparison


def preprocess_text(text: str, method: str = 'lemmatize') -> str:
    """
    Full standard preprocessing pipeline for ML classifiers:
    Tokenize -> Lowercase -> Stopword Removal -> Stem/Lemmatize -> Joined string.
    """
    tokens = tokenize_words(text, remove_punctuation=True)
    filtered = remove_stopwords([t.lower() for t in tokens], preserve_legal_negations=True)
    
    if method == 'lemmatize':
        processed_tokens = apply_lemmatization(filtered, pos_aware=True)
    elif method == 'porter':
        processed_tokens = apply_porter_stemmer(filtered)
    elif method == 'lancaster':
        processed_tokens = apply_lancaster_stemmer(filtered)
    else:
        processed_tokens = filtered
        
    return " ".join(processed_tokens)
