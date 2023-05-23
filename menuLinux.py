
class Usuario:
    def __init__(self,id):
        self.id = id
    def menuUsuario(self,id):
        print("Esto es el menú de Usuario...")
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
                                                opcionesProyectos = ["Listar proyectos","Listar proyectos por usuario","Crear un proyecto","Editar un proyecto","Eliminar un proyecto","Salir"]
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
                                                            listarProyectos()
                                                        case 2:
                                                            print("[*] Ingresando al formulario de proyecto por usuario")
                                                            proyectoXUsuario()
                                                        case 3:
                                                            print("[*] Ingresando al formulario de creación de proyecto")
                                                            creandoProyecto()
                                                        case 4:
                                                            print("[*] Ingresando al formulario de edición de proyecto")
                                                            editandoProyecto()
                                                        case 5:
                                                            print("[*] Ingresando al formulario de eliminación de proyecto")
                                                            eliminandoProyecto()
                                                        case 6:
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
                            pass
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