# Association of Liberians in Musanze Online Voting System

This is an online voting system for the Association of Liberians in Musanze, built with Django and MySQL.

## Features

- User authentication and authorization
- Multiple voting positions
- Candidate management
- Voter registration and verification
- Secure online voting
- Results tracking and display

## Requirements

- Python 3.12+
- Django 3.1.7
- MySQL 9.3.0
- mysql-connector-python

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ASSOCIATION-OF-LIBERIANS-IN-MUSANZE.git
cd ASSOCIATION-OF-LIBERIANS-IN-MUSANZE
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MySQL:
- Install MySQL
- Create a database named 'voting_system'
- Update database settings in `e_voting/settings.py` if needed

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

## Usage

- Access the admin panel at http://127.0.0.1:8000/admin/
- Register voters and candidates through the admin panel
- Configure voting positions
- Allow voters to cast their votes

## Security

- All passwords are hashed
- Secure password validation
- CSRF protection
- SSL/TLS recommended for production

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
