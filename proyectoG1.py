from getpass import getpass
from keystone import KeystoneAuth
from AutheticationDriver import AuthenticationManager
import requests

############################################    F   U   N   C   I   O   N   E   S   ############################################
# Display principal
def menuPrincipal(keystone,privilegios):
    opcionesAdmin = ["Información de usuarios","Información de slices"]
    opcionesUsuario = []
    
    #Para Admin
    if (privilegios == 1):
        while True:
            print("\n")
            print("   |---------Bienvenido "+str(keystone.getUsername())+" al menú principal----------|")
            i = 0
            for opt in opcionesAdmin:
                print("|- Opción "+str(opt+1)+" -> "+opt[i]+"           |")
                i = i + 1
                
            print("|- Opción "+str(i+1)+" -> Salir                             |")
            print("|------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")

            if int(opcion) == (len(opcionesAdmin)+1):
                opcion = "Salir"
                break
            else:
                if int(opcion) <= len(opcionesAdmin):
                    opcion = opcionesAdmin[int(opcion)-1]
                    break
                else:
                    print("[*]Ingrese una opción válida.")
               
    #Para usuario     
    else:
        opcion = "Información de slices"
    
    print("")    
    return opcion

# Display info de servidores
def menuInfoServidores(privilegios):
    print("|----------------------------------------------------------------|")
    
    if privilegios == 1:
        print("|- Opción 1 -> Información de los servidores                     |")
        print("|- Opción 2 -> Editar el nivel máximo de sobre aprovisionamiento |")
        print("|- Opción 3 -> Mostrar el nivel máximo de sobre aprovisionamiento|")
        print("|- Otras opciones proximamente ...                               |")
        print("|- Opcion 11 -> Salir                                            |")
        opcion = input("| Ingrese una opción: ")
        
    elif privilegios == 2:
        #print("|- Opción 1 -> Información de los servidores                     |")
        print("|- Opción 2 -> Editar el nivel máximo de sobre aprovisionamiento |")
        #print("|- Opción 3 -> Mostrar el nivel máximo de sobre aprovisionamiento|")
        print("|- Otras opciones proximamente ...                               |")
        print("|- Opcion 11 -> Salir                                            |")
        opcion = input("| Ingrese una opción: ")
        
        if (opcion == 1 or opcion == 3):
            opcion = 4 #Le mapeamos una opcion incorrecta
        
    else:
        print("|- Opción 1 -> Información de los servidores                     |")
        #print("|- Opción 2 -> Editar el nivel máximo de sobre aprovisionamiento |")
        print("|- Opción 3 -> Mostrar el nivel máximo de sobre aprovisionamiento|")
        print("|- Otras opciones proximamente ...                               |")
        print("|- Opcion 11 -> Salir                                            |")
        opcion = input("| Ingrese una opción: ")
    
        if (opcion == 2):
            opcion = 4 #Le mapeamos una opcion incorrecta
    
    
    print("\n")
    return opcion

# Display info topology
#def menuInfoTopologias():
#    print("|----------------------------------------------------------------|")
#    print("|- Opción 1 -> Lista de topologías existentes                    |")
#    print("|- Opción 2 -> Lista detalle de una topología                    |")
#    print("|- Opción 3 -> Crear una nueva topología                         |")
#    print("|- Opción 4 -> Editar una topología existente                    |")
#    print("|- Opción 5 -> Visualización de una topología                    |")
#    print("|- Opción 6 -> Borrar una topología existente                    |")
#    print("|- Opcion 11 -> Salir                                             |")
#    opcion = input("| Ingrese una opción: ")
#    print("\n")
#    return opcion

# Display create topology
#def menuCrearTopologia():
#    print("|---------------------------------|")
#    nombreTopologia = input("| Ingrese el nombre de su topología: ")
#    print("|---Ingrese el tipo de topología--|")
#    print("|- Opción 1 -> Lineal             |")
#    print("|- Opción 2 -> Malla              |")
#    print("|- Opción 3 -> Árbol              |")
#    print("|- Opcion 4 -> Anillo             |")
#    print("|- Opcion 5 -> Bus                |")
#    print("|---------------------------------|")
#    tipoTopologia = input("| Ingrese una opción: ")
    #Validaciones
#    print("[*]Topología creada exitosamente\n")
    #Se crea aca la topologia y se guarda en db 

def obtenerInfoRemoto():
    monitoringAPI = "http://10.20.12.39:9090/recursos"
    response = requests.get(monitoringAPI,headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        print("[*]El servicio de monitoreo se encuentra caído")
        return "Error"
        
def mostrarNivelAprovionamiento():
    global nivelMaximoAprovisionamiento
    if(nivelMaximoAprovisionamiento==0):
        print("[*]Aún no se ha definido el nivel de aprovionamiento en el sistema!")
    else:
        print("[*]El nivel de aprovisionamiento máximo en el sistema es "+str(nivelMaximoAprovisionamiento)+"% ")
    print("\n")
        
def editarNivelAprovisionamiento():
    global nivelMaximoAprovisionamiento
    if(nivelMaximoAprovisionamiento==0):
        try:
            nuevoNivel = int(input("Ingrese el nivel de aprovisionamiento máximo en (%): "))
            if(nuevoNivel>0 and nuevoNivel<100):
                nivelMaximoAprovisionamiento = nuevoNivel
                print("[*]Se añadio el nivel de aprovisionamiento exitosamente")
            else:
                print("[*]Debe ser un valor que se encuentre entre ]0;100[ (%)")
        except Exception as e:
            print("[*]Debe ingresar un valor entero!")
    else:
        try:
            nivelAprovisionamiento = int(input("Edite el valor del nivel de aprovisionamiento(%): "))
            if(nivelAprovisionamiento>0 and nivelAprovisionamiento<100):
                nivelMaximoAprovisionamiento = nivelAprovisionamiento
                print("S[*]e editó el nivel de aprovisionamiento exitosamente")
            else:
                print("[*]Debe ser un valor que se encuentre entre ]0;100[ (%)")
        except Exception as e:
            print("[*]Debe ingresar un valor entero!")
    print("\n")
           
def obtenerInfoServidores():
    #Con toda la informacion recolectada toca mostrar los resultados
    output = obtenerInfoRemoto()
    if ( output == "Error"):
        print("[*]Hubo error obteniendo la información del cluster")
    else:
        workers  = output.keys()
        for worker in workers:
            infoWorker = output[worker]
            print("------------------"+worker+"--------------------")
            print("|-Informacion del CPU: ")
            print("|-Core0 : "+infoWorker["Core0(%)"]+"%")
            print("|-Core1 : "+infoWorker["Core1(%)"]+"%")       
            print("|-Informacion de la RAM: ")
            print("| Memoria usada: "+infoWorker["MemoriaUsada"])
            print("| Memoria disponible: "+infoWorker["MemoriaDisponible"])
            print("| Memoria total: "+infoWorker["MemoriaTotal"])
            print("|-Informacion del almacenamiento: ")
            print("| Almacenamiento usado: "+infoWorker["AlmacenamientoUsado"])
            print("| Almacenamiento usado(%): "+infoWorker["AlmacenamientoUsado(%)"])
            print("| Almacenamiento total:"+ infoWorker["AlmacenamientoTotal"])
            print("|-Informacion de red: ")
            print("| Interfaz ens3 (RX): "+str(infoWorker["ens3(RX)bps"])+"bps")
            print("| Interfaz ens3 (TX): "+str(infoWorker["ens3(TX)bps"])+"bps")
            print("| Interfaz ens4 (RX): "+str(infoWorker["ens4(RX)bps"])+"bps")
            print("| Interfaz ens4 (TX): "+str(infoWorker["ens4(TX)bps"])+"bps")
            print("---------------------------------------------")
    
#Crear Rol
def crearRol():
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombreRol = input("| Ingrese el nombre del rol: ")
        if(nombreRol != ''):
            if(nombreRol == "ESC"):
                print("[*]Ha salido de la opción de -Crear Rol-")
                return
            descripcionRol = input("| Ingrese una descripción del rol: ")
            if(descripcionRol == "ESC"):
                print("[*]Ha salido de la opción de -Crear Rol-")
                return
            keystone.crear_Rol(nombreRol, descripcionRol)
            break
        
        else:
            print("[*]Ingrese un nombre de rol válido")
            continue

#Eliminar Rol
def eliminarRol():
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombreRol = input("| Ingrese el nombre del rol a eliminar: ")
        if(nombreRol != ''):
            if(nombreRol == "ESC"):
                print("[*]Ha salido de la opción de -Eliminar Rol-")
                return
            keystone.delete_rol(nombreRol)
            break
        
        else:
            print("[*]Ingrese un nombre de rol válido")
            continue
        
#Eliminar Usuario
def eliminarUsuario():
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        nombreUsuario = input("| Ingrese el nombre de usuario a eliminar: ")
        if(nombreUsuario != ''):
            if(nombreUsuario == "ESC"):
                print("[*]Ha salido de la opción de -Eliminar Usuario-")
                return
            keystone.delete_user(nombreUsuario)   
            return nombreUsuario
        
        else:
            print("[*]Ingrese un nombre de usuario válido")
            continue

#Crear Usuario
def crearUsuario():
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        username = input("| Ingrese un nombre de usuario: ")
        if(username != ''):
            if(username == "ESC"):
                print("[*]Ha salido de la opción de -Crear Usuario-")
                return
            while True:
                password = getpass("| Ingrese su contraseña: ")
                if(password != ''):
                    if(password == "ESC"):
                        print("[*]Ha salido de la opción de -Crear Usuario-")
                        return
                    email = input("| Ingrese una dirección de correo: ")
                    if(email == "ESC"):
                        print("[*]Ha salido de la opción de -Crear Usuario-")
                        return
                    while True:
                        rol_name = input("| Ingrese un rol al usuario: ")
                        if(rol_name != ''):
                            if(rol_name == "ESC"):
                                print("[*]Ha salido de la opción de -Crear Usuario-")
                                return
                            keystone.crear_usuario(username, password, email, rol_name)
                            return
                        else:
                            print("[*]Ingrese un rol válido")
                        continue
                else:
                    print("[*]Ingrese una contraseña válida")
                    continue
        else:
            print("[*]Ingrese un nombre de usuario válido")
            continue

#Editar Usuario
def editarUsuario():
    print("**Escriba ESC para poder salir de esta opción**")
    while True:
        username = input("| Ingrese un nombre de usuario: ")
        if(username != ''):
            if(username == "ESC"):
                print("[*]Ha salido de la opción de -Editar Usuario-")
                return
            
            verificarPass = input("| ¿Desea cambiar su contraseña?[Y/N]: ")
            password = None
            if verificarPass == "Y" or verificarPass == "y":
                while True:
                    password = getpass("| Ingrese la nueva contraseña: ")
                    if(password == ''):
                        print("[*]Ingrese una contraseña válida")
                        continue
                    else:
                        if(password == "ESC"):
                            print("[*]Ha salido de la opción de -Editar Usuario-")
                            return
                        break
            elif(verificarPass == "ESC"):
                print("[*]Ha salido de la opción de -Editar Usuario-")
                return     
                    
            verificarEmail = input("| ¿Desea cambiar su email?[Y/N]: ")
            email = None
            if verificarEmail == "Y" or verificarEmail == "y":
                email = input("| Ingrese la nueva dirección de correo: ")
                if(email == "ESC"):
                    print("[*]Ha salido de la opción de -Editar Usuario-")
                    return 
                
            elif(verificarEmail == "ESC"):
                print("[*]Ha salido de la opción de -Editar Usuario-")
                return
            
            verificarRol = input("| ¿Desea cambiar su rol?[Y/N]: ")
            rol = None
            if verificarRol == "Y" or verificarRol == "y":
                while True:
                    rol = input("| Ingrese el nuevo rol: ")
                    if (rol == ''):
                        print("[*]Ingrese un rol válido")
                        continue
                    else:
                        if(rol == "ESC"):
                            print("[*]Ha salido de la opción de -Editar Usuario-")
                            return
                        break
            elif(verificarRol == "ESC"):
                print("[*]Ha salido de la opción de -Editar Usuario-")
                return 
                    
            if (verificarPass == "N") and (verificarEmail=="N") and (verificarRol=="N"):
                print("[*]Ha decidido no realizar ningún cambio al usuario")
                break 
                
            keystone.editar_usuario(username,rol,password,email)
            
            break
            
        else:
            print("[*]Ingrese un nombre de usuario válido")
            continue

# Menú logico
def menu(opcion,nivel,jerarquia,keystone):
    try:
        opcion = int(opcion)
        if opcion == 1:
            # Mapea desde qué menú se está ingresando p.e Menú principal -> Nivel 0 / Así se permite reusar el menú
            # Mapea desde qué menú se está ingresando p.e MenuInfoServidores -> Nivel 1 / Así se permite reusar el menú
            # Mapea desde qué menú se está ingresando p.e MenuInfoTopologia -> Nivel 2 / Así se permite reusar el menú
            if(nivel == 0):
                while True:
                        opcion = menuInfoServidores(jerarquia)
                        resultado = menu(opcion,1,jerarquia,keystone)
                        if not (resultado):
                            break
                        
            elif(nivel == 1):
                # No es necesario validar porque la validacion se hace a nivel de menu
                obtenerInfoServidores()
                
            elif(nivel == 2):
                pass #ELIMINAR
            
            elif(nivel == 3):
                pass #ELIMINAR
            
            return True
        
        elif opcion == 2:
            if(nivel == 0):
                pass
            
            if(nivel == 1):
                #Posteriormente este nivel se vinculará con OpenStack
                editarNivelAprovisionamiento()
                
            if(nivel == 2):
                pass #ELIMINAR
            
            if(nivel == 3):
                pass #ELIMINAR
            
            return True
        
        elif opcion == 3:
            if(nivel == 0):
                if(jerarquia == 3 or jerarquia == 1):
                    while True:
                        opcion = menuInfoTopologias()
                        resultado = menu(opcion,2,jerarquia,keystone)
                        if not (resultado):
                            break
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
                    
            if(nivel == 1):
                #Posteriormente este nivel se vinculará con OpenStack
                mostrarNivelAprovionamiento()
    
            if(nivel == 2):
                if(jerarquia == 3 or jerarquia == 1):
                    menuCrearTopologia()
                    resultado = menu(3,0,jerarquia,keystone)
 
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
            
            if(nivel == 3):
                pass #ELIMINAR
                  
            return True
        
        elif opcion == 4:
            if(nivel == 0):
                # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 2 or jerarquia == 1):
                    crearUsuario()
                        
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
            
            if(nivel == 1):
                pass #ELIMINAR
            
            if(nivel == 2):
                pass #ELIMINAR
            
            if(nivel == 3):
                pass #ELIMINAR
            
            return True
        
        elif opcion == 5:
            if(nivel == 0):
                # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 2 or jerarquia == 1):
                    editarUsuario()
                
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
            
            if(nivel == 1):
               pass #ELIMINAR
           
            if(nivel == 2):
                print("|---------------------------------|")
                nombreTopologia = input("| Ingrese el nombre de su topología: ")
                #validaciones
                print("[*]Topología lista para ser visualizada\n")
                resultado = menu(3,0,jerarquia,keystone)
            
            if(nivel == 3):
                pass #ELIMINAR
            
            return True
        
        elif opcion == 6:
            if(nivel == 0):
                # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 3 or jerarquia == 1):
                    keystone.list_users()
                        
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
                    
            if(nivel == 1):
                pass
            if(nivel == 2):
                print("|---------------------------------|")
                nombreTopologia = input("| Ingrese el nombre de su topología: ")
                #validaciones
                confirmacion = input("|¿Está seguro de borrar la topología "+nombreTopologia+" ?[Y/N]: ")
                
                if (confirmacion == "Y"):
                    #se borra la topologia
                    print("[*]Topología borrada exitosamente\n")
                
                resultado = menu(3,0,jerarquia,keystone) 
            
            return True
        
        elif opcion == 7:
            if(nivel == 0):
                 # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 2 or jerarquia == 1):
                    crearRol()
                        
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
                
            return True
        
        elif opcion == 8:
            if(nivel == 0):
                 # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 3 or jerarquia == 1):
                    keystone.listar_roles()
                        
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
                
            return True
        
        elif opcion == 9:
            if(nivel == 0):
                 # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 2 or jerarquia == 1):
                    name = eliminarUsuario()
                    if name == username:
                        print("[*]Se cerrará su sesión. Vuelva a logearse")
                        return False    
                        
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
                
            return True
        
        
        elif opcion == 10:
            if(nivel == 0):
                 # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 2 or jerarquia == 1):
                    eliminarRol()    
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
                
            return True
            
        elif opcion == 11:
            return False
        
        else:
            print("Usted ha ingresado una opción inválida")
            print("Por favor ingresa una opción valida")
            return True
        
    except Exception as e:
        print(e)
        print("Usted ha ingresado una opción inválida")
        print("Por favor ingresa una opción valida")
        return True

def getTokensito(Keystone):
    tokensito = Keystone.get_token()
    return tokensito

def getTokensitoAdmin(keystone):
    keystone.get_token_admin()

def validarCredenciales(username,pwd):
    usuarios = credenciales.keys()
    pwds = credenciales.values()
    attemptcounter = 3
    while True:
        if (username in usuarios) and (pwd in pwds):
            print("[*]Usuario logueado exitosamente!\n")
            return jerarquias[username]
        else:
            if attemptcounter > 0:
                print("[*]Usuario y/o contraseñas incorrectas")
                attemptcounter -= 1
                print("[*]Le quedan "+str(attemptcounter)+" intentos\n")
                return -1
            else:
                #Quiere decir que excedio
                print("[*]Excedió el número de intentos para el proceso de logueo\n")
                return 0
    
def MenuListaProyectos(keystone):
    listaProyectos = keystone.getListProjects()
    #Consideramos que un admin tiene que estar asignado a un unico proyecto llamado admin
    if ((len(listaProyectos) == 1) and (listaProyectos[0][1] == "admin")):
        keystone.setProjectID(listaProyectos[0][0])
        return True,1 
    
    if len(listaProyectos) == 0:   
        print("|--------------------Lista de Proyectos------------------------|")
        print("|Actualmente, usted no se encuentra asignado a ningún proyecto.|")
        print("|Porfavor, póngase en contacto con algún administrador.        |")
        print("|--------------------------------------------------------------|")
        return False,2
    
    else:
        while True:
            print("|--------------------Lista de Proyectos------------------------|")
            i = 0
            for proyecto in listaProyectos:
                print("|- Proyecto "+str(i+1)+" -> "+str(proyecto[1])+"|")
                i = i + 1
            print("|--------------------------------------------------------------|")
            opcionProyecto = input("| Ingrese el # del proyecto al que desea ingresar: ")
            
            if opcionProyecto > len(listaProyectos):
                 print("[*]Ingrese el # de un proyecto válido\n")
            else:
                idProyecto = listaProyectos[int(opcionProyecto)-1][0]
                keystone.setProjectID(idProyecto)
                return True,2     
     
      
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
    tokensito = getTokensito(keystone)
     
    #Si tiene cuenta de Openstack 
    if tokensito != None:
        getTokensitoAdmin(keystone) #Para actualizar el token de admin para hacer las consultas
        
        while True:
            #Menu Lista de todos los proyectos
            result,privilegios = MenuListaProyectos(keystone)
                    
            if not(result): #No esta asignado a ningun proyecto
                print("[*]Gracias por usar nuestro sistema!\n")
                privilegios = 0
                break
 
            else:        
                while True:
                    opcion = menuPrincipal(keystone,privilegios)
                    resultado = menu(opcion,0,privilegios,keystone)
                    if not (resultado):
                        break
                                 
    #Si tiene cuenta de Linux
    else:
        AutenticacionLinux = AuthenticationManager()
        response = AutenticacionLinux.get_auth(username, password)
        