# RetailAI Copilot — integration runbook

## Local (no cloud required)
1. Copy `.env.example` to `.env` and replace `DEMO_API_TOKEN` with a random long value.
2. `docker compose up --build`
3. Open `http://localhost:3000` and paste the token in the password field.
4. Check API at `http://localhost:8000/health`.
5. Optional vector RAG: set `INSTALL_VECTOR=true` and `RAG_BACKEND=vector`, then rebuild; first query downloads embedding model.
6. Tests: `python -m pip install -r requirements.txt && python -m pytest -q`.

## MCP (trusted local client)
`python -m pip install -r requirements-data.txt` then `python -m app.mcp_server`.
MCP is stdio-only. Scopes are enforced server-side by `DEMO_ALLOWED_BRANDS`, `DEMO_ALLOWED_COUNTRIES`, `DEMO_ROLE`.

## BigQuery + dbt (requires GCP account; not auto-deployed)
1. Install `requirements-data.txt`, authenticate with `gcloud auth application-default login`.
2. Set `GCP_PROJECT_ID`, `BIGQUERY_DATASET=retailai_demo`, `BIGQUERY_LOCATION=EU`.
3. `python scripts/upload_bigquery.py` to create and load `ventes_raw`.
4. Copy `dbt/profiles.example.yml` to `~/.dbt/profiles.yml`, update GCP project.
5. `cd dbt && dbt debug && dbt run && dbt test`.
6. RLS SQL in `cloud/bigquery_rls_example.sql` is an administrator-only example; replace placeholders and verify permissions with real user identities.

## Airflow (optional)
`docker compose --profile orchestration up --build airflow` (optional profile, first-time initialization).
Open `http://localhost:8080`, then manually trigger `retailai_data_pipeline`.
This DAG validates local files only. BigQuery upload is a separate explicit command to prevent surprise charges.

## Cloud Run (private API example)
Requires a GCP project, service account, Secret Manager secret and configured `gcloud` CLI. Run `cloud/deploy-cloud-run.sh` after inspecting the script. This deployment is **not** production-ready: local SQLite and Chroma are ephemeral on Cloud Run. Replace with managed persistent services and OIDC before any public rollout.

## Known limitations
- All commercial sales are synthetic. Moroccan stock movements are user-provided demo data and not official Hoortrade data.
- Oracle connector is a connection-check script and Oracle staging SQL; Oracle is **not** wired into the API.
- The document corpus contains fictional examples; there is no per-tenant document authorization.
- Shared demo token is not production IAM; IAM and RLS require real cloud setup.
- No live integration with Hoortrade systems. No claim of official affiliation.
