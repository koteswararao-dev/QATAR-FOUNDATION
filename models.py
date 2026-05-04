"""
Database models for Qatar Foundation Admin Portal
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class Admin(UserMixin, db.Model):
    """Admin user model"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship: One Admin can have many Opportunities
    opportunities = db.relationship('Opportunity', backref='creator', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert admin to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Admin {self.email}>'

class Opportunity(db.Model):
    """Opportunity model"""
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)  # Comma-separated string
    category = db.Column(db.String(50), nullable=False)
    future_opportunities = db.Column(db.Text, nullable=False)
    max_applicants = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Key linking to the Admin table
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    
    # Valid categories
    VALID_CATEGORIES = [
        'Technology', 'Business', 'Design', 'Marketing', 'Data Science', 'Other'
    ]
    
    def get_skills_list(self):
        """Get skills as a list"""
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
    
    def set_skills_from_list(self, skills_list):
        """Set skills from a list"""
        self.skills = ', '.join(skills_list)
    
    def to_dict(self):
        """Convert opportunity to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'duration': self.duration,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'description': self.description,
            'skills': self.get_skills_list(),
            'category': self.category,
            'future_opportunities': self.future_opportunities,
            'max_applicants': self.max_applicants,
            'admin_id': self.admin_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Opportunity {self.title}>'

class PasswordResetToken(db.Model):
    """Password reset token model"""
    __tablename__ = 'password_reset_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False, unique=True, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    admin = db.relationship('Admin', backref='reset_tokens')
    
    def is_expired(self):
        """Check if token is expired"""
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f'<PasswordResetToken {self.token[:8]}...>'