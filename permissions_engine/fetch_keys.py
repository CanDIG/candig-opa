import requests
import json

data = dict()
data["keys"] = dict()
issuers = [("http://localhost:8080/auth/realms/mockrealm", "https://oidc1:8443/auth/realms/mockrealm"),
            ("http://localhost:8081/auth/realms/mockrealm", "https://oidc2:8443/auth/realms/mockrealm")]

for (external, internal) in issuers:
    response = requests.get(external + "/.well-known/openid-configuration")
    json_data = json.loads(response.text)
    jwks = requests.get(json_data["jwks_uri"]).text
    data["keys"][internal] = jwks

with open('permissions_engine/data.json', 'w') as f:
    json.dump(data, f)