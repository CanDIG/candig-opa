package idp
# for interacting with the IdP

#
# Store decode and verified token
#

import data.store_token.token as token
keys = http.send({"method": "get", "url": "http://vault:8200/v1/opa/data", "headers": {"X-Vault-Token": token}}).body.data.keys

decode_verify_token_output[issuer] := output {
    some i
    issuer := keys[i].iss
    cert := keys[i].cert
    output := io.jwt.decode_verify(     # Decode and verify in one-step
        input.token,
        {                         # With the supplied constraints:
            "cert": cert,
            "iss": issuer,
            "aud": "CLIENT_ID"
        }
    )
}

#
# Check if token is valid by checking whether decoded_verify output exists or not
#
valid_token = true {
    decode_verify_token_output[_][0]
}

#
# Check trusted_researcher in the token payload
#
trusted_researcher = true {
    decode_verify_token_output[_][2].trusted_researcher == "true"
}

#
# Check OPA_SITE_ADMIN_KEY in the token payload
#
OPA_SITE_ADMIN_KEY = true {
    decode_verify_token_output[_][2].realm_access.roles[_] == "OPA_SITE_ADMIN_KEY"
}

email := decode_verify_token_output[_][2].email        # get email from the token payload
