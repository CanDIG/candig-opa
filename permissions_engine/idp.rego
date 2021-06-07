package idp
# for interacting with the IdP

#
# Configuration
#

env := opa.runtime().env
rootCA := object.get(env, "ROOT_CA", "/rootCA.crt")
audience := "account"
#
# Define valid keys
#
key_sets := {"https://oidc:8443/auth/realms/mockrealm" : `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv01+/YRAwXaVVC7qYM1uCVZeRqePwOWQ/IJU9z8fFeuTGMREIltMV865DHFA4ZZRxD2hQWri0D3YkMwfe/qrJeEWxCGzI0wFiemE9ezEwh5d6en8oqBg3YahKWRbGquPBTrz0B5quMKzvG0rTWELYiGIrIaUiNRzDE7Z4tFDzB30oM5o/5O5/gm/vwuA08HqpoYb+/Xql6+R3p7xk7ZtvlhdYKxJbRueOAsUmvlvaKS7xDg8Igx0NuBoZxkeURhVF0ZqjPfZlo7mhL0LpgzIOMLye46Cc5bdaU7T+qpI77QNgcR2xgp89wDqEnqLMLWrhOYCM1X6n+sokZyFloyNqQIDAQAB
-----END PUBLIC KEY-----`}

#
# Store decode and verified token
#
decode_verify_token_output = output{
	some iss
    output:=io.jwt.decode_verify(     # Decode and verify in one-step
            input.token,
            {                                                 # With the supplied constraints:
                "cert": key_sets[iss],
                "iss": iss,
                "aud": audience
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