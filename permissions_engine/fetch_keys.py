import requests
import json
import os

IDP = os.getenv("IDP")

data = dict()
data["keys"] = []
issuers = [IDP]

for external in issuers:
    response = requests.get(external + "/.well-known/openid-configuration")
    json_data = json.loads(response.text)
    jwks = requests.get(json_data["jwks_uri"]).text
    data["keys"].append({"iss": external, "cert": jwks})
with open('/app/data.json', 'w') as f:
    json.dump(data, f)
