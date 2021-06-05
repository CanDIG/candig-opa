#!/usr/bin/expect
set timeout 90

eval spawn docker-compose logs -f oidc
expect "Admin console listening"
close