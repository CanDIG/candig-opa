import requests
import os
import sys
IDP1_OPENCONNECT = os.getenv("OIDC1_OPENCONNECT", "https://oidc1:8443/auth/realms/mockrealm/protocol/openid-connect")
IDP2_OPENCONNECT = os.getenv("OIDC2_OPENCONNECT", "https://oidc2:8443/auth/realms/mockrealm/protocol/openid-connect")
client_id = os.getenv("IDP_CLIENT_ID", "mock_login_client")
client_secret = os.getenv("IDP_CLIENT_SECRET", "mock_login_secret")
idp_map = {
    "oidc1": IDP1_OPENCONNECT,
    "oidc2": IDP2_OPENCONNECT
}

def helper_get_user_token(username, password, oidc_name="oidc1"):
    oidc = idp_map[oidc_name]
    payload = {'grant_type': 'password',
               'username': username,
               'password': password,
               'redirect_uri': "http://fake_beacon:8000/auth/oidc"}
    response = requests.post(f"{oidc}/token", auth=(client_id, client_secret), data=payload)
    token = response.json()['access_token']
    return token

print(helper_get_user_token(sys.argv[1], sys.argv[2], sys.argv[3]))