#!/bin/bash

password="ubuntu"
declare -a used_ports

get_used_ports() {
    local ports=$(sudo iptables -t nat -L PREROUTING -n --line-numbers | awk '/DNAT/ {split($9, a, ":"); print a[length(a)]}')
    used_ports=()
    for port in $ports; do
        if ((port >= 5800 && port <= 6000)); then
            used_ports+=("$port")
        fi
    done
    used_ports=($(printf "%s\n" "${used_ports[@]}" | sort -rn))
}

find_next_port() {
    local next_port=5800
    for port in "${used_ports[@]}"; do
        if ((next_port <= port)); then
            ((next_port = port + 1))
        fi
    done
    if ((next_port <= 6000)); then
        echo "$next_port"
    else
        echo "No se encontró un puerto disponible en la secuencia."
        exit 1
    fi
}

get_used_ports

next_port=$(find_next_port)
echo "$next_port"
