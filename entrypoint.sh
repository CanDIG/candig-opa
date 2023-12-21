#!/usr/bin/env bash

set -Euo pipefail

OPA_ROOT_TOKEN=$(cat /run/secrets/opa-root-token)

if [[ -f "/app/initial_setup" ]]; then
    sed -i s/CLIENT_ID/$KEYCLOAK_CLIENT_ID/ /app/permissions_engine/idp.rego && sed -i s/CLIENT_ID/$KEYCLOAK_CLIENT_ID/ /app/permissions_engine/authz.rego
    sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ /app/permissions_engine/idp.rego && sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ /app/permissions_engine/authz.rego

    OPA_SERVICE_TOKEN=$(cat /run/secrets/opa-service-token)
    sed -i s/OPA_SERVICE_TOKEN/$OPA_SERVICE_TOKEN/ /app/permissions_engine/authz.rego

    sed -i s/OPA_ROOT_TOKEN/$OPA_ROOT_TOKEN/ /app/permissions_engine/authz.rego
    echo "initializing idp"
    python3 /app/permissions_engine/initialize_idp.py

    # install base jsons at vault
    token=$(bash get_vault_store_token.sh)
    echo "storing data.json"
    curl -X "PUT" "${VAULT_URL}/v1/opa/data" \
     -H "X-Vault-Token: ${token}" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d @/app/data.json

    echo "storing access.json"
    curl -X "PUT" "${VAULT_URL}/v1/opa/access" \
     -H "X-Vault-Token: ${token}" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d @/app/permissions_engine/access.json

    echo "storing paths.json"
    curl -X "PUT" "${VAULT_URL}/v1/opa/paths" \
     -H "X-Vault-Token: ${token}" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d @/app/permissions_engine/paths.json

    rm /app/initial_setup
fi

token=$(bash get_vault_store_token.sh)
echo $(curl "${VAULT_URL}/v1/opa/data" -H "X-Vault-Token: ${token}")
echo $(curl "${VAULT_URL}/v1/opa/access" -H "X-Vault-Token: ${token}")
echo $(curl "${VAULT_URL}/v1/opa/paths" -H "X-Vault-Token: ${token}")

while [ 0 -eq 0 ]
do
  token=$(bash get_vault_store_token.sh)
  sleep 300
done
