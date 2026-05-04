#!/usr/bin/env python3
"""
Setup script for Qatar Foundation Admin Portal
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Qatar Foundation Admin Portal Backend")
    print("=" * 50)
    
    # Check if Python is available
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print(f"✅ Python found: {python_version}")
    except:
        print("❌ Python not found. Please install Python 3.8 or higher.")
        return False
    
    # Install dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Initialize database
    print("🔄 Initializing database...")
    try:
        from app import app
        with app.app_context():
            from extensions import db
            db.create_all()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the application: python app.py")
    print("2. Open your browser to: http://localhost:5000")
    print("3. Create an admin account using the signup form")
    print("4. Start managing opportunities!")
    print("\n📚 API Documentation:")
    print("- Health check: GET /api/health")
    print("- Authentication: POST /api/signup, /api/login, /api/logout")
    print("- Opportunities: GET/POST/PUT/DELETE /api/opportunities")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)