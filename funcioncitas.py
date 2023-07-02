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
