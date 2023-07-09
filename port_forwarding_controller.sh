#!/bin/bash

PUERTO="$1"
IP_VM="$2"
PUERTO_ACCESO="$3"
ACTION="$4"
password="ubuntu"

if [ "$ACTION" == "CREAR" ]; then
    sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport $PUERTO -j DNAT --to-destination $IP_VM:$PUERTO_ACCESO
    comando="sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport $PUERTO -j DNAT --to-destination $IP_VM:$PUERTO_ACCESO"
    echo $comando
else
    sudo iptables -t nat -D PREROUTING -p tcp -m tcp --dport $PUERTO -j DNAT --to-destination $IP_VM:$PUERTO_ACCESO
    comando="sudo iptables -t nat -D PREROUTING -p tcp -m tcp --dport $PUERTO -j DNAT --to-destination $IP_VM:$PUERTO_ACCESO"
    echo $comando
fi
