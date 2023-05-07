"""""
from schemas import *
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import requests
#Para uso futuro
"""
from getpass import getpass
from keystone import KeystoneAuth
import threading # Para uso futuro
import requests
#Posteriormente se podría leer desde un archivo
credenciales = {'admin':'admin'}
jerarquias = {'admin':3}
nivelMaximoAprovisionamiento = 0
#Posteriormente se podrá leer desde una base de datos
#Se trabajará con un esquema de programacion modular

############################################    F   U   N   C   I   O   N   E   S   ############################################
# Display principal
def menuPrincipal(username):
    print("\n")
    print("   |---------Bienvenido "+username+" al menú principal----------|")
    print("|- Opción 1 -> Información del consumo de recursos           |")
    print("|- Opción 2 -> Información de los recursos creados           |")
    print("|- Opción 3 -> Información de topologías                     |")
    print("|- Opción 4 -> Crear nuevo usuario                           |")
    print("|- Opción 5 -> Editar usuario existente                      |")
    print("|- Opción 6 -> Listar usuarios existentes                    |")
    print("|- Opción 7 -> Crear nuevo rol                               |")
    print("|- Opción 8 -> Listar roles existentes                       |")
    print("|- Opción 9 -> Eliminar usuario existente                    |")
    print("|- Opción 10 -> Eliminar rol existente                       |")
    print("|- Opcion 11 -> Salir                                        |")
    opcion = input("| Ingrese una opción: ")
    print("\n")
    return opcion

# Display info de servidores
def menuInfoServidores():
    print("|----------------------------------------------------------------|")
    print("|- Opción 1 -> Información de los servidores                     |")
    print("|- Opción 2 -> Editar el nivel máximo de sobre aprovisionamiento |")
    print("|- Opción 3 -> Mostrar el nivel máximo de sobre aprovisionamiento|")
    print("|- Otras opciones proximamente ...                               |")
    print("|- Opcion 9 -> Salir                                             |")
    opcion = input("| Ingrese una opción: ")
    print("\n")
    return opcion

# Display info topology
def menuInfoTopologias():
    print("|----------------------------------------------------------------|")
    print("|- Opción 1 -> Lista de topologías existentes                    |")
    print("|- Opción 2 -> Lista detalle de una topología                    |")
    print("|- Opción 3 -> Crear una nueva topología                         |")
    print("|- Opción 4 -> Editar una topología existente                    |")
    print("|- Opción 5 -> Visualización de una topología                    |")
    print("|- Opción 6 -> Borrar una topología existente                    |")
    print("|- Opcion 9 -> Salir                                             |")
    opcion = input("| Ingrese una opción: ")
    print("\n")
    return opcion

# Display create topology
def menuCrearTopologia():
    print("|---------------------------------|")
    nombreTopologia = input("| Ingrese el nombre de su topología: ")
    print("|---Ingrese el tipo de topología--|")
    print("|- Opción 1 -> Lineal             |")
    print("|- Opción 2 -> Malla              |")
    print("|- Opción 3 -> Árbol              |")
    print("|- Opcion 4 -> Anillo             |")
    print("|- Opcion 5 -> Bus                |")
    print("|---------------------------------|")
    tipoTopologia = input("| Ingrese una opción: ")
    #Validaciones
    print("[*]Topología creada exitosamente\n")
    #Se crea aca la topologia y se guarda en db 

# Funciones
def obtenerInfoRemoto():
    monitoringAPI = "http://10.20.12.39:9090/recursos"
    response = requests.get(monitoringAPI,headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        print("El servicio de monitoreo se encuentra caído")
        return "Error"
        
def mostrarNivelAprovionamiento():
    global nivelMaximoAprovisionamiento
    if(nivelMaximoAprovisionamiento==0):
        print("Aún no se ha definido el nivel de aprovionamiento en el sistema!")
    else:
        print("El nivel de aprovisionamiento máximo en el sistema es "+str(nivelMaximoAprovisionamiento)+"% ")
        
def editarNivelAprovisionamiento():
    global nivelMaximoAprovisionamiento
    if(nivelMaximoAprovisionamiento==0):
        try:
            nuevoNivel = int(input("Ingrese el nivel de aprovisionamiento máximo en (%): "))
            if(nuevoNivel>0 and nuevoNivel<100):
                nivelMaximoAprovisionamiento = nuevoNivel
                print("Se añadio el nivel de aprovisionamiento exitosamente")
            else:
                print("Debe ser un valor que se encuentre entre ]0;100[ (%)")
        except Exception as e:
            print("Debe ingresar un valor entero!")
    else:
        try:
            nivelAprovisionamiento = int(input("Edite el valor del nivel de aprovisionamiento(%): "))
            if(nivelAprovisionamiento>0 and nivelAprovisionamiento<100):
                nivelMaximoAprovisionamiento = nivelAprovisionamiento
                print("Se editó el nivel de aprovisionamiento exitosamente")
            else:
                print("Debe ser un valor que se encuentre entre ]0;100[ (%)")
        except Exception as e:
            print("Debe ingresar un valor entero!")
            
def obtenerInfoServidores():
    #Con toda la informacion recolectada toca mostrar los resultados
    output = obtenerInfoRemoto()
    if ( output == "Error"):
        print("Hubo error obteniendo la información del cluster")
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
    while True:
        nombreRol = input("| Ingrese el nombre del rol: ")
        if(nombreRol != ''):
            descripcionRol = input("| Ingrese una descripción del rol: ")
            keystone.crear_Rol(nombreRol, descripcionRol)
            break
        
        else:
            print("[*]Ingrese un nombre de rol válido")
            continue


#Eliminar Rol
def eliminarRol():
    while True:
        nombreRol = input("| Ingrese el nombre del rol a eliminar: ")
        if(nombreRol != ''):
            keystone.delete_rol(nombreRol)
            break
        
        else:
            print("[*]Ingrese un nombre de rol válido")
            continue
        
#Eliminar Usuario
def eliminarUsuario():
    while True:
        nombreUsuario = input("| Ingrese el nombre de usuario a eliminar: ")
        if(nombreUsuario != ''):
            keystone.delete_user(nombreUsuario)   
            return nombreUsuario
        
        else:
            print("[*]Ingrese un nombre de usuario válido")
            continue

#Crear Usuario
def crearUsuario():
    while True:
        username = input("| Ingrese un nombre de usuario: ")
        if(username != ''):
            while True:
                password = getpass("| Ingrese su contraseña: ")
                if(password != ''):
                    email = input("| Ingrese una dirección de correo: ") #Es obligatorio ingresar un correo?
                    while True:
                        rol_name = input("| Ingrese un rol al usuario: ")
                        if(rol_name != ''):
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
    while True:
        username = input("| Ingrese un nombre de usuario: ")
        if(username != ''):
            verificarPass = input("| ¿Desea cambiar su contraseña?[Y/N]: ")
            password = None
            if verificarPass == "Y" or verificarPass == "y":
                while True:
                    password = getpass("| Ingrese la nueva contraseña: ")
                    if(password == ''):
                        print("[*]Ingrese una contraseña válida")
                        continue
                    else:
                        break
                    
            verificarEmail = input("| ¿Desea cambiar su email?[Y/N]: ")
            email = None
            if verificarEmail == "Y" or verificarEmail == "y":
                email = input("| Ingrese la nueva dirección de correo: ") #Es obligatorio ingresar un correo?
            
            verificarRol = input("| ¿Desea cambiar su rol?[Y/N]: ")
            rol = None
            if verificarRol == "Y" or verificarRol == "y":
                while True:
                    rol = input("| Ingrese el nuevo rol: ")
                    if (rol == ''):
                        print("[*]Ingrese un rol válido")
                        continue
                    else:
                        break
                    
            if (verificarPass == "N") and (verificarEmail=="N") and (verificarRol=="N"):
                print("[*]No te creas hábil ctm")
                break 
                
            keystone.editar_usuario(username,rol,password,email)
            
            break
            
        else:
            print("[*]Ingrese un nombre de usuario válido")
            continue

# Menú logico
def menu(opcion,nivel,jerarquia):
    try:
        opcion = int(opcion)
        if opcion == 1:
            # Mapea desde qué menú se está ingresando p.e Menú principal -> Nivel 0 / Así se permite reusar el menú
            # Mapea desde qué menú se está ingresando p.e MenuInfoServidores -> Nivel 1 / Así se permite reusar el menú
            # Mapea desde qué menú se está ingresando p.e MenuInfoTopologia -> Nivel 2 / Así se permite reusar el menú
            if(nivel == 0):
                # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 3 or jerarquia == 1):
                    while True:
                        opcion = menuInfoServidores()
                        resultado = menu(opcion,1,jerarquia)
                        if not (resultado):
                            break
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
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
                        resultado = menu(opcion,2,jerarquia)
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
                    resultado = menu(3,0,jerarquia)
 
                else:
                    #Quiere decir que no tengo los privilegios para poder ingresar
                    print("Lo sentimos usted no tiene los privilegios para poder ingresar")
            
            if(nivel == 3):
                pass #ELIMINAR
                  
            return True
        
        elif opcion == 4:
            if(nivel == 0):
                # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 3 or jerarquia == 1):
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
                if(jerarquia == 3 or jerarquia == 1):
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
                resultado = menu(3,0,jerarquia)
            
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
                
                resultado = menu(3,0,jerarquia) 
            
            return True
        
        elif opcion == 7:
            if(nivel == 0):
                 # Instanciamos las políticas de jerarquía p.e Admin tiene permiso de visualizar la información de servidores la validacion siempre se dará a nivel de menú
                if(jerarquia == 3 or jerarquia == 1):
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
                if(jerarquia == 3 or jerarquia == 1):
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
                if(jerarquia == 3 or jerarquia == 1):
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
    #print("Tu tokensito es: "+str(tokensito))
    
    if tokensito == None:
        privilegios = 0
        
    else:
        rol = keystone.getUserRol(username)
        if rol == "admin":
            privilegios = 1
        else:
            privilegios = 2
        #privilegios = validarCredenciales(username,password)
    
if(int(privilegios)>0):
    while True:
        opcion = menuPrincipal(username)
        resultado = menu(opcion,0,privilegios)
        if not (resultado):
            print("------------------------------------------------------------")
            print("[*]Gracias por usar nuestro sistema!")
            break