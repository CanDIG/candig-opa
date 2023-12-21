#!/usr/bin/env bash

OPA_ROOT_TOKEN=$(cat /run/secrets/opa-root-token)

# get the token for the opa store
opa_token=$(python -c "import authx.auth
print(authx.auth.get_vault_token_for_service(\"opa\"))")
while [ $opa_token -eq "" ]
do
    sleep 5
    # get the token for the opa store
    opa_token=$(python -c "import authx.auth
print(authx.auth.get_vault_token_for_service(\"opa\"))")
done

# store the token locally in Opa
curl -X "PUT" "${OPA_URL}/v1/data/store_token" -H "X-Opa: ${OPA_ROOT_TOKEN}" -H 'Content-Type: application/json; charset=utf-8' -d "{\"token\": \"${opa_token}\"}"

echo $opa_token
