#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media

# Set proper permissions
chmod -R 755 staticfiles
chmod -R 755 media

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py create_superuser --noinput || true
