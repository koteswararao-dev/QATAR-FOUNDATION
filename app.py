"""
Qatar Foundation Admin Portal - Flask Backend
Main application file
"""
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import login_required
from extensions import db, login_manager
from models import Admin
from routes.auth import auth_bp
from routes.opportunities import opportunities_bp
from config import config

def create_app(config_name=None):
    """Application factory pattern"""
    
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    cfg = config.get(config_name, config['default'])
    app.config.from_object(cfg)
    if hasattr(cfg, 'init_app'):
        cfg.init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(opportunities_bp, url_prefix='/api')
    
    # Serve static files (frontend)
    @app.route('/')
    def serve_frontend():
        """Serve the main HTML file"""
        return send_from_directory('sky', 'admin.html')
    
    @app.route('/<path:filename>')
    def serve_static_files(filename):
        """Serve static files (CSS, JS, images)"""
        return send_from_directory('sky', filename)
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "success",
            "message": "Qatar Foundation Admin Portal API is running",
            "version": "1.0.0"
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 errors"""
        return jsonify({"error": "Authentication required"}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors"""
        return jsonify({"error": "Access forbidden"}), 403
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    return app

# Create the application
app = create_app()

if __name__ == '__main__':
    print("Starting Qatar Foundation Admin Portal...")
    print("Frontend available at: http://localhost:5000")
    print("API endpoints available at: http://localhost:5000/api/")
    print("Health check: http://localhost:5000/api/health")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )