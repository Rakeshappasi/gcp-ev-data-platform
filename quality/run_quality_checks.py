from google.cloud import bigquery as bq

client = bq.Client()

query ='''select countif(id is null) as null_ids from silver_ds.users_clean'''

df= client.query(query).to_dataframe()

if df["null_ids"][0]==0:
    print("null check pass")
else:
    print("null check fail")

