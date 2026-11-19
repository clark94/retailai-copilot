"""Load synthetic CSV to BigQuery with explicit schema. Requires ADC and project permissions."""
import os
from pathlib import Path
from google.cloud import bigquery

def main():
    project=os.environ['GCP_PROJECT_ID']
    dataset=os.getenv('BIGQUERY_DATASET','retailai_demo')
    location=os.getenv('BIGQUERY_LOCATION','EU')
    client=bigquery.Client(project=project,location=location)
    ds=bigquery.Dataset(f'{project}.{dataset}');ds.location=location
    client.create_dataset(ds,exists_ok=True)
    schema=[bigquery.SchemaField(name,typ) for name,typ in [
      ('id_commande','STRING'),('date_commande','DATE'),('id_client','STRING'),('pays','STRING'),
      ('marque','STRING'),('id_produit','STRING'),('categorie','STRING'),('produit','STRING'),
      ('quantite','INTEGER'),('prix_unitaire_eur','FLOAT'),('remise_pct','FLOAT'),
      ('montant_total_eur','FLOAT'),('statut_commande','STRING'),('stock_disponible','INTEGER'),('canal_vente','STRING')]]
    table=f'{project}.{dataset}.ventes_raw'
    job_config=bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV,
      skip_leading_rows=1,schema=schema,write_disposition='WRITE_TRUNCATE',
      max_bad_records=0)
    file=Path(__file__).resolve().parents[1]/'data'/'ventes_synthetiques.csv'
    with file.open('rb') as handle:
        job=client.load_table_from_file(handle,table,job_config=job_config,location=location)
    job.result()
    print('Loaded',client.get_table(table).num_rows,'rows into',table)
if __name__=='__main__':main()
