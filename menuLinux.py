import random
from AutheticationDriver import AuthenticationManager
from NetworkingDriver import NetworkingManager
from PlacementDriver import PlacementManager
from ProvisionInstancesDriver import ProvisionInstancesManager
from tabulate import tabulate
class Usuario:
    def __init__(self,id):
        self.id = id
    def menuUsuario(self,id):
        print("Esto es el menú de Usuario...")
        opcionesUsuario = ["Topologias","VM's","Salir"]
        while True:
            print("|----------------Menú principal------------------|")
            listarProyectosxUsuario(id)
            i = 0
            for opt in opcionesUsuario:
                longitud_print = 50
                chain = "|- Opción "+str(i+1)+" -> "+opt
                falta = longitud_print - len(chain) - 1
                chain = chain + (falta* " ")+ "|"
                print(chain)
                i += 1
            print("|------------------------------------------------|")     
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opcionesUsuario)):
                break
            else:
                if int(opcion) <= len(opcionesUsuario):
                    match int(opcion):
                        case 1:
                            opcionesTopologia = ["Listar VM's por Topologia","Modificar Topologia","Listar Usuarios x Topologia","Salir"]
                            while True:
                                print("|----------------Menú Topologias------------------|")
                                i = 0
                                for opt in opcionesTopologia:
                                    longitud_print = 50
                                    chain = "|- Opción "+str(i+1)+" -> "+opt
                                    falta = longitud_print - len(chain) - 1
                                    chain = chain + (falta* " ")+ "|"
                                    print(chain)
                                    i += 1
                                print("|------------------------------------------------|")     
                                opcion = input("| Ingrese una opción: ")
                                if opcion.isdigit():
                                    match int(opcion):
                                        case 1:
                                            listarTopologiasXProyecto(id)
                                        case 2:
                                            modificarTopologiaXUsuario(id)
                                        case 3:
                                            listarUserXRolXTopologia(id)
                                        case 4:
                                            print("[*] Regresando al menú principal")
                                            break
                                        case _:
                                            print("[*] Ingrese una opción valida")
                                else:
                                    print("[*] Se ingresaron un ID de proyecto o una opcion inválida")
                        case 2:
                            opcionesVMs = ["Listar Imagenes","Agregar una imagen","Eliminar una imagen","Listar flavors","Agregar un flavor","Editar un Flavor","Eliminar un flavor","Salir"]
                            while True:
                                 print("|----------------Menú VM's------------------|")
                                 for opt in opcionesVMs:
                                        longitud_print = 50
                                        chain = "|- Opción "+str(i+1)+" -> "+opt
                                        falta = longitud_print - len(chain) - 1
                                        chain = chain + (falta* " ")+ "|"
                                        print(chain)
                                        i += 1
                                 print("|------------------------------------------------|")
                                 opcion = input("| Ingrese una opción: ")
                                 if opcion.isdigit():
                                     match int(opcion):
                                         case 1:
                                             listarImagenesXVMXTopologiaXUsuario(id)
                                         case 2:
                                             agregarImagenXTopologiaXProyecto(id)
                                         case 3:
                                             eliminarImagenXTopologiaXProyecto(id)
                                         case 4:
                                             listarImagenesXVMXTopologiaXUsuario(id)
                                         case 5:
                                             agregarFlavorXTopologiaXProyecto(id)
                                         case 6:
                                             editarFlavorXTopologiaXProyecto(id)
                                         case 7:
                                             eliminarFlavorXTopologiaXProyecto(id)
                                         case 8:
                                             print("[*] Regresando al menú principal")
                                             break
                                         case _:
                                             print("[*] Ingrese una opción valida")
                                 else:
                                     print("[*] Se ingresaron un ID de proyecto o una opcion inválida")
class Administrador:
    def __init__(self,id):
        self.id = id
    def menuAdministrador(self,id):
        opcionesAdmin = ["Información de usuarios","Información de slices","Salir"]
        while True:
            print("|----------------Menú principal------------------|")
            i = 0
            for opt in opcionesAdmin:
                longitud_print = 50
                chain = "|- Opción "+str(i+1)+" -> "+opt
                falta = longitud_print - len(chain) - 1
                chain = chain + (falta* " ")+ "|"
                print(chain)
                i += 1
            print("|------------------------------------------------|")
            opcion = input("| Ingrese una opción: ")
            if int(opcion) == (len(opcionesAdmin)):
                    break
            else:
                if int(opcion) <= len(opcionesAdmin):
                    match int(opcion):
                        case 1:
                            #Información de usuarios
                            opcionesUsuarios = ["Listar usuarios","Crear un usuario","Editar un usuario","Eliminar un usuario","Información de Proyectos","Salir"]
                            while True:
                                i = 0
                                print("|----------------Menú de usuarios------------------|")
                                for opt in opcionesUsuarios:
                                    longitud_print = 50
                                    chain = "|- Opción "+str(i+1)+" -> "+opt
                                    falta = longitud_print - len(chain) - 1
                                    chain = chain + (falta* " ")+ "|"
                                    print(chain)
                                    i += 1
                                print("|------------------------------------------------|")
                                opcion = input("| Ingrese una opción: ")
                                if opcion.isdigit():
                                    match int(opcion):
                                        case 1:
                                            ids = listarUsuarios()
                                        case 2:
                                            creandoUsuario()
                                        case 3:
                                            editandoUsuario()
                                        case 4:
                                            eliminarUsuario()
                                        case 5:
                                            print("[*] Ingresando al menú de proyectos")
                                            while True:
                                                print("|----------------Menú de Proyectos------------------|")
                                                opcionesProyectos = ["Listar proyectos","Listar Proyecto por usuario","Salir"]
                                                i = 0
                                                for opt in opcionesProyectos:
                                                    longitud_print = 50
                                                    chain = "|- Opción "+str(i+1)+" -> "+opt
                                                    falta = longitud_print - len(chain) - 1
                                                    chain = chain + (falta* " ")+ "|"
                                                    print(chain)
                                                    i += 1
                                                print("|------------------------------------------------|")
                                                opcion = input("| Ingrese una opción: ")
                                                if opcion.isdigit():
                                                    match int(opcion):
                                                        case 1:
                                                            ids=listarProyectos()
                                                        case 2:
                                                            proyectoXUsuario()
                                                        case 3:
                                                            print("[*] Regresando al menú principal")
                                                            break                    
                                                        case _:
                                                            print("[*] Ingrese una opción valida")
                                                else:
                                                    print("[*] Ingrese una opción valida")       
                                        case 6:
                                            print("[*] Regresando al menú principal")
                                            break
                                        case _:
                                            print("[*] Ingrese una opción valida")
                                else:
                                    print("[*] Ingrese una opción valida")
                        case 2:
                            #Información de Slices
                            opcionesSlices = ["Listar detalles de proyectos","Crear un proyecto","Editar un proyecto","Eliminar un proyecto","Información del Proyecto","Salir"]
                            while True:
                                i = 0
                                print("|----------------Menú de slices------------------|")
                                for opt in opcionesSlices:
                                    longitud_print = 50
                                    chain = "|- Opción "+str(i+1)+" -> "+opt
                                    falta = longitud_print - len(chain) - 1
                                    chain = chain + (falta* " ")+ "|"
                                    print(chain)
                                    i += 1
                                print("|------------------------------------------------|")
                                opcion = input("| Ingrese una opción: ")
                                if opcion.isdigit():
                                    match int(opcion):
                                        case 1:
                                            listarDetallesProyecto()
                                        case 2:
                                            print("Ingresando al metodo")
                                            value=creandoProyecto()
                                        case 3:
                                            print("[*] Ingresando al menú de edición de proyectos ")
                                            while True:
                                                print("|-----------Menú de edición de proyecto----------|")
                                                opcionesEdicionProyectos = ["Editar usuarios","Editar topología","Salir"]
                                                i = 0
                                                for opt in opcionesEdicionProyectos:
                                                    longitud_print = 50
                                                    chain = "|- Opción "+str(i+1)+" -> "+opt
                                                    falta = longitud_print - len(chain) - 1
                                                    chain = chain + (falta* " ")+ "|"
                                                    print(chain)
                                                    i += 1
                                                print("|------------------------------------------------|")
                                                opcion = input("| Ingrese una opción: ")
                                                if opcion.isdigit():
                                                    match int(opcion):
                                                        case 1:
                                                            value=editandoUsuariosXProyecto()
                                                        case 2:
                                                            value=editandoTopologiaXProyecto()
                                                        case 3:
                                                            print("[*] Regresando al menú de slices")
                                                            break                    
                                                        case _:
                                                            print("[*] Ingrese una opción valida")
                                                else:
                                                    print("[*] Ingrese una opción valida")       
                                        case 4:
                                            print("[*] Ingresando al menú de eliminación de usuarios ")
                                            while True:
                                                print("|--------Menú de eliminación de proyecto---------|")
                                                opcionesEdicionProyectos = ["Eliminar usuarios","Eliminar topología","Salir"]
                                                i = 0
                                                for opt in opcionesEdicionProyectos:
                                                    longitud_print = 50
                                                    chain = "|- Opción "+str(i+1)+" -> "+opt
                                                    falta = longitud_print - len(chain) - 1
                                                    chain = chain + (falta* " ")+ "|"
                                                    print(chain)
                                                    i += 1
                                                print("|------------------------------------------------|")
                                                opcion = input("| Ingrese una opción: ")
                                                if opcion.isdigit():
                                                    match int(opcion):
                                                        case 1:
                                                            value = eliminarUsuarioXProyecto()
                                                        case 2:
                                                            value = eliminarTopologia()
                                                        case 3:
                                                            print("[*] Regresando al menú de slices")
                                                            break                    
                                                        case _:
                                                            print("[*] Ingrese una opción valida")
                                                else:
                                                    print("[*] Ingrese una opción valida")       
                                        case 5:
                                            value = getInfoTopo()
                                        case 6:
                                            print("[*] Regresando al menú principal")
                                            break
                                        case _:
                                            print("[*] Ingrese una opción valida")
                                else:
                                    print("[*] Ingrese una opción valida")
                else:
                    print("[*] Ingrese una opción válida.")
#### Funciones de Usuario y Proyecto#####
def listarUsuarios():
    UserManagerLinux = AuthenticationManager()
    response = UserManagerLinux.listar_usuarios()
    ids = []
    if response['mensaje'] == "Lista de usuarios":
        cabeceras = ["Id","Nombre","Correo","Rol"]
        filas = []
        for value in response['usuarios']:
            columnas= []
            for data in value:
                if data != 'pwd' and data != 'permisos':
                    columnas.append(str(value[data]))
                if data == 'permisos':
                    columnas.append("admin" if value[data] == 1 else "user")
                if data == 'id':
                    ids.append(str(value[data]))                 
            filas.append(columnas)
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    else:
        print("[*] Existió un error de conexión!")
    return ids
## variante
def listarUsuariosSinPrint():
    UserManagerLinux = AuthenticationManager()
    response = UserManagerLinux.listar_usuarios()
    ids = []
    if response['mensaje'] == "Lista de usuarios":
        cabeceras = ["Id","Nombre","Correo","Rol"]
        filas = []
        for value in response['usuarios']:
            columnas= []
            for data in value:
                if data != 'pwd' and data != 'permisos':
                    columnas.append(str(value[data]))
                if data == 'permisos':
                    columnas.append("admin" if value[data] == 1 else "user")
                if data == 'id':
                    ids.append(str(value[data]))                 
            filas.append(columnas)
        # print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    else:
        print("[*] Existió un error de conexión!")
    return ids
##
def listarDetallesProyecto():
    #    def listar_links_topo_proyectos(self):
    ProjectManagerLinux = NetworkingManager()
    response = ProjectManagerLinux.listar_links_topo_proyectos()
    if response['mensaje'] == 'Lista de vinculos':
        cabeceras = ["Id","Proyecto","Nombre","Topologia","Tipo","Subnet"]
        filas = []
        for value in response['vinculos']:
            columnas= []
            for data in value:
                columnas.append(str(value[data]))
            filas.append(columnas)
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    else:
        print("[*] Existió un error de conexión!")
def creandoUsuario():
    ##Defina Aquí la lógica para la creacion de usuario
    #def create_user(self, nombre, correo, pwd):
    UserManagerLinux = AuthenticationManager()
    print("--------Bienvenido al formulario de creacion de usuario-----")
    nombre = input("| Ingrese el nombre del usuario: ") 
    correo = input("| Ingrese el correo del usuario: ")
    contra = input("| Ingrese la contraseña del usuario: ")
    confcontra = input("| Confirme la contraseña del usuario: ")
    if contra == confcontra:
        response = UserManagerLinux.create_user(nombre,correo,contra) 
        if response['mensaje']=="se creo al usuario con las credenciales brindadas":
            print("[*] Se creo el usuario "+nombre+"con id: "+str(response['id']))
        else:
            print("[*] Ocurrio un error en la creacion del usuario "+response['mensaje'])
    else:
        print("[*] Las contraseñas registradas no coinciden")
def listar_roles():
    UserManagerLinux = AuthenticationManager()
    response = UserManagerLinux.listar_roles()
    ids = []
    if response['mensaje'] == 'Lista de roles':
        cabeceras = ["Id","Rol"]
        filas = []
        for value in response['roles']:
            columnas= []
            for data in value:
                if data == 'id':
                    ids.append(str(value[data]))                 
                columnas.append(str(value[data]))
            filas.append(columnas)
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    else:
        print("[*] "+response['mensaje'])
    return ids
def editandoUsuario():
    # edit_user(self, user_id, nombre, correo, pwd):
    UserManagerLinux = AuthenticationManager()
    print("--------Bienvenido al formulario de edición de usuario-----")
    ids = listarUsuarios()
    id = input("| Ingrese el ID del usuario a editar: ")
    if id in ids and id != "1":
        nombre = input("| Desea editar el nombre del usuario [S/n]?: ") 
        correo = input("| Desea editar el correo del usuario [S/n]?: ")
        edicionNombre = nombre == "S" or nombre == "s"
        edicionCorreo = correo == "S" or correo == "s"
        response = UserManagerLinux.get_user_by_id(id)
        if response['mensaje'] == "Se encontró al usuario exitosamente":
            if edicionNombre:
                response['usuario']['nombre']=input("| Ingrese el nuevo nombre del usuario: ")
            if edicionCorreo:
                response['usuario']['correo']=input("| Ingrese el nuevo correo del usuario: ")
            if  edicionCorreo or edicionNombre:
                print("[*] Procesando información ...")
                response = UserManagerLinux.edit_user(id,response['usuario']['nombre'],response['usuario']['correo'])
                if response['mensaje'] == "Se editó correctamente al usuario":
                    print("[*] "+response['mensaje'])
                else:
                    print("[*] Ocurrio un error al momento de editar al usuario")                    
            else:
                print("[*] Usted no ingreso información a modificar")
        else:
            print["[*] Hubo un error con el ID del usuario solicitado!"]
    else:
        print("[*] Digitó un ID inválido para edición")
def eliminarUsuario():
    UserManagerLinux = AuthenticationManager()
    print("--------Bienvenido al formulario de edición de usuario-----")
    ids = listarUsuarios()
    id = input("| Ingrese el ID del usuario a editar: ")
    if id in ids:
        confirmacion = input("| Esta seguro de eliminar al usuario con ID="+id+" [S/n]?: ") 
        if confirmacion == "S" or confirmacion == "s":
            response=UserManagerLinux.delete_user(id)
            if response['mensaje'] != "No se pudo eliminar al usuario":
                print("[*] "+response['mensaje'])
            else: 
                print("[*] "+response['mensaje'])
        else:
            print("[*] Regresando al menú principal")
    else:
        print("[*] Digitó un ID inválido para edición")
    ##Defina Aquí la lógica para la eliminación de usuario
def listarProyectos():
    # def listar_proyectos(self):
    ProjectManagerLinux = NetworkingManager()
    response = ProjectManagerLinux.listar_proyectos()
    filas = []
    cabeceras = ["ID", "Nombre"]
    ids = []
    if response['mensaje'] == 'Lista de proyectos':
        for value in response["proyectos"]:
            columnas = []
            for data in value:
                columnas.append(str(value[data]))
                if data == 'id':
                    ids.append(str(value[data]))
            filas.append(columnas)   
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    else:
        print("[*] "+response['mensaje'])
    return ids
    ##Defina Aquí la lógica para el listado de proyecto
def proyectoXUsuario():
    UserManagerLinux = AuthenticationManager()
    ids = listarUsuarios()
    id = input("| Ingrese el ID del usuario a consultar: ")
    if id in ids:
        filas = []
        cabeceras=["ID", "Nombre", "Rol"]
        response = UserManagerLinux.get_role_project_por_user(id)
        if response['mensaje'] == 'Lista de vinculos':
            for value in response["vinculos"]:
                columnas = []
                for data in value:
                    columnas.append(str(value[data]))
                filas.append(columnas)  
            print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
        else:
            print("[*] "+response['mensaje'])
    else:
        print("[*] Digitó un ID inválido para la consulta")
def creandoProyecto():
    UserManagerLinux = AuthenticationManager()
    ProjectManagerLinux = NetworkingManager()
    print("--------Bienvenido al formulario de edición de usuario-----")
    nombreProyecto = input("| Ingrese el nombre del proyecto a crear: ")
    if nombreProyecto != "":
        print("--------Ahora ingrese información acerca de la topologia-------")
        tipos = ["bus","estrella","mesh","anillo"]
        cabeceras = ["ID","Tipo"]
        filas = []
        i = 1
        mapTipo = {}
        for value in tipos:
            columnas = [i,value]
            filas.append(columnas)
            mapTipo[str(i)] = value
            i=i+1
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
        tipoTopologia = input("| Ingrese el ID del tipo de topologia: ")
        if tipoTopologia in mapTipo.keys():
            tipo = mapTipo[tipoTopologia]
            subnetname = input("| Ingrese el nombre de la subred: ")
            if subnetname != "":
                network = input("| Ingrese el formato de la subred en formato CIDR (x.x.x.x/y): ")
                if network != "":
                    gateway = input("| Ingrese la direccion IP del gateway: ")
                    if gateway != "":
                        iprange=input("| Ingrese un rango de direcciones IP's [a.a.a.a-b.b.b.b]: ")
                        if iprange != "":
                            workers = ["Worker1","Worker2","Worker3"]
                            ## Ojo para el que implemente el placement de los Workers
                            worker = random.choice(workers)
                            print("----Ahora ingrese información acerca de los usuarios de esta topología-----")
                            numero_usuarios = input("Ingrese el numero de usuarios de esta topología: ")
                            if numero_usuarios.isdigit():
                                n = int(numero_usuarios)
                                usuarios_roles = {}
                                ids = listarUsuarios()
                                ids_roles = listar_roles()
                                for i in range(n):
                                   id_user = input("Ingrese el ID de usuario a añadir al proyecto: ")
                                   if id_user in ids:
                                       id_rol = input("Ingrese el ID del rol a añadir al proyecto: ")
                                       if id_rol in ids_roles and id_user in ids:
                                           ## Quiere decir que todo esta bien
                                           usuarios_roles[id_user] = id_rol
                                       else:
                                           print("[*] El ID del rol es incorrecto el usuario junto con el rol no serán añadidos")
                                   else:
                                       print("[*] El ID ingresado es incorrecto")
                                if usuarios_roles:
                                    ## Quiere decir que todo esta bien (en teoria)
                                    # Creacion del proyecto
                                    print("[*] Creando al proyecto...")
                                    # def add_proyecto(self, nombre):
                                    response = ProjectManagerLinux.add_proyecto(nombreProyecto)
                                    if response["mensaje"] == "se añadio el proyecto con los parámetros especificados":
                                        print("[*]"+response["mensaje"])
                                        idProyecto = response["id"]
                                        print("[*] Creando al topologia...")
                                        #def create_topology(self, tipo, subnetname, network, gateway, iprange, worker):
                                        response = ProjectManagerLinux.create_topology(tipo,subnetname,network,gateway,iprange,worker)
                                        if response["mensaje"] == "se creo la topologia usuario con los parametros brindados":
                                            idTopologia = response["id"]
                                            print("[*]"+response["mensaje"])
                                            print("[*] Añadiendo topologia al proyecto...")
                                            # def create_link_topo_proyecto(self, proyecto, topologia):
                                            response = ProjectManagerLinux.create_link_topo_proyecto(idProyecto,idTopologia)
                                            if response["mensaje"] == "se vinculo la topologia con el proyecto de manera exitosa":
                                                print("[*]"+response["mensaje"])
                                                print("[*] Añadiendo usuario al proyecto...")
                                                for value in usuarios_roles:
                                                    #def add_user_project_role(self, usuario, proyecto, rol):
                                                    response = UserManagerLinux.add_user_project_role(value, idProyecto, usuarios_roles[value])
                                                    if response["mensaje"] == "se vinculo al usuario con el proyecto y su rol":
                                                        print("[*]" + response["mensaje"])
                                                    else:
                                                        print("[*] "+response["mensaje"])
                                                        return 1
                                                print("[*] Se añadio satisfactoriamente los usuarios al proyecto")
                                            else:
                                                print("[*] "+response["mensaje"])
                                                return 1    
                                        else:
                                            print("[*] "+response["mensaje"])
                                            return 1    
                                    else:
                                        print("[*] "+response["mensaje"])
                                        return 1
                                else:
                                    print("[*] Ingreso de manera incorrecta a los usuarios y sus roles")
                                    return 1
                            else:
                                print("[*] El número de usuarios debe ser un numero") 
                                return 1   
                        else:
                            print("[*] Ingreso una direccion una IP invalida ")
                            return 1    
                    else:
                        print("[*] Ingreso una direccion una IP invalida ")
                        return 1    
                else:
                    print("[*] Ingreso una direccion de red invalida")
                    return 1    
            else:
                print("[*] Ingreso un nombre invalido de la subred")
                return 1
        else:
            print("[*] Ingreso un tipo inválido de topologia")
            return 1
    else:
        print("[*] Debe ingresar el nombre del proyecto de manera correcta")
    return 0
    ##Defina Aquí la lógica para la creacion del proyecto
def editandoUsuariosXProyecto():
    UserManagerLinux = AuthenticationManager()
    ids = listarProyectos()
    idProyecto = input("| Ingrese el ID del proyecto a editar: ")
    if idProyecto in ids:
        ids = listarUsuarios()
        idUsuario = input("| Ingrese el ID del usuario a editar: ")
        if idUsuario in ids:
            ids = listar_roles()
            idRol = input("| Ingrese el ID del rol a editar: ")
            if idRol in ids:
                ## Validaciones ##
                # def edit_user_project_role(self, user_id, project_id, usuario, proyecto, rol):
                response = UserManagerLinux.edit_user_project_role(idUsuario,idProyecto,idUsuario,idProyecto,idRol)
                if response['mensaje'] == 'Se editó correctamente el vinculo':
                    print("[*] "+response['mensaje'])
                else:
                    print("[*] "+response['mensaje'])
                    return 1
            else:
                print("[*] Debe ingresar un ID de proyecto válido")
                return 1        
        else:
            print("[*] Debe ingresar un ID de proyecto válido")
            return 1    
    else:
        print("[*] Debe ingresar un ID de proyecto válido")
        return 1
    return 0
    ##Defina Aquí la lógica para la edicion del proyecto
def listarTopologias():
    #def listar_topologias(self):
    ProjectManagerLinux = NetworkingManager()
    response = ProjectManagerLinux.listar_topologias()
    filas = []
    cabeceras = ["ID", "Tipo","SubnetName","Network","Gateway","Iprange","Worker"]
    ids = []
    if response['mensaje'] == 'Lista de topologias':
        for value in response["topologias"]:
            columnas = []
            for data in value:
                columnas.append(str(value[data]))
                if data == 'id':
                    ids.append(str(value[data]))
            filas.append(columnas)   
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    else:
        print("[*] "+response['mensaje'])
    return ids
def editandoTopologiaXProyecto():
    ProjectManagerLinux = NetworkingManager()
    ids = listarTopologias()
    idTopologia = input("| Ingrese el ID de la topologia que desea editar: ")
    if idTopologia in ids:
        subnetname = input("| Desea editar el subnetname de la topologia [S/n]?: ")
        network = input("| Desea editar la red de la topologia [S/n]?: ")
        gateway = input("| Desea editar el gateway de la topologia [S/n]?: ")
        iprange = input("| Desea editar el rango de IP's de la topologia [S/n]?: ")
        edicionSubnetname = subnetname == "S" or subnetname == "s" 
        edicionNetwork = network == "S" or network == "s"
        edicionGateway = gateway == "S" or gateway == "s"
        edicionIprange = iprange == "S" or iprange == "s"
        response = ProjectManagerLinux.get_topology(idTopologia)
        if response['mensaje'] == "Se encontró a la topologia exitosamente":
            if edicionSubnetname:
                response['topologia']['subnetname']=input("| Ingrese el nuevo nombre de la subred: ")
            if edicionNetwork:
                response['topologia']['network']=input("| Ingrese el nuevo formato de la subred en formato CIDR (x.x.x.x/y): ")
            if edicionGateway:
                response['topologia']['gateway']=input("| Ingrese la nueva direccion IP del gateway: ")
            if edicionIprange:
                response['topologia']['iprange']=input("| Ingrese un nuevo rango de direcciones IP's [a.a.a.a-b.b.b.b]: ")
            if  edicionSubnetname or edicionNetwork or edicionGateway or edicionIprange:
                print("[*] Procesando información ...")
                # def edit_topology(self, topology_id, tipo, subnetname, network, gateway, iprange, worker):
                response = ProjectManagerLinux.edit_topology(idTopologia,response['topologia']['tipo'],response['topologia']['subnetname'],response['topologia']['network'],response['topologia']['gateway'],response['topologia']['iprange'],response['topologia']['worker'])
                if response['mensaje'] == "Se editó correctamente la topologia":
                    print("[*] "+response['mensaje'])
                else:
                    print("[*] "+response['mensaje'])        
                    return 1            
            else:
                print("[*] Usted no ingreso información a modificar")
                return 1
    else:
        print("[*] Debe ingresar un ID de topologia válido")
        return 1
    return 0
def eliminarUsuarioXProyecto():
    UserManagerLinux = AuthenticationManager()
    ids = listarProyectos()
    idProyecto = input("| Ingrese el ID del proyecto a consultar: ")
    if idProyecto in ids:
        ids = listarUsuarios()
        idUsuario = input("| Ingrese el ID del usuario a eliminar: ")
        if idUsuario in ids:    
            ## Validaciones ##
            # def edit_user_project_role(self, user_id, project_id, usuario, proyecto, rol):
            response = UserManagerLinux.delete_rol_project_user(idProyecto,idUsuario)
            if response['mensaje'] != 'No se encontró el vinculo con el ID proporcionado':
                print("[*] "+response['mensaje'])
            else:
                print("[*] "+response['mensaje'])
                return 1
        else:
                print("[*] Debe ingresar un ID de proyecto válido")
                return 1        
    else:
        print("[*] Debe ingresar un ID de proyecto válido")
        return 1
    return 0
def eliminarTopologia():
    ProjectManagerLinux = NetworkingManager()
    ids = listarProyectos()
    idProyecto = input("| Ingrese el ID del proyecto a consultar: ")
    if idProyecto in ids:
        ids = listarTopologias()
        idTopologia = input("| Ingrese el ID de la topologia que desea eliminar: ")
        if idTopologia in ids:
            # def delete_link_topo_proyecto(self, topology_id, project_id):
            # def delete_topology(self, topology_id):
            print("[*] Eliminando el vinculo entre el proyecto y la topologia...")
            response = ProjectManagerLinux.delete_link_topo_proyecto(idTopologia, idProyecto)
            if response['mensaje'] != 'No se encontró el vinculo con el ID proporcionado':
                print("[*] "+response['mensaje'])
                print("[*] Eliminando la topologia...")
                response = ProjectManagerLinux.delete_topology(idTopologia)
                if response['mensaje'] != 'No se encontró la topologia con el ID proporcionado':
                    print("[*] "+response['mensaje'])
                else:
                    print("[*] "+response['mensaje'])
                    return 1    
            else:
                print("[*] "+response['mensaje'])
                return 1
        else:
            print("[*] Debe ingresar un ID de topologia válido")
            return 1
    else:
        print("[*] Debe ingresar un ID de proyecto válido")
        return 1
    return 0
def getInfoTopo():
    ProjectManagerLinux = NetworkingManager()
    ids = listarProyectos()
    idProyecto = input("| Ingrese el ID del proyecto a consultar: ")
    if idProyecto in ids:
        response = ProjectManagerLinux.get_link_topo_proyecto(idProyecto)
        if response['mensaje'] == 'Vinculo encontrado exitosamente':
            cabeceras = ["ID Vinculo","ID Proyecto","Nombre Proyecto","ID Topologia","Tipo","Subnet"]
            filas = []
            columnas = []
            for value in response["vinculo"]:
                columnas.append(str(response['vinculo'][value]))
            filas.append(columnas)   
            print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
        else:
            print("[*] "+response['mensaje'])
            return 1
    else:
        print("[*] Debe ingresar un ID de proyecto válido")
        return 1
    return 0
#################################### 
def listarProyectosxUsuario(id):
    ProjectManagerLinux = NetworkingManager()
    response = ProjectManagerLinux.get_user_topo_rol(id)
    filas = []
    cabeceras = ["Proyecto", "Rol","Tipo de Topología","Worker"]
    if response['mensaje'] == 'Lista de vinculos':
        for value in response["vinculos"]:
            columnas = []
            for data in value:
                columnas.append(str(value[data]))
            filas.append(columnas)   
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    else:
        print("[*] "+response['mensaje'])
    ##Defina Aquí la lógica para el listado del proyecto
## Variante sin input
def proyectoXUsuarioSinInput(id):
    UserManagerLinux = AuthenticationManager()
    ids = listarUsuariosSinPrint()
    idProyectos = []
    if str(id) in ids:
        filas = []
        cabeceras=["ID", "Nombre", "Rol"]
        response = UserManagerLinux.get_role_project_por_user(id)
        if response['mensaje'] == 'Lista de vinculos':
            for value in response["vinculos"]:
                columnas = []
                for data in value:
                    columnas.append(str(value[data]))
                    if data == 'id_proyecto':
                        idProyectos.append(str(value['id_proyecto']))
                filas.append(columnas)  
            print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
        else:
            print("[*] "+response['mensaje'])
    else:
        print("[*] Digitó un ID inválido para la consulta")
    return idProyectos
def listarTopologiasXProyecto(id):
    ## Muestro los proyectos en los que se encuentra el usuario
    ProjectManagerLinux = NetworkingManager()
    VmManagerLinux = PlacementManager()
    idProyectos = proyectoXUsuarioSinInput(id)
    if len(idProyectos) == 0:
        print("[*] No tiene proyectos asignados, por favor contacte con el administrador")
    else:
        idProyecto=input("| Ingrese el ID de proyecto que desea consultar: ")
        if idProyecto in idProyectos:
            response = ProjectManagerLinux.get_link_topo_proyecto(idProyecto)
            if response['mensaje'] == 'Vinculo encontrado exitosamente':
                print("[*] Listando la VM's relacionadas a la topología ...")
                response = VmManagerLinux.get_vms_por_topologia(response['vinculo']['topologia'])
                if response['mensaje'] == "No se encontró VM's asociadas a esta topologia":
                    print("[*] No se encontró VM's asociadas a esta topología")
                else:
                    filas = []
                    cabeceras=["ID", "PID", "Imagen","Flavor","VNC Port","Nombre VM"]
                    for value in response["vinculos"]:
                        columnas = []
                        for data in value:
                            columnas.append(str(value[data]))
                        filas.append(columnas)  
                    print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))         
            else:
                print("[*] La topología aún no cuenta con una topología asociada")
        else:
            print("[*] Ha ingresado un ID de proyecto incorrecto")
    
def modificarTopologiaXUsuario(id):
    ## CRUD para añadir editar o eliminar VM's a una topología
    ## Primero debo listar las topologias vinculadas al usuario definido por su ID
    ProjectManagerLinux = NetworkingManager()
    UserManagerLinux = AuthenticationManager()
    response = ProjectManagerLinux.get_detalle_user_topo(id)
    if response['mensaje'] == "Lista de vinculos":
        filas = []
        ids_topo = {}
        cabeceras=["ID de Topologia", "Proyecto", "Worker","Rol"]
        for value in response["vinculos"]:
            columnas = []
            for data in value:
                if data == 'id':
                    ids_topo[str(value[data]['topologia'])] = str(value[data]['proyecto'])
                    columnas.append(str(value[data]['topologia']))    
                else:
                    columnas.append(str(value[data]))
            filas.append(columnas)  
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center')) 
        id_topo = input("| Ingrese el ID de la topología que desea modificar: ")
        if id_topo in ids_topo.keys():
            ## Quiere decir que puede modificar
            ## Verificamos si es que tiene permisos o no
            response = UserManagerLinux.get_rol_topo(ids_topo[id_topo],id,id_topo)
            if response['mensaje'] == 'Rol encontrado' and response['rol'] == 'admin':
                ## Crear, Editar y Eliminar Topologías
                cabeceras=["Opción", "Descripción"]
                filas = [["1","Crear VM"],["2","Editar VM"],["3","Eliminar VM"],["4","Salir"]]
                print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center')) 
                opciones = [fila[0] for fila in filas]
                opcion = input("| Ingrese la opcion que desea realizar: ")
                if opcion in opciones:
                    match opcion:
                        case "1":
                            crearVMxTopologia(id_topo,ids_topo[id_topo])
                        case "2":
                            editarVMxTopologia(id_topo,ids_topo[id_topo])
                        case "3":
                            eliminarVMxTopologia(id_topo,ids_topo[id_topo])
                        case "4":
                            print("[*] Regresando al menú de topologias")
                        case _:
                            print("[*] Ingresó una opción inválida (no debería pasar)")
                else:
                    print("[*] Ingreso una alternativa incorrecta")
            else:
                print("[*] No cuenta con los permisos necesarios para ejecutar esta acción")
        else:
            print("[*] Ha digitado una opción inválida")
    else:
        print("[*] No tiene topologias asociadas")

def listFlavorsXProyecto(idproyecto):
    FlavorImageManager = ProvisionInstancesManager()
    filas = []
    cabeceras=["ID", "Nombre", "CPU (cores)", "Memoria (MB)", "Disco (GB)"]
    response = FlavorImageManager.listar_flavor_project(idproyecto)
    ids = []
    if response['mensaje'] == 'Lista de flavors':
        for value in response["flavors"]:
            columnas = []
            for data in value:
                columnas.append(str(value[data]))
                if data == 'id':
                    ids.append(str(value['id']))
            filas.append(columnas)  
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    return ids
def listImagenesXProyecto(idproyecto):
    FlavorImageManager = ProvisionInstancesManager()
    filas = []
    cabeceras=["ID", "Imagen"]
    response = FlavorImageManager.listar_imagenes_project(idproyecto)
    ids = []
    if response['mensaje'] == 'Lista de imagenes':
        for value in response["imagenes"]:
            columnas = []
            for data in value:
                columnas.append(str(value[data]))
                if data == 'id':
                    ids.append(str(value['id']))
            filas.append(columnas)  
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
    return ids
def crearVMxTopologia(idtopo,idproyecto):
    FlavorImageManager = ProvisionInstancesManager()
    VmManagerLinux = PlacementManager()
    print("--------Bienvenido al formulario de creacion de VM-----")
    nombre = input("| Ingrese el nombre de la VM: ") 
    ## Listar Imagenes
    ids_imagenes = listImagenesXProyecto(idproyecto)
    id_imagen = input("| Ingrese el ID de la imagen a usar: ")
    ## Listar Flavors
    ids_flavor = listFlavorsXProyecto(idproyecto)
    id_flavor = input("| Ingrese el ID del flavor a usar: ")
    # Si no se tienen o flavors o imagenes no se podrá crear
    if len(ids_flavor) == 0 or len(ids_imagenes) == 0:
        print("[*] No tiene imagenes o flavors que pueda utilizar en este proyecto por lo que no podrá efectuar la creación de una VM")
    else:
        if id_flavor in ids_flavor and id_imagen in ids_imagenes:
            ## Proceso con la creacion
            #  add_vm(self, imagen_id, flavor_id,nombre):
            print("[*] Instanciando la VM ...")
            response = FlavorImageManager.add_vm(id_imagen, id_flavor, nombre)
            if response['mensaje'] == "se añadio la VM con los parámetros especificados":
                print("[*]" + response['mensaje'])
                idVM = response['id']
                print("[*] Creando el enlace entre la VM y la topología ...")
                # add_vm_topology(self, topology_id, vm_id):
                response = VmManagerLinux.add_vm_topology(idtopo,idVM)
                print("[*]"+ response['mensaje'])
            else:
                print("[*] "+response['mensaje'])
        else:
            print("[*] Digito una opción inválida de ID ya sea de Flavor o de Imagen en el proceso de la creacion")
def editarVMxTopologia(idtopo,idproyecto):
    FlavorImageManager = ProvisionInstancesManager()
    VmManagerLinux = PlacementManager()
    print("--------Bienvenido al formulario de creacion de VM-----")
    response = VmManagerLinux.get_vms_por_topologia(idtopo)
    if response['mensaje'] == "No se encontró VM's asociadas a esta topologia":
        print("[*] No se encontró VM's asociadas a esta topología")
    else:
        filas = []
        cabeceras=["ID", "PID", "Imagen","Flavor","VNC Port","Nombre VM"]
        idsVMs = []
        for value in response["vinculos"]:
            columnas = []
            for data in value:
                columnas.append(str(value[data]))
                if data == 'id':
                   idsVMs.append(str(value[data])) 
            filas.append(columnas)  
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))         
        vm_id = input("| Ingrese el ID de la VM que desea editar: ")
        if vm_id in idsVMs:
            nombre = input("| Desea editar el nombre de la VM [S/n]?: ")
            imagen = input("| Desea editar la imagen de la VM [S/n]?: ")
            flavor = input("| Desea editar el flavor de la VM [S/n]?: ")
            edicionNombre = nombre == "S" or nombre == "s" 
            edicionImagen = imagen == "S" or imagen == "s"
            edicionflavor = flavor == "S" or flavor == "s"
            response = FlavorImageManager.get_vm_basic(vm_id)
            if response['mensaje'] == "Se encontró la vm exitosamente":
                if edicionNombre:
                    response['vm']['nombre']=input("| Ingrese el nuevo nombre de la vm: ")
                if edicionImagen:
                    ids_imagenes = listImagenesXProyecto(idproyecto)
                    new_imagen=input("| Ingrese el ID de la nueva imagen: ")
                    if new_imagen in ids_imagenes:
                        response['vm']['imagen'] = new_imagen
                    else:
                        print("[*] Ingresó el ID de forma incorrecta, los cambios no se guardarán")
                if edicionflavor:
                    ids_flavor = listFlavorsXProyecto(idproyecto)
                    new_flavor=input("| Ingrese el ID del nuevo flavor: ")
                    if new_flavor in ids_flavor:
                        response['vm']['flavor'] = new_flavor
                    else:
                        print("[*] Ingresó el ID de forma incorrecta, los cambios no se guardarán")
                if  edicionNombre or edicionImagen or edicionflavor:
                    print("[*] Procesando información ...")
                    # def edit_vm(self, vm_id, imagen_id,flavor_id,nombre):
                    response = FlavorImageManager.edit_vm(vm_id,response['vm']['imagen'],response['vm']['flavor'],response['vm']['nombre'])
                    if response['mensaje'] == "Se editó correctamente la vm":
                        print("[*] "+response['mensaje'])
                    else:
                        print("[*] "+response['mensaje'])        
                        return 1            
                else:
                    print("[*] Usted no ingreso información a modificar")
                    return 1
        else:
            print("[*] Debe ingresar un ID de VM válido")
            return 1
        return 0
def eliminarVMxTopologia(idtopo,idproyecto):
    FlavorImageManager = ProvisionInstancesManager()
    VmManagerLinux = PlacementManager()
    response = VmManagerLinux.get_vms_por_topologia(idtopo)
    if response['mensaje'] == "No se encontró VM's asociadas a esta topologia":
        print("[*] No se encontró VM's asociadas a esta topología")
    else:
        filas = []
        cabeceras=["ID", "PID", "Imagen","Flavor","VNC Port","Nombre VM"]
        idsVMs = []
        for value in response["vinculos"]:
            columnas = []
            for data in value:
                columnas.append(str(value[data]))
                if data == 'id':
                   idsVMs.append(str(value[data])) 
            filas.append(columnas)  
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))         
        vm_id = input("| Ingrese el ID de la VM que desea eliminar: ")
        if vm_id in idsVMs:
            confirmacion = input("| Desea editar el nombre de la VM [S/n]?: ")
            eliminacionconfirmacion = confirmacion == "S" or confirmacion == "s" 
            if  eliminacionconfirmacion:
                # def delete_vm(self, vm_id):
                print("[*] Eliminando Vm ...")
                response = FlavorImageManager.delete_vm(vm_id)
                if response['mensaje'] != "No se pudo eliminar la vm":
                    print("[*] "+response['mensaje'])
                else:
                    print("[*] "+response['mensaje'])        
                    return 1            
        else:
            print("[*] Debe ingresar un ID de VM válido")
            return 1
        return 0
def listarUserXRolXTopologia(id):
    ProjectManagerLinux = NetworkingManager()
    UserManagerLinux = AuthenticationManager()
    filas = []
    response = ProjectManagerLinux.get_detalle_user_topo(id)
    if response['mensaje'] == "Lista de vinculos":
        filas = []
        ids_topo = {}
        cabeceras=["ID de Topologia", "Proyecto", "Worker","Rol"]
        for value in response["vinculos"]:
            columnas = []
            for data in value:
                if data == 'id':
                    ids_topo[str(value[data]['topologia'])] = str(value[data]['proyecto'])
                    columnas.append(str(value[data]['topologia']))    
                else:
                    columnas.append(str(value[data]))
            filas.append(columnas)  
        print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center')) 
        id_topo = input("| Ingrese el ID de la topología que desea consultar: ")
        if id_topo in ids_topo.keys():
            filas = []
            cabeceras=["Proyecto", "Nombre", "Correo","Rol"]
            # get_rol_topoxuser(self,topo_id,project_id):
            response = UserManagerLinux.get_rol_topoxuser(id_topo,ids_topo[id_topo])
            if response['mensaje'] == 'Lista de vinculos':
                for value in response["vinculos"]:
                    columnas = []
                    for data in value:
                        columnas.append(str(value[data]))
                    filas.append(columnas)  
                print(tabulate(filas,headers=cabeceras,tablefmt='fancy_grid',stralign='center'))
        else:
            print("[*] Digito una opcion de ID incorrecta")
    else:
        print("[*] No tiene topologias asociadas")
##Defina Aquí la lógica
def listarImagenesXVMXTopologiaXUsuario(id):
    print("[*] Listando imagenes de la topologia")
def agregarImagenXTopologiaXProyecto(id):
    print("[*] Ingresando al menú para añadir imagen")
def eliminarImagenXTopologiaXProyecto(id):
    print("[*] Ingresando al menú para eliminar imagen")
def listarFlavorsXTopologiaXProyecto(id):
    print("[*] Listando flavors de la topologia")
def agregarFlavorXTopologiaXProyecto(id):
    print("[*] Ingresando al menú para añadir un flavor")
def editarFlavorXTopologiaXProyecto(id):
    print("[*] Ingresando al menú para editar un flavor")
def eliminarFlavorXTopologiaXProyecto(id):
    print("[*] Ingresando al menú para eliminar un flavor")