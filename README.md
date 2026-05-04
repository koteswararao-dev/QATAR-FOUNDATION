# Qatar Foundation Admin Portal - Backend

A complete Flask backend implementation for the Qatar Foundation Admin Portal, supporting authentication and opportunity management with a secure, production-ready architecture.

## 🚀 Features

### Authentication System (Task 1)
- **Admin Sign Up (US-1.1)**: Complete registration with validation
- **Admin Login (US-1.2)**: Secure authentication with "Remember Me" functionality
- **Forgot Password (US-1.3)**: Password reset with secure token system

### Opportunity Management (Task 2)
- **View All Opportunities (US-2.1)**: Display user-specific opportunities
- **Add New Opportunity (US-2.2)**: Create opportunities with full validation
- **Persistent Storage (US-2.3)**: Database-backed opportunity storage
- **View Details (US-2.4)**: Detailed opportunity information
- **Edit Opportunities (US-2.5)**: Update existing opportunities
- **Delete Opportunities (US-2.6)**: Remove opportunities with confirmation

## 🛠️ Tech Stack

- **Backend**: Python 3.8+ with Flask
- **Database**: SQLite (easily configurable to PostgreSQL/MySQL)
- **Authentication**: Flask-Login with secure password hashing
- **ORM**: SQLAlchemy for database operations
- **Security**: CSRF protection, secure sessions, password hashing
- **Frontend**: Pre-built HTML/CSS/JS (unchanged as required)

## 📁 Project Structure

```
qatar_foundation_admin/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── extensions.py          # Flask extensions initialization
├── models.py              # Database models (Admin, Opportunity)
├── requirements.txt       # Python dependencies
├── setup.py              # Setup script
├── routes/
│   ├── __init__.py
│   ├── auth.py           # Authentication routes
│   └── opportunities.py  # Opportunity management routes
└── sky/                  # Frontend files (provided, unchanged)
    ├── admin.html
    ├── admin.css
    └── admin.js          # Updated with API integration
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Neerajvs32/Test1.git qatar_foundation_admin
cd qatar_foundation_admin

# Run the setup script
python setup.py
```

### 2. Manual Setup (Alternative)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### 3. Access the Application

- **Frontend**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health
- **API Base URL**: http://localhost:5000/api/

## 📋 API Documentation

### Authentication Endpoints

#### Sign Up
```http
POST /api/signup
Content-Type: application/json

{
  "full_name": "John Doe",
  "email": "john@qf.org.qa",
  "password": "securepassword123",
  "confirm_password": "securepassword123"
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "email": "john@qf.org.qa",
  "password": "securepassword123",
  "remember_me": true
}
```

#### Forgot Password
```http
POST /api/forgot-password
Content-Type: application/json

{
  "email": "john@qf.org.qa"
}
```

### Opportunity Management Endpoints

#### Get All Opportunities
```http
GET /api/opportunities
Authorization: Required (session-based)
```

#### Create Opportunity
```http
POST /api/opportunities
Content-Type: application/json
Authorization: Required

{
  "title": "Full Stack Development Program",
  "duration": "6 Months",
  "start_date": "2026-03-01",
  "description": "Comprehensive web development program...",
  "skills": "HTML, CSS, JavaScript, React, Node.js",
  "category": "Technology",
  "future_opportunities": "Career paths include...",
  "max_applicants": 50
}
```

#### Get Opportunity Details
```http
GET /api/opportunities/{id}
Authorization: Required
```

#### Update Opportunity
```http
PUT /api/opportunities/{id}
Content-Type: application/json
Authorization: Required

{
  "title": "Updated Program Name",
  "duration": "8 Months",
  // ... other fields
}
```

#### Delete Opportunity
```http
DELETE /api/opportunities/{id}
Authorization: Required
```

## 🔒 Security Features

- **Password Hashing**: PBKDF2 with SHA-256
- **Session Management**: Secure session cookies with configurable lifetime
- **CSRF Protection**: Built-in Flask security measures
- **Input Validation**: Comprehensive server-side validation
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Email Enumeration Protection**: Consistent responses for forgot password

## 🗄️ Database Schema

### Admin Table
- `id` (Primary Key)
- `full_name` (String, 100 chars)
- `email` (String, 120 chars, unique)
- `password_hash` (String, 255 chars)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Opportunity Table
- `id` (Primary Key)
- `title` (String, 200 chars)
- `duration` (String, 50 chars)
- `start_date` (Date)
- `description` (Text)
- `skills` (Text, comma-separated)
- `category` (String, 50 chars)
- `future_opportunities` (Text)
- `max_applicants` (Integer, nullable)
- `admin_id` (Foreign Key to Admin)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Password Reset Tokens Table
- `id` (Primary Key)
- `admin_id` (Foreign Key to Admin)
- `token` (String, 255 chars, unique)
- `expires_at` (DateTime)
- `used` (Boolean)
- `created_at` (DateTime)

## ⚙️ Configuration

### Environment Variables
```bash
# Optional - defaults provided
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///qatar_foundation_admin.db
FLASK_ENV=development
```

### Valid Opportunity Categories
- Technology
- Business
- Design
- Marketing
- Data Science
- Other

## 🧪 Testing the Application

### 1. Test Authentication Flow
1. Visit http://localhost:5000
2. Click "Create Account" and register a new admin
3. Login with your credentials
4. Test "Remember Me" functionality
5. Test "Forgot Password" (check console for reset link)

### 2. Test Opportunity Management
1. Navigate to "Opportunity Management" tab
2. Click "Add New Opportunity"
3. Fill out the form and submit
4. Verify the opportunity appears in the list
5. Test "View Details", "Edit", and "Delete" functions

### 3. Test Data Persistence
1. Create several opportunities
2. Logout and login again
3. Verify all opportunities are still visible
4. Test that you can only see your own opportunities

## 🚀 Production Deployment

### 1. Environment Setup
```bash
# Set production environment
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### 2. Database Migration
```python
# For PostgreSQL/MySQL
pip install psycopg2-binary  # for PostgreSQL
# or
pip install PyMySQL  # for MySQL

# Update DATABASE_URL in config
```

### 3. Security Considerations
- Use HTTPS in production
- Set secure session cookies
- Use a strong SECRET_KEY
- Configure proper CORS origins
- Set up proper logging
- Use environment variables for sensitive data

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Delete the database file and restart
   rm qatar_foundation_admin.db
   python app.py
   ```

2. **Port Already in Use**
   ```bash
   # Change port in app.py or kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

3. **Module Import Errors**
   ```bash
   # Ensure you're in the correct directory and dependencies are installed
   pip install -r requirements.txt
   ```

## 📝 User Stories Implementation

### Task 1 - Authentication ✅
- ✅ US-1.1: Admin Sign Up with validation
- ✅ US-1.2: Admin Login with Remember Me
- ✅ US-1.3: Forgot Password with secure tokens

### Task 2 - Opportunity Management ✅
- ✅ US-2.1: View All Opportunities (user-specific)
- ✅ US-2.2: Add New Opportunity with validation
- ✅ US-2.3: Opportunities Persist After Login
- ✅ US-2.4: View Opportunity Details
- ✅ US-2.5: Edit Opportunity
- ✅ US-2.6: Delete Opportunity with confirmation

## 🤝 Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Include input validation
4. Write clear commit messages
5. Test all functionality before submitting

## 📄 License

This project is part of the Qatar Foundation internship assessment.

## 📞 Support

For technical issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Examine the console logs for detailed error messages
4. Ensure all dependencies are properly installed

---

**Built with ❤️ for Qatar Foundation**