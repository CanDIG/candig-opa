package idp
# for interacting with the IdP

#
# Store decode and verified token
#
decode_verify_token_output = output{
	some i
    output:=io.jwt.decode_verify(     # Decode and verify in one-step
            input.token,
            {                         # With the supplied constraints:
                "cert": data.keys[i].cert,
                "iss": data.keys[i].iss,
                "aud": "CLIENT_ID"
            }
    )
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

#
# Check OPA_SITE_ADMIN_KEY in the token payload
#
OPA_SITE_ADMIN_KEY = true {
    decode_verify_token_output[0]
    decode_verify_token_output[2].OPA_SITE_ADMIN_KEY == true        
}

username := decode_verify_token_output[2].preferred_username        # get username from the token payload
