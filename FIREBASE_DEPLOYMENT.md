# Firebase Deployment Fix

## The Problem

Firebase Hosting uses buildpacks by default, which doesn't work well with Django applications. The error:
```
ERROR: No buildpack groups passed detection.
```

This happens because Firebase can't auto-detect Django projects using buildpacks.

## The Solution

Deploy to **Google Cloud Run** (not Firebase Hosting) using Docker. Firebase Hosting can then be used as a CDN in front of Cloud Run.

## Step-by-Step Deployment

### Option 1: Direct Cloud Run Deployment (Recommended)

```bash
# 1. Set your project ID
export PROJECT_ID=your-firebase-project-id
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# 3. Deploy using Cloud Build (uses your Dockerfile)
gcloud builds submit --config cloudbuild.yaml

# 4. Get your service URL
gcloud run services describe danielahlberg-app \
  --region us-central1 \
  --format='value(status.url)'
```

### Option 2: Manual Docker Build

```bash
# 1. Build Docker image
docker build -t gcr.io/$PROJECT_ID/danielahlberg-app .

# 2. Push to Container Registry
docker push gcr.io/$PROJECT_ID/danielahlberg-app

# 3. Deploy to Cloud Run
gcloud run deploy danielahlberg-app \
  --image gcr.io/$PROJECT_ID/danielahlberg-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

### Option 3: Firebase Hosting + Cloud Run (CDN)

After deploying to Cloud Run, you can use Firebase Hosting as a CDN:

```bash
# 1. First deploy to Cloud Run (see Option 1)

# 2. Update .firebaserc with your project ID
# Replace "your-project-id" with your actual Firebase project ID

# 3. Update firebase.json "serviceId" to match your Cloud Run service name

# 4. Deploy Firebase Hosting
firebase deploy --only hosting
```

## Environment Variables

Set these using Secret Manager or Cloud Run environment variables:

```bash
# Create secrets
echo -n "your-secret-key" | gcloud secrets create SECRET_KEY --data-file=-
echo -n "postgresql://..." | gcloud secrets create DATABASE_URL --data-file=-

# Update Cloud Run service to use secrets
gcloud run services update danielahlberg-app \
  --region us-central1 \
  --update-secrets \
  SECRET_KEY=SECRET_KEY:latest,\
  DATABASE_URL=DATABASE_URL:latest,\
  FIREBASE_CREDENTIALS=FIREBASE_CREDENTIALS:latest,\
  FIREBASE_API_KEY=FIREBASE_API_KEY:latest,\
  FIREBASE_AUTH_DOMAIN=FIREBASE_AUTH_DOMAIN:latest,\
  FIREBASE_PROJECT_ID=FIREBASE_PROJECT_ID:latest
```

## Why Not Firebase Hosting Directly?

Firebase Hosting is designed for:
- Static sites (HTML, CSS, JS)
- Single Page Applications (React, Vue, Angular)
- Cloud Functions (Node.js serverless functions)

**NOT** for:
- Django/Flask/FastAPI applications
- Traditional server-side frameworks
- Applications requiring system dependencies

## The Right Architecture

```
┌─────────────────────┐
│  Firebase Hosting   │  <- Optional CDN layer
│   (Static files)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Cloud Run         │  <- Your Django app runs here
│  (Docker container) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Cloud SQL         │  <- PostgreSQL database
│  (PostgreSQL)       │
└─────────────────────┘
```

## Quick Deploy Script

```bash
#!/bin/bash
export PROJECT_ID=your-project-id
gcloud builds submit --config cloudbuild.yaml
```

## Troubleshooting

**Error: "buildpack(s) failed"**
- Don't use `firebase deploy` for the Django app
- Use `gcloud builds submit` or `gcloud run deploy` instead

**Error: "permission denied"**
```bash
gcloud auth login
gcloud config set project $PROJECT_ID
```

**Error: "service not found"**
- The service name in `cloudbuild.yaml` must match
- Default is `danielahlberg-app`

**Static files not loading**
- Run `python manage.py collectstatic` (done in Dockerfile)
- Check `STATIC_URL` and `STATIC_ROOT` in settings.py
- Verify WhiteNoise is configured

## Cost Estimate

- Cloud Run: $0.00002400/vCPU-second, first 2 million requests free
- Cloud SQL (db-f1-micro): ~$7.67/month
- Container Registry: $0.026/GB/month
- Firebase Hosting: 10 GB free, then $0.026/GB

For a small portfolio site: **~$8-15/month**
