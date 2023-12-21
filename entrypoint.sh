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
    rm /app/initial_setup
fi

cd /app; ls *-roleid
while [ $? -ne 0 ]
do
  echo "..."
  sleep 5
  cd /app; ls *-roleid
done

while [ 0 -eq 0 ]
do
  roleid_file=$(cd /app; ls *-roleid)
  role_id=$(cat ${roleid_file})
  service=${roleid_file/-roleid/}
  token=$(cat /run/secrets/vault-approle-token)
  curl -X "POST" "${VAULT_URL}/v1/auth/approle/role/${service}/secret-id" -H "X-Vault-Token: ${token}" -H 'Content-Type: application/json; charset=utf-8' | jq '.["data"]["secret_id"]' > /app/${service}-secretid
  secret_id=$(cat /app/${service}-secretid)
  echo "{\"role_id\": \"${role_id}\", \"secret_id\": ${secret_id}}" > /app/permissions_engine/approle.json
  token=$(curl -X "POST" "${VAULT_URL}/v1/auth/approle/login" -H 'Content-Type: application/json; charset=utf-8' -d @/app/permissions_engine/approle.json | jq -r '.["auth"]["client_token"]')
  curl -X "PUT" "${OPA_URL}/v1/data/store_token" -H "X-Opa: ${OPA_ROOT_TOKEN}" -H 'Content-Type: application/json; charset=utf-8' -d "{\"token\": \"${token}\"}"
  sleep 300
done
