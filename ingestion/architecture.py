import json
from datetime import datetime

'''
Read watermark
'''
with open(
    "config/watermark.json",
    "r"
)as file:
    watermark_data = json.load(file)
last_watermark = watermark_data["users"]

print(f"last watermark : {last_watermark}")

'''
simulate api call
'''
print("calling api..")

print("Api call successfull")

'''
update watermark
'''
new_watermark = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

watermark_data["users"] = (new_watermark)

with open("config/watermark.json", "w")as file:
    watermark_data = json.dump(watermark_data,file,indent=4)

print(f"new watermark : {new_watermark}")


