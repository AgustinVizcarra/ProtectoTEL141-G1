import random
from AutheticationDriver import AuthenticationManager
from NetworkingDriver import NetworkingManager
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
                            opcionesTopologia = ["Listar VM's por Topologia","Modificar Topologia","Listar Usuarios asignados a la Topologia","Salir"]
                            while True:
                                print("|----------------Menú Topologias------------------|")
                                for opt in opcionesTopologia:
                                    longitud_print = 50
                                    chain = "|- Opción "+str(i+1)+" -> "+opt
                                    falta = longitud_print - len(chain) - 1
                                    chain = chain + (falta* " ")+ "|"
                                    print(chain)
                                    i += 1
                                print("|------------------------------------------------|")     
                                proyecto = input("| Ingrese el ID del proyecto: ")
                                opcion = input("| Ingrese una opción: ")
                                if opcion.isdigit() and proyecto.isdigit():
                                    match int(opcion):
                                        case 1:
                                            listarTopologiasXProyecto(proyecto)
                                        case 2:
                                            modificarTopologiaXUsuario(proyecto)
                                        case 3:
                                            listarUsuarioXTopologiaXProyecto(proyecto)
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
                                 proyecto = input("| Ingrese el ID del proyecto: ")
                                 opcion = input("| Ingrese una opción: ")
                                 if opcion.isdigit() and proyecto.isdigit():
                                     match int(opcion):
                                         case 1:
                                             listarImagenesXVMXTopologiaXUsuario(id,proyecto)
                                         case 2:
                                             agregarImagenXTopologiaXProyecto(id,proyecto)
                                         case 3:
                                             eliminarImagenXTopologiaXProyecto(id,proyecto)
                                         case 4:
                                             listarImagenesXVMXTopologiaXUsuario(id,proyecto)
                                         case 5:
                                             agregarFlavorXTopologiaXProyecto(id,proyecto)
                                         case 6:
                                             editarFlavorXTopologiaXProyecto(id,proyecto)
                                         case 7:
                                             eliminarFlavorXTopologiaXProyecto(id,proyecto)
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
                                                opcionesProyectos = ["Listar proyectos","Listar proyectos por usuario","Salir"]
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
                                                            print("[*] Ingresando al menú de edición de usuarios x proyecto")
                                                        case 2:
                                                            print("[*] Ingresando al menú de edición de topología x proyecto")
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
                                                            print("[*] Ingresando al menú de eliminación de usuarios x proyecto")
                                                        case 2:
                                                            print("[*] Ingresando al menú de eliminación de topología x proyecto")
                                                        case 3:
                                                            print("[*] Regresando al menú de slices")
                                                            break                    
                                                        case _:
                                                            print("[*] Ingrese una opción valida")
                                                else:
                                                    print("[*] Ingrese una opción valida")       
                                        case 5:
                                            print("[*] Ingresando al formulario de visualización del proyecto")
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
    ##Defina Aquí la lógica para el proyecto x usuario
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
def editandoTopologiaXProyecto():
    print("[*] Editando proyecto...")
    ##Defina Aquí la lógica para la edicion del proyecto
def eliminandoProyecto():
    print("[*] Eliminando proyecto...")
    ##Defina Aquí la lógica para la eliminación del proyecto
#################################### 
def listarProyectosxUsuario(id):
    print("[*] Listando proyestos")
    ##Defina Aquí la lógica para el listado del proyecto
def listarTopologiasXProyecto(id):
    print("[*] Listando la topología en el proyecto")
    ##Defina Aquí la lógica
def modificarTopologiaXUsuario(id):
    print("[*] Ingresando al menú de modificación de topologia")
    ##Defina Aquí la lógica
def listarUsuarioXTopologiaXProyecto(id,proyecto):
    print("[*] Ingresando al menú de listado de usuarios por topologia")
    ##Defina Aquí la lógica
def listarImagenesXVMXTopologiaXUsuario(id,proyecto):
    print("[*] Listando imagenes de la topologia")
def agregarImagenXTopologiaXProyecto(id,proyecto):
    print("[*] Ingresando al menú para añadir imagen")
def eliminarImagenXTopologiaXProyecto(id,proyecto):
    print("[*] Ingresando al menú para eliminar imagen")
def listarFlavorsXTopologiaXProyecto(id,proyecto):
    print("[*] Listando flavors de la topologia")
def agregarFlavorXTopologiaXProyecto(id,proyecto):
    print("[*] Ingresando al menú para añadir un flavor")
def editarFlavorXTopologiaXProyecto(id,proyecto):
    print("[*] Ingresando al menú para editar un flavor")
def eliminarFlavorXTopologiaXProyecto(id,proyecto):
    print("[*] Ingresando al menú para eliminar un flavor")