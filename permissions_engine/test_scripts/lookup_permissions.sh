#!/bin/bash
set -euo pipefail

readonly token=${1:-"notoken"}
if [[ "${token}" == "notoken" ]]
then
    >&2 echo "Usage: $0 token"
    exit -1
fi

source config.sh
curl "${OPAURL}" \
    -H "Content-Type: application/json" -H "Accept: application/json" \
    -d "{\"input\": {\"method\": \"GET\", \"path\": [\"beacon\"], \"token\": \""${token}"\"}}"
