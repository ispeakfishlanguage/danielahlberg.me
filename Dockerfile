FROM python:3.11-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install system dependencies for Pillow (image processing) and PostgreSQL
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . .

# Create media and static directories
RUN mkdir -p media/photos media/thumbnails staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn (note: photography_config not photography_site)
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 0 photography_config.wsgi:application
