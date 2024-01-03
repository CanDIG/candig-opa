import json
import os
from authx.auth import set_service_store_secret
import sys

results = []
with open('/app/data.json') as f:
    data = "\n".join(f.readlines())
    response, status_code = set_service_store_secret("opa", key="data", value=json.loads(data))
    if status_code != 200:
        sys.exit(1)
    results.append(response)

with open('/app/permissions_engine/access.json') as f:
    data = "\n".join(f.readlines())
    response, status_code = set_service_store_secret("opa", key="access", value=json.loads(data))
    if status_code != 200:
        sys.exit(2)
    results.append(response)

with open('/app/permissions_engine/paths.json') as f:
    data = "\n".join(f.readlines())
    response, status_code = set_service_store_secret("opa", key="paths", value=json.loads(data))
    if status_code != 200:
        sys.exit(3)
    results.append(response)

print(json.dumps(results))
