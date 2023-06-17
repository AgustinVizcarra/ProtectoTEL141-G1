
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
                                            print("[*] Listando usuarios ")
                                            listarUsuarios()
                                        case 2:
                                            print("[*] Ingresando al formulario de creación de usuarios ")
                                            creandoUsuario()
                                        case 3:
                                            print("[*] Ingresando al formulario de edición de usuarios ")
                                            editandoUsuario()
                                        case 4:
                                            print("[*] Ingresando al formulario de eliminación de usuarios ")
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
                                                            print("[*] Listando proyectos")
                                                        case 2:
                                                            print("[*] Ingresando al formulario de proyecto por usuario")
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
                            opcionesSlices = ["Listar proyectos","Crear un proyecto","Editar un proyecto","Eliminar un proyecto","Información del Proyecto","Salir"]
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
                                            print("[*] Listando proyecto ")
                                            listarProyectos()
                                        case 2:
                                            print("[*] Ingresando al formulario de creación de proyectos ")
                                            creandoProyecto()
                                        case 3:
                                            print("[*] Ingresando al menú de edición de proyectos ")
                                            while True:
                                                print("|----------------Menú de edición de proyecto------------------|")
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
                                                print("|----------------Menú de eliminación de proyecto------------------|")
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
    print("[*] Listando usuarios ....")
    ##Defina Aquí la lógica para el listado de usuarios
def creandoUsuario():
    print("[*] Creando usuario...")
    ##Defina Aquí la lógica para la creacion de usuario
def editandoUsuario():
    print("[*] Editando usuario...")
    ##Defina Aquí la lógica para la edicion de usuario
def eliminarUsuario():
    print("[*] Eliminar usuario...")
    ##Defina Aquí la lógica para la eliminación de usuario
def listarProyectos():
    print("[*] Listando proyectos...")
    ##Defina Aquí la lógica para el listado de proyecto
def proyectoXUsuario():
    print("[*] Obteniendo proyecto por usuario...")
    ##Defina Aquí la lógica para el proyecto x usuario
def creandoProyecto():
    print("[*] Creando proyecto...")
    ##Defina Aquí la lógica para la creacion del proyecto
def editandoProyecto():
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