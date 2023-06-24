#!/bin/sh

rm -f .env
touch .env

for i in $(printenv); do
value=$(awk -FCI_ENV_ '{print $2}' <<< "$i")
if [ -n "$value" ]; then
    echo "$value" >> .env
fi
done
