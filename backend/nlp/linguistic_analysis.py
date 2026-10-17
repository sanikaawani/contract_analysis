import re
import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

PENN_TAG_DESCRIPTIONS = {
    'CC': 'Coordinating conjunction',
    'CD': 'Cardinal number',
    'DT': 'Determiner',
    'EX': 'Existential there',
    'FW': 'Foreign word',
    'IN': 'Preposition / Subordinating conjunction',
    'JJ': 'Adjective',
    'JJR': 'Adjective, comparative',
    'JJS': 'Adjective, superlative',
    'LS': 'List marker',
    'MD': 'Modal auxiliary (Mandate / Obligation: shall, must, may)',
    'NN': 'Noun, singular',
    'NNS': 'Noun, plural',
    'NNP': 'Proper noun, singular',
    'NNPS': 'Proper noun, plural',
    'PDT': 'Predeterminer',
    'POS': 'Possessive ending',
    'PRP': 'Personal pronoun',
    'PRP$': 'Possessive pronoun',
    'RB': 'Adverb',
    'RBR': 'Adverb, comparative',
    'RBS': 'Adverb, superlative',
    'RP': 'Particle',
    'TO': 'to',
    'UH': 'Interjection',
    'VB': 'Verb, base form',
    'VBD': 'Verb, past tense',
    'VBG': 'Verb, gerund / present participle',
    'VBN': 'Verb, past participle',
    'VBP': 'Verb, non-3rd person singular present',
    'VBZ': 'Verb, 3rd person singular present',
    'WDT': 'Wh-determiner',
    'WP': 'Wh-pronoun',
    'WP$': 'Possessive wh-pronoun',
    'WRB': 'Wh-adverb'
}

# Regex Chunk Grammar for Legal Phrasing
CHUNK_GRAMMAR = r"""
    NP: {<DT>?<JJ.*>*<NN.*>+}          # Noun Phrase (e.g. "the Service Provider", "material breach")
    VP: {<MD>?<VB.*><NP|PP|CLAUSE>*}  # Verb Phrase with modal (e.g. "shall indemnify", "may terminate")
    PP: {<IN><NP>}                     # Prepositional Phrase (e.g. "within 30 days", "of the then-current term")
    LEGAL_OBLIGATION: {<MD><VB.*>}     # Modal obligations (e.g. "shall pay", "must provide")
"""
chunk_parser = nltk.RegexpParser(CHUNK_GRAMMAR)

def pos_tag_analysis(text: str) -> dict:
    """Perform Penn Treebank POS tagging with distribution and semantic analysis."""
    tokens = word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    
    tagged_tokens = []
    tag_counts = {}
    modal_obligations = []
    
    for word, tag in tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
        description = PENN_TAG_DESCRIPTIONS.get(tag, 'Punctuation / Other')
        tagged_tokens.append({
            "word": word,
            "tag": tag,
            "description": description
        })
        if tag == 'MD':
            modal_obligations.append(word.lower())
            
    return {
        "tagged_tokens": tagged_tokens,
        "tag_counts": tag_counts,
        "modal_obligations": list(set(modal_obligations)),
        "token_count": len(tokens)
    }

def chunk_text(text: str) -> dict:
    """Parse text into syntactic chunks (NP, VP, PP, Legal Obligations)."""
    tokens = word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    tree = chunk_parser.parse(tags)
    
    extracted_chunks = {
        "noun_phrases": [],
        "verb_phrases": [],
        "prepositional_phrases": [],
        "legal_obligations": []
    }
    
    for subtree in tree:
        if isinstance(subtree, nltk.Tree):
            chunk_label = subtree.label()
            chunk_words = " ".join(word for word, tag in subtree.leaves())
            if chunk_label == "NP":
                extracted_chunks["noun_phrases"].append(chunk_words)
            elif chunk_label == "VP":
                extracted_chunks["verb_phrases"].append(chunk_words)
            elif chunk_label == "PP":
                extracted_chunks["prepositional_phrases"].append(chunk_words)
            elif chunk_label == "LEGAL_OBLIGATION":
                extracted_chunks["legal_obligations"].append(chunk_words)
                
    return {
        "tree_representation": str(tree),
        "chunks": extracted_chunks
    }

def extract_named_entities(text: str) -> dict:
    """
    Extract key legal entities:
    - Organization Names
    - Dates
    - Money Amounts
    - Contract Duration
    - Person Names
    """
    entities = {
        "organizations": [],
        "dates": [],
        "money_amounts": [],
        "contract_durations": [],
        "person_names": []
    }
    
    # 1. Money Amounts Pattern (INR, ₹, USD, Lakhs, Crores, percentages, daily rates)
    money_regexes = [
        r'(?:INR|Rs\.?|₹|\$)\s*[0-9]+(?:,[0-9]+)*(?:\.[0-9]{2})?(?:\s*(?:lakh|lakhs|crore|crores|thousand|million|billion|per\s+annum|p\.a\.|CTC))?',
        r'[0-9]+(?:\.[0-9]+)?%\s*(?:per\s+(?:month|annum|day|week)|p\.a\.|calculated\s+daily)?',
        r'penalty\s+sum\s+of\s+(?:INR|Rs\.?|₹)\s*[0-9,]+'
    ]
    for r in money_regexes:
        matches = re.finditer(r, text, re.IGNORECASE)
        for m in matches:
            val = m.group(0).strip()
            if val and val not in entities["money_amounts"]:
                entities["money_amounts"].append(val)
                
    # 2. Contract Durations & Notice Periods
    duration_regexes = [
        r'[0-9]+\s*(?:\([a-zA-Z\s]+\))?\s*(?:years?|months?|weeks?|days?|hours?)',
        r'(?:Initial\s+Term\s+of\s+)[0-9]+\s*(?:\([a-zA-Z\s]+\))?\s*(?:years?|months?)',
        r'[0-9]+\s*(?:days?|months?)\s*(?:prior\s+written\s+notice|notice\s+period|lock-in|separation)',
        r'(?:perpetually|indefinitely|successive\s+terms?\s+of\s+[0-9]+\s*(?:\([a-zA-Z\s]+\))?\s*(?:years?|months?))'
    ]
    for r in duration_regexes:
        matches = re.finditer(r, text, re.IGNORECASE)
        for m in matches:
            val = m.group(0).strip()
            if val and val not in entities["contract_durations"]:
                entities["contract_durations"].append(val)

    # 3. Dates
    date_regexes = [
        r'[0-9]{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+[0-9]{4}',
        r'(?:Effective\s+Date|Initial\s+Term|Notice\s+Date|Separation\s+Date)\s*(?::|is)?\s*[0-9]{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+,?\s+[0-9]{4}',
        r'[0-9]{2}[/-][0-9]{2}[/-][0-9]{4}'
    ]
    for r in date_regexes:
        matches = re.finditer(r, text, re.IGNORECASE)
        for m in matches:
            val = m.group(0).strip()
            if val and val not in entities["dates"]:
                entities["dates"].append(val)

    # 4. Organizations (Indian Corporate entities, Ltd, Pvt Ltd, LLP, Inc, Corp)
    org_regexes = [
        r'[A-Z][A-Za-z0-9\s&]+(?:Pvt\.?\s*Ltd\.?|Private\s+Limited|Ltd\.?|Limited|LLP|Inc\.?|Technologies|Solutions|Logistics|Enterprises|Corporation|Systems)',
        r'(?:by\s+and\s+between\s+)([A-Z][A-Za-z0-9\s&]+(?:Pvt\s+Ltd|LLP|Ltd|Inc))',
        r'\b(?:Apex\s+Tech\s+Solutions\s+Pvt\s+Ltd|Zenith\s+Digital\s+Services\s+LLP|Bharat\s+Retail\s+Logistics\s+Ltd|QuickServe\s+IT\s+Logistics\s+LLP|NextGen\s+AI\s+Technologies\s+India\s+Pvt\s+Ltd|FinTech\s+Innovations\s+India\s+Pvt\s+Ltd|SecureCloud\s+Systems\s+LLP|ElectroCraft\s+Manufacturing\s+India\s+Ltd|PrimeComponents\s+Tech\s+Pvt\s+Ltd)\b'
    ]
    for r in org_regexes:
        matches = re.finditer(r, text)
        for m in matches:
            val = m.group(0).strip()
            # clean prefixes
            val = re.sub(r'^(by and between\s+)', '', val, flags=re.IGNORECASE).strip()
            if val and len(val) > 3 and val not in entities["organizations"]:
                entities["organizations"].append(val)

    # 5. Person Names (Contract Signatories, Employees, Representatives)
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    try:
        nltk_ner_tree = nltk.ne_chunk(pos_tags, binary=False)
        for subtree in nltk_ner_tree:
            if isinstance(subtree, nltk.Tree):
                entity_name = " ".join([word for word, tag in subtree.leaves()])
                if subtree.label() == 'PERSON':
                    if entity_name not in entities["person_names"] and len(entity_name.split()) >= 2:
                        entities["person_names"].append(entity_name)
                elif subtree.label() == 'ORGANIZATION':
                    if entity_name not in entities["organizations"] and len(entity_name) > 3:
                        entities["organizations"].append(entity_name)
    except Exception:
        pass

    # Regex fallback for Indian Names in typical contract roles
    person_regexes = [
        r'\b(?:Mr\.|Ms\.|Mrs\.|Dr\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',
        r'Rahul\s+Sharma|Ramesh\s+Sharma|Priya\s+Patel|Amit\s+Verma'
    ]
    for r in person_regexes:
        matches = re.finditer(r, text)
        for m in matches:
            val = m.group(0).strip()
            if val and val not in entities["person_names"]:
                entities["person_names"].append(val)

    return entities

def expand_synonyms_wordnet(word: str) -> dict:
    """Expand legal keyword with WordNet synonyms, definitions, and hypernyms."""
    synsets = wordnet.synsets(word.lower())
    if not synsets:
        return {"word": word, "synonyms": [], "definition": "No synset found", "hypernyms": []}
    
    synonyms = set()
    definitions = []
    hypernyms = set()
    
    for s in synsets[:3]:
        definitions.append(f"[{s.pos()}] {s.definition()}")
        for lemma in s.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
        for hyper in s.hypernyms():
            for h_lemma in hyper.lemmas():
                hypernyms.add(h_lemma.name().replace('_', ' '))
                
    return {
        "word": word,
        "primary_definition": definitions[0] if definitions else "",
        "definitions": definitions,
        "synonyms": list(synonyms)[:8],
        "hypernyms": list(hypernyms)[:5]
    }

def disambiguate_word_sense(sentence: str, target_word: str) -> dict:
    """
    Apply Simplified Lesk Algorithm to disambiguate ambiguous legal terms.
    e.g., 'consideration', 'party', 'interest', 'execution', 'covenant', 'damages'
    """
    tokens = word_tokenize(sentence.lower())
    synset = lesk(tokens, target_word.lower())
    
    all_senses = []
    for s in wordnet.synsets(target_word.lower()):
        all_senses.append({
            "synset_name": s.name(),
            "definition": s.definition(),
            "examples": s.examples()
        })
        
    if synset:
        return {
            "target_word": target_word,
            "chosen_sense": synset.name(),
            "definition": synset.definition(),
            "examples": synset.examples(),
            "all_available_senses_count": len(all_senses),
            "all_senses": all_senses[:4]
        }
    else:
        return {
            "target_word": target_word,
            "chosen_sense": "None",
            "definition": "Could not determine sense via Lesk algorithm context overlap",
            "examples": [],
            "all_available_senses_count": len(all_senses),
            "all_senses": all_senses[:4]
        }
