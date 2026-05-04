"""
Authentication routes for Qatar Foundation Admin Portal
"""
import re
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from extensions import db
from models import Admin, PasswordResetToken

# Create blueprint
auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

def create_success_response(message, data=None):
    """Create standardized success response"""
    response = {"status": "success", "message": message}
    if data:
        response["data"] = data
    return jsonify(response)

def create_error_response(message, status_code=400):
    """Create standardized error response"""
    return jsonify({"error": message}), status_code

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Admin Sign Up - US-1.1
    Required fields: full_name, email, password, confirm_password
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_error_response("No data provided")
        
        # Extract and validate required fields
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation: All fields must be filled
        if not all([full_name, email, password, confirm_password]):
            return create_error_response("All fields are required")
        
        # Validation: Email must be valid format
        if not is_valid_email(email):
            return create_error_response("Please enter a valid email address")
        
        # Validation: Password must be at least 8 characters
        if len(password) < 8:
            return create_error_response("Password must be at least 8 characters")
        
        # Validation: Password and confirm password must match
        if password != confirm_password:
            return create_error_response("Passwords do not match")
        
        # Check if email already exists
        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            return create_error_response("An account with this email already exists")
        
        # Create new admin
        new_admin = Admin(
            full_name=full_name,
            email=email
        )
        new_admin.set_password(password)
        
        # Save to database
        db.session.add(new_admin)
        db.session.commit()
        
        return create_success_response("Account created successfully! Please log in.")
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(f"An error occurred: {str(e)}", 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Admin Login - US-1.2
    Required fields: email, password
    Optional: remember_me
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_error_response("No data provided")
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        remember_me = data.get('remember_me', False)
        
        # Validation
        if not email or not password:
            return create_error_response("Email and password are required")
        
        if not is_valid_email(email):
            return create_error_response("Invalid email or password")
        
        # Find admin by email
        admin = Admin.query.filter_by(email=email).first()
        
        # Check credentials - US-1.2: Generic error message
        if not admin or not admin.check_password(password):
            return create_error_response("Invalid email or password", 401)
        
        # Log in the user
        login_user(admin, remember=remember_me)
        
        # Set session as permanent if remember_me is checked
        if remember_me:
            session.permanent = True
        
        return create_success_response("Login successful", {
            "admin": admin.to_dict(),
            "redirect": "/dashboard"
        })
        
    except Exception as e:
        return create_error_response(f"An error occurred: {str(e)}", 500)

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Forgot Password - US-1.3
    Always returns success message for security
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_error_response("No data provided")
        
        email = data.get('email', '').strip().lower()
        
        # Validation
        if not email or not is_valid_email(email):
            return create_error_response("Please enter a valid email address")
        
        # US-1.3: Always show success message regardless of email existence
        success_message = "If an account with this email exists, a password reset link has been sent."
        
        # Check if admin exists
        admin = Admin.query.filter_by(email=email).first()
        
        if admin:
            # Generate secure token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(seconds=3600)  # 1 hour
            
            # Create reset token record
            reset_token = PasswordResetToken(
                admin_id=admin.id,
                token=token,
                expires_at=expires_at
            )
            
            db.session.add(reset_token)
            db.session.commit()
            
            # US-1.3: Log reset link instead of sending email
            reset_link = f"http://localhost:5000/reset-password/{token}"
            print(f"Password reset link for {email}: {reset_link}")
            print(f"Token expires at: {expires_at}")
        
        return create_success_response(success_message)
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(f"An error occurred: {str(e)}", 500)

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    """
    Reset Password with Token
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_error_response("No data provided")
        
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation
        if not new_password or not confirm_password:
            return create_error_response("Both password fields are required")
        
        if len(new_password) < 8:
            return create_error_response("Password must be at least 8 characters")
        
        if new_password != confirm_password:
            return create_error_response("Passwords do not match")
        
        # Find and validate token
        reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()
        
        if not reset_token:
            return create_error_response("Invalid or expired reset link", 400)
        
        if reset_token.is_expired():
            return create_error_response("Reset link has expired. Please request a new one.", 400)
        
        # Update password
        admin = reset_token.admin
        admin.set_password(new_password)
        
        # Mark token as used
        reset_token.used = True
        
        db.session.commit()
        
        return create_success_response("Password reset successfully! You can now log in with your new password.")
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(f"An error occurred: {str(e)}", 500)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Admin Logout
    """
    try:
        logout_user()
        session.clear()
        return create_success_response("Logged out successfully")
        
    except Exception as e:
        return create_error_response(f"An error occurred: {str(e)}", 500)

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """
    Get current admin profile
    """
    try:
        return create_success_response("Profile retrieved", current_user.to_dict())
        
    except Exception as e:
        return create_error_response(f"An error occurred: {str(e)}", 500)