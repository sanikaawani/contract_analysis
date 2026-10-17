import os
import sys
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_validate, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
import joblib

# Ensure project root is in sys.path
sys.path.append("C:/Users/JIJAU/.gemini/antigravity/scratch/legal_contract_risk_analyzer")
from backend.nlp.feature_engineering import LegalFeatureExtractor

def train_and_benchmark():
    dataset_path = "C:/Users/JIJAU/.gemini/antigravity/scratch/legal_contract_risk_analyzer/backend/data/indian_contract_clauses.json"
    saved_model_dir = "C:/Users/JIJAU/.gemini/antigravity/scratch/legal_contract_risk_analyzer/backend/ml/saved_models"
    os.makedirs(saved_model_dir, exist_ok=True)
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    df = pd.DataFrame(data)
    texts = df["clause_text"].tolist()
    categories = df["category"].tolist()
    risk_levels = df["risk_level"].tolist()
    
    print(f"Loaded {len(df)} samples across {df['category'].nunique()} categories and {df['risk_level'].nunique()} risk levels.")
    
    # 1. Fit & Train Feature Extractors
    fe = LegalFeatureExtractor(model_dir=saved_model_dir)
    fe.fit_corpus(texts)
    
    X_bow = fe.bow_vectorizer.transform(texts)
    X_tfidf = fe.tfidf_vectorizer.transform(texts)
    X_w2v = np.array([fe.get_document_w2v_vector(t) for t in texts])
    
    # 2. Benchmarking Experiments: Compare Classifiers across Feature Extractors
    benchmark_results = {
        "dataset_summary": {
            "total_samples": len(df),
            "categories_count": int(df["category"].nunique()),
            "categories": sorted(list(df["category"].unique())),
            "risk_levels": sorted(list(df["risk_level"].unique())),
            "contract_types": sorted(list(df["contract_type"].unique()))
        },
        "feature_comparison_category": [],
        "feature_comparison_risk": [],
        "best_category_model_metrics": {},
        "best_risk_model_metrics": {}
    }
    
    # Stratified split for evaluation
    X_train_tfidf, X_test_tfidf, y_cat_train, y_cat_test, y_risk_train, y_risk_test = train_test_split(
        X_tfidf, categories, risk_levels, test_size=0.25, random_state=42, stratify=categories
    )
    
    # Models to benchmark
    models_to_test = [
        ("Multinomial Naive Bayes (TF-IDF)", MultinomialNB(alpha=0.1), X_tfidf, categories),
        ("Logistic Regression (TF-IDF)", LogisticRegression(C=10.0, max_iter=500), X_tfidf, categories),
        ("Linear SVM / LinearSVC (TF-IDF)", LinearSVC(C=1.5, max_iter=2000, random_state=42), X_tfidf, categories),
        ("Random Forest (TF-IDF)", RandomForestClassifier(n_estimators=100, random_state=42), X_tfidf, categories),
        ("Logistic Regression (Word2Vec)", LogisticRegression(max_iter=500), X_w2v, categories),
        ("Random Forest (Word2Vec)", RandomForestClassifier(n_estimators=100, random_state=42), X_w2v, categories),
        ("Multinomial Naive Bayes (BoW)", MultinomialNB(alpha=0.1), X_bow, categories)
    ]
    
    for name, clf, feat_matrix, labels in models_to_test:
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
        scores = cross_validate(clf, feat_matrix, labels, cv=skf, scoring=['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted'])
        
        benchmark_results["feature_comparison_category"].append({
            "model_feature_combination": name,
            "mean_accuracy": round(float(np.mean(scores['test_accuracy']) * 100), 2),
            "mean_precision": round(float(np.mean(scores['test_precision_weighted']) * 100), 2),
            "mean_recall": round(float(np.mean(scores['test_recall_weighted']) * 100), 2),
            "mean_f1_score": round(float(np.mean(scores['test_f1_weighted']) * 100), 2)
        })
        print(f"Category Benchmark -> {name}: F1-Score = {np.mean(scores['test_f1_weighted'])*100:.2f}%")

    # Risk level benchmark
    risk_models_to_test = [
        ("Linear SVM (TF-IDF)", LinearSVC(C=2.0, max_iter=2000, random_state=42), X_tfidf, risk_levels),
        ("Logistic Regression (TF-IDF)", LogisticRegression(C=10.0, max_iter=500), X_tfidf, risk_levels),
        ("Multinomial Naive Bayes (TF-IDF)", MultinomialNB(alpha=0.1), X_tfidf, risk_levels),
        ("Random Forest (TF-IDF)", RandomForestClassifier(n_estimators=100, random_state=42), X_tfidf, risk_levels),
        ("Random Forest (Word2Vec)", RandomForestClassifier(n_estimators=100, random_state=42), X_w2v, risk_levels)
    ]
    
    for name, clf, feat_matrix, labels in risk_models_to_test:
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
        scores = cross_validate(clf, feat_matrix, labels, cv=skf, scoring=['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted'])
        
        benchmark_results["feature_comparison_risk"].append({
            "model_feature_combination": name,
            "mean_accuracy": round(float(np.mean(scores['test_accuracy']) * 100), 2),
            "mean_precision": round(float(np.mean(scores['test_precision_weighted']) * 100), 2),
            "mean_recall": round(float(np.mean(scores['test_recall_weighted']) * 100), 2),
            "mean_f1_score": round(float(np.mean(scores['test_f1_weighted']) * 100), 2)
        })

    # 3. Train and Persist Best Production Models (LinearSVC / LogisticRegression with TF-IDF)
    best_cat_clf = LogisticRegression(C=10.0, max_iter=1000)
    best_cat_clf.fit(X_train_tfidf, y_cat_train)
    y_cat_pred = best_cat_clf.predict(X_test_tfidf)
    
    cat_acc = accuracy_score(y_cat_test, y_cat_pred)
    cat_cm = confusion_matrix(y_cat_test, y_cat_pred, labels=sorted(list(set(categories))))
    cat_report = classification_report(y_cat_test, y_cat_pred, output_dict=True, zero_division=0)
    
    benchmark_results["best_category_model_metrics"] = {
        "algorithm": "Logistic Regression with Multi-Class TF-IDF (1-2 N-grams)",
        "test_accuracy": round(float(cat_acc * 100), 2),
        "classification_report": cat_report,
        "labels": sorted(list(set(categories))),
        "confusion_matrix": cat_cm.tolist()
    }
    
    # Train full category model on 100% data
    best_cat_clf.fit(X_tfidf, categories)
    joblib.dump(best_cat_clf, os.path.join(saved_model_dir, "clause_category_model.joblib"))
    
    # Best Risk Level model
    best_risk_clf = LogisticRegression(C=10.0, max_iter=1000)
    best_risk_clf.fit(X_train_tfidf, y_risk_train)
    y_risk_pred = best_risk_clf.predict(X_test_tfidf)
    
    risk_acc = accuracy_score(y_risk_test, y_risk_pred)
    risk_cm = confusion_matrix(y_risk_test, y_risk_pred, labels=["Low", "Medium", "High"])
    risk_report = classification_report(y_risk_test, y_risk_pred, output_dict=True, zero_division=0)
    
    benchmark_results["best_risk_model_metrics"] = {
        "algorithm": "Logistic Regression with TF-IDF (1-2 N-grams)",
        "test_accuracy": round(float(risk_acc * 100), 2),
        "classification_report": risk_report,
        "labels": ["Low", "Medium", "High"],
        "confusion_matrix": risk_cm.tolist()
    }
    
    # Train full risk model on 100% data
    best_risk_clf.fit(X_tfidf, risk_levels)
    joblib.dump(best_risk_clf, os.path.join(saved_model_dir, "risk_level_model.joblib"))
    
    # Save benchmark metrics to JSON
    with open(os.path.join(saved_model_dir, "model_benchmarks.json"), "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, indent=2)
        
    print(f"\nModel training and comparative benchmarking complete! Saved in {saved_model_dir}")

if __name__ == "__main__":
    train_and_benchmark()
