#!/usr/bin/env bash
set -euo pipefail
: "${GCP_PROJECT:?Set GCP_PROJECT}"
: "${GCP_REGION:=europe-west1}"
: "${SERVICE_ACCOUNT:?Set SERVICE_ACCOUNT to existing service account email}"
: "${DEMO_TOKEN_SECRET:?Set DEMO_TOKEN_SECRET to existing Secret Manager secret name}"
gcloud config set project "$GCP_PROJECT"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
# Private, stateless demo only. Local SQLite/Chroma files are ephemeral on Cloud Run.
gcloud run deploy retailai-api --source . --region "$GCP_REGION" \
 --service-account "$SERVICE_ACCOUNT" --no-allow-unauthenticated \
 --set-secrets "DEMO_API_TOKEN=${DEMO_TOKEN_SECRET}:latest" \
 --set-env-vars "DEMO_ROLE=analyst,DEMO_ALLOWED_COUNTRIES=France,RAG_BACKEND=tfidf"
