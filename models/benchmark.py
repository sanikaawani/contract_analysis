"""
Model Benchmarking & Evaluation Reporting Module
Reads benchmark results and presents formatted comparison tables and confusion matrices.
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'trained')
BENCHMARK_FILE = os.path.join(MODELS_DIR, 'benchmark_results.json')


def get_benchmark_data() -> dict:
    """Retrieves benchmark results dictionary."""
    if not os.path.exists(BENCHMARK_FILE):
        from .train_models import train_all_models
        return train_all_models()

    with open(BENCHMARK_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_benchmark_summary():
    """Prints formatted comparison table to terminal."""
    data = get_benchmark_data()
    models_dict = data.get('clause_category_models', {})

    print("\n" + "=" * 75)
    print("NLP & ML MODEL COMPARISON BENCHMARK (CLAUSE CATEGORY CLASSIFICATION)")
    print("=" * 75)
    print(f"{'Algorithm':<25} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'5-Fold CV'}")
    print("-" * 75)

    for name, metrics in models_dict.items():
        acc = f"{metrics['accuracy'] * 100:.2f}%"
        prec = f"{metrics['precision_weighted'] * 100:.2f}%"
        rec = f"{metrics['recall_weighted'] * 100:.2f}%"
        f1 = f"{metrics['f1_weighted'] * 100:.2f}%"
        cv = f"{metrics['cv_mean'] * 100:.2f}% (±{metrics['cv_std'] * 100:.2f}%)"
        print(f"{name:<25} | {acc:<10} | {prec:<10} | {rec:<10} | {f1:<10} | {cv}")

    print("=" * 75)

    risk_model = data.get('risk_level_model', {})
    if risk_model:
        print(f"\nRISK LEVEL CLASSIFIER: {risk_model.get('model_name')}")
        print(f"Accuracy: {risk_model.get('accuracy', 0) * 100:.2f}% | F1-Score: {risk_model.get('f1_weighted', 0) * 100:.2f}%")
        print("=" * 75)


if __name__ == '__main__':
    print_benchmark_summary()
