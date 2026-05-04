"""
Opportunity management routes for Qatar Foundation Admin Portal
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Opportunity

# Create blueprint
opportunities_bp = Blueprint('opportunities', __name__)

def create_success_response(message, data=None):
    """Create standardized success response"""
    response = {"status": "success", "message": message}
    if data:
        response["data"] = data
    return jsonify(response)

def create_error_response(message, status_code=400):
    """Create standardized error response"""
    return jsonify({"error": message}), status_code

def validate_opportunity_data(data, is_update=False):
    """Validate opportunity form data"""
    errors = []
    
    # Required fields
    required_fields = ['title', 'duration', 'start_date', 'description', 'skills', 'category', 'future_opportunities']
    
    for field in required_fields:
        if not data.get(field, '').strip():
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    # Validate category
    category = data.get('category', '').strip()
    if category and category not in Opportunity.VALID_CATEGORIES:
        errors.append(f"Category must be one of: {', '.join(Opportunity.VALID_CATEGORIES)}")
    
    # Validate start_date format
    start_date_str = data.get('start_date', '').strip()
    if start_date_str:
        try:
            datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            errors.append("Start date must be in YYYY-MM-DD format")
    
    # Validate max_applicants if provided
    max_applicants = data.get('max_applicants')
    if max_applicants is not None and max_applicants != '':
        try:
            max_applicants_int = int(max_applicants)
            if max_applicants_int < 1:
                errors.append("Maximum applicants must be a positive number")
        except (ValueError, TypeError):
            errors.append("Maximum applicants must be a valid number")
    
    return errors

@opportunities_bp.route('/opportunities', methods=['GET'])
@login_required
def get_opportunities():
    """
    Get all opportunities for the current admin - US-2.1
    """
    try:
        # US-2.1: Return only current user's opportunities
        opportunities = Opportunity.query.filter_by(admin_id=current_user.id).order_by(Opportunity.created_at.desc()).all()
        
        # Convert to list of dictionaries
        opportunities_data = [opp.to_dict() for opp in opportunities]
        
        return create_success_response("Opportunities retrieved successfully", opportunities_data)
        
    except Exception as e:
        return create_error_response(f"An error occurred: {str(e)}", 500)

@opportunities_bp.route('/opportunities', methods=['POST'])
@login_required
def create_opportunity():
    """
    Create a new opportunity - US-2.2
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_error_response("No data provided")
        
        # Validate required fields
        validation_errors = validate_opportunity_data(data)
        if validation_errors:
            return create_error_response("; ".join(validation_errors))
        
        # Parse and validate start_date
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return create_error_response("Invalid start date format")
        
        # Handle max_applicants
        max_applicants = None
        if data.get('max_applicants') and data['max_applicants'] != '':
            try:
                max_applicants = int(data['max_applicants'])
            except (ValueError, TypeError):
                return create_error_response("Maximum applicants must be a valid number")
        
        # Create new opportunity
        new_opportunity = Opportunity(
            title=data['title'].strip(),
            duration=data['duration'].strip(),
            start_date=start_date,
            description=data['description'].strip(),
            skills=data['skills'].strip(),  # Store as comma-separated string
            category=data['category'].strip(),
            future_opportunities=data['future_opportunities'].strip(),
            max_applicants=max_applicants,
            admin_id=current_user.id
        )
        
        # Save to database
        db.session.add(new_opportunity)
        db.session.commit()
        
        return create_success_response("Opportunity created successfully", new_opportunity.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(f"An error occurred: {str(e)}", 500)

@opportunities_bp.route('/opportunities/<int:opportunity_id>', methods=['GET'])
@login_required
def get_opportunity_details(opportunity_id):
    """
    Get opportunity details - US-2.4
    """
    try:
        # US-2.4: Check ownership
        opportunity = Opportunity.query.filter_by(id=opportunity_id, admin_id=current_user.id).first()
        
        if not opportunity:
            return create_error_response("Opportunity not found or access denied", 404)
        
        return create_success_response("Opportunity details retrieved", opportunity.to_dict())
        
    except Exception as e:
        return create_error_response(f"An error occurred: {str(e)}", 500)

@opportunities_bp.route('/opportunities/<int:opportunity_id>', methods=['PUT'])
@login_required
def update_opportunity(opportunity_id):
    """
    Update an existing opportunity - US-2.5
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_error_response("No data provided")
        
        # US-2.5: Check ownership
        opportunity = Opportunity.query.filter_by(id=opportunity_id, admin_id=current_user.id).first()
        
        if not opportunity:
            return create_error_response("Opportunity not found or access denied", 404)
        
        # Validate required fields
        validation_errors = validate_opportunity_data(data, is_update=True)
        if validation_errors:
            return create_error_response("; ".join(validation_errors))
        
        # Parse and validate start_date
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return create_error_response("Invalid start date format")
        
        # Handle max_applicants
        max_applicants = None
        if data.get('max_applicants') and data['max_applicants'] != '':
            try:
                max_applicants = int(data['max_applicants'])
            except (ValueError, TypeError):
                return create_error_response("Maximum applicants must be a valid number")
        
        # Update opportunity fields
        opportunity.title = data['title'].strip()
        opportunity.duration = data['duration'].strip()
        opportunity.start_date = start_date
        opportunity.description = data['description'].strip()
        opportunity.skills = data['skills'].strip()
        opportunity.category = data['category'].strip()
        opportunity.future_opportunities = data['future_opportunities'].strip()
        opportunity.max_applicants = max_applicants
        opportunity.updated_at = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        
        return create_success_response("Opportunity updated successfully", opportunity.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(f"An error occurred: {str(e)}", 500)

@opportunities_bp.route('/opportunities/<int:opportunity_id>', methods=['DELETE'])
@login_required
def delete_opportunity(opportunity_id):
    """
    Delete an opportunity - US-2.6
    """
    try:
        # US-2.6: Check ownership
        opportunity = Opportunity.query.filter_by(id=opportunity_id, admin_id=current_user.id).first()
        
        if not opportunity:
            return create_error_response("Opportunity not found or access denied", 404)
        
        # Delete the opportunity
        db.session.delete(opportunity)
        db.session.commit()
        
        return create_success_response("Opportunity deleted successfully")
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(f"An error occurred: {str(e)}", 500)

@opportunities_bp.route('/opportunities/categories', methods=['GET'])
@login_required
def get_categories():
    """
    Get available opportunity categories
    """
    try:
        return create_success_response("Categories retrieved", Opportunity.VALID_CATEGORIES)
        
    except Exception as e:
        return create_error_response(f"An error occurred: {str(e)}", 500)