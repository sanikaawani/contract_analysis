import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer

# Initialize NLTK tools
try:
    nltk_stopwords = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk_stopwords = set(stopwords.words('english'))

porter = PorterStemmer()
lancaster = LancasterStemmer()
lemmatizer = WordNetLemmatizer()

# Legal negations and risk-sensitive modifiers to preserve
LEGAL_PRESERVED_WORDS = {
    'not', 'no', 'nor', 'neither', 'never', 'none', 'without', 
    'except', 'unless', 'against', 'strictly', 'sole', 'exclusive', 
    'indefinite', 'perpetual', 'uncapped', 'liable', 'breach'
}

def get_wordnet_pos(treebank_tag):
    """Map POS tag to first character lemmatize() accepts"""
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

def tokenize_sentences(text: str) -> list[str]:
    """Segment text into individual sentences/clauses."""
    if not text or not text.strip():
        return []
    # Clean excessive whitespace while preserving structure
    cleaned = re.sub(r'\r\n|\r', '\n', text)
    sentences = sent_tokenize(cleaned)
    # If standard tokenizer returns very few long blocks, split by numbered clause patterns
    final_sentences = []
    for s in sentences:
        sub_splits = re.split(r'\n(?=[0-9]+\.|\([a-z0-9]+\)|[A-Z\s]{4,}:)', s)
        for sub in sub_splits:
            if sub.strip():
                final_sentences.append(sub.strip())
    return final_sentences

def tokenize_words(text: str) -> list[str]:
    """Tokenize a sentence into words and punctuation."""
    return word_tokenize(text)

def remove_stopwords(tokens: list[str], preserve_legal_negations: bool = True) -> dict:
    """
    Filter stop words while optionally keeping legally vital words.
    Returns filtered tokens and a list of removed words.
    """
    filtered = []
    removed = []
    for token in tokens:
        token_lower = token.lower()
        if preserve_legal_negations and token_lower in LEGAL_PRESERVED_WORDS:
            filtered.append(token)
        elif token_lower in nltk_stopwords or not re.search(r'\w', token):
            removed.append(token)
        else:
            filtered.append(token)
    return {
        "filtered_tokens": filtered,
        "removed_stopwords": removed,
        "original_count": len(tokens),
        "filtered_count": len(filtered)
    }

def apply_porter_stemmer(tokens: list[str]) -> list[dict]:
    """Apply Porter Stemmer to tokens."""
    return [{"word": t, "stem": porter.stem(t)} for t in tokens if re.search(r'\w', t)]

def apply_lancaster_stemmer(tokens: list[str]) -> list[dict]:
    """Apply Lancaster Stemmer to tokens."""
    return [{"word": t, "stem": lancaster.stem(t)} for t in tokens if re.search(r'\w', t)]

def compare_stemmers(tokens: list[str]) -> list[dict]:
    """Compare Porter vs Lancaster stemming side-by-side."""
    comparison = []
    for t in tokens:
        if re.search(r'[a-zA-Z]', t):
            p_stem = porter.stem(t)
            l_stem = lancaster.stem(t)
            comparison.append({
                "word": t,
                "porter_stem": p_stem,
                "lancaster_stem": l_stem,
                "is_different": p_stem != l_stem,
                "reduction_type": "Aggressive (Lancaster)" if len(l_stem) < len(p_stem) else ("Equal" if len(l_stem) == len(p_stem) else "Porter Shorter")
            })
    return comparison

def lemmatize_tokens(tokens: list[str], pos_tags: list[tuple[str, str]] = None) -> list[dict]:
    """
    Apply WordNet Lemmatizer with optional POS context.
    """
    if pos_tags is None:
        pos_tags = nltk.pos_tag(tokens)
    
    results = []
    for word, tag in pos_tags:
        if re.search(r'[a-zA-Z]', word):
            wn_pos = get_wordnet_pos(tag)
            lemma = lemmatizer.lemmatize(word.lower(), pos=wn_pos)
            results.append({
                "word": word,
                "pos_tag": tag,
                "wordnet_pos": wn_pos,
                "lemma": lemma
            })
    return results

def full_preprocessing_pipeline(text: str) -> dict:
    """
    Execute end-to-end preprocessing pipeline for visual exploration.
    """
    sentences = tokenize_sentences(text)
    sample_sentence = sentences[0] if sentences else text
    words = tokenize_words(sample_sentence)
    stopword_result = remove_stopwords(words)
    filtered_words = stopword_result["filtered_tokens"]
    
    pos_tagged = nltk.pos_tag(words)
    stemmer_comparison = compare_stemmers(filtered_words)
    lemmas = lemmatize_tokens(filtered_words, [p for p in pos_tagged if p[0] in filtered_words])
    
    return {
        "sentence_count": len(sentences),
        "sentences": sentences[:10], # preview
        "word_count": len(words),
        "tokens": words,
        "stopwords_analysis": stopword_result,
        "stemmer_comparison": stemmer_comparison,
        "lemmatization": lemmas
    }
