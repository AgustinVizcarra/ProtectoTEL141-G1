#!/bin/bash

ip_address="$1"

output=$(sudo iptables -t nat -L -n | grep "$ip_address" | head -n 1)

port=$(echo "$output" | awk -F "dpt:" '{split($2,a," to:"); print a[1]}')
dest_port=$(echo "$output" | awk -F ":" '{split($4,a," "); print a[1]}')

echo -n "$port "
echo "$dest_port"
