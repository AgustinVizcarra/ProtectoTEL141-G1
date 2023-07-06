#!/bin/bash

PUERTO="$1"
ACTION="$2"
password="ubuntu"

if [ "$ACTION" == "CREAR" ]; then
     sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport ${PUERTO} -j DNAT --to-destination 10.0.0.10:${PUERTO}
else
     sudo iptables -t nat -D PREROUTING -p tcp -m tcp --dport ${PUERTO} -j DNAT --to-destination 10.0.0.10:${PUERTO}
fi
