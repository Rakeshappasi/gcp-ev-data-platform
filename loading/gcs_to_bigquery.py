from google.cloud import bigquery

client= bigquery.Client()

query= '''select count(*) from bronze_ds.users'''

df = client.query(query).to_dataframe()


print(df)