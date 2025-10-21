# Deployment Guide

This guide covers deploying the Django photography portfolio to Google Cloud Platform.

## Prerequisites

1. Google Cloud SDK installed: https://cloud.google.com/sdk/docs/install
2. Docker installed (optional, for local testing)
3. Active Google Cloud Project with billing enabled
4. Firebase project configured

## Environment Variables

Set these in Google Cloud Secret Manager or Cloud Run environment variables:

```bash
SECRET_KEY=your-django-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-key
CLOUDINARY_API_SECRET=your-cloudinary-secret
FIREBASE_CREDENTIALS={"type":"service_account",...}
FIREBASE_API_KEY=your-firebase-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123:web:abc
```

## Deployment Methods

### Method 1: Cloud Run with Cloud Build (Recommended)

This is the easiest method using the Dockerfile and cloudbuild.yaml.

```bash
# 1. Set your project ID
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com

# 3. Create secrets in Secret Manager
echo -n "your-secret-key" | gcloud secrets create SECRET_KEY --data-file=-
echo -n "postgresql://..." | gcloud secrets create DATABASE_URL --data-file=-
# ... create other secrets

# 4. Submit build and deploy
gcloud builds submit --config cloudbuild.yaml

# 5. Update environment variables in Cloud Run
gcloud run services update danielahlberg-app \
  --region us-central1 \
  --update-secrets SECRET_KEY=SECRET_KEY:latest,DATABASE_URL=DATABASE_URL:latest
```

### Method 2: Direct Docker Build and Deploy

```bash
# 1. Build the Docker image
docker build -t gcr.io/$PROJECT_ID/danielahlberg-app .

# 2. Push to Google Container Registry
docker push gcr.io/$PROJECT_ID/danielahlberg-app

# 3. Deploy to Cloud Run
gcloud run deploy danielahlberg-app \
  --image gcr.io/$PROJECT_ID/danielahlberg-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "DJANGO_SETTINGS_MODULE=photography_config.settings"
```

### Method 3: App Engine (Alternative)

```bash
# 1. Update app.yaml with your environment variables
# 2. Deploy to App Engine
gcloud app deploy

# 3. View your app
gcloud app browse
```

## Post-Deployment

### 1. Run Migrations

```bash
# Get Cloud Run service URL
SERVICE_URL=$(gcloud run services describe danielahlberg-app \
  --region us-central1 \
  --format 'value(status.url)')

# Run migrations (connect to Cloud SQL or use Cloud Run jobs)
gcloud run jobs create migrate-db \
  --image gcr.io/$PROJECT_ID/danielahlberg-app \
  --command python \
  --args manage.py,migrate \
  --region us-central1

gcloud run jobs execute migrate-db --region us-central1
```

### 2. Create Superuser

```bash
# Connect to Cloud Run instance
gcloud run services proxy danielahlberg-app --region us-central1

# In another terminal
docker exec -it <container-id> python manage.py createsuperuser
```

### 3. Configure Custom Domain

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service danielahlberg-app \
  --domain danielahlberg.me \
  --region us-central1
```

## Database Setup

### Cloud SQL (PostgreSQL)

```bash
# 1. Create Cloud SQL instance
gcloud sql instances create photography-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1

# 2. Create database
gcloud sql databases create photography_db --instance=photography-db

# 3. Create user
gcloud sql users create django_user \
  --instance=photography-db \
  --password=your-secure-password

# 4. Get connection name
gcloud sql instances describe photography-db --format='value(connectionName)'

# 5. Update DATABASE_URL
# postgresql://django_user:password@//cloudsql/PROJECT:REGION:INSTANCE/photography_db
```

## Monitoring

```bash
# View logs
gcloud run services logs read danielahlberg-app --region us-central1

# Monitor metrics
gcloud run services describe danielahlberg-app --region us-central1
```

## Troubleshooting

### Build Fails

- Check `cloudbuild.yaml` syntax
- Verify all dependencies in `requirements.txt`
- Check Docker build locally: `docker build -t test .`

### Runtime Errors

- Check environment variables are set correctly
- View logs: `gcloud run services logs read`
- Verify database connection

### Static Files Not Loading

- Ensure `python manage.py collectstatic` runs in Dockerfile
- Configure WhiteNoise in settings.py (already done)
- Check STATIC_ROOT and STATIC_URL settings

## Cost Optimization

1. Use Cloud Run (pay per request) instead of App Engine
2. Use Cloud SQL shared-core instances for development
3. Use Cloudinary for media storage (already configured)
4. Enable autoscaling with min instances = 0

## Security Checklist

- [ ] Set DEBUG=False in production
- [ ] Use Secret Manager for sensitive data
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Enable HTTPS (automatic on Cloud Run)
- [ ] Set up CSRF_TRUSTED_ORIGINS
- [ ] Configure Cloud Armor for DDoS protection
- [ ] Enable Cloud SQL SSL connections
- [ ] Regular security updates
