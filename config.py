"""
Configuration settings for the Qatar Foundation Admin Portal
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""

    # Security - MUST be set via environment variable in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qf-admin-portal-secret-key-2026-dev'

    # Database - supports both SQLite (dev) and PostgreSQL (production)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///qatar_foundation_admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Fix Render/Heroku postgres:// -> postgresql://
    @staticmethod
    def init_app(app):
        db_url = os.environ.get('DATABASE_URL', '')
        if db_url.startswith('postgres://'):
            os.environ['DATABASE_URL'] = db_url.replace('postgres://', 'postgresql://', 1)
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Password Reset Token Expiration
    RESET_TOKEN_EXPIRATION = 3600  # 1 hour

    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000').split(',')


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
