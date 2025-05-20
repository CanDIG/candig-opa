import json
from authx.auth import get_service_store_secret, set_service_store_secret
import sys

## Initializes Vault's opa service store with the data in site_roles.json, paths.json, programs.json

results = []

try:
    # response, status_code = get_service_store_secret("opa", key="paths")
    # if status_code != 200:
    with open('/app/defaults/paths.json') as f:
        data = f.read()
        response, status_code = set_service_store_secret("opa", key="paths", value=data)
        if status_code != 200:
            raise Exception(f"failed to save paths: {response} {status_code}")
        results.append(response)

    response, status_code = get_service_store_secret("opa", key="site_roles")
    if status_code != 200:
        with open('/app/defaults/site_roles.json') as f:
            data = f.read()
            response, status_code = set_service_store_secret("opa", key="site_roles", value=data)
            if status_code != 200:
                raise Exception(f"failed to save site roles: {response} {status_code}")
            results.append(response)

except Exception as e:
    print(str(e))
    sys.exit(4)

# initialize pending users
response, status_code = get_service_store_secret("opa", key="pending_users")
if status_code == 404:
    response, status_code = set_service_store_secret("opa", key="pending_users", value=json.dumps({"pending_users": {}}))
    if status_code != 200:
        sys.exit(2)

# initialize approved users
response, status_code = get_service_store_secret("opa", key="preapproved_users")
if status_code == 404:
    response, status_code = set_service_store_secret("opa", key="preapproved_users", value=json.dumps({"preapproved_users": []}))
    if status_code != 200:
        sys.exit(2)

# print(json.dumps(results, indent=4))
sys.exit(0)
