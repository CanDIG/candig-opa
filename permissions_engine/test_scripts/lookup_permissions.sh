#!/bin/bash
set -euo pipefail

readonly token=${1:-"notoken"}
if [[ "${token}" == "notoken" ]]
then
    >&2 echo "Usage: $0 token"
    exit -1
fi

source config.sh
curl -k "${OPAURL}" \
    -H "Content-Type: application/json" -H "Accept: application/json" \
    -H "Authorization: Bearer my-secret-root-token" \
    -d "{\"input\": {\"method\": \"GET\", \"path\": [\"beacon\"], \"token\": \"${token}\"}}"
