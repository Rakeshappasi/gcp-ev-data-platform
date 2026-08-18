from google.cloud import storage
bucket_name = "ev-data-lake-rakesh"
source_file = "datasets/ev_vechile_data.csv"
destination_blob = (
    "bronze/raw/ev_vechile_data.csv"
)
client = storage.Client()
bucket = client.bucket(bucket_name)
blob = bucket.blob(destination_blob)
blob.upload_from_filename(source_file)
print("upload successful")

