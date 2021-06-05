#!/usr/bin/expect
set timeout 20

eval spawn docker-compose logs -f oidc
expect "Admin console listening"
close