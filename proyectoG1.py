from getpass import getpass
from keystone import KeystoneAuth
from Nova import NovaClient
from Glance import GlanceClient
from Neutron import NeutronClient
from AutheticationDriver import AuthenticationManager
from menuLinux import Usuario
from menuLinux import Administrador
import requests
from tabulate import tabulate
from Classes.VM import VM
from TopoHandler import TopoConstructor
from funcioncitas import *
from MonitoreoRecursos import obtenerInfoRemoto
############################################    F   U   N   C   I   O   N   E   S   ############################################
#Funcion que muestra el menu de la lista de Proyectos
def MenuListaProyectos(keystone):
    listaProyectos, listaRoles = keystone.getListProjects()
    if len(listaProyectos) == 0:   
        Cabecera = ["Lista de Proyectos"]
        Filas = [["Actualmente, usted no se encuentra asignado a ningún proyecto.\nPorfavor, póngase en contacto con un administrador."]]
        print("\n")
        print(tabulate(Filas1,headers=Cabecera1,tablefmt='fancy_grid',stralign='center'))
        return False,keystone
    else:
        while True:
            Cabecera = ["Lista de Proyectos"]
            filas = []
            filasopt = []
            i = 0
            for proyecto in listaProyectos:
                filasopt.append("Proyecto "+str(i+1)+". -> "+str(proyecto[1])+"     |   Rol: "+ str(listaRoles[i]))
                i = i + 1
            filas.append(["\n".join(filasopt)])
            filas.append(["**Escriba ESC para poder salir**"])
            print("\n")
            print(tabulate(filas,headers=Cabecera,tablefmt='fancy_grid',stralign='center'))
            opcionProyecto = input("| Ingrese el # del proyecto al que desea ingresar: ")
            if str(opcionProyecto) == "ESC":
                return False,keystone
            try:
                if int(opcionProyecto) > len(listaProyectos):
                    print("[*] Ingrese el # de un proyecto válido\n")
                else:
                    idProyecto = listaProyectos[int(opcionProyecto)-1][0]
                    keystone.setProjectID(idProyecto)
                    keystone.setRolName(listaRoles[int(opcionProyecto)-1])
                    break
            except ValueError:
                print("[*] Ingrese el # de un proyecto válido\n")
        return True,keystone
   
#Funcion que muestra el Menú Principal        
def menuPrincipal(keystone):
    opcionesAdmin = ["Usuario","Red","Topología","KeyPair","SecurityGroup","VirtualMachine","Flavors","Images","Monitoreo de Recursos"]
    opcionesUsuario = ["Red","KeyPair","SecurityGroup","VirtualMachine","Monitoreo de Recursos"]
    if keystone.getRolName() == "admin":
        opciones = opcionesAdmin
    else:
        opciones = opcionesUsuario
    while True:
            Cabecera = ["Menú Principal"]
            filas = []
            filasopt = []
            i = 0
            for opt in opciones:
                filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1
            filas.append(["\n".join(filasopt)])
            filas.append(["Opción "+str(i+1)+" -> Salir"])
            print("\n")
            print(tabulate(filas,headers=Cabecera,tablefmt='fancy_grid',stralign='center'))
            opcion = input("| Ingrese una opción: ")
            try:
                if int(opcion) == (len(opciones)+1):
                    opcion = "Salir"
                    break
                else:
                    if int(opcion) <= len(opciones):
                        opcion = opciones[int(opcion)-1]
                        break
                    else:
                        print("[*] Ingrese una opción válida.\n")
            except ValueError:            
                print("[*] Ingrese una opción válida.\n")
    return opcion

#Funcion que muestra el Menú Usuarios
def menuUsuarios():
    opciones = ["Listar usuarios"]
    while True:
            filas = []
            filasopt = []
            i = 0
            for opt in opciones:
                filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            filas.append(["\n".join(filasopt)])
            filas.append(["Opción "+str(i+1)+" -> Salir"])
            print("\n")
            print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
            opcion = input("| Ingrese una opción: ")
            try:
                if int(opcion) == (len(opciones)+1):
                    opcion = "Salir"
                    break
                else:
                    if int(opcion) <= len(opciones):
                        opcion = opciones[int(opcion)-1]
                        break
                    else:
                        print("[*] Ingrese una opción válida\n")
            except ValueError:
                print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion para listar proyectos por usuario
def listarUsuariosProyecto(keystone):
    listado = keystone.listarProyectosUsuarios()
    if len(listado) != 0:
        head = ["USUARIOS"]
        filas = []
        for user in listado:
            filas.append([str(user)])
        print("\n")
        print(tabulate(filas,headers=head,tablefmt='grid',stralign='center'))
    else:
        print("\n")
        print(tabulate([["No hay usuarios en este proyecto."]],headers=[],tablefmt='grid',stralign='center'))
        
#Funcion que muestra el Menú redesprovider
def menuRedes(keystone):
    opcionesAdmin = ["Crear red","Listar redes","Borrar red"]
    opcionesUsuario = ["Listar redes"]
    if keystone.getRolName() == "admin":
        opciones = opcionesAdmin
    else:
        opciones = opcionesUsuario
    while True:
            filas = []
            filasopt = []
            i = 0
            for opt in opciones:
                filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            filas.append(["\n".join(filasopt)])
            filas.append(["Opción "+str(i+1)+" -> Salir"])
            print("\n")
            print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
            opcion = input("| Ingrese una opción: ")
            try:
                if int(opcion) == (len(opciones)+1):
                    opcion = "Salir"
                    break
                else:
                    if int(opcion) <= len(opciones):
                        opcion = opciones[int(opcion)-1]
                        break
                    else:
                        print("[*] Ingrese una opción válida\n")
            except ValueError:
                print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion que permite crear Red
def crearRed(keystone,neutron,nova,glance):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        red = input("| Ingrese un nombre de red: ")
        if(red != ''):
            if(red == "ESC"):
                print("[*] Ha salido de la opción de -Crear Red-\n")
                return
            while True:
                subred = input("| Ingrese un nombre de subred: ")
                if(subred != ''):
                    if(subred == "ESC"):
                        print("[*] Ha salido de la opción de -Crear Red- \n")
                        return
                    while True:
                        cidr = input("| Ingrese un CIDR: ")
                        if(cidr == "ESC"):
                            print("[*] Ha salido de la opción de -Crear Red- \n")
                            return
                        if validar_cidr(cidr):
                            while True:
                                gatewayIP = input("| Ingrese una IP del gateway: ")
                                if(gatewayIP == "ESC"):
                                    print("[*] Ha salido de la opción de -Crear Red- \n")
                                    return
                                if validar_direccion_ip(gatewayIP):
                                    neutron.create_network(red,subred,cidr,gatewayIP)
                                    return
                                else:
                                    print("[*] Ingrese una IP válida\n")
                                    continue
                        else:
                            print("[*] Ingrese un CIDR válido\n")
                            continue
                else:
                    print("[*] Ingrese un nombre de subred válido\n")
                    continue
        else:
            print("[*] Ingrese un nombre de red válido\n")
            continue

#Funcion que permite mostrar la info de la Red
def infoRed(keystone,neutron):
    informacion = neutron.infoRedProvider(keystone.getProjectID())
    if len(informacion) != 0:
        cabeceras = ["NOMBRE RED","DESCRIPCION","FECHA CREACIÓN","CIDR","GATEWAY IP"]
        print("\n")
        print(tabulate(informacion,headers=cabeceras,tablefmt='grid',stralign='center'))    
    else:
        print("\n")
        print(tabulate([["No hay redes en este proyecto."]],headers=[],tablefmt='grid',stralign='center'))
    
#Funcion que permite borrar una Red
def borrarRed(keystone,neutron):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese el nombre de la red: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Eliminar Red- \n")
                return
            neutron.delete_network(nombre,keystone.getProjectID())
            break
        else:
            print("[*] Ingrese un nombre válido\n")
            continue
    
#Funcion que muestra el Menú keypair
def menuKeyPair():
    opcionesAdmin = ["Crear keypair","Listar keypair","Info keypair","Eliminar keypair"]
    opcionesUsuario = ["Listar keypair","Info keypair"]
    if keystone.getRolName() == "admin":
        opciones = opcionesAdmin
    else:
        opciones = opcionesUsuario
    while True:
            filas = []
            filasopt = []
            i = 0
            for opt in opciones:
                filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            
            filas.append(["\n".join(filasopt)])
            filas.append(["Opción "+str(i+1)+" -> Salir"])
            print("\n")
            print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
            opcion = input("| Ingrese una opción: ")
            try:
                if int(opcion) == (len(opciones)+1):
                    opcion = "Salir"
                    break
                else:
                    if int(opcion) <= len(opciones):
                        opcion = opciones[int(opcion)-1]
                        break
                    else:
                        print("[*] Ingrese una opción válida\n")
            except ValueError:
                print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion que permite crear la keypair
def crearKeyPair(keystone,nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre de keypair: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Crear KeyPair-\n")
                return
            while True:
                ruta = input("| Ingrese la ruta donde desea que se descargue la keypair: ")
                if(ruta != ''):
                    if(ruta == "ESC"):
                        print("[*] Ha salido de la opción de -Crear KeyPair-\n")
                        return
                    nova.crearKeyPair(nombre,ruta)
                    break
                else:
                    print("[*] Ingrese una ruta válida\n")
                    continue
        else:
            print("[*] Ingrese un nombre de keypair válido\n")
            continue

#Funcion para listar las keypair
def listarKeypair(keystone,nova):
    listado = nova.listarKeyPair(keystone.getUserID())
    if len(listado) != 0:
        head = ["KEYPAIRS"]
        filas = []
        for key in listado:
            filas.append([str(key)])
        print("\n")
        print(tabulate(filas,headers=head,tablefmt='grid',stralign='center'))
    else:
        print("\n")
        print(tabulate([["No hay keypairs creadas hasta el momento."]],headers=[],tablefmt='grid',stralign='center'))
        
#Funcion para ver info de la keypair
def infoKeypair(keystone,nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese el nombre de la KeyPair: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Ver Info KeyPair- \n")
                return
            break
        else:
            print("[*] Ingrese un nombre válido\n")
            continue
    informacionsita = nova.infoKeyPair(nombre,keystone.getUserID())
    if len(informacionsita) != 0:
        cabeceras = ["NOMBRE KEYPAIR","TIPO","FINGERPRINT","FECHA CREACIÓN"]
        print("\n")
        print(tabulate([informacionsita],headers=cabeceras,tablefmt='grid',stralign='center'))  
    else:
        print("\n")
        print(tabulate([["No hay información sobre esa llave."]],headers=[],tablefmt='grid',stralign='center'))
        
#Funcion para borrar la keypair
def borrarKeypair(keystone,nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese el nombre de la KeyPair: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Borrar KeyPair- \n")
                return
            nova.borrarKeyPair(nombre,keystone.getUserID())
            break
        else:
            print("[*] Ingrese un nombre válido\n")
            continue

#Funcion que muestra el Menú SecurityGroup
def menuSecurityGroup():
    opcionesAdmin = ["Crear SecurityGroup","Listar SecurityGroup","Info SecurityGroup","Editar SecurityGroup","Configurar SecurityGroup","Eliminar SecurityGroup"]
    opcionesUsuario = ["Listar SecurityGroup"]
    if keystone.getRolName() == "admin":
        opciones = opcionesAdmin
    else:
        opciones = opcionesUsuario
    while True:
            filas = []
            filasopt = []
            i = 0
            for opt in opciones:
                filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            filas.append(["\n".join(filasopt)])
            filas.append(["Opción "+str(i+1)+" -> Salir"])
            print("\n")
            print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
            opcion = input("| Ingrese una opción: ")
            try:
                if int(opcion) == (len(opciones)+1):
                    opcion = "Salir"
                    break
                else:
                    if int(opcion) <= len(opciones):
                        opcion = opciones[int(opcion)-1]
                        break
                    else:
                        print("[*] Ingrese una opción válida\n")
            except ValueError:
                print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion que permite crear la security group
def crearSecurityGroup(nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre de securitygroup: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Crear SecurityGroup-\n")
                return
            while True:
                descripcion = input("| Ingrese una descripcion del securitygroup: ")
                if(descripcion != ''):
                    if(descripcion == "ESC"):
                        print("[*] Ha salido de la opción de -Crear SecurityGroup- \n")
                        return
                    nova.crearSecurityGroup(nombre, descripcion)
                    return
                else:
                    print("[*] Ingrese una descripción válida\n")
                    continue
        else:
            print("[*] Ingrese un nombre de securitygroup válido\n")
            continue

#Funcion que permite listar los security group
def listarSecurityGroup(nova):
    listado = nova.listarSecurityGroup()
    if len(listado) != 0:
        cabeceras = ["SECURITY GROUP","DESCRIPCION"]
        print("\n")
        print(tabulate(listado,headers=cabeceras,tablefmt='grid',stralign='center'))    
    else:
        print("\n")
        print(tabulate([["No hay security groups creados hasta el momento."]],headers=[],tablefmt='grid',stralign='center'))

#Funcion que permite mostrar la información de un security group
def infoSecurityGroup(nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese el nombre del securitygroup: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Crear SecurityGroup- \n")
                return
            break
        else:
            print("[*] Ingrese un nombre válido\n")
            continue
    listado = nova.infoSecurityGroupRules(nombre)
    if len(listado) != 0:
        cabeceras = ["ID","DIRECTION","PROTOCOL","PORT_RANGE_MAX","PORT_RANGE_MIN"]
        print("\n")
        print(tabulate(listado,headers=cabeceras,tablefmt='grid',stralign='center')) 
    else:
        print("\n")
        print(tabulate([["No hay información sobre ese security group."]],headers=[],tablefmt='grid',stralign='center'))
        
#Funcion que permite editar un security group
def editarSecurityGroup(nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        name = input("| Ingrese un nombre de SecurityGroup: ")
        if(name != ''):
            if(name == "ESC"):
                print("[*] Ha salido de la opción de -Editar SecurityGroup-\n")
                return
            while True:
                verificarNombre = input("| ¿Desea cambiar el nombre?[Y/N]: ")
                nuevoNombre = None
                if verificarNombre == "Y" or verificarNombre == "y":
                    while True:
                        nuevoNombre = input("| Ingrese un nuevo nombre de SecurityGroup: ")
                        if(nuevoNombre == ''):
                            print("[*] Ingrese un nombre válido\n")
                            continue
                        else:
                            if(nuevoNombre == "ESC"):
                                print("[*] Ha salido de la opción de -Editar SecurityGroup-\n")
                                return
                            break
                elif(verificarNombre == "ESC"):
                    print("[*] Ha salido de la opción de -Editar SecurityGroup-\n")
                    return    
                elif verificarNombre == "N" or verificarNombre == "n":
                    break
                else:
                    print("[*] Ingrese una opción correcta\n")
            while True:
                verificarDescripcion = input("| ¿Desea cambiar la descripcion?[Y/N]: ")
                descripcion = None
                if verificarDescripcion == "Y" or verificarDescripcion == "y":
                    while True:
                        descripcion = input("| Ingrese una nueva descripcion: ")
                        if(descripcion == ''):
                            print("[*] Ingrese un descripcion válida\n")
                            continue
                        else:
                            if(descripcion == "ESC"):
                                print("[*] Ha salido de la opción de -Editar SecurityGroup-\n")
                                return 
                            break 
                elif(verificarDescripcion == "ESC"):
                    print("[*] Ha salido de la opción de -Editar SecurityGroup-\n")
                    return
                elif verificarDescripcion == "N" or verificarDescripcion == "n":
                    break
                else:
                    print("[*] Ingrese una opción correcta\n")
            if (verificarNombre == "N" or verificarNombre == "n") and (verificarDescripcion=="N" or verificarDescripcion == "n"):
                print("[*] Ha decidido no realizar ningún cambio al SecurityGroup\n")
                break 
            nova.editarSecurityGroup(name,nuevoNombre,descripcion)
            break
        else:
            print("[*] Ingrese un nombre de SecurityGroup válido\n")
            continue

#Funcion que permite eliminar un SecurityGroup
def borrarSecurityGroup(nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre de securitygroup: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Crear SecurityGroup-\n")
                return
            nova.eliminarSecurityGroup(nombre)
            break
        else:
            print("[*] Ingrese un nombre de securitygroup válido\n")
            continue

#Funcion que permite configurar un SecurityGroup
def configurarSecurityGroup(nova):
    while True:
        filas = []
        filas.append(["Opción 1 -> Añadir Regla\nOpción 2 -> Eliminar Regla"])
        filas.append(["Opción 3 -> Salir"])
        print("\n")
        print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center')) 
        opcion = input("| Ingrese una opción: ")
        try:
            if int(opcion) == 1:
                print("**Escriba ESC para poder salir de esta opción**")
                while True:
                    nombre = input("| Ingrese un nombre de securitygroup: ")
                    if(nombre != ''):
                        if(nombre == "ESC"):
                            print("[*] Ha salido de la opción de -Añadir Regla-\n")
                            return
                        while True:
                            protocol_ip = input("| Ingrese el protocolo IP: ")
                            if(protocol_ip != ''):
                                if(protocol_ip == "ESC"):
                                    print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                    return
                                while True:
                                    from_port = input("| Ingrese el from port: ")
                                    if(from_port == "ESC"):
                                        print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                        return
                                    if validar_puerto(from_port):
                                        while True:
                                            dest_port = input("| Ingrese el dest port: ")
                                            if(dest_port == "ESC"):
                                                print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                return 
                                            if validar_puerto(dest_port):
                                                while True:
                                                    verificar = input("| ¿Desea agregar permitir un CIDR ?[Y/N]: ")
                                                    cidr = None
                                                    if verificar == "Y" or verificar == "y":
                                                        while True:
                                                            cidr = input("| Ingrese un CIDR: ")
                                                            if(cidr == "ESC"):
                                                                print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                            return 
                                                            if validar_cidr(cidr):
                                                                nova.agregarRegla(nombre,protocol_ip,from_port,dest_port,cidr)
                                                                break
                                                            else:
                                                                print("[*] Ingrese un CIDR válido\n")
                                                                continue
                                                            break
                                                    elif(verificar == "ESC"):
                                                        print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                        return
                                                    elif verificar == "N" or verificar == "n":
                                                        break
                                                    else:
                                                        print("[*] Ingrese una opción correcta\n")
                                                    break
                                            else:
                                                print("[*] Ingrese un puerto válido\n")
                                                continue
                                            break
                                    else:
                                        print("[*] Ingrese un puerto válido\n")
                                        continue
                                    break
                            else:
                                print("[*] Ingrese un protocolo IP válido\n")
                                continue
                            break
                    else:
                        print("[*] Ingrese un nombre de securitygroup válido\n")
                        continue
                    break
            elif int(opcion) == 2:
                print("**Escriba ESC para poder salir de esta opción**")
                while True:
                    id = input("| Ingrese el ID de la regla a eliminar: ")
                    if(id != ''):
                        if(id == "ESC"):
                            print("[*] Ha salido de la opción de -Eliminar Regla-\n")
                            return
                        nova.eliminarRegla(id)
                        break
                    else:
                        print("[*] Ingrese un ID válido\n")
                        continue
            elif int(opcion) == 3:
                break
            else:
                print("[*] Ingrese una opción correcta\n")
        except ValueError:
            print("[*] Ingrese una opción correcta\n")

#Funcion que muestra el Menú VirtualMachine
def menuVirtualMachine():
    opcionesAdmin = ["Crear VirtualMachine","Listar VirtualMachine","Editar VirtualMachine","Eliminar VirtualMachine"]
    opcionesUsuario = ["Listar VirtualMachine"]
    if keystone.getRolName() == "admin":
        opciones = opcionesAdmin
    else:
        opciones = opcionesUsuario
    while True:
            filas = []
            filasopt = []
            i = 0
            for opt in opciones:
                filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            filas.append(["\n".join(filasopt)])
            filas.append(["Opción "+str(i+1)+" -> Salir"])
            print("\n")
            print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
            opcion = input("| Ingrese una opción: ")
            try:
                if int(opcion) == (len(opciones)+1):
                    opcion = "Salir"
                    break
                else:
                    if int(opcion) <= len(opciones):
                        opcion = opciones[int(opcion)-1]
                        break
                    else:
                        print("[*] Ingrese una opción válida\n")
            except ValueError:
                print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion que permite crear una VirtualMachine
def crearVirtualMachine(nova,neutron,glance,keystone):
    while True:
        nombre = input("| Ingrese un nombre de VirtualMachine: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Crear VirtualMachine-\n")
                return
            flavorID = getFlavorsID(nova)
            imagenID = getImagenesID(glance)
            networkID = getNetworkID(neutron,keystone)
            keyPairID = getKeyPairID(nova,keystone)
            securityGroupID = getSecurityGroupID(nova)
            tieneSalidaInternet = None
            while True:
                salidaInternet = input("| ¿Desea permitir la salida a Internet?[Y/N]: ")
                if salidaInternet == "Y" or salidaInternet == "y":
                    tieneSalidaInternet = 1
                elif salidaInternet == "N" or salidaInternet == "n":
                    tieneSalidaInternet = 0
                else:
                    print("[*] Ingrese una opción correcta\n")
                    continue
                break
            if tieneSalidaInternet == 1:
                accesoDesdeInternet = None
                while True:
                    accesoInternet = input("| ¿Desea permitir acceso desde Internet a la VM?[Y/N]: ")
                    if accesoInternet == "Y" or accesoInternet == "y":
                        accesoDesdeInternet = 1
                    elif accesoInternet == "N" or accesoInternet == "n":
                        accesoDesdeInternet = 0
                    else:
                        print("[*] Ingrese una opción correcta\n")
                        continue
                    break
                listaPuertos = []
                if accesoDesdeInternet == 1:
                    while True:
                        print("**Escriba ESC para salir**")
                        puerto = input("| Ingrese el puerto para acceder desde Internet: ")
                        try:
                            if puerto == "ESC":
                                break
                            puerto = int(puerto)
                            listaPuertos.append(puerto)
                        except ValueError:
                            print("[*] Ingrese una opción válida\n")
                            continue
            else:
                accesoDesdeInternet = 0
                listaPuertos = []
            nova.create_instance_internet(nombre, flavorID, imagenID, networkID,keyPairID,securityGroupID,tieneSalidaInternet,accesoDesdeInternet,listaPuertos)
            break
        else:
            print("[*] Ingrese un nombre de VirtualMachine válido\n")
            continue
    
#Funcion que permite listar las VirtualMachine
def listarVirtualMachine(keystone,nova):
    listado = nova.list_instances(keystone.ProjectID)
    if len(listado) != 0:
        cabeceras = ["VIRTUAL MACHINES"]
        lista_resultante = [[elemento] for elemento in listado]
        print("\n")
        print(tabulate(lista_resultante,headers=cabeceras,tablefmt='grid',stralign='center'))    
    else:
        print("\n")
        print(tabulate([["No hay VirtualMachines en este proyecto."]],headers=[],tablefmt='grid',stralign='center'))

#Funcion que permite editar una VirtualMachine
def editarVirtualMachine(nova,projectID):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre de VirtualMachine: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Editar VirtualMachine-\n")
                return
            while True:
                verificarNombre = input("| ¿Desea cambiar su nombre?[Y/N]: ")
                nuevoNombre = None
                if verificarNombre == "Y" or verificarNombre == "y":
                    while True:
                        nuevoNombre = input("| Ingrese un nuevo nombre para la VirtualMachine: ")
                        if(nuevoNombre == ''):
                            print("[*] Ingrese un nombre válida\n")
                            continue
                        else:
                            if(nuevoNombre == "ESC"):
                                print("[*] Ha salido de la opción de -Editar VirtualMachine-\n")
                                return
                            break
                elif(verificarNombre == "ESC"):
                    print("[*] Ha salido de la opción de -Editar VirtualMachine-\n")
                    return
                elif verificarNombre == "N" or verificarNombre == "n":
                    break
                else:
                    print("[*] Ingrese una opción correcta\n")
            while True:
                verificarDescripcion = input("| ¿Desea cambiar su descripcion?[Y/N]: ")
                descripcion = None
                if verificarDescripcion == "Y" or verificarDescripcion == "y":
                    while True:
                        descripcion = input("| Ingrese una descripcion para la VirtualMachine: ")
                        if(descripcion == ''):
                            print("[*] Ingrese una descripcion válida\n")
                            continue
                        else:
                            if(descripcion == "ESC"):
                                print("[*] Ha salido de la opción de -Editar VirtualMachine-\n")
                                return
                            break
                elif(verificarDescripcion == "ESC"):
                    print("[*] Ha salido de la opción de -Editar VirtualMachine-\n")
                    return
                elif verificarDescripcion == "N" or verificarDescripcion == "n":
                    break
                else:
                    print("[*] Ingrese una opción correcta\n")
            if (verificarNombre == "N" or verificarNombre == "n") and (verificarDescripcion=="N" or verificarDescripcion == "n"):
                print("[*] Ha decidido no realizar ningún cambio a la VirtualMachine\n")
                break   
            nova.update_instance(nombre,nuevoNombre,descripcion,projectID)
            break
        else:
            print("[*] Ingrese un nombre de VirtualMachine válido\n")
            continue
        
#Funcion que permite eliminar una VM
def borrarVirtualMachine(nova,projectID):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese el nombre de una VirtualMachine: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Borrar VirtualMachine- \n")
                return
            nova.delete_instance(nombre)
            break
        else:
            print("[*] Ingrese un nombre válido\n")
            continue
   
#Funcion que permite obtener el ID de un Flavor   
def getFlavorsID(nova):
    idFlavor = None
    listado = nova.list_flavors()
    if len(listado) != 0:
        while True:
            Cabecera = ["#","NOMBRE FLAVOR","RAM (MB)","DISK (GB)","vCPUS"]
            filas = []
            i = 0
            for flavor in listado:
                filasopt = []
                filasopt.append(str(i+1))
                filasopt.append(str(flavor[1]))
                filasopt.append(str(flavor[2]))
                filasopt.append(str(flavor[3]))
                filasopt.append(str(flavor[4]))
                filas.append(filasopt)
                i = i + 1
            print("\n")
            print(tabulate(filas,headers=Cabecera,tablefmt='grid',stralign='center'))   
            opcionFlavor = input("| Ingrese el # del flavor que desea usar: ")
            try:
                if int(opcionFlavor) > len(listado):
                    print("[*] Ingrese el # de un flavor válido\n")
                else:
                    idFlavor = listado[int(opcionFlavor)-1][0]
                    break
            except ValueError:
                print("[*] Ingrese el # de un flavor válido\n")
    else:
        print("\n")
        print(tabulate([["No hay flavors creados."]],headers=[],tablefmt='grid',stralign='center'))
    return idFlavor
    
#Funcion que permite obtener el ID de una Imagen
def getImagenesID(glance):   
    idImagen = None
    listado = glance.listar_imagenes() 
    if len(listado) != 0:
        while True:
            Cabecera = ["#","NOMBRE IMAGE"]
            filas = []
            i = 0
            for imagen in listado:
                filasopt = []
                filasopt.append(str(i+1))
                filasopt.append(str(imagen[1]))
                filas.append(filasopt)
                i = i + 1
            print("\n")
            print(tabulate(filas,headers=Cabecera,tablefmt='grid',stralign='center'))
            opcionImagen = input("| Ingrese el # de la imagen que desea usar: ")
            try:
                if int(opcionImagen) > len(listado):
                    print("[*] Ingrese el # de una imagen válida\n")
                else:
                    idImagen = listado[int(opcionImagen)-1][0]
                    break
            except ValueError:
                print("[*] Ingrese el # de una imagen válida\n")
    else:
        print("\n")
        print(tabulate([["No hay imágenes creadas."]],headers=[],tablefmt='grid',stralign='center'))
    return idImagen

#Funcion que permite obtener el ID de una red
def getNetworkID(neutron,keystone):
    idRed = None
    listado = neutron.list_networks(keystone.getProjectID())
    if len(listado) != 0:
        while True:
            Cabecera = ["#","NOMBRE RED","CIDR","GATEWAY IP"]
            filas = []
            i = 0
            for red in listado:
                filasopt = []
                filasopt.append(str(i+1))
                filasopt.append(str(red[0]))
                filasopt.append(str(red[1]))
                filasopt.append(str(red[2]))
                filas.append(filasopt)
                i = i + 1
            print("\n")
            print(tabulate(filas,headers=Cabecera,tablefmt='grid',stralign='center'))
            opcionRed= input("| Ingrese el # de la red que desea usar: ")
            try:
                if int(opcionRed) > len(listado):
                    print("[*] Ingrese el # de una red válida\n")
                else:
                    idRed = listado[int(opcionRed)-1][3]
                    break
            except ValueError:
                print("[*] Ingrese el # de una red válida\n")
    else:
        print("\n")
        print(tabulate([["No hay redes creadas."]],headers=[],tablefmt='grid',stralign='center'))                 
    return idRed

#Funcion que permite obtener el ID de una keypair
def getKeyPairID(nova,keystone):
    listado = nova.listarKeyPair(keystone.getUserID())
    if len(listado) != 0:
        while True:
            Cabecera = ["#","NOMBRE KEYPAIR"]
            filas = []
            i = 1
            for key in listado:
                filasopt = []
                filasopt.append(str(i))
                filasopt.append(str(key))
                filas.append(filasopt)
                i = i + 1
            print("\n")
            print(tabulate(filas,headers=Cabecera,tablefmt='grid',stralign='center'))
            opcionKeyPair = input("| Ingrese el # de la keypair que desea usar: ")
            try:
                if int(opcionKeyPair) > len(listado):
                    print("[*] Ingrese el # de una keypair válida\n")
                else:
                    keypair = listado[int(opcionKeyPair)-1]
                    break
            except ValueError:
                print("[*] Ingrese el # de una keypair válida\n")
        return nova.obtenerIDKeyPair(keypair,keystone.getUserID())
    else:
        print("\n")
        print(tabulate([["No hay keypairs creadas."]],headers=[],tablefmt='grid',stralign='center'))
        return None
    
#Funcion que permite obtener el ID de un SecurityGroup
def getSecurityGroupID(nova):
    listado = nova.listarSecurityGroup()
    if len(listado) != 0:
        while True:
            Cabecera = ["#","NOMBRE SECURITYGROUP","DESCRIPTION"]
            filas = []
            i = 0
            for SG in listado:
                filasopt = []
                filasopt.append(str(i+1))
                filasopt.append(str(SG[0]))
                filasopt.append(str(SG[1]))
                filas.append(filasopt)
                i = i + 1
            print("\n")
            print(tabulate(filas,headers=Cabecera,tablefmt='grid',stralign='center'))           
            opcionSecurityGroup = input("| Ingrese el # del securitygroup que desea usar: ")
            try:
                if int(opcionSecurityGroup) > len(listado):
                    print("[*] Ingrese el # de un securitygroup válido\n")
                else:
                    securitygroup = listado[int(opcionSecurityGroup)-1][0]
                    break
            except ValueError:
                print("[*] Ingrese el # de un securitygroup válido\n")
        return nova.obtenerIDSecurityGroup(securitygroup)[0]
    else:
        print("\n")
        print(tabulate([["No hay security groups creados."]],headers=[],tablefmt='grid',stralign='center'))
        return None
    
#Funcion que muestra el Menú Flavors
def menuFlavors():    
    opciones = ["Crear Flavor","Listar Flavors","Eliminar Flavor"]
    while True:
            filas = []
            filasopt = []
            i = 0
            for opt in opciones:
                filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            filas.append(["\n".join(filasopt)])
            filas.append(["Opción "+str(i+1)+" -> Salir"])
            print("\n")
            print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
            opcion = input("| Ingrese una opción: ")
            try:
                if int(opcion) == (len(opciones)+1):
                    opcion = "Salir"
                    break
                else:
                    if int(opcion) <= len(opciones):
                        opcion = opciones[int(opcion)-1]
                        break
                    else:
                        print("[*] Ingrese una opción válida\n")
            except ValueError:
                print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion que permite crear Flavors
def crearFlavor(nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre para el flavor: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Crear Flavor-\n")
                return
            while True:
                ram = input("| Ingrese la cantidad de RAM (MB): ")
                if(ram == "ESC"):
                    print("[*] Ha salido de la opción de -Crear Flavor-\n")
                    return
                if validar_ram(ram):
                    while True:
                        vcpus = input("| Ingrese la cantidad de vCPUs: ")
                        if(vcpus == "ESC"):
                            print("[*] Ha salido de la opción de -Crear Flavor-\n")
                            return
                        if validar_vcpus(vcpus):
                            while True:
                                disk = input("| Ingrese el tamaño del DISK (GB): ")
                                if(disk == "ESC"):
                                    print("[*] Ha salido de la opción de -Crear Flavor-\n")
                                    return
                                if validar_disk(disk):
                                    nova.create_flavor(nombre, ram, vcpus, disk)
                                    return
                                else:
                                    print("[*] Ingrese un tamaño de DISK válido\n")
                                    continue
                        else:
                            print("[*] Ingrese una cantidad de vCPUs válido\n")
                            continue    
                else:
                    print("[*] Ingrese una cantidad de RAM válido\n")
                    continue
        else:
            print("[*] Ingrese un nombre de flavor válido\n")
            continue

#Funcion que permite listar flavors
def listarFlavors(nova):
    listado = nova.list_flavors()
    if len(listado) != 0:
        Cabecera = ["NOMBRE FLAVOR","RAM (MB)","DISK (GB)","vCPUS"]
        filas = []
        for flavor in listado:
            filasopt = []
            filasopt.append(str(flavor[1]))
            filasopt.append(str(flavor[2]))
            filasopt.append(str(flavor[3]))
            filasopt.append(str(flavor[4]))
            filas.append(filasopt)
        print("\n")
        print(tabulate(filas,headers=Cabecera,tablefmt='grid',stralign='center'))   
    else:
        print("\n")
        print(tabulate([["No hay flavors creados hasta el momento."]],headers=[],tablefmt='grid',stralign='center'))
        
#Funcion que permite borrar flavor
def borrarFlavor(nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese el nombre del flavor: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Borrar Flavor- \n")
                return
            nova.delete_flavor(nombre)
            break
        else:
            print("[*] Ingrese un nombre válido\n")
            continue

#Funcion que muestra el Menú Imagenes
def menuImages():    
    opciones = ["Crear Image","Listar Images","Editar Image","Eliminar Image"]
    while True:
        filas = []
        filasopt = []
        i = 0
        for opt in opciones:
            filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
            i = i + 1   
        filas.append(["\n".join(filasopt)])
        filas.append(["Opción "+str(i+1)+" -> Salir"])
        print("\n")
        print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
        opcion = input("| Ingrese una opción: ")
        try:
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida\n")
        except ValueError:
            print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion que permite crear una Image
def crearImage(glance):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre para el image: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Crear Image-\n")
                return
            while True:
                ruta = input("| Ingrese la ruta de la imagen a importar: ")
                if(ruta != ''):
                    if(ruta == "ESC"):
                        print("[*] Ha salido de la opción de -Crear Image-\n")
                        return
                    glance.cargar_imagen(nombre, ruta)
                    return
                else:
                    print("[*] Ingrese una ruta válida\n")
                    continue
        else:
            print("[*] Ingrese un nombre de image válido\n")
            continue
        
#Funcion que permite listar Images
def listarImages(glance):
    listado = glance.listar_imagenes() 
    if len(listado) != 0:
        cabeceras = ["IMAGES"]
        lista_resultante = [[elemento[1]] for elemento in listado]
        print("\n")
        print(tabulate(lista_resultante,headers=cabeceras,tablefmt='grid',stralign='center'))  
    else:
        print("\n")
        print(tabulate([["No hay imagenes creadas hasta el momento."]],headers=[],tablefmt='grid',stralign='center')) 
        
#Funcion que permite editar Images
def editarImage(glance):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre de image: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Editar Image-\n")
                return
            while True:
                verificarContenido = input("| ¿Desea cambiar el contenido de la image?[Y/N]: ")
                nuevoContenido = None
                if verificarContenido == "Y" or verificarContenido == "y":
                    while True:
                        nuevoContenido = input("| Ingrese la ruta de la image: ")
                        if(nuevoContenido == ''):
                            print("[*] Ingrese una ruta válida\n")
                            continue
                        else:
                            if(nuevoContenido == "ESC"):
                                print("[*] Ha salido de la opción de -Editar Image-\n")
                                return
                            break
                elif(verificarContenido == "ESC"):
                    print("[*] Ha salido de la opción de -Editar Image-\n")
                    return
                elif verificarContenido == "N" or verificarContenido == "n":
                    break
                else:
                    print("[*] Ingrese una ruta válida\n")
                    continue
            if nuevoContenido != None:
                glance.update(nombre,nuevoContenido)
            else:
                print("[*] No se ha realizado modificaciones al image\n")
            break
        else:
            print("[*] Ingrese un nombre de image válido\n")
            continue
        
#Funcion que permite eliminar Images
def borrarImage(glance):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese el nombre del image: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Borrar Image- \n")
                return
            glance.eliminar_imagen(nombre)
            break
        else:
            print("[*] Ingrese un nombre válido\n")
            continue

#Funcion que muestra el menú Topología
def menuTopologia():
    opciones = ["Añadir Topología","Editar Slice"]
    while True:
        filas = []
        filasopt = []
        i = 0
        for opt in opciones:
            filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
            i = i + 1   
        filas.append(["\n".join(filasopt)])
        filas.append(["Opción "+str(i+1)+" -> Salir"])
        print("\n")
        print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
        opcion = input("| Ingrese una opción: ")
        try:
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida\n")
        except ValueError:
            print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion que permite crear una topología
def crearTopologia(keystone,neutron,nova,glance):
    opciones = ["Lineal","Malla","Árbol","Anillo","Bus"]
    while True:
        filas = []
        filasopt = []
        i = 0
        for opt in opciones:
            filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
            i = i + 1   
        filas.append(["\n".join(filasopt)])
        filas.append(["Opción "+str(i+1)+" -> Salir"])
        print("\n")
        print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
        opcion = input("| Ingrese una opción: ")
        try:
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida\n")    
        except ValueError:
            print("[*] Ingrese una opción válida\n")       
    if opcion == "Lineal" or opcion == "Anillo" or opcion == "Bus" or opcion == "Malla":
        while True:
            cantidadNodos = input("| Ingrese la cantidad de nodos: ")
            if validar_cantidad_nodos(cantidadNodos):
                cantidadNodos = int(cantidadNodos)
                break 
            else:
                print("[*] Ingrese una cantidad válida\n")
                continue 
    elif opcion == "Árbol":
        while True:
            numeroNiveles = input("| Ingrese el número de niveles del árbol(Mayor a 2): ")
            if validar_cantidad_niveles(numeroNiveles):
                numeroNiveles = int(numeroNiveles)
                break 
            else:
                print("[*] Ingrese una cantidad válida\n")
                continue 
        while True:
            cantidadNodos = input("| Ingrese la cantidad de nodos: ")
            if validar_cantidad_nodos(cantidadNodos):
                cantidadNodos = int(cantidadNodos)
                break 
            else:
                print("[*] Ingrese una cantidad válida\n")
                continue   
    elif opcion == "Salir":
        return "Salir"
    while True:
        decision = input("| Desea configurar cada VM?[1] o Desea configurar todas de una vez?[2]: ")
        if int(decision) == 1 or int(decision) == 2:
            break
        else:
            print("[*] Ingrese una opción válida\n")
            continue    
    if int(decision) == 1:
        i = 1
        listaVMs = []
        while i <= cantidadNodos:
            print("|\n---Virtual Machine "+str(i) + "---")
            nombre = input("| Ingrese un nombre de VirtualMachine: ")
            if(nombre != ''):
                flavorID = getFlavorsID(nova)
                imagenID = getImagenesID(glance)
                keypairID = getKeyPairID(nova,keystone)
                securityID = getSecurityGroupID(nova)
                listaVMs.append(VM(nombre,flavorID,imagenID,keypairID,securityID))
                i = i + 1
            else:
                print("[*] Ingrese un nombre de VirtualMachine válido\n")
                continue
    if int(decision) == 2:
        flavorID = getFlavorsID(nova)
        imagenID = getImagenesID(glance)
        i = 1
        listaVMs = []
        while i <= cantidadNodos:
            print("|\n---Virtual Machine "+str(i) + "---")
            nombre = input("| Ingrese un nombre de VirtualMachine: ")
            if(nombre != ''):
                keypairID = getKeyPairID(nova,keystone)
                securityID = getSecurityGroupID(nova)
                listaVMs.append(VM(nombre,flavorID,imagenID,keypairID,securityID))
                i = i + 1
            else:
                print("[*] Ingrese un nombre de VirtualMachine válido\n")
                continue
    while True:
        CIDR = input("| Ingrese el CIDR de la red: ")
        if validar_cidr(CIDR):
            break
        else:
            print("[*] Ingrese un CIDR válido\n")
            continue         
    if opcion == "Lineal":
        TopoConstructor().lineConstructor(listaVMs,CIDR, neutron, nova)      
    elif opcion == "Anillo":
        TopoConstructor().ringConstructor(listaVMs,CIDR, neutron, nova)   
    elif opcion == "Bus":
        TopoConstructor().busConstructor(listaVMs,CIDR, neutron, nova)   
    elif opcion == "Malla":
        TopoConstructor().meshConstructorV2(listaVMs,CIDR, neutron, nova)   
    elif opcion == "Árbol":
        TopoConstructor().treeConstructor(listaVMs,CIDR,neutron,nova,numeroNiveles)
    return "Salir"
    
#Funcion que permite editar un slice
def editarSlice(keystone,neutron,nova):
    opciones = ["Unir VMs","Unir VM a Red"]
    while True:
        filas = []
        filasopt = []
        i = 0
        for opt in opciones:
            filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
            i = i + 1   
        filas.append(["\n".join(filasopt)])
        filas.append(["Opción "+str(i+1)+" -> Salir"])
        print("\n")
        print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
        opcion = input("| Ingrese una opción: ")
        try:
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida\n")
        except ValueError:
            print("[*] Ingrese una opción válida\n")
    if opcion == "Unir VMs":            
        print("**Escriba ESC para poder salir de esta opción**")
        while True:
            nombre = input("| Ingrese el nombre de la primera VM: ")
            if(nombre != ''):
                if(nombre == "ESC"):
                    print("[*] Ha salido de la opción de -Editar Slice- \n")
                    return "Salir"
                while True:
                    nombre2 = input("| Ingrese el nombre de la segunda VM: ")
                    if(nombre2 != ''):
                        if(nombre2 == "ESC"):
                            print("[*] Ha salido de la opción de -Editar Slice- \n")
                            return "Salir"
                        while True:
                            cidrRed = input("| Ingrese el CIDR de la red: ")
                            if(cidrRed == "ESC"):
                                print("[*] Ha salido de la opción de -Editar Slice- \n")
                                return "Salir"
                            if validar_cidr(cidrRed):
                                TopoConstructor.linkConstructor(neutron=neutron,nova=nova,VMs=[VM(name=nombre,flavorID=None,imageID=None,keyPairID=None,securitygroupID=None),VM(name=nombre2,flavorID=None,imageID=None,keyPairID=None,securitygroupID=None)],network=[],CIDR=cidrRed)
                                return "Salir"
                            else:
                                print("[*] Ingrese un CIDR válido\n")
                                continue
                    else:
                        print("[*] Ingrese un nombre válido\n")
                        continue
            else:
                print("[*] Ingrese un nombre válido\n")
                continue
    if opcion == "Unir VM a Red":
        print("**Escriba ESC para poder salir de esta opción**")
        while True:
            nombre = input("| Ingrese el nombre de la VM: ")
            if(nombre != ''):
                if(nombre == "ESC"):
                    print("[*] Ha salido de la opción de -Editar Slice- \n")
                    return "Salir"
                while True:
                    red = input("| Ingrese el nombre de la red provider: ")
                    if(red != ''):
                        if(red == "ESC"):
                            print("[*] Ha salido de la opción de -Editar Slice- \n")
                            return "Salir"
                        TopoConstructor.linkConstructor(neutron=neutron,nova=nova,VMs=[VM(name=nombre,flavorID=None,imageID=None,keyPairID=None,securitygroupID=None)],network=[red],CIDR=None)
                        return "Salir"
                    else:
                        print("[*] Ingrese un nombre de red válido\n")
                        continue    
            else:
                print("[*] Ingrese un nombre válido\n")
                continue
    return "Salir"

#Función que muestra el Menú Recursos
def menuRecursos(keystone):
    opcionesAdmin = ["Info Servidores","Editar Nivel Máximo de Sobreaprovisionamiento","Mostrar Nivel Máximo de Sobreaprovisionamiento"]
    opcionesUsuario = ["Info Servidores","Mostrar Nivel Máximo de Sobreaprovisionamiento"]
    if keystone.getRolName() == "admin":
        opciones = opcionesAdmin
    else:
        opciones = opcionesUsuario
    while True:
            filas = []
            filasopt = []
            i = 0
            for opt in opciones:
                filasopt.append("Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            filas.append(["\n".join(filasopt)])
            filas.append(["Opción "+str(i+1)+" -> Salir"])
            print("\n")
            print(tabulate(filas,headers=[],tablefmt='fancy_grid',stralign='center'))
            opcion = input("| Ingrese una opción: ")
            try:
                if int(opcion) == (len(opciones)+1):
                    opcion = "Salir"
                    break
                else:
                    if int(opcion) <= len(opciones):
                        opcion = opciones[int(opcion)-1]
                        break
                    else:
                        print("[*] Ingrese una opción válida\n")
            except ValueError:
                print("[*] Ingrese una opción válida\n")
    return opcion

#Funcion que muestra la informacion de servidores
def obtenerInfoServidores():
    informacion = obtenerInfoRemoto()
    if len(informacion) != 0:
        for datita in informacion:
            print("\n")
            print(tabulate(datita,headers=[],tablefmt='grid',stralign='left'))
    else:
        print("\n")
        print(tabulate([["El servicio de monitoreo se encuentra caído."]],headers=[],tablefmt='grid',stralign='center'))

#Funcion que muestra el nivel de sobreaprovisionamiento
def mostrarNivelDeSobreaprovisionamiento():
    global nivelMaximoAprovisionamiento
    if(nivelMaximoAprovisionamiento==0):
        print("\n")
        print(tabulate([["Aún no se ha definido el nivel de aprovisionamiento en el sistema."]],headers=["Nivel de Sobreaprovisionamiento"],tablefmt='grid',stralign='center'))
    else:
        print("\n")
        print(tabulate([["El nivel de aprovisionamiento máximo en el sistema es "+str(nivelMaximoAprovisionamiento)+"%"]],headers=["Nivel de Sobreaprovisionamiento"],tablefmt='grid',stralign='center'))

#Funcion que permite editar el nivel de sobreaprovisionamiento
def editarNivelDeSobreaprovisionamiento():
    global nivelMaximoAprovisionamiento
    if(nivelMaximoAprovisionamiento==0):
        while True:
            try:
                nuevoNivel = int(input("| Ingrese el nivel de aprovisionamiento máximo en (%): "))
                if(nuevoNivel>0 and nuevoNivel<100):
                    nivelMaximoAprovisionamiento = nuevoNivel
                    print("[*] Se añadio el nivel de aprovisionamiento exitosamente\n")
                    return
                else:
                    print("[*] Debe ser un valor que se encuentre entre ]0;100[ (%)\n")
                    continue
            except ValueError:
                print("[*] Debe ingresar un valor entero\n")
                continue
    else:
        while True:
            try:
                nivelAprovisionamiento = int(input("| Edite el valor del nivel de aprovisionamiento(%): "))
                if(nivelAprovisionamiento>0 and nivelAprovisionamiento<100):
                    nivelMaximoAprovisionamiento = nivelAprovisionamiento
                    print("[*] Se editó el nivel de aprovisionamiento exitosamente\n")
                    return
                else:
                    print("[*] Debe ser un valor que se encuentre entre ]0;100[ (%)\n")
                    continue
            except ValueError:
                print("[*] Debe ingresar un valor entero\n")
                continue

#Funcion SubMenú
def menu2(opcion,nivel,keystone,nova,glance,neutron):
    if opcion == "Usuario":
        if(nivel == "Menú"):
            while True:
                seleccion = menuUsuarios()
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)
                if not (resultado):
                    break
        elif(nivel == "Listar usuarios"):
            listarUsuariosProyecto(keystone)
        elif(nivel == "Crear usuario"):
            crearUsuario(keystone)   
        elif(nivel == "Añadir usuario"):
            asignarRolUsuarioAProyecto(keystone) 
        elif(nivel == "Editar usuario"):
            editarUsuario(keystone)
        elif(nivel == "Eliminar usuario"):
            eliminarRolUsuarioDeProyecto(keystone)
        elif(nivel == "Salir"):        
            return False
        return True
        
    elif opcion == "Red":
        if(nivel == "Menú"):
            while True:
                seleccion = menuRedes(keystone)
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break
        elif(nivel == "Crear red"):
            crearRed(keystone,neutron,nova,glance)
        elif(nivel == "Listar redes"):
            infoRed(keystone,neutron)   
        elif(nivel == "Borrar red"):
            borrarRed(keystone, neutron)      
        elif(nivel == "Salir"):        
            return False
        return True
    
    elif opcion == "Topología":
        if(nivel == "Menú"):
            while True:
                seleccion = menuTopologia()
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break
        elif(nivel == "Añadir Topología"):
            crearTopologia(keystone,neutron,nova,glance)
        elif(nivel == "Editar Slice"):
            editarSlice(keystone,neutron,nova)    
        elif(nivel == "Salir"):        
            return False
        return True
    
    elif opcion == "KeyPair":
        if(nivel == "Menú"):
           while True:
                seleccion = menuKeyPair()
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break
        elif(nivel == "Crear keypair"):
            crearKeyPair(keystone,nova)
        elif(nivel == "Listar keypair"):
            listarKeypair(keystone,nova)
        elif(nivel == "Info keypair"):
            infoKeypair(keystone,nova)
        elif(nivel == "Eliminar keypair"):
            borrarKeypair(keystone,nova)
        elif(nivel == "Salir"):
            return False
        return True
    
    elif opcion == "SecurityGroup":
        if(nivel == "Menú"):
           while True:
                seleccion = menuSecurityGroup()
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break
        elif(nivel == "Crear SecurityGroup"):
            crearSecurityGroup(nova)
        elif(nivel == "Listar SecurityGroup"):
            listarSecurityGroup(nova)
        elif(nivel == "Info SecurityGroup"):
            infoSecurityGroup(nova)
        elif(nivel == "Editar SecurityGroup"):
            editarSecurityGroup(nova)
        elif(nivel == "Eliminar SecurityGroup"):
            borrarSecurityGroup(nova)
        elif(nivel == "Configurar SecurityGroup"):
            configurarSecurityGroup(nova)
        elif(nivel == "Salir"):
            return False
        return True
    
    elif opcion == "VirtualMachine":
        if(nivel == "Menú"):
           while True:
                seleccion = menuVirtualMachine()
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break
        elif(nivel == "Crear VirtualMachine"):
            crearVirtualMachine(nova,neutron,glance,keystone)
        elif(nivel == "Listar VirtualMachine"):
            listarVirtualMachine(keystone,nova)
        elif(nivel == "Editar VirtualMachine"):
            editarVirtualMachine(nova,keystone.getProjectID())
        elif(nivel == "Eliminar VirtualMachine"):
            borrarVirtualMachine(nova,keystone.getProjectID())
        elif(nivel == "Salir"):
            return False
        return True
    
    elif opcion == "Flavors":
        if(nivel == "Menú"):
           while True:
                seleccion = menuFlavors()
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break    
        elif(nivel == "Crear Flavor"):
            crearFlavor(nova)
        elif(nivel == "Listar Flavors"):
            listarFlavors(nova)
        elif(nivel == "Eliminar Flavor"):
            borrarFlavor(nova)
        elif(nivel == "Salir"):
            return False
        return True
    
    elif opcion == "Images":
        if(nivel == "Menú"):
           while True:
                seleccion = menuImages()
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break 
        elif(nivel == "Crear Image"):
            crearImage(glance)
        elif(nivel == "Listar Images"):
            listarImages(glance)
        elif(nivel == "Editar Image"):
            editarImage(glance)
        elif(nivel == "Eliminar Image"):
            borrarImage(glance)
        elif(nivel == "Salir"):
            return False
        return True
    
    elif opcion == "Monitoreo de Recursos":
        if(nivel == "Menú"):
           while True:
                seleccion = menuRecursos(keystone)
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break 
        elif(nivel == "Info Servidores"):
            obtenerInfoServidores()
        elif(nivel == "Editar Nivel Máximo de Sobreaprovisionamiento"):
            editarNivelDeSobreaprovisionamiento()
        elif(nivel == "Mostrar Nivel Máximo de Sobreaprovisionamiento"):
            mostrarNivelDeSobreaprovisionamiento()
        elif(nivel == "Salir"):
            return False
        return True
    elif opcion == "Salir":
        return False  
    
############################################    M   A   I   N   ############################################      
#Mensaje de bienvenida
nivelMaximoAprovisionamiento = 0
Cabecera1 = ["Ingeniería de Redes Cloud"]
Filas1 = [["TEL141\nProyecto del Grupo 1\nProfesor: Cesar Santivañez\nAsesor: Fernando Guzman"] , ["Integrantes"], ["José Ortiz Velasquez\nAlonso Rosales Antunez\nRonny Pastor Kolmakov\nAgustin Vizcarra Lizarbe (L)"]]
print(tabulate(Filas1,headers=Cabecera1,tablefmt='fancy_grid',stralign='center'))
print("|---Ingrese sus crendenciales--|")
privilegios = -1
while(int(privilegios)<0):
    username = input("| Ingrese su nombre de usuario: ")
    password = getpass("| Ingrese su contraseña: ")
    keystone = KeystoneAuth(username, password)
    tokensito = keystone.get_token()
    #Si tiene cuenta de Openstack 
    if tokensito != None:
        tokensito = keystone.updateToken()
        while True:
            result,keystone = MenuListaProyectos(keystone)
            project_id=keystone.getProjectID()
            tokensito = keystone.get_token_project(project_id)
            if not (result): #No esta asignado a ningun proyecto
                print("[*] Gracias por usar nuestro sistema!\n")
                privilegios = 0
                break
            else:
                while True:
                    nova = NovaClient(tokensito,username,password)
                    glance = GlanceClient(tokensito)
                    neutron = NeutronClient(tokensito)
                    opcion = menuPrincipal(keystone)
                    resultado = menu2(opcion,"Menú",keystone,nova,glance,neutron)
                    if not (resultado):
                        break  
            tokensito = keystone.updateToken()   
                    
    #Si tiene cuenta de Linux
    else:
        AutenticacionLinux = AuthenticationManager()    
        response = AutenticacionLinux.get_auth(username, password)
        id = response["id"]
        if id == 0:
            print("[*]Ha ingresado credenciales inválidas o su usuario no existe.")
        else:
            while True:
                print("[*]Bienvenido al Menú Principal")
                print("[*]Orquestador: Linux")
                permisos = response["permisos"] 
                if permisos == 0:
                    print("[*] Bienvenido usuario "+username+" !")
                    usuario = Usuario(id=id)
                    usuario.menuUsuario(id)
                    print("[*] Gracias por usar nuestro sistema!\n")
                    privilegios = 0
                    break 
                else:
                    print("[*] Bienvenido administrador "+username+" !")
                    admin = Administrador(id=id)
                    admin.menuAdministrador(id)
                    print("[*] Gracias por usar nuestro sistema!\n")
                    privilegios = 0
                    break 
