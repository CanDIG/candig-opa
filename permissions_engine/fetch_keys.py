import requests
import json
import os

IDP1 = os.getenv("OIDC1", "https://oidc1:8443/auth/realms/mockrealm")
IDP2 = os.getenv("OIDC2", "https://oidc2:8443/auth/realms/mockrealm")

data = dict()
data["keys"] = dict()
issuers = [(IDP1, "https://oidc1:8443/auth/realms/mockrealm"),
            (IDP2, "https://oidc2:8443/auth/realms/mockrealm")]

for (external, internal) in issuers:
    response = requests.get(external + "/.well-known/openid-configuration")
    json_data = json.loads(response.text)
    jwks = requests.get(json_data["jwks_uri"]).text
    data["keys"][external] = jwks

data["keys"]["https://keycloakdev01.bcgsc.ca/auth/realms/HOSTSEQ"] = json.dumps({"keys":[{"kid":"vkTPEgwcx3IkgC8leYOzI-j_sD0tyFsLcWi_6ukf_rs","kty":"RSA","alg":"RS256","use":"sig","n":"vuzTAenhQhjtTcowJuEl-dhqTNUVwo8vwhPMoxR3-AhotOPkfeaVH502ThdurGXeqsxX59XVcXrvxu4Fishp2NiDfh5PQ0HxRxE-4xZvk7yfdLJMO2SzDO3Ep5mxBWSDkXtD0USqWJ6SerWDJma4rq3G_7hE8C8do889yDr9r22b3v8Ge0Qd1nYjtnw-4dbaGkTfcN2PQqBtv08cv-7W1UIBJhXBq-GjLXyC_wWU1RHNg4-Zmqdnr08IyEfLz0bsgVPlrwHaVudiRxgVBnllwQTzUio15qJ36B6jbW8C6Zvu6j3F0xJ8Id-eK5k0JJPXfPLhszuhd2bVeN7NAOab4w","e":"AQAB"}]})

with open('permissions_engine/data.json', 'w') as f:
    json.dump(data, f)
