#!/bin/bash
set -euo pipefail

readonly token=${1:-"notoken"}
if [[ "${token}" == "notoken" ]]
then
    >&2 echo "Usage: $0 token"
    exit -1
fi

curl -X "POST" "${OPA_URL}/v1/data/permissions/datasets" \
    -H "Content-Type: application/json" -H "Accept: application/json" \
    -H "Authorization: Bearer my-secret-root-token" \
    -d "{ \"input\": { \"token\": \"${token}\", \"body\": { \"method\": \"GET\", \"path\": \"/api/phenopackets\" } } } "

echo ""
