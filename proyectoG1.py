from getpass import getpass
from keystone import KeystoneAuth
from Nova import NovaClient
from Glance import GlanceClient
from Neutron import NeutronClient
from AutheticationDriver import AuthenticationManager
from menuLinux import Usuario
from menuLinux import Administrador
import requests
############################################    F   U   N   C   I   O   N   E   S   ############################################
#Funcion que muestra el menu de la lista de Proyectos
def MenuListaProyectos(keystone):
    listaProyectos, listaRoles = keystone.getListProjects()
    if len(listaProyectos) == 0:   
        print("|--------------------Lista de Proyectos------------------------|")
        print("|Actualmente, usted no se encuentra asignado a ningún proyecto.|")
        print("|Porfavor, póngase en contacto con su PhD. Santivañez.         |")
        print("|--------------------------------------------------------------|")
        return False,keystone
    else:
        while True:
            print("\n|--------------------Lista de Proyectos------------------------|")
            i = 0
            for proyecto in listaProyectos:
                print("|- Proyecto "+str(i+1)+" -> "+str(proyecto[1])+"     |   Rol: "+ str(listaRoles[i]))
                i = i + 1
            print("|--------------------------------------------------------------|")
            print("                **Escriba ESC para poder salir**               ")
            print("|--------------------------------------------------------------|")
            opcionProyecto = input("| Ingrese el # del proyecto al que desea ingresar: ")
            if str(opcionProyecto) == "ESC":
                return False,keystone
            
            if int(opcionProyecto) > len(listaProyectos):
                 print("[*] Ingrese el # de un proyecto válido\n")
            else:
                idProyecto = listaProyectos[int(opcionProyecto)-1][0]
                keystone.setProjectID(idProyecto)
                keystone.setRolName(listaRoles[int(opcionProyecto)-1])
                break
        return True,keystone
   
#Funcion que muestra el Menú Principal        
def menuPrincipal(keystone):
    opcionesAdmin = ["Usuario","RedProvider","KeyPair","SecurityGroup","VirtualMachine","Flavors","Images"]
    opcionesUsuario = ["RedProvider","KeyPair","SecurityGroup","VirtualMachine"]
    if keystone.getRolName() == "admin":
        opciones = opcionesAdmin
    else:
        opciones = opcionesUsuario
    while True:
            print("\n|--------------------Menú Principal------------------------|")
            i = 0
            for opt in opciones:
                print("|- Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1
            print("|- Opción "+str(i+1)+" -> Salir                             ")
            print("|------------------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida.\n")
    return opcion

#Funcion que muestra el Menú Usuarios
def menuUsuarios():
    #opciones = ["Listar usuarios","Crear usuario","Añadir usuario","Editar usuario",
    #                 "Eliminar usuario"]
    opciones = ["Listar usuarios","Eliminar usuario"]
    while True:
            print("\n|-----------------------------------------------------|")
            i = 0
            for opt in opciones:
                print("|- Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            print("|- Opción "+str(i+1)+" -> Salir")
            print("|-----------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida.")
    return opcion

#Funcion para listar proyectos por usuario
def listarUsuariosProyecto(keystone):
    listado = keystone.listarProyectosUsuarios()
    print("\n|-----------------------------------------------------|")
    i = 1
    for user in listado:
        print("| Usuario "+str(i)+": "+str(user))
        i = i + 1
    print("|-----------------------------------------------------|")
    
#Funcion para Crear Usuario
def crearUsuario(keystone):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        username = input("| Ingrese un nombre de usuario: ")
        if(username != ''):
            if(username == "ESC"):
                print("[*] Ha salido de la opción de -Crear Usuario-\n")
                return
            while True:
                password = getpass("| Ingrese su contraseña: ")
                if(password != ''):
                    if(password == "ESC"):
                        print("[*] Ha salido de la opción de -Crear Usuario- \n")
                        return
                    email = input("| Ingrese una dirección de correo: ")
                    if(email == "ESC"):
                        print("[*] Ha salido de la opción de -Crear Usuario-\n")
                        return
                    keystone.crear_usuario(username, password, email)
                    return
                else:
                    print("[*] Ingrese una contraseña válida\n")
                    continue
        else:
            print("[*] Ingrese un nombre de usuario válido\n")
            continue

#Funcion para asignar usuario a un proyecto
def asignarRolUsuarioAProyecto(keystone):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        username = input("| Ingrese un nombre de usuario: ")
        if(username != ''):
            if(username == "ESC"):
                print("[*] Ha salido de la opción de -Añadir usuario-\n")
                return
            keystone.asignarUsuarioProyecto(username)
            return
        else:
            print("[*] Ingrese un nombre de usuario válido\n")
            continue
  
#Funcion para editar usuario
def editarUsuario(keystone):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        username = input("| Ingrese un nombre de usuario: ")
        if(username != ''):
            if(username == "ESC"):
                print("[*] Ha salido de la opción de -Editar Usuario-\n")
                return
            verificarPass = input("| ¿Desea cambiar su contraseña?[Y/N]: ")
            password = None
            if verificarPass == "Y" or verificarPass == "y":
                while True:
                    password = getpass("| Ingrese la nueva contraseña: ")
                    if(password == ''):
                        print("[*] Ingrese una contraseña válida\n")
                        continue
                    else:
                        if(password == "ESC"):
                            print("[*] Ha salido de la opción de -Editar Usuario-\n")
                            return
                        break
            elif(verificarPass == "ESC"):
                print("[*] Ha salido de la opción de -Editar Usuario-\n")
                return           
            verificarEmail = input("| ¿Desea cambiar su email?[Y/N]: ")
            email = None
            if verificarEmail == "Y" or verificarEmail == "y":
                email = input("| Ingrese la nueva dirección de correo: ")
                if(email == "ESC"):
                    print("[*] Ha salido de la opción de -Editar Usuario-\n")
                    return    
            elif(verificarEmail == "ESC"):
                print("[*] Ha salido de la opción de -Editar Usuario-\n")
                return
            if (verificarPass == "N") and (verificarEmail=="N"):
                print("[*] Ha decidido no realizar ningún cambio al usuario\n")
                break 
            keystone.editar_usuario(username,password,email)
            break
        else:
            print("[*] Ingrese un nombre de usuario válido\n")
            continue
        
#Eliminar usuario de un proyecto
def eliminarRolUsuarioDeProyecto(keystone):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        username = input("| Ingrese un nombre de usuario: ")
        if(username != ''):
            if(username == "ESC"):
                print("[*] Ha salido de la opción de -Eliminar usuario-\n")
                return
            keystone.eliminarUsuarioProyecto(username)
            return
        else:
            print("[*] Ingrese un nombre de usuario válido\n")
            continue

#Funcion que muestra el Menú redesprovider
def menuRedes(keystone):
    opcionesAdmin = ["Crear red","Info red"]
    opcionesUsuario = ["Info red"]
    if keystone.getRolName() == "admin":
        opciones = opcionesAdmin
    else:
        opciones = opcionesUsuario
    while True:
            print("\n|-----------------------------------------------------|")
            i = 0
            for opt in opciones:
                print("|- Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            print("|- Opción "+str(i+1)+" -> Salir")
            print("|-----------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida.")
    return opcion

#Funcion que permite crear RedProvider
def crearRed(keystone,neutron):
    existe = neutron.existe_network(keystone.getProjectID())
    if existe == True:
        print("[*] Ya existe una RedProvider creada.\n")
        return
    
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        red = input("| Ingrese un nombre de red: ")
        if(red != ''):
            if(red == "ESC"):
                print("[*] Ha salido de la opción de -Crear RedProvider-\n")
                return
            while True:
                subred = input("| Ingrese un nombre de subred: ")
                if(subred != ''):
                    if(subred == "ESC"):
                        print("[*] Ha salido de la opción de -Crear RedProvider- \n")
                        return
                    while True:
                        cidr = input("| Ingrese un CIDR: ")
                        if(cidr != ''):
                            if(cidr == "ESC"):
                                print("[*] Ha salido de la opción de -Crear RedProvider- \n")
                                return
                            while True:
                                gatewayIP = input("| Ingrese una IP del gateway: ")
                                if(gatewayIP != ''):
                                    if(gatewayIP == "ESC"):
                                        print("[*] Ha salido de la opción de -Crear RedProvider- \n")
                                        return
                                    neutron.create_network(red,subred,cidr,gatewayIP,keystone.getProjectID())
                                    return
                                else:
                                    print("[*] Ingrese una IP válido\n")
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

#Funcion que permite mostrar la info de la RedProvider
def infoRed(neutron):
    informacion = neutron.infoRedProvider()
    print("\n|-----------------------------------------------------|")
    print("|Nombre RedProvider: "+ str(informacion[0]))
    print("|Descripcion: "+ str(informacion[1]))
    print("|Fecha Creación: "+ str(informacion[2]))
    print("|CIDR: "+ str(informacion[3]))
    print("|Gateway IP: "+ str(informacion[4]))
    print("|-----------------------------------------------------|")
    
#Funcion que muestra el Menú keypair
def menuKeyPair():
    opciones = ["Crear keypair","Listar keypair","Info keypair","Eliminar keypair"]
    while True:
            print("\n|-----------------------------------------------------|")
            i = 0
            for opt in opciones:
                print("|- Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            print("|- Opción "+str(i+1)+" -> Salir")
            print("|-----------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida.")
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
                ubicacion = input("| Ingrese la ubicación de la KeyPair: ")
                if(ubicacion != ''):
                    if(ubicacion == "ESC"):
                        print("[*] Ha salido de la opción de -Crear KeyPair- \n")
                        return
                    nova.crearKeyPair(nombre, ubicacion, keystone.getUserID())
                    return
                else:
                    print("[*] Ingrese una dirección válida\n")
                    continue
        else:
            print("[*] Ingrese un nombre de keypair válido\n")
            continue

#Funcion para listar las keypair
def listarKeypair(keystone,nova):
    listado = nova.listarKeyPair(keystone.getUserID())
    print("\n|-----------------------------------------------------|")
    i = 1
    for key in listado:
        print("| KeyPair "+str(i)+": "+str(key))
        i = i + 1
    print("|-----------------------------------------------------|")

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
    informacionsita = nova.infoKeyPair(nombre, keystone.getUserID())
    print("\n|-----------------------------------------------------|")
    print("|Nombre KeyPair: "+ str(informacionsita[0]))
    print("|Tipo: "+ str(informacionsita[1]))
    print("|FingerPrint: "+ str(informacionsita[2]))
    print("|Fecha Creación: "+ str(informacionsita[3]))
    print("|Public Key: "+ str(informacionsita[4]))
    print("|-----------------------------------------------------|")

#Funcion para borrar la keypair
def borrarKeypair(keystone,nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese el nombre de la KeyPair: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Borrar KeyPair- \n")
                return
            nova.borrarKeyPair(nombre, keystone.getUserID())
            break
        else:
            print("[*] Ingrese un nombre válido\n")
            continue

#Funcion que muestra el Menú SecurityGroup
def menuSecurityGroup():
    opciones = ["Crear SecurityGroup","Listar SecurityGroup","Editar SecurityGroup","Configurar SecurityGroup","Eliminar SecurityGroup"]
    while True:
            print("\n|-----------------------------------------------------|")
            i = 0
            for opt in opciones:
                print("|- Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            print("|- Opción "+str(i+1)+" -> Salir")
            print("|-----------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida.")
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
    print("\n|-----------------------------------------------------|")
    for SG in listado:
        print("| SecurityGroup "+str(SG[0])+" |  Descripcion : "+str(str(SG[1])))
    print("|-----------------------------------------------------|")

#Funcion que permite editar un security group
def editarSecurityGroup(nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        name = input("| Ingrese un nombre de SecurityGroup: ")
        if(name != ''):
            if(name == "ESC"):
                print("[*] Ha salido de la opción de -Editar SecurityGroup-\n")
                return
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
            verificarDescripcion = input("| ¿Desea cambiar la descripcion?[Y/N]: ")
            descripcion = None
            if verificarDescripcion == "Y" or verificarDescripcion == "y":
                descripcion = input("| Ingrese una nueva descripcion: ")
                if(descripcion == "ESC"):
                    print("[*] Ha salido de la opción de -Editar SecurityGroup-\n")
                    return    
            elif(verificarDescripcion == "ESC"):
                print("[*] Ha salido de la opción de -Editar SecurityGroup-\n")
                return
            if (verificarNombre == "N") and (verificarDescripcion=="N"):
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
        else:
            print("[*] Ingrese un nombre de securitygroup válido\n")
            continue

#Funcion que permite configurar un SecurityGroup
def configurarSecurityGroup(nova):
    while True:
        print("\n|------------------------------------|")
        print("|1. Añadir Regla                     |")
        print("|2. Eliminar Regla                    |")
        print("|3. Salir                            |")
        print("|------------------------------------|")
        opcion = input("| Ingrese una opción: ")
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
                                if(from_port != ''):
                                    if(from_port == "ESC"):
                                        print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                        return
                                    while True:
                                        dest_port = input("| Ingrese el dest port: ")
                                        if(dest_port != ''):
                                            if(dest_port == "ESC"):
                                                print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                return 
                                            verificar = input("| ¿Desea agregar un CIDR?[Y/N]: ")
                                            cidr = None
                                            if verificar == "Y" or verificar == "y":
                                                cidr = input("| Ingrese un CIDR: ")
                                                if(cidr == "ESC"):
                                                    print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                    return        
                                            elif(verificar == "ESC"):
                                                print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                return
                                            nova.agregarRegla(nombre,protocol_ip,from_port,dest_port,cidr)
                                            return
                                        else:
                                            print("[*] Ingrese un puerto válido\n")
                                            continue
                                else:
                                    print("[*] Ingrese un puerto válido\n")
                                    continue
                        else:
                            print("[*] Ingrese un protocolo IP válido\n")
                            continue
                else:
                    print("[*] Ingrese un nombre de securitygroup válido\n")
                    continue
        elif int(opcion) == 2:
            print("**Escriba ESC para poder salir de esta opción**")
            while True:
                id = input("| Ingrese el ID de la regla: ")
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

#Funcion que muestra el Menú VirtualMachine
def menuVirtualMachine():
    opciones = ["Crear VirtualMachine","Listar VirtualMachine","Editar VirtualMachine","Eliminar VirtualMachine"]
    while True:
            print("\n|-----------------------------------------------------|")
            i = 0
            for opt in opciones:
                print("|- Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            print("|- Opción "+str(i+1)+" -> Salir")
            print("|-----------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida.")
    return opcion

#Funcion que permite crear una VirtualMachine
def crearVirtualMachine(nova,neutron,glance,keystone):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre para la VirtualMachine: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Crear VirtualMachine-\n")
                return
            flavorID = getFlavorsID(nova)
            imagenID = getImagenesID(glance)
            networkID = neutron.getNetworkID()
            keyPairID = getKeyPairID(nova,keystone)
            securityGroupID = getSecurityGroupID(nova)
            nova.create_instance(nombre, flavorID, imagenID, networkID,keyPairID,securityGroupID)
        else:
            print("[*] Ingrese un nombre de VirtualMachine válido\n")
            continue

#Funcion que permite listar las VirtualMachine
def listarVirtualMachine(keystone,nova):
    listado = nova.list_instances(keystone.ProjectID)
    print("\n|-----------------------------------------------------|")
    i = 1
    for VM in listado:
        print("| "+str(i)+". VM "+str(VM)+" |")
        i = i + 1
    print("|-----------------------------------------------------|")

#Funcion que permite editar una VirtualMachine
def editarVirtualMachine(nova):
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombre = input("| Ingrese un nombre de VirtualMachine: ")
        if(nombre != ''):
            if(nombre == "ESC"):
                print("[*] Ha salido de la opción de -Editar VirtualMachine-\n")
                return
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
            nova.update_instance(nombre,nuevoNombre,descripcion)
        else:
            print("[*] Ingrese un nombre de VirtualMachine válido\n")
            continue
        
#Funcion que permite eliminar una VM
def borrarVirtualMachine(nova):
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
    listado = nova.list_flavors()
    while True:
        print("|--------------------Lista de Flavors------------------------|")
        i = 0
        for flavor in listado:
            print("|- Flavor "+str(i+1)+" -> "+str(flavor[1])+"| RAM: "+ str(flavor[2])+ "   | DISK: "+ str(flavor[3])+" | VCPUS: "+ str(flavor[4]))
            i = i + 1
        print("|--------------------------------------------------------------|")
        opcionFlavor = input("| Ingrese el # del flavor que desea usar: ")
        if opcionFlavor > len(listado):
            print("[*] Ingrese el # de un flavor válido\n")
        else:
            idFlavor = listado[int(opcionFlavor)-1][0]
            break
    return idFlavor
    
#Funcion que permite obtener el ID de una Imagen
def getImagenesID(glance):   
    listado = glance.listar_imagenes() 
    while True:
        print("|--------------------Lista de Imagenes------------------------|")
        i = 0
        for imagen in listado:
            print("|- Imagen "+str(i+1)+" -> "+str(imagen[1]))
            i = i + 1
        print("|--------------------------------------------------------------|")
        opcionImagen = input("| Ingrese el # de la imagen que desea usar: ")
        if opcionImagen > len(listado):
            print("[*] Ingrese el # de una imagen válida\n")
        else:
            idImagen = listado[int(opcionImagen)-1][0]
            break
    return idImagen

#Funcion que permite obtener el ID de una keypair
def getKeyPairID(nova,keystone):
    listado = nova.listarKeyPair(keystone.getUserID())
    while True:
        print("\n|-----------------------------------------------------|")
        i = 1
        for key in listado:
            print("| KeyPair "+str(i)+": "+str(key)+ "  |")
            i = i + 1
        print("|-----------------------------------------------------|")
        opcionKeyPair = input("| Ingrese el # de la keypair que desea usar: ")
        if opcionKeyPair > len(listado):
            print("[*] Ingrese el # de una keypair válida\n")
        else:
            keypair = listado[int(opcionKeyPair)-1][0]
            break
    return nova.obtenerIDKeyPair(keypair)
    
#Funcion que permite obtener el ID de un SecurityGroup
def getSecurityGroupID(nova):
    listado = nova.listarSecurityGroup()
    while True:
        print("\n|-----------------------------------------------------|")
        for SG in listado:
            print("| SecurityGroup "+str(SG[0])+" |  Descripcion : "+str(str(SG[1]))+ "  |")
        print("|-----------------------------------------------------|")    
        opcionSecurityGroup = input("| Ingrese el # del securitygroup que desea usar: ")
        if opcionSecurityGroup > len(listado):
            print("[*] Ingrese el # de un securitygroup válido\n")
        else:
            securitygroup = listado[int(opcionSecurityGroup)-1][0]
            break
    return nova.obtenerIDSecurityGroup(securitygroup)
    
    
#Funcion que muestra el Menú Flavors
def menuFlavors():    
    opciones = ["Crear Flavor","Listar Flavors","Editar Flavor","Eliminar Flavor"]
    while True:
            print("\n|-----------------------------------------------------|")
            i = 0
            for opt in opciones:
                print("|- Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            print("|- Opción "+str(i+1)+" -> Salir")
            print("|-----------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida.")
    return opcion

#Funcion que muestra el Menú Imagenes
def menuImages():    
    opciones = ["Crear Image","Listar Images","Editar Image","Eliminar Image"]
    while True:
            print("\n|-----------------------------------------------------|")
            i = 0
            for opt in opciones:
                print("|- Opción "+str(i+1)+" -> "+str(opt))
                i = i + 1   
            print("|- Opción "+str(i+1)+" -> Salir")
            print("|-----------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opciones)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opciones):
                    opcion = opciones[int(opcion)-1]
                    break
                else:
                    print("[*] Ingrese una opción válida.")
    return opcion

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
        
    elif opcion == "RedProvider":
        if(nivel == "Menú"):
            while True:
                seleccion = menuRedes(keystone)
                resultado = menu2(opcion,seleccion,keystone,nova,glance,neutron)  
                if not (resultado):
                    break
        elif(nivel == "Crear red"):
            crearRed(keystone,neutron)
        elif(nivel == "Info red"):
            infoRed(neutron)         
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
            editarVirtualMachine(nova)
        elif(nivel == "Eliminar VirtualMachine"):
            borrarVirtualMachine(nova)
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
        elif(nivel == "Salir"):
            return False

        return True
    
    
    elif opcion == "Salir":
        return False  
    
############################################    M   A   I   N   ############################################      
#Mensaje de bienvenida
print("----------------Ingeniería de Redes Cloud--------------------")
print("|                        TEL141                             |")
print("|                 Proyecto del Grupo 1                      |")
print("|               Profesor: Cesar Santivañez                  |")
print("|                 Asesor: Fernando Guzman                   |")
print("|----------------------Integrantes--------------------------|")
print("|                   José Ortiz Velasquez                    |")
print("|                   Alonso Rosales Antunez                  |")
print("|                   Ronny Pastor Kolmakov                   |")
print("|                Agustin Vizcarra Lizarbe (L)               |")
print("-------------------------------------------------------------")
print("|-----------------Ingrese sus crendenciales-----------------|")
privilegios = -1
while(int(privilegios)<0):
    username = input("| Ingrese su nombre de usuario: ")
    password = getpass("| Ingrese su contraseña: ")
    keystone = KeystoneAuth(username, password)
    tokensito = keystone.get_token()
    #Si tiene cuenta de Openstack 
    if tokensito != None:
        tokensito = keystone.updateToken()
        nova = NovaClient(tokensito)
        glance = GlanceClient(tokensito)
        neutron = NeutronClient(tokensito)
        while True:
            result,keystone = MenuListaProyectos(keystone)
            if not (result): #No esta asignado a ningun proyecto
                print("[*] Gracias por usar nuestro sistema!\n")
                privilegios = 0
                break
            else:
                while True:
                    opcion = menuPrincipal(keystone)
                    resultado = menu2(opcion,"Menú",keystone,nova,glance,neutron)
                    if not (resultado):
                        break

                                 
    #Si tiene cuenta de Linux
    else:
        #AutenticacionLinux = AuthenticationManager()    
        #response = AutenticacionLinux.get_auth(username, password)
        #permisos = response["permisos"]
        #id = response["id"]
        id = 1
        permisos = 1
        if id == 0:
            print("[*]Ha ingresado credenciales inválidas o su usuario no existe.")
        else:
            while True:
                print("[*]Bienvenido al Menú Principal")
                print("[*]Orquestador: Linux")
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
