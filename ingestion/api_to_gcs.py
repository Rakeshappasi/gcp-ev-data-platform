import requests
import json
from datetime import datetime
from google.cloud import storage

#'''
#onfiguration
#'''
Bucket_Name  = "ev-data-lake-rakesh"

api_url = (
    "https://jsonplaceholder.typicode.com/users"
)

#-------------------------------
#API CALL
#____________________________________

print("Calling API")

response = requests.get(api_url)
response.raise_for_status()
data = response.json()
print(
    f"successfully Extracted "
    f"{len(data)} records"
)

#____________________________
#Create File Name
#___________________________
timestamp =datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"users_{timestamp}.json"

#____________________________
#Save file Local
#______________________________

with open(filename, 'w') as file:
    for record in data:
        file.write(json.dumps(record) + "\n")
print(f"local file created :{filename}")

#Upload to GCS

client = storage.Client()
bucket =  client.bucket(Bucket_Name)
blob = bucket.blob(f"bronze/raw/users/{filename}")

blob.upload_from_filename(filename)

print("Uploaded to Bucket")