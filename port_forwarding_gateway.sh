#!/bin/bash

PUERTO = "$1"

sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport ${PUERTO} -j DNAT --to-destination 10.0.0.10:${PUERTO}