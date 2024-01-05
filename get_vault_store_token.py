import json
import os
from authx.auth import get_vault_token_for_service
import sys
import requests


# get the token for the opa store
try:
    opa_token = get_vault_token_for_service("opa")
    headers = {
        "X-Opa": os.getenv("OPA_ROOT_TOKEN"),
        "Content-Type": "application/json; charset=utf-8"
    }
    json = {
        "token": opa_token
    }
    response = requests.put(url=f"{os.getenv('OPA_URL')}/v1/data/store_token", headers=headers, json=json)
except:
    sys.exit(1)
