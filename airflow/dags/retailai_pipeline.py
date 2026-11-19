"""Optional DAG: validate synthetic CSV and optionally load BigQuery with ADC."""
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
with DAG('retailai_data_pipeline',start_date=datetime(2026,1,1),schedule=None,catchup=False,
         tags=['retailai','demo']) as dag:
    validate=BashOperator(task_id='validate_csv',bash_command='cd /opt/airflow/retailai && python scripts/validate_data.py')
    # BigQuery upload is opt-in; avoid accidental cloud charges / missing credentials.
    # To run manually: python scripts/upload_bigquery.py (after GCP auth).
