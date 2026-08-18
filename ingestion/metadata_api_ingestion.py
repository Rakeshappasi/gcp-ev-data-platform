from google.cloud import bigquery

client = bigquery.Client()

query = '''
select * from  metadata_ds.source_config
where active_flag ='Y'
'''
df = client.query(query).to_dataframe()

print(df)