#!/usr/bin/env python3
"""
A thin shim between the beacon and the OPA server to align beacon
developer preferences with microservices/kubernetes style service
authentication.
"""
import argparse
import os
import connexion
import requests

rootCA = os.getenv("ROOT_CA", None)
permissions_server = os.getenv("PERMISSIONS_ENGINE",
                               "https://opa:8181/v1/data/permissions/datasets")

def permissions(request):
    """
    flip the secrets, pass forward to the permissions engine
    """
    user_token = connexion.request.headers['Authorization'].split(' ')[1]
    client_secret = request['clientSecret']
    response = requests.post(permissions_server,
                             headers={"Authorization": f"Bearer {client_secret}"},
                             json={"input": {"method": request['method'],
                                             "path": request['path'],
                                             "token": user_token}},
                             verify=rootCA)

    if response.status_code != 200:
        return response.reason, response.status_code

    body = response.json()
    if not 'result' in body:
        return 'Data not returned', 500

    return {'datasets': body['result']}


def main():
    """
    start the server
    """
    parser = argparse.ArgumentParser(description='Permissions shim.')
    parser.add_argument('--host', default="0.0.0.0", help='host to listen on')
    parser.add_argument('--port', default="8180", help="port to listen on")
    parser.add_argument('--tls_key', default="/tls.key", help="path to private key")
    parser.add_argument('--tls_cert', default="/tls.crt", help="path to tls cert")
    args = parser.parse_args()

    options = {"swagger_ui": False}
    app = connexion.FlaskApp(__name__, specification_dir='swagger/', options=options)
    app.add_api("swagger.yaml")
    app.run(host=args.host, port=args.port, ssl_context=(args.tls_cert, args.tls_key))


if __name__ == "__main__":
    main()
