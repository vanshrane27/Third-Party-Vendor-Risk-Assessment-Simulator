import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Upload config
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # PDF config
    PDF_FOLDER = os.path.join(basedir, 'app', 'static', 'pdfs')
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)
    
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