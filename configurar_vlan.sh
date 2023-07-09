#!/bin/bash

VLAN_ID="$1"
CIDR_RED="$2"
GATEWAY="$3"
ACTION="$4"
password="ubuntu"

if [ "$ACTION" == "CREAR" ]; then
    echo ${password} | sudo -S ip link add link ens6 name ens6.${VLAN_ID} type vlan id ${VLAN_ID}
    echo ${password} | sudo -S ip addr add ${GATEWAY}/24 dev ens6.${VLAN_ID}
    echo ${password} | sudo -S ip link set ens6.${VLAN_ID} up
    echo ${password} | sudo -S iptables -t nat -A POSTROUTING -s ${CIDR_RED} -j SNAT --to-source 10.0.0.0
else
    echo ${password} | sudo -S ip link delete ens6.${VLAN_ID}
    echo ${password} | sudo -S iptables -t nat -D POSTROUTING -s ${CIDR_RED} -j SNAT --to-source 10.0.0.0
fi
