from google.cloud import bigquery as bq

client =bq.Client()

query = open("sql/silver_validation.sql").read()

df= client.query(query).to_dataframe()

print(df)