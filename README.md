# Rego Development Playground

[![Build Status](https://travis-ci.com/CanDIG/rego_development_playground.svg?branch=main)](https://travis-ci.com/CanDIG/rego_development_playground)

![Diagram showing interactions between services](./diagram.png)

## Running

Generate internal TLS certificates, self-signed by a root CA:

```
./generate-certs.sh
```

You'll be asked for a passphrase for the signing key and to validate it, and then asked for that key three times more.

Once done, fire everything up - currently that's the IdP (Keycloak), permission engine (OPA), and fake_beacon, which
plays role of a beacon here - triggering login and requesting permissions, and a shim between the fake_beacon and
opa:

```
docker-compose up -d
```

Then create the realm and the users (user1 and user2), with user1 being a trusted researcher.
In the OPA configuration, user1 has  access to controlled dataset #4, (and registered #3 since they are a trusted researcher)
and user2 is has access to controlled dataset #5.

```
 ./oidc/config-oidc-service
```

That restarts the IdP and so will take 20 seconds or so.

When keycloak is up and running (when `docker-compose logs oidc` shows `Admin console listening`), it should be ready to go.

In addition to the policies defined in OPA (the permissions engine), OPA directly connects to the IdP's userinfo
to validate the token.

When everything is ready, you can "log in" to the fake beacon; it currenly returns the access token to you, which of course
isn't realistic:

```
curl "http://localhost:8000/login?username=user1&password=pass1"

```

you can capture the tokens as:

```
TOKEN1=$( curl "http://localhost:8000/login?username=user1&password=pass1" | jq .access_token | tr -d \" )
TOKEN2=$( curl "http://localhost:8000/login?username=user2&password=pass2" | jq .access_token | tr -d \" )
```

then you can have the beacon query the permissions server:

```
curl "http://localhost:8000/permissions?token=${TOKEN1}" | jq .
curl "http://localhost:8000/permissions?token=${TOKEN2}" | jq .
```

Both users can access the open data sets, only trusted researcher `user1` can access the registered datset,
and each can access their particular controlled dataset.

You can query the permission for COUNT in case some datasets might opt in for COUNT permission to everyone with valid token:
```
curl "http://localhost:8000/permissions_count?token=${TOKEN1}" | jq .
curl "http://localhost:8000/permissions_count?token=${TOKEN2}" | jq .
```
Both tokens can access open datasets and controlled4 dataset which opts in for COUNT permission.

You can test a properly signed expired token and should only get the open datasets

```
curl "http://localhost:8000/permissions?token=$(cat expired_token)" | jq .
```
