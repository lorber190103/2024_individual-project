import json

import requests

url = "https://www.cheapshark.com/api/1.0/deals?id=X8sebHhbc1Ga0dTkgg59WgyM506af9oNZZJLU9uSrX8%3D"

payload = {}
headers = {}

r = requests.get(url)
data = r.json()
json_object = json.dumps(data, indent=3)
with open("data.json", "w") as outfile:
    outfile.write(json_object)
