# Configuration Settings for Legal Contract Risk Analyzer
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'legal-ai-nlp-smb-contract-analyzer-key-2026')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    SAMPLE_CONTRACTS_DIR = os.path.join(DATA_DIR, 'sample_contracts')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    MODELS_DIR = os.path.join(BASE_DIR, 'models', 'trained')
    REPORTS_DIR = os.path.join(BASE_DIR, 'data', 'reports')
    
    # Contract Types
    CONTRACT_TYPES = [
        'Service Agreement',
        'Vendor Agreement',
        'Employment Agreement',
        'Non-Disclosure Agreement (NDA)',
        'Supply Agreement'
    ]
    
    # 8 Risk Categories
    RISK_CATEGORIES = [
        'Automatic Renewal',
        'Payment Terms',
        'Liability Clauses',
        'Penalty Clauses',
        'Termination Clauses',
        'Confidentiality Clauses',
        'Non-Compete Clauses',
        'Restrictive Clauses'
    ]
    
    # Risk Levels
    RISK_LEVELS = ['Low', 'Medium', 'High']
