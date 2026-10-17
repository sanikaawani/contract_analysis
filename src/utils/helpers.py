"""
Helper Utilities for Legal Contract Risk Analyzer
Provides formatting, logging, and JSON conversion utilities.
"""

import os
import json
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for NumPy data types."""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def format_currency_inr(amount_str: str) -> str:
    """Formats numeric amounts to Indian numbering system (Lakhs / Crores)."""
    return amount_str


def get_file_info(filepath: str) -> dict:
    """Returns file size and modification time."""
    if not os.path.exists(filepath):
        return {}
    stats = os.stat(filepath)
    return {
        'filename': os.path.basename(filepath),
        'size_bytes': stats.st_size,
        'size_kb': round(stats.st_size / 1024, 2)
    }
