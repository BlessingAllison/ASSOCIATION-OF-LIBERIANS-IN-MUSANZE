"""
WSGI config for e_voting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_voting.settings')

# This application object is used by the development server and any WSGI server.
application = get_wsgi_application()

# Apply WhiteNoise middleware
application = WhiteNoise(
    application,
    root=os.path.join(BASE_DIR, 'staticfiles'),
    prefix='static/'
)

# Add static files from the main static directory
main_static = os.path.join(BASE_DIR, 'static')
if os.path.exists(main_static):
    application.add_files(main_static, prefix='static/')

# Add static files from app directories
for app in os.listdir(BASE_DIR):
    app_static = os.path.join(BASE_DIR, app, 'static')
    if os.path.exists(app_static) and os.path.isdir(app_static):
        application.add_files(app_static, prefix='static/')
