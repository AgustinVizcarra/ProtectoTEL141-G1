
class Usuario:
    def __init__(self,id):
        self.id = id
    def menuUsuario(self,id):
        print("Esto es el menú de Usuario...")
class Administrador:
    def __init__(self,id):
        self.id = id
    def menuAdministrador(self,id):
        print("Esto es el menú de Administrador...")
        opcionesAdmin = ["Información de usuarios","Información de slices","Salir"]
        while True:
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
                    print("Procesando Información...")
                    print("Informacion correctamente procesada")
                else:
                    print("[*]Ingrese una opción válida.")