# Tableau + Azure ML POC

Small proof-of-concept with:
- Streamlit UI (Tableau iframe + upload button)
- Flask backend API (file upload + Azure ML pipeline trigger)
- Azure Blob Storage for uploaded input files

## Repo Structure

- `frontend/app.py`: Streamlit UI
- `backend/api.py`: Flask API endpoint (`/upload-trigger`)
- `backend/storage.py`: Blob upload helper
- `backend/aml_trigger.py`: AML pipeline submission helper
- `aml/pipeline_job.yml`: AML pipeline job template
- `aml/preview.py`: Sample AML command step script
- `scripts/run_local.sh`: Run backend + frontend locally
- `scripts/deploy_webapps.sh`: Create App Service resources (POC)

## 1. Conda Setup

```bash
conda activate tableau-aml-poc
cd /Users/ppant/tech/coding/github_repos/tableau-aml-poc
pip install -r requirements.txt
```

## 2. Configure Environment

```bash
cp .env.example .env
# edit .env with your values
```

Required values for Azure integration:
- `AZ_SUBSCRIPTION_ID`
- `AZ_RESOURCE_GROUP`
- `AZ_ML_WORKSPACE`
- `BLOB_ACCOUNT_URL` (or `AZURE_STORAGE_CONNECTION_STRING`)
- `BLOB_CONTAINER`

## 3. Run Locally

```bash
./scripts/run_local.sh
```

Then open:
- Streamlit: `http://localhost:8501`
- Backend health: `http://localhost:8000/health`

## 4. Azure ML Pipeline Notes

`aml/pipeline_job.yml` currently references:
- `compute: azureml:cpu-cluster`

Create AML compute with that name or update the YAML.

The backend updates `inputs.input_data` at runtime using uploaded blob URL.

## 5. Deploy To Azure (POC)

Create resources:

```bash
export AZ_RESOURCE_GROUP=<rg>
export AZ_REGION=<region>
export FRONTEND_APP_NAME=<unique-frontend-name>
export BACKEND_APP_NAME=<unique-backend-name>
./scripts/deploy_webapps.sh
```

Set web app startup commands:

Backend app (working dir `backend`):
```bash
gunicorn --bind=0.0.0.0 --timeout 600 api:app
```

Frontend app (repo root):
```bash
streamlit run frontend/app.py --server.port 8000 --server.address 0.0.0.0
```

Set environment variables in both apps as needed (`az webapp config appsettings set ...`).

## 6. Managed Identity + RBAC

For production-style auth (recommended over secrets):
- Enable system-assigned managed identity on backend web app.
- Grant backend app identity:
  - `Storage Blob Data Contributor` on Storage Account
  - AML workspace role with job submit permissions (e.g., Contributor scoped to workspace)

## 7. Tableau Embed

Set `TABLEAU_EMBED_URL` to your dashboard URL.

If dashboard is private, use Tableau embedding auth strategy separately; this POC assumes direct iframe-accessible URL.
