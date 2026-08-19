from google.cloud import bigquery as bq

client = bq.Client()

query = open("sql/user_silver.sql").read()

client.query(query).result()

print("Silver Load Completed")