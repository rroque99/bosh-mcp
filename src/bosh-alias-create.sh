#!/bin/bash

if [ $# -ne 2 ]
  then
    echo "usage: $0 <env-name> <director>"
    exit 1
fi

echo | openssl s_client -servername $2 -connect ${2}:8443 2>/dev/null |   openssl x509 -outform PEM > $1-cert.pem

echo | openssl s_client -servername $2 -connect ${2}:25555 2>/dev/null |   openssl x509 -outform PEM >> $1-cert.pem

bosh alias-env $1 -e $2 --ca-cert=./$1-cert.pem
