import os

print("Running api ingestion")

os.system("python ingestion/api_to_gcs.py")
print("running meatadata process....")
os.system("python ingestion/metadata_api_ingestion.py")
print("pipeline completed")
