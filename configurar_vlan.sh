#!/bin/bash

VLAN_ID = "$1"
CIDR_RED = "$2"

sudo ip link add link ens6 name ens6.${VLAN_ID} type vlan id ${VLAN_ID}

sudo ip link set ens6.${VLAN_ID} up

sudo iptables -t nat -A POSTROUTING -s ${CIDR_RED} -j SNAT --to-source 10.0.0.0