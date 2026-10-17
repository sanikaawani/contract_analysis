"""
Model Training & Benchmarking Pipeline
Trains, evaluates, and serializes:
1. Logistic Regression
2. Random Forest Classifier
3. Multinomial Naive Bayes
4. Word2Vec Legal Embeddings
Across 8 Clause Categories and 3 Risk Levels.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

# Append src to path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.nlp.preprocessor import preprocess_text, tokenize_words, remove_stopwords
from src.nlp.feature_engineering import LegalWord2Vec

DATA_FILE = os.path.join(BASE_DIR, 'data', 'processed', 'clauses_dataset.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'trained')


def train_all_models():
    os.makedirs(MODELS_DIR, exist_ok=True)
    print("=" * 60)
    print("LEGAL CONTRACT NLP MODEL TRAINING & BENCHMARKING ENGINE")
    print("=" * 60)

    if not os.path.exists(DATA_FILE):
        print(f"Dataset file not found at {DATA_FILE}. Running generator...")
        from data.dataset_generator import main as gen_main
        gen_main()

    df = pd.read_csv(DATA_FILE)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # 1. NLP Preprocessing
    print("\n[Step 1/5] Applying NLP Preprocessing Pipeline (Tokenization, Lemmatization, Stopword Filtering)...")
    df['processed_text'] = df['clause_text'].apply(lambda x: preprocess_text(str(x), method='lemmatize'))

    # 2. Vectorization (TF-IDF and BoW)
    print("[Step 2/5] Building Feature Vectors (TF-IDF & CountVectorizer)...")
    tfidf_vec = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=3500,
        sublinear_tf=True,
        stop_words='english'
    )
    X_tfidf = tfidf_vec.fit_transform(df['processed_text'])
    joblib.dump(tfidf_vec, os.path.join(MODELS_DIR, 'tfidf_vectorizer.joblib'))

    count_vec = CountVectorizer(
        ngram_range=(1, 2),
        max_features=3500,
        stop_words='english'
    )
    X_count = count_vec.fit_transform(df['processed_text'])
    joblib.dump(count_vec, os.path.join(MODELS_DIR, 'count_vectorizer.joblib'))

    # 3. Train Word2Vec Embeddings
    print("[Step 3/5] Training Domain-Specific Legal Word2Vec Model...")
    sentences = [remove_stopwords(tokenize_words(str(text).lower()), preserve_legal_negations=True) for text in df['clause_text']]
    w2v_model = LegalWord2Vec(vector_size=100, window=5, min_count=1)
    w2v_model.train_on_corpus(sentences, epochs=35)
    w2v_model.save(os.path.join(MODELS_DIR, 'word2vec_legal.model'))
    print("Word2Vec model trained and saved successfully.")

    # 4. Clause Category Classification Benchmark (8 Classes)
    print("\n[Step 4/5] Training & Evaluating 3 ML Algorithms for Clause Category Detection (8 Categories)...")
    y_cat = df['clause_category']
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X_tfidf, y_cat, test_size=0.25, random_state=42, stratify=y_cat
    )

    models_config = {
        'Logistic Regression': (
            LogisticRegression(max_iter=1000, C=1.5, random_state=42),
            'clause_classifier_lr.joblib'
        ),
        'Random Forest': (
            RandomForestClassifier(n_estimators=150, max_depth=20, random_state=42),
            'clause_classifier_rf.joblib'
        ),
        'Multinomial Naive Bayes': (
            MultinomialNB(alpha=0.1),
            'clause_classifier_nb.joblib'
        )
    }

    benchmark_report = {
        'clause_category_models': {},
        'risk_level_model': {},
        'dataset_summary': {
            'total_samples': len(df),
            'categories_count': df['clause_category'].value_counts().to_dict(),
            'risk_levels_count': df['risk_level'].value_counts().to_dict()
        }
    }

    for model_name, (model_obj, filename) in models_config.items():
        print(f"\n--- Training {model_name} ---")
        model_obj.fit(X_train_c, y_train_c)
        y_pred = model_obj.predict(X_test_c)

        acc = accuracy_score(y_test_c, y_pred)
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_test_c, y_pred, average='macro', zero_division=0)
        p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(y_test_c, y_pred, average='weighted', zero_division=0)
        
        cv_scores = cross_val_score(model_obj, X_tfidf, y_cat, cv=5)

        # Save model
        joblib.dump(model_obj, os.path.join(MODELS_DIR, filename))

        print(f"Accuracy: {acc * 100:.2f}% | F1-Score (Weighted): {f1_weighted * 100:.2f}% | 5-Fold CV: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)")

        classes_list = sorted(list(set(y_cat)))
        cm = confusion_matrix(y_test_c, y_pred, labels=classes_list).tolist()

        benchmark_report['clause_category_models'][model_name] = {
            'accuracy': round(float(acc), 4),
            'precision_macro': round(float(p_macro), 4),
            'recall_macro': round(float(r_macro), 4),
            'f1_macro': round(float(f1_macro), 4),
            'precision_weighted': round(float(p_weighted), 4),
            'recall_weighted': round(float(r_weighted), 4),
            'f1_weighted': round(float(f1_weighted), 4),
            'cv_mean': round(float(cv_scores.mean()), 4),
            'cv_std': round(float(cv_scores.std()), 4),
            'confusion_matrix': cm,
            'classes': classes_list,
            'filename': filename
        }

    # 5. Risk Level Classification (Low, Medium, High)
    print("\n[Step 5/5] Training Risk Level Classifier (Low / Medium / High)...")
    y_risk = df['risk_level']
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X_tfidf, y_risk, test_size=0.25, random_state=42, stratify=y_risk
    )

    risk_clf = RandomForestClassifier(n_estimators=150, max_depth=15, random_state=42)
    risk_clf.fit(X_train_r, y_train_r)
    y_pred_risk = risk_clf.predict(X_test_r)

    acc_r = accuracy_score(y_test_r, y_pred_risk)
    p_r, r_r, f1_r, _ = precision_recall_fscore_support(y_test_r, y_pred_risk, average='weighted', zero_division=0)
    
    joblib.dump(risk_clf, os.path.join(MODELS_DIR, 'risk_level_classifier.joblib'))
    print(f"Risk Level Classifier Accuracy: {acc_r * 100:.2f}% | F1-Score: {f1_r * 100:.2f}%")

    risk_classes = ['High', 'Medium', 'Low']
    cm_risk = confusion_matrix(y_test_r, y_pred_risk, labels=risk_classes).tolist()

    benchmark_report['risk_level_model'] = {
        'model_name': 'Random Forest Risk Classifier',
        'accuracy': round(float(acc_r), 4),
        'precision_weighted': round(float(p_r), 4),
        'recall_weighted': round(float(r_r), 4),
        'f1_weighted': round(float(f1_r), 4),
        'classes': risk_classes,
        'confusion_matrix': cm_risk
    }

    # Save benchmark results JSON
    benchmark_file = os.path.join(MODELS_DIR, 'benchmark_results.json')
    with open(benchmark_file, 'w', encoding='utf-8') as f:
        json.dump(benchmark_report, f, indent=2)
    print(f"\nAll models and benchmark report saved to: {MODELS_DIR}")
    print(f"Benchmark Report: {benchmark_file}")
    print("=" * 60)

    return benchmark_report


if __name__ == '__main__':
    train_all_models()
