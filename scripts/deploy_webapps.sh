#!/usr/bin/env bash
set -euo pipefail

# Required env vars
: "${AZ_RESOURCE_GROUP:?AZ_RESOURCE_GROUP is required}"
: "${AZ_REGION:?AZ_REGION is required}"
: "${FRONTEND_APP_NAME:?FRONTEND_APP_NAME is required}"
: "${BACKEND_APP_NAME:?BACKEND_APP_NAME is required}"

PLAN_NAME="${APP_SERVICE_PLAN_NAME:-tableau-aml-poc-plan}"
RUNTIME="PYTHON:3.11"

az group create --name "$AZ_RESOURCE_GROUP" --location "$AZ_REGION"

az appservice plan create \
  --name "$PLAN_NAME" \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --is-linux \
  --sku B1

az webapp create \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --plan "$PLAN_NAME" \
  --runtime "$RUNTIME"

az webapp create \
  --name "$FRONTEND_APP_NAME" \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --plan "$PLAN_NAME" \
  --runtime "$RUNTIME"

echo "Now deploy backend and frontend code (zip deploy or GitHub actions), then set startup commands:"
echo "Backend startup: gunicorn --bind=0.0.0.0 --timeout 600 api:app"
echo "Frontend startup: streamlit run frontend/app.py --server.port 8000 --server.address 0.0.0.0"
