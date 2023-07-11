import re

## Funcion que valida el CIDR
def validar_cidr(cidr):
    patron = r"^(?!0\.)((?!255\.)\d{1,3}\.){3}(?!255$)\d{1,3}/(0|[1-2]?\d|3[0-2])$"
    if re.match(patron, cidr):
        return True
    return False

#Funcion que valida una IP
def validar_direccion_ip(ip):
    patron = r"^(?!0\.)(?!255\.)(?!255\.255\.)(?!255\.255\.255\.)(?!255$)((?!255\.)\d{1,3}\.){3}(?!0$)\d{1,3}$"
    if re.match(patron, ip):
        return True
    return False

#Funcion que valida un puerto
def validar_puerto(puerto):
    patron = r"^[1-9]\d*$"
    if re.match(patron, puerto):
        return True
    return False

#Funcion que valida la RAM (MB)
def validar_ram(ram):
    patron = r"^[1-9]\d*$"
    if re.match(patron, ram):
        return True
    return False

#Funcion que valida los vCPUS
def validar_vcpus(vcpus):
    patron = r"^[1-9]$"
    if re.match(patron, vcpus):
        return True
    return False

#Funcion que valida el Disk (GB)
def validar_disk(disk):
    patron = r"^[1-9]\d*$"
    if re.match(patron, disk):
        return True
    return False

#Funcion que valida la cantidad de nodos
def validar_cantidad_nodos(cantidad):
    patron = r"^[2-9]\d*$"
    if re.match(patron, cantidad):
        return True
    return False

#Funcion que valida la cantida de niveles
def validar_cantidad_niveles(cantidad):
    patron = r"^[3-9]\d*$"
    if re.match(patron, cantidad):
        return True
    return False

#Funcion que valida la dirección IPV4
def validar_direccion_ip2(ip):
    patron = r'^30\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if re.match(patron, ip):
        return True
    else:
        return False