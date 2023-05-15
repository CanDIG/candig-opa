package system.authz

# this defines authentication to have access to opa at all
# from: https://www.openpolicyagent.org/docs/v0.22.0/security/#token-based-authentication-example

rights = {
    "admin": {
        "path": "*"
    },
    "datasets": {
        "path": ["v1", "data", "permissions", "datasets"]
    },
    "tokenControlledAccessREMS": {
        "path": ["v1", "data", "ga4ghPassport", "tokenControlledAccessREMS"]
    }
}

root_token := "OPA_ROOT_TOKEN"
service_token := "OPA_SERVICE_TOKEN"

tokens = {
    root_token : {
        "roles": ["admin"]
    },
    service_token : {
        "roles": ["datasets", "tokenControlledAccessREMS"]
    }
}

default allow = false               # Reject requests by default.

allow {                             # Allow request if...
    some right
    identity_rights[right]          # Rights for identity exist, and...
    right.path == "*"               # Right.path is '*'.
}

allow {                             # Allow request if...
    some right
    identity_rights[right]          # Rights for identity exist, and...
    right.path == input.path        # Right.path matches input.path.
}

x_opa := input.headers["X-Opa"][_]

identity_rights[right] {             # Right is in the identity_rights set if...
    token := tokens[x_opa]  # Token exists for identity, and...
    role := token.roles[_]           # Token has a role, and...
    right := rights[role]            # Role has rights defined.
}

# If token payload has OPA_SITE_ADMIN_KEY in it, allow always
allow {
    decode_verify_token_output[_][2].realm_access.roles[_] == "OPA_SITE_ADMIN_KEY"
}

decode_verify_token_output[issuer] := output {
    some i
    issuer := data.keys[i].iss
    cert := data.keys[i].cert
    output := io.jwt.decode_verify(     # Decode and verify in one-step
        input.identity,
        {                         # With the supplied constraints:
            "cert": cert,
            "iss": issuer,
            "aud": "CLIENT_ID"
        }
    )
}
