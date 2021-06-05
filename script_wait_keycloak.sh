#!/usr/bin/expect

eval spawn docker-compose logs oidc
expect "Admin console listening"
interact
