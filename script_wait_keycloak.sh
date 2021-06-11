#!/usr/bin/expect
set timeout 90

eval spawn docker-compose logs -f oidc1
expect "Admin console listening"
eval spawn docker-compose logs -f oidc2
expect "Admin console listening"
close