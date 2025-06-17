import os
from datetime import timedelta

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'
    
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Upload config
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # PDF config
    PDF_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static', 'pdfs')
    
    # Risk scoring config
    RISK_THRESHOLDS = {
        'low': 30,
        'medium': 70,
        'high': float('inf')
    }
    
    # Control weights
    CONTROL_WEIGHTS = {
        'critical': 10,
        'high': 7,
        'medium': 4,
        'low': 2
    } 