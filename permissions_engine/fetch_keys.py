import requests
import json
import os

MY_KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM_URL")

data = dict()
data["keys"] = []

response = requests.get(MY_KEYCLOAK_REALM + "/.well-known/openid-configuration")
json_data = json.loads(response.text)
jwks = requests.get(json_data["jwks_uri"]).text
data["keys"].append({"iss": MY_KEYCLOAK_REALM, "cert": jwks})
with open('/app/data.json', 'w') as f:
    json.dump(data, f)
