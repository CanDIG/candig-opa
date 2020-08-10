package permissions

default datasets = []

oidc_base = "http://localhost:8080/auth/realms/mockrealm/"
client_id := "mockclient"
client_secret := "851f0479-56c3-4a26-b861-c8470a4e06b2"

basic_client_authn := concat(" ", ["Basic", base64.encode(concat(":", [client_id, client_secret]))])

wellknown_url = concat("", [oidc_base, ".well-known/openid-configuration"])
oidc_config := http.send({"method": "get", "url": wellknown_url})

introspection_url := oidc_config.body.introspection_endpoint
userinfo_url := oidc_config.body.userinfo_endpoint

introspect = http.send({"url": introspection_url, "headers": {"Authorization": basic_client_authn, "Content-Type": "application/x-www-form-urlencoded"}, "method": "post", "raw_body": concat("=",["token",input.token])}).body

userinfo = http.send({"url": userinfo_url, "headers": {"Authorization": concat(" ", ["Bearer", input.token])}, "method": "get"}).body
