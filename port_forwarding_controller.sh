#!/bin/bash

PUERTO = "$1"
IP_VM = "$2"

sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport ${PUERTO} -j DNAT --to-destination ${IP_VM}:22