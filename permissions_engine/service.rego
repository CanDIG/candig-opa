package service

#
# Verifies that a service is who it says it is
#
import data.vault.service_token as service_token
import rego.v1

verified if {
	service_token == input.token
}

else if {
	data.idp.is_external_service[input.service] == true
}

else := false


minus(service, info) := "opa service is running"
