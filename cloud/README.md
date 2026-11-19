# Cloud / IAM / RLS
- `deploy-cloud-run.sh`: private Cloud Run API deployment template. Requires configured GCP project, service account, Secret Manager secret and gcloud.
- `bigquery_rls_example.sql`: example BigQuery row access policy. Replace placeholders and adapt groups to actual organization.
- Cloud Run IAM controls who can invoke the service; API demo token is additional **demo-only** authorization and does not validate Google OIDC.
- Do **not** deploy publicly without replacing demo authentication with validated Google identity tokens, real tenant-aware document ACLs, managed SQL/vector storage, monitoring and security review.
- Docker/SQLite/Chroma persistent volume works locally; Cloud Run container storage is ephemeral. Use managed external storage for persistence.
