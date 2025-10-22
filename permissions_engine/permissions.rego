package permissions

import rego.v1

#
# Values that are used by authx
#
valid_token if {
	data.idp.valid_token
}

else := false

is_local_token if {
	data.idp.is_local_token
}

else := false

site_admin := data.calculate.site_admin if {
	valid_token
	is_local_token
}

else := false

site_curator := data.calculate.site_curator if {
	valid_token
	is_local_token
}

else := false

datasets := data.calculate.datasets if {
	valid_token
}

else := []

# true if the path and method in the input match a readable combo in paths.json
readable_method_path if {
	input.body.method = "GET"
	data.calculate.readable_get[_]
}

else if {
	input.body.method = "POST"
	data.calculate.readable_post[_]
}

else if {
	input.body.method = "DELETE"
	data.calculate.curateable_delete[_]
}

else := false

# true if the path and method in the input match a curateable combo in paths.json
curateable_method_path if {
	input.body.method = "GET"
	data.calculate.curateable_get[_]
}

else if {
	input.body.method = "POST"
	data.calculate.curateable_post[_]
}

else if {
	input.body.method = "DELETE"
	data.calculate.curateable_delete[_]
}

else := false

# if a specific program is in the body, allowed = true if that program is in datasets
# or if the user is a site admin
# or if the user is a site curator and wants to curate something
allowed if {
	datasets[input.body.program] == true
}

else if {
	input.body.program in datasets
}

else if {
	regex.match("/me$", input.body.path)
	input.body.method == "GET"
}

else if {
	site_admin
}

else if {
	site_curator
	curateable_method_path
}

else if {
	site_curator
	readable_method_path
}

else := false

#
# User information, for decision log
#

# information from the jwt
user_key := data.idp.user_key

issuer := data.idp.user_info.iss

user_is_candig_authorized if {
	data.vault.user_auth.status_code == 200
	data.vault.user_auth.body.data.userinfo.sample_jwt
}

else := false

#
# Debugging information for decision log
#

debug.local_issuer := data.vault.keys[0].iss

debug.user_key_listed_as_site_admin if {
	user_key in data.vault.site_roles.admin
}

else := false

debug.user_key_listed_as_site_curator if {
	user_key in data.vault.site_roles.curator
}

else := false

# programs the user is listed as a team member for
debug.user_key_has_team_member_programs := data.calculate.team_readable_programs

# programs the user is approved by dac for
debug.user_key_has_dac_programs := object.keys(data.vault.user_programs)

# programs the user is listed as a program curator for
debug.user_key_has_curator_programs := data.calculate.program_curateable_programs
