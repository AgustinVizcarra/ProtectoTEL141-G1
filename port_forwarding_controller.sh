#!/bin/bash

PUERTO = "$1"

sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport ${PUERTO} -j DNAT --to-destination ${IP_VM}:22