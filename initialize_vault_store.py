import json
import os
from authx.auth import set_service_store_secret, add_provider_to_opa
import sys

## Initializes Vault's opa service store with the information for our IDP and the data in access.json and paths.json

results = []

try:
    with open('/app/bearer.txt') as f:
        try:
            token = f.read().strip()
            response, status_code = set_service_store_secret("opa", key="data", value=json.dumps({"keys":[]}))
            response = add_provider_to_opa(token, os.getenv("KEYCLOAK_REALM_URL"))
            results.append(response)
        except Exception as e:
            print(str(e))
            sys.exit(1)

    with open('/app/permissions_engine/access.json') as f:
        data = f.read()
        response, status_code = set_service_store_secret("opa", key="access", value=data)
        if status_code != 200:
            sys.exit(2)
        results.append(response)

    with open('/app/permissions_engine/paths.json') as f:
        data = f.read()
        response, status_code = set_service_store_secret("opa", key="paths", value=data)
        if status_code != 200:
            sys.exit(3)
        results.append(response)

    with open('/app/permissions_engine/roles.json') as f:
        data = f.read()
        response, status_code = set_service_store_secret("opa", key="roles", value=data)
        if status_code != 200:
            sys.exit(2)
        results.append(response)
except Exception as e:
    print(str(e))
    sys.exit(4)

# print(json.dumps(results, indent=4))
sys.exit(0)
