#!/usr/bin/expect

set timeout 20
set password [lindex $argv 0]

eval spawn ./generate-certs.sh
expect "rootCA.key:"
send "$password\r";
expect "rootCA.key:"
send "$password\r";
expect "rootCA.key:"
send "$password\r";
expect "rootCA.key:"
send "$password\r";
expect "rootCA.key:"
send "$password\r";
expect "rootCA.key:"
send "$password\r";
expect "rootCA.key:"
send "$password\r";
interact
