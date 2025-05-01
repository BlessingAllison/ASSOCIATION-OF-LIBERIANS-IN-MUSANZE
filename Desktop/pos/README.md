# Point of Sale (POS) System

## Project Description
A comprehensive Point of Sale system built with Django, designed to streamline business operations. This system provides robust features for managing sales, tracking inventory, and handling customer transactions. It's built with scalability and user-friendliness in mind, making it suitable for various retail and service-based businesses.

Key Features:
- Real-time sales tracking and management
- Comprehensive inventory management system
- Customer transaction history
- User authentication and authorization
- Admin dashboard for system management
- Sales reports and analytics
- Product categorization and management

## System Screenshots

### Dashboard View
![Dashboard](Screenshots/Screenshot%202025-04-29%20at%2007.22.20.png)

### Product Management
![Product Management](Screenshots/Screenshot%202025-04-29%20at%2007.22.55.png)

### Sales Interface
![Sales Interface](Screenshots/Screenshot%202025-04-29%20at%2007.23.06.png)

### Inventory Overview
![Inventory Overview](Screenshots/Screenshot%202025-04-29%20at%2007.23.15.png)

### Customer Transactions
![Customer Transactions](Screenshots/Screenshot%202025-04-29%20at%2007.23.26.png)

### Reports and Analytics
![Reports and Analytics](Screenshots/Screenshot%202025-04-29%20at%2007.23.35.png)

## Technologies Used
- **Backend Framework**: 
  - Django 4.x (Python web framework)
  - Django REST framework for API endpoints
  - Django ORM for database operations
- **Database**: 
  - SQLite (Development)
  - Support for PostgreSQL (Production-ready)
- **Frontend**: 
  - HTML5 for structure
  - CSS3 with Material Design for styling
  - JavaScript for dynamic functionality
  - jQuery for DOM manipulation
  - Bootstrap for responsive design
- **Development Tools**:
  - Python Virtual Environment for dependency isolation
  - Django Admin Interface for backend management
  - SQLite Database for data storage
  - Git for version control
  - pip for package management

## Setup Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)
- Git (for version control)

### Installation Steps

1. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   # Install required packages
   pip install -r requirements.txt
   
   # Verify installation
   pip list
   ```

3. **Set up the database**
   ```bash
   # Apply database migrations
   python manage.py migrate
   
   # Verify database setup
   python manage.py showmigrations
   ```

4. **Create admin user**
   ```bash
   # Create superuser account
   python manage.py createsuperuser
   
   # Follow prompts to set up admin credentials
   # Username: [your choice]
   # Email: [your email]
   # Password: [secure password]
   ```

5. **Run the development server**
   ```bash
   # Start development server
   python manage.py runserver
   
   # Server will run on http://127.0.0.1:8000
   ```

6. **Access the application**
   - Main application: `http://127.0.0.1:8000`
   - Admin interface: `http://127.0.0.1:8000/admin`
   - API endpoints: `http://127.0.0.1:8000/api/`

### Additional Configuration
- Configure static files:
  ```bash
  python manage.py collectstatic
  ```
- Set up environment variables in `.env` file
- Configure database settings in `settings.py`
- Set up email backend for notifications

### Troubleshooting
- If you encounter port conflicts, use:
  ```bash
  python manage.py runserver 8001
  ```
- For database issues, try:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- Clear cache if needed:
  ```bash
  python manage.py clear_cache
  ``` 