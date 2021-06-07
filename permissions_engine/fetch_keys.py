import requests
import json
issuers = ["http://localhost:8080/auth/realms/mockrealm"]

data = dict()
data["keys"] = dict()
data["keys"]["https://oidc:8443/auth/realms/mockrealm"] = requests.get("http://localhost:8080/auth/realms/mockrealm/protocol/openid-connect/certs").text



#
# issuer and where certs get fetched from do not match 
# can't use solution below
#
# for i in issuers:
#     response = requests.get(i + "/.well-known/openid-configuration")
#     json_data = json.loads(response.text)
#     jwks = json.loads(requests.get(json_data["jwks_uri"]).text)
#     data["keys"][i] = jwks

with open('permissions_engine/data.json', 'w') as f:
    json.dump(data, f)