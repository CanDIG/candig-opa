import requests
import os
import sys
import json


def helper_get_permissions(token):
    opa_url = os.getenv("OPA_URL", "https://localhost:8181") + "/v1/data/permissions/datasets"

    payload = {
                'input': {
                  'token': token,
                  'body': {'method': 'GET', 'path': '/api/phenopackets'}
                }
              }

    headers = {
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer my-secret-root-token'
              }

    # NOTE!  Can't verify https using the certificate because from here 'outside' the
    # docker network, the hostname of 'opa' is 'localhost'.  You could fix this by
    # updating /etc/hosts etc.
    response = requests.post(opa_url, headers=headers, data=json.dumps(payload), verify=False)

    body = response.json()
    return body["result"]

if __name__ == '__main__':
    print(helper_get_permissions(sys.argv[1]))
