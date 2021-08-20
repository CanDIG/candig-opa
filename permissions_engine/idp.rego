package idp
# for interacting with the IdP

#
# Configuration
#

env := opa.runtime().env
rootCA := object.get(env, "ROOT_CA", "/rootCA.crt")
audience := ["account", "portal"]
key_sets = data.keys

#
# Store decode and verified token
#
decode_verify_token_output = output{
	some iss
    some x
    output:=io.jwt.decode_verify(     # Decode and verify in one-step
            input.headers[x],
            {                                                 # With the supplied constraints:
                "cert": key_sets[iss],
                "iss": iss,
                "aud": audience[_]
            }
    )
    valid = output[0]
    valid == true
}

#
# Check if token is valid by checking whether decoded_verify output exists or not
#
valid_token = true {
    decode_verify_token_output
}

#
# Check trusted_researcher in the token payload
#
trusted_researcher = true {
    decode_verify_token_output[0]
    decode_verify_token_output[2].trusted_researcher == true        
}

username := decode_verify_token_output[2].preferred_username        # get username from the token payload
