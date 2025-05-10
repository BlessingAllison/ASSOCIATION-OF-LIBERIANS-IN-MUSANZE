FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmysqlclient-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install bower globally
RUN npm install -g bower

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install bower components
RUN bower install

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "e_voting.wsgi:application", "--bind", "0.0.0.0:$PORT"]
