import requests
import os
import sys
IDP_OPENCONNECT = os.getenv("IDP") + "/protocol/openid-connect"
client_id = os.getenv("IDP_CLIENT_ID", "mock_login_client")
client_secret = os.getenv("IDP_CLIENT_SECRET", "mock_login_secret")
idp_map = {
    "oidc": IDP_OPENCONNECT
}

def helper_get_user_token(username, password, oidc_name="oidc"):
    oidc = idp_map[oidc_name]
    payload = {'grant_type': 'password',
               'username': username,
               'password': password,
               'redirect_uri': "http://fake_beacon:8000/auth/oidc"}
    response = requests.post(f"{oidc}/token", auth=(client_id, client_secret), data=payload)
    token = response.json()['access_token']
    return token

print(helper_get_user_token(sys.argv[1], sys.argv[2], sys.argv[3]))
