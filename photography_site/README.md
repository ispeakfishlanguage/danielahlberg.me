# Daniel Ahlberg Photography Portfolio

A Django-based photography portfolio website with client authentication and private gallery access.

## Features

- **Public Portfolio**: Minimalist photo gallery with category filtering
- **Client Authentication**: Secure login system for clients
- **Private Galleries**: Password-protected galleries for individual clients
- **Admin Interface**: Full content management system
- **Responsive Design**: Bootstrap-based responsive layout
- **Contact Form**: Integrated contact system with email notifications

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd photography_site
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` file with your settings:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to view the site.

## Admin Interface

Access the admin interface at `http://localhost:8000/admin/` to:

- Upload and manage photos
- Create categories
- Set up client profiles
- Create private galleries
- Manage contact messages

## Client Gallery System

### Setting Up Clients

1. Create a user account in Django admin
2. Create a `ClientProfile` linked to the user
3. Create one or more `Gallery` objects for the client
4. Add photos to the galleries
5. Optionally set password protection for galleries

### Client Login Process

1. Clients visit `/login/`
2. Enter username/password provided by photographer
3. Access private galleries at `/gallery/`
4. View individual galleries with full-resolution images

## Models Overview

- **Category**: Photo categories (Portrait, Landscape, etc.)
- **Photo**: Individual photos with metadata
- **ClientProfile**: Extended user profile for clients
- **Gallery**: Collections of photos for specific clients
- **ContactMessage**: Messages from the contact form

## Customization

### Adding New Categories

1. Go to Django admin
2. Add new `Category` objects
3. Set order and slug for URL routing

### Customizing Appearance

- Edit `static/css/style.css` for styling changes
- Modify templates in `templates/portfolio/`
- Update Google Fonts in `base.html`

### Email Configuration

Add email settings to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email'
EMAIL_HOST_PASSWORD = 'your-password'
```

## Security Features

- CSRF protection on all forms
- Login required for private galleries
- Password protection for sensitive galleries
- Session-based gallery access
- Secure file uploads with validation

## Production Deployment

1. Set `DEBUG=False` in production
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving (WhiteNoise included)
4. Configure email backend
5. Set secure headers and HTTPS

## File Structure

```
photography_site/
├── manage.py
├── photography_site/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
├── templates/
│   ├── base.html
│   └── portfolio/
├── static/
│   ├── css/
│   └── js/
└── media/
    ├── photos/
    └── thumbnails/
```

## Support

For questions or support, contact the development team or refer to Django documentation.