# AI-Based Contract Risk Analysis and Clause Detection System for Small and Medium-Sized Businesses using Natural Language Processing

An academic Final Year Natural Language Processing (NLP) and Legal-Tech Intelligence System designed to empower Small and Medium-Sized Businesses (SMBs) under Indian commercial jurisprudence (**Indian Contract Act 1872**).

---

## Key Features

1. **Document Ingestion**: Supports Drag-and-Drop file uploads for **PDF**, **Microsoft Word (.docx)**, and plain text (**TXT**), with 1-click test loaders for 5 commercial contract types.
2. **Comprehensive NLP Experiments & Implementations**:
   - **Tokenization**: Sentence segmentation and word-level tokenization.
   - **Stop Word Removal**: Custom legal negation preservation (`not`, `without`, `unless`, `except`, `against`).
   - **Porter vs. Lancaster Stemmers**: Morphological comparison and reduction divergence analysis.
   - **WordNet Lemmatization**: Dynamic POS-aware dictionary root extraction.
   - **POS Tagging**: Penn Treebank tagging + isolation of Modal Auxiliaries (`shall`, `must`, `may`) dictating legal obligations.
   - **Regexp Chunking**: Shallow grammatical parsing of Noun Phrases (NP), Verb Phrases (VP), Prepositional Phrases (PP), and Legal Obligations.
   - **Named Entity Recognition (NER)**: Extraction of Organizations, Key Dates, Financial Terms (INR / ₹), Durations, and Signatories.
   - **Bag of Words (BoW)**: Term frequency vectors and vocabulary distribution.
   - **N-Gram Analysis**: Detection of 1-gram, 2-gram, and 3-gram collocations (e.g. *liquidated damages*, *hold harmless*).
   - **WordNet Synonym Expansion**: Gloss definitions, synsets, and hypernym trees.
   - **Continuous Word2Vec Embeddings**: 100-dimensional Skip-gram embeddings trained on contract corpora.
   - **Word Sense Disambiguation (WSD)**: Simplified Lesk algorithm for ambiguous legal polysemy (*consideration*, *party*, *interest*, *execution*, *covenant*, *damages*, *title*).
3. **Machine Learning Model Suite**:
   - Multi-class Clause Category Classifier (8 statutory categories + boilerplate).
   - Risk Level Classifier (Low, Medium, High).
   - Benchmarking comparison across **Multinomial Naive Bayes**, **Linear SVM (LinearSVC)**, **Logistic Regression**, and **Random Forest** over **BoW**, **TF-IDF**, and **Word2Vec** feature spaces.
4. **Indian Statutory & Regulatory Grounding**:
   - **Section 27, Indian Contract Act 1872**: Automatic voiding of post-termination non-competes (*Niranjan Shankar Golikari* precedent).
   - **Sections 15 & 16, MSMED Act 2006**: Flagging credit periods exceeding 45 days.
   - **Section 74, Indian Contract Act 1872**: Flagging exorbitant liquidated damages and daily delay penalties.
   - **Section 73, Indian Contract Act 1872**: Auditing uncapped indemnities and indirect/consequential damages.
5. **Interactive Legal-Tech UI**:
   - **Risk Gauge**: 0–100 Contract Risk Score with Low/Medium/High severity badges.
   - **Recharts Analytics**: 8-category Radar profile, Risk distribution donut, and Severity bar chart.
   - **Clause Detection Table**: Search, filter by category or risk level, and modal guidance.
   - **AI Explanation Modal**: Plain-English risk rationale, legal citation, SMB impact, and 1-click copyable counter-clause template.
   - **PDF Report Generator**: Downloadable executive risk audit report using `reportlab`.

---

## 5 Supported Contract Verticals

1. **Master Service Agreement (MSA)** (Cloud, software development, consulting)
2. **Vendor Procurement Agreement** (IT hardware, supplies, facilities management)
3. **Executive Employment Agreement** (Employment contracts, bond penalties, IP assignment)
4. **Non-Disclosure Agreement (NDA)** (Confidentiality, trade secrets, mutual non-disclosure)
5. **Commercial Supply Agreement** (Hardware distribution, territorial exclusivity, minimum order quantity)

---

## 8 Evaluated Risk Categories

1. `Automatic Renewal` (Evergreen clauses and onerous 180-day notice traps)
2. `Payment Terms` (Violations of 45-day MSMED ceiling, unilateral invoice withholding)
3. `Liability Clauses` (Uncapped liabilities, one-sided indemnities, consequential damages)
4. `Penalty Clauses` (Liquidated damages > 5%/day, arbitrary employment bonds)
5. `Termination Clauses` (Unilateral immediate exit without compensation for work completed)
6. `Confidentiality Clauses` (Perpetual non-disclosure without standard exceptions)
7. `Non-Compete Clauses` (Illegal post-termination restraints under Section 27)
8. `Restrictive Clauses` (Expropriation of background IP, 5-year non-solicitation)

---

## Project Structure

```
legal_contract_risk_analyzer/
├── backend/
│   ├── app.py                      # Flask REST API Server
│   ├── data/
│   │   ├── indian_contract_clauses.json # Dataset (180 balanced Indian clauses)
│   │   └── samples/                # 5 Authentic sample contracts (.txt)
│   ├── nlp/
│   │   ├── preprocessing.py        # Tokenization, Stopwords, Stemmers, Lemmatization
│   │   ├── linguistic_analysis.py  # POS, Chunking, NER, WordNet Synonyms, Lesk WSD
│   │   └── feature_engineering.py  # BoW, TF-IDF, N-Grams, Word2Vec embeddings
│   ├── ml/
│   │   ├── train.py                # Model training & comparative benchmarking
│   │   ├── models.py               # ML inference pipeline
│   │   └── saved_models/           # Serialized models & benchmark JSON
│   ├── risk_engine/
│   │   ├── legal_knowledge.py      # Indian Contract Act statutes & risk rules
│   │   └── risk_analyzer.py        # Hybrid ML + Heuristic Risk Scorer & Explanations
│   ├── utils/
│   │   ├── parser.py               # PDF, DOCX, TXT document parser
│   │   └── report_generator.py     # ReportLab PDF generator
│   └── tests/
│       ├── test_nlp.py             # NLP unit tests (10 tests)
│       ├── test_risk_engine.py     # Risk engine & PDF tests
│       └── test_api.py             # Flask API integration tests
├── frontend/
│   ├── src/
│   │   ├── components/             # Navbar, Footer, RiskGauge, ClauseTable, AI Modal, Charts, NLPWorkbench
│   │   ├── pages/                  # HomePage, UploadPage, AnalysisPage, RiskReportPage, AboutPage
│   │   ├── services/api.js         # REST API connector
│   │   └── App.jsx                 # Main state & page router
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## How to Run the Project

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**

### Step 1: Start the Backend Flask API
```bash
cd legal_contract_risk_analyzer
python backend/app.py
```
*Backend runs on `http://127.0.0.1:5000`*

### Step 2: Start the Frontend React UI
```bash
cd legal_contract_risk_analyzer/frontend
npm run dev
```
*Frontend runs on `http://localhost:5173`*

### Step 3: Run Automated Test Suites
```bash
# Run NLP test suite
python backend/tests/test_nlp.py

# Run Risk Engine test suite
python backend/tests/test_risk_engine.py

# Run API test suite
python backend/tests/test_api.py
```
