import json

import requests

url = "https://www.cheapshark.com/api/1.0/deals?upperPrice=15"

payload = {}
headers = {}

r = requests.get(url)
data = r.json()
json_object = json.dumps(data, indent=3)
with open("data.json", "w") as outfile:
    outfile.write(json_object)
