import requests
import os
import sys


IDP_OPENCONNECT = os.getenv("IDP") + "/protocol/openid-connect"
idp_map = {
    "oidc": IDP_OPENCONNECT
}

client_id = os.getenv("IDP_CLIENT_ID")

client_secret = os.getenv("IDP_CLIENT_SECRET")
if client_secret is None:
    with open("/run/secrets/idp_client_secret", "r") as f:
        client_secret = f.read().strip()

def helper_get_user_token(username, password, oidc_name="oidc"):
    oidc = idp_map[oidc_name]
    payload = {'grant_type': 'password',
               'username': username,
               'password': password,
               'redirect_uri': "http://fake_beacon:8000/auth/oidc"}
    response = requests.post(f"{oidc}/token", auth=(client_id, client_secret), data=payload)
    token = response.json()['access_token']
    return token

if __name__ == '__main__':
    print(helper_get_user_token(sys.argv[1], sys.argv[2], sys.argv[3]))
