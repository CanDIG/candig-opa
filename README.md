# Rego Development Playground

[![Build Status](https://travis-ci.com/CanDIG/rego_development_playground.svg?branch=main)](https://travis-ci.com/CanDIG/rego_development_playground)

![Diagram showing interactions between services](./diagram.png)

## Running

Add katsu submodule to the current directory
```
git pull
git submodule update --init
```

Generate internal TLS certificates, self-signed by a root CA:

```
./generate-certs.sh
```

You'll be asked for a passphrase for the signing key and to validate it, and then asked for that key three times more.

Create a file in permission_engine:
```
touch permissions_engine/data.json
```

Once done, fire everything up - currently that's the IdP (Keycloak), permission engine (OPA) and katsu(a data service)

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

Then export environment variables for the keycloaks(OIDCs) later use in fetching keys:
```
export OIDC1="http://localhost:8080/auth/realms/mockrealm"
export OIDC2="http://localhost:8081/auth/realms/mockrealm"
export OIDC1_OPENCONNECT="http://localhost:8080/auth/realms/mockrealm/protocol/openid-connect"
export OIDC2_OPENCONNECT="http://localhost:8081/auth/realms/mockrealm/protocol/openid-connect"
```

Then download certificate from the keycloak's jwk uri into `data.json ` under the directory `permissions_engine`.
```
python3 permissions_engine/fetch_keys.py
```

Restart OPA to update the jwks for permission verification
```
docker-compose restart opa
```


In addition to the policies defined in OPA (the permissions engine), OPA directly connects to the IdP's userinfo
to validate the token.

you can capture the tokens as:

```
TOKEN1=$( python3 capture_token.py user1 pass1 oidc1 )
TOKEN2=$( python3 capture_token.py user1 pass1 oidc1 )
```

## Testing with katsu
Fill katsu with testing data by running: 
```
./tests/test_setup.sh 
```
This script creates 6 datasets *name_i*(open1, open2, registered3, controlled4, controlled5, controlled6) with one phenopacket with id *pheno_i* in each one.

Capture tokens by running: 
```
TOKEN1=$( python3 capture_token.py user1 pass1 oidc1 )
TOKEN2=$( python3 capture_token.py user1 pass1 oidc1 )
```

then you can have the beacon query the katsu server(currently only phenopackets endpoint protected):

```
curl --insecure -XGET -H "X-CANDIG-LOCAL-OIDC: \"$TOKEN1\"" 'localhost:8001/api/phenopackets'|jq '.results'|jq '[.[] | {id: .id}]'
curl --insecure -XGET -H "X-CANDIG-LOCAL-OIDC: \"$TOKEN2\"" 'localhost:8001/api/phenopackets'|jq '.results'|jq '[.[] | {id: .id}]'
```
User1 should have access to 4 datasets, open1, open2, registered3 and controlled4. 
User2 should have access to 3 datasets, open1, open2, and controlled4. 

You can also do the same thing for the second keycloak
Capture tokens by running: 
```
TOKEN3=$( python3 capture_token.py user3 pass3 oidc2 )
TOKEN4=$( python3 capture_token.py user4 pass4 oidc2 )
```

then you can have the beacon query the katsu server(currently only phenopackets endpoint protected):

```
curl --insecure -XGET -H "X-CANDIG-LOCAL-OIDC: \"$TOKEN3\"" 'localhost:8001/api/phenopackets'|jq '.results'|jq '[.[] | {id: .id}]'
curl --insecure -XGET -H "X-CANDIG-LOCAL-OIDC: \"$TOKEN4\"" 'localhost:8001/api/phenopackets'|jq '.results'|jq '[.[] | {id: .id}]'
```
User3 should have access to 5 datasets, open1, open2, registered3, controlled4, controlled6.
User4 should have access to 3 datasets, open1, open2, and controlled5. 
