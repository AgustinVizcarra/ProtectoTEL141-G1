import json
import os
from random import randint
from fastapi import FastAPI, APIRouter, Path
from fastapi.responses import JSONResponse
import psycopg2

app = FastAPI(title = "Orquestador Linux",
              description = "Corriendo orquestador!",
              version = "1.0.1")

@app.on_event('startup')
async def startup():
    print("Iniciando el API del Orquestador Linux")
    print("Esperando solicitudes")

###### CRUD de Usuarios ######
@app.post("/auth/")
async def authentication(body: dict):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'nombre' in body and 'pwd' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario where (nombre = %s AND pwd = %s AND estado=1) OR (correo = %s AND pwd = %s AND estado=1)",(body['nombre'],body['pwd'],body['nombre'],body['pwd'],))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result is None:
                data = {"mensaje": "no se encontró al usuario con las credenciales",
                        "id": 0}
            else:
                data = {"mensaje": "se encontró al usuario con las credenciales dadas",
                        "id": result[0],
                        "permisos": result[5]}
            return JSONResponse(content=data,status_code=200)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)

@app.post("/createUser/")
async def create(body: dict):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'nombre' in body and 'pwd' in body and 'correo' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                #Cuando se crea un usuario se crea con permisos de usuario
                cur.execute("INSERT INTO usuario (nombre,correo,pwd,estado,permisos) VALUES (%s, %s, %s, 1, 0)",(body['nombre'],body['correo'],body['pwd'],))
                cur.execute("SELECT currval('usuario_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo crear al usuario!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se creo al usuario con las credenciales brindadas",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se pudo crear al usuario!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.put("/editUser/{user_id}")
async def edit_user(user_id: int = Path(..., description="ID del usuario a editar"),
                    body: dict = None):
    if body is None:
        data = {"mensaje": "No se envió datos en el body"}
        return JSONResponse(content=data, status_code=400)
    else:
        if 'nombre' in body and 'correo' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE id = %s", (user_id,))
            result = cur.fetchone()
            if result is None:
                cur.close()
                conn.close()
                data = {"mensaje": "No se encontró al usuario con el ID proporcionado"}
                return JSONResponse(content=data, status_code=404)
            else:
                try:
                    cur.execute("UPDATE usuario SET nombre = %s, correo = %s WHERE id = %s",
                                (body['nombre'], body['correo'],user_id, ))
                    conn.commit()
                    cur.execute("SELECT * FROM usuario WHERE id = %s", (user_id,))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    usuario={
                        "id":result[0],
                        "nombre": result[1],
                        "correo": result[2],
                        "pwd": result[3],
                        "permisos": result[5],
                    }
                    data = {"mensaje": "Se editó correctamente al usuario", "user": usuario}
                    return JSONResponse(content=data, status_code=200)
                except psycopg2.Error as e:
                    print(e)
                    cur.close()
                    conn.close()
                    data = {"mensaje": "No se pudo editar al usuario"}
                    return JSONResponse(content=data, status_code=400)
        else:
            data = {"mensaje": "Se enviaron campos incorrectos"}
            return JSONResponse(content=data, status_code=400)
        
@app.get("/listarUsers/")
async def listar_usuarios():
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE estado = 1")
        result = cur.fetchall()
        cur.close()
        conn.close()
        usuarios = []
        for row in result:
            usuario = {
                "id": row[0],
                "nombre": row[1],
                "correo": row[2],
                "pwd": row[3],
                "permisos": row[5]
            }
            usuarios.append(usuario)
        data = {"mensaje": "Lista de usuarios", "usuarios": usuarios}
        return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la lista de usuarios"}
        return JSONResponse(content=data, status_code=400)
    
@app.get("/getUser/{user_id}")
async def get_user(user_id: int = Path(..., description="ID del usuario a buscar")):
    if user_id is None:
        data = {"mensaje": "No se proporcionó el ID del usuario"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE id = %s AND estado = 1", (user_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is None:
            data = {"mensaje": "No se encontró al usuario con el ID proporcionado o ha sido eliminado"}
            return JSONResponse(content=data, status_code=404)
        else:
            usuario = {
                "id": result[0],
                "nombre": result[1],
                "correo": result[2],
                "pwd": result[3],
                "permisos": result[5]
            }
            data = {"mensaje": "Se encontró al usuario exitosamente", "usuario": usuario}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener el usuario"}
        return JSONResponse(content=data, status_code=400)
    
@app.delete("/deleteUser/{user_id}")
async def delete_user(user_id: int = Path(..., description="ID del usuario a eliminar")):
    if user_id is None:
        data = {"mensaje": "No se proporcionó el ID del usuario"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE id = %s", (user_id,))
        result = cur.fetchone()

        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró al usuario con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE usuario SET estado = 0 WHERE id = %s", (user_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "Usuario con id "+str(user_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar al usuario"}
        return JSONResponse(content=data, status_code=400)
    
###### CRUD de VM's ######
@app.get("/listarImagenes/")
async def listar_imagenes():
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("select distinct imagen from vm where estado = 1")
        result = cur.fetchall()
        cur.close()
        conn.close()
        vms = []
        for row in result:
            vm = {
                "imagen": row[0],
            }
            vms.append(vm)
        data = {"mensaje": "Lista de imagenes", "vms": vms}
        return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la lista de imagenes"}
        return JSONResponse(content=data, status_code=400)
    
@app.post("/addVM/")
async def create_VM(body: dict):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'imagen' in body and 'flavor' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                vncport = randint(5000,9999)
                pid = randint(10000,99999)
                cur.execute("INSERT INTO vm (estado,vncport,imagen,flavor,pid) VALUES (1,%s,%s,%s,%s)",(vncport,body['imagen'],body['flavor'],pid))
                cur.execute("SELECT currval('vm_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo añadir la vm!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se añadio la VM con los parámetros especificados",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se añadir la VM!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.put("/editVM/{vm_id}")
async def edit_VM(vm_id: int = Path(..., description="ID de la VM a editar"),
                    body: dict = None):
    if body is None:
        data = {"mensaje": "No se envió datos en el body"}
        return JSONResponse(content=data, status_code=400)
    else:
        if 'imagen' in body and 'flavor' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM vm WHERE id = %s AND estado = 1", (vm_id,))
            result = cur.fetchone()
            if result is None:
                cur.close()
                conn.close()
                data = {"mensaje": "No se encontró la vm con el ID proporcionado"}
                return JSONResponse(content=data, status_code=404)
            else:
                try:
                    cur.execute("UPDATE vm SET imagen = %s, flavor = %s WHERE id = %s AND estado = 1",
                                (body['imagen'],body['flavor'], vm_id))
                    conn.commit()
                    cur.execute("SELECT * FROM vm WHERE id = %s AND estado = 1", (vm_id,))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    vm={
                        "id":result[0],
                        "imagen": result[2],
                        "flavor": result[3],
                    }
                    data = {"mensaje": "Se editó correctamente la vm", "vm": vm}
                    return JSONResponse(content=data, status_code=200)
                except psycopg2.Error as e:
                    print(e)
                    cur.close()
                    conn.close()
                    data = {"mensaje": "No se pudo editar la vm"}
                    return JSONResponse(content=data, status_code=400)
        else:
            data = {"mensaje": "Se enviaron campos incorrectos"}
            return JSONResponse(content=data, status_code=400)
        
@app.get("/listarVms/")
async def listar_vms():
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("select vm.pid,vm.vncport,imagen.imagen,flavor.descripcion,proyecto.nombre from vm inner join imagen on vm.imagen = imagen.id inner join flavor on flavor.id = vm.flavor inner join proyecto on flavor.proyecto = proyecto.id where vm.estado = 1")
        result = cur.fetchall()
        cur.close()
        conn.close()
        vms = []
        for row in result:
            vm = {
                "pid": row[0],
                "vncport": row[1],
                "imagen": row[2],
                "descripcion": row[3],
                "proyecto": row[4]
            }
            vms.append(vm)
        data = {"mensaje": "Lista de vms", "vms": vms}
        return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la lista de vms"}
        return JSONResponse(content=data, status_code=400)

@app.get("/getVM/{vm_id}")
async def get_vm(vm_id: int = Path(..., description="ID de la VM a buscar")):
    if vm_id is None:
        data = {"mensaje": "No se proporcionó el ID de la VM"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("select vm.pid,vm.vncport,imagen.imagen,flavor.descripcion,proyecto.nombre from vm inner join imagen on vm.imagen = imagen.id inner join flavor on flavor.id = vm.flavor inner join proyecto on flavor.proyecto = proyecto.id where vm.estado = 1 and vm.id = %s", (vm_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is None:
            data = {"mensaje": "No se encontró la vm con el ID proporcionado o ha sido eliminada"}
            return JSONResponse(content=data, status_code=404)
        else:
            vm = {
                "pid": result[0],
                "vncport": result[1],
                "imagen": result[2],
                "descripcion": result[3],
                "proyecto": result[4]
            }
            data = {"mensaje": "Se encontró la vm exitosamente", "vm": vm}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la vm"}
        return JSONResponse(content=data, status_code=400)
    
@app.delete("/deleteVm/{vm_id}")
async def delete_user(vm_id: int = Path(..., description="ID del usuario a eliminar")):
    if vm_id is None:
        data = {"mensaje": "No se proporcionó el ID de la VM"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vm WHERE id = %s", (vm_id,))
        result = cur.fetchone()

        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró la VM con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE vm SET estado = 0 WHERE id = %s", (vm_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "vm con id "+str(vm_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar la vm"}
        return JSONResponse(content=data, status_code=400)
    
###### CRUD de proyectos ######
@app.post("/addProyecto/")
async def create_Proyecto(body: dict):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'nombre' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO proyecto (estado,nombre) VALUES (1,%s)",(body['nombre'],))
                cur.execute("SELECT currval('proyecto_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo añadir el proyecto!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se añadio el proyecto con los parámetros especificados",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se puede añadir el proyecto!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.put("/editProyecto/{proyecto_id}")
async def edit_Proyecto(proyecto_id: int = Path(..., description="ID de la VM a editar"),
                    body: dict = None):
    if body is None:
        data = {"mensaje": "No se envió datos en el body"}
        return JSONResponse(content=data, status_code=400)
    else:
        if 'nombre' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM proyecto WHERE id = %s AND estado = 1", (proyecto_id,))
            result = cur.fetchone()
            if result is None:
                cur.close()
                conn.close()
                data = {"mensaje": "No se encontró el proyecto con el ID proporcionado"}
                return JSONResponse(content=data, status_code=404)
            else:
                try:
                    cur.execute("UPDATE proyecto SET nombre = %s WHERE id = %s AND estado = 1",
                                (body['nombre'], proyecto_id))
                    conn.commit()
                    cur.execute("SELECT * FROM proyecto WHERE id = %s AND estado = 1", (proyecto_id,))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    proyecto={
                        "id":result[0],
                        "nombre": result[1],
                    }
                    data = {"mensaje": "Se editó correctamente el proyecto", "proyecto": proyecto}
                    return JSONResponse(content=data, status_code=200)
                except psycopg2.Error as e:
                    print(e)
                    cur.close()
                    conn.close()
                    data = {"mensaje": "No se pudo editar el proyecto"}
                    return JSONResponse(content=data, status_code=400)
        else:
            data = {"mensaje": "Se enviaron campos incorrectos"}
            return JSONResponse(content=data, status_code=400)
        
@app.get("/listarProyecto/")
async def listar_Proyecto():
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM proyecto WHERE estado = 1")
        result = cur.fetchall()
        cur.close()
        conn.close()
        proyectos = []
        for row in result:
            proyecto = {
                "id": row[0],
                "nombre": row[1]
            }
            proyectos.append(proyecto)
        data = {"mensaje": "Lista de proyectos", "proyectos": proyectos}
        return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la lista de proyectos"}
        return JSONResponse(content=data, status_code=400)

@app.get("/getProyecto/{proyecto_id}")
async def get_vm(proyecto_id: int = Path(..., description="ID del usuario a buscar")):
    if proyecto_id is None:
        data = {"mensaje": "No se proporcionó el ID del usuario"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM proyecto WHERE id = %s AND estado = 1", (proyecto_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is None:
            data = {"mensaje": "No se encontró la proyecto con el ID proporcionado o ha sido eliminada"}
            return JSONResponse(content=data, status_code=404)
        else:
            proyecto = {
                "id": result[0],
                "nombre": result[1],
            }
            data = {"mensaje": "Se encontró el proyecto exitosamente", "proyecto": proyecto}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener el proyecto"}
        return JSONResponse(content=data, status_code=400)
    
@app.delete("/deleteProyecto/{proyecto_id}")
async def delete_user(proyecto_id: int = Path(..., description="ID del usuario a eliminar")):
    if proyecto_id is None:
        data = {"mensaje": "No se proporcionó el ID del proyecto"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM proyecto WHERE id = %s and estado = 1", (proyecto_id,))
        result = cur.fetchone()

        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró el proyecto con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE proyecto SET estado = 0 WHERE id = %s", (proyecto_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "proyecto con id "+str(proyecto_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar la proyecto"}
        return JSONResponse(content=data, status_code=400)

###### CRUD de topologias ######

@app.post("/createTopology/")
async def createTopology(body: dict):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'tipo' in body and 'subnetname' in body and 'network' in body and 'gateway' in body and 'iprange' in body and 'worker' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                print(body)
                cur.execute("INSERT INTO topologia (tipo,estado,subnetname,network,gateway,iprange,worker) VALUES (%s, 1, %s, %s, %s, %s, %s)",(body['tipo'],body['subnetname'],body['network'],body['gateway'],body['iprange'],body['worker']))
                cur.execute("SELECT currval('topologia_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo crear la topologia!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se creo la topologia usuario con los parametros brindados",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se pudo crear la topologia usuario!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.put("/editTopology/{topology_id}")
async def edit_user(topology_id: int = Path(..., description="ID de la topologia a editar"),
                    body: dict = None):
    if body is None:
        data = {"mensaje": "No se envió datos en el body"}
        return JSONResponse(content=data, status_code=400)
    else:
        if 'tipo' in body and 'subnetname' in body and 'network' in body and 'gateway' in body and 'iprange' in body and 'worker' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM topologia WHERE id = %s AND estado=1", (topology_id,))
            result = cur.fetchone()
            if result is None:
                cur.close()
                conn.close()
                data = {"mensaje": "No se encontró la topologia con el ID proporcionado"}
                return JSONResponse(content=data, status_code=404)
            else:
                try:
                    cur.execute("UPDATE topologia SET tipo = %s, subnetname = %s, network = %s, gateway = %s, iprange= %s, worker= %s WHERE id = %s",
                                (body['tipo'],body['subnetname'],body['network'],body['gateway'],body['iprange'],body['worker'], topology_id,))
                    conn.commit()
                    cur.execute("SELECT * FROM topologia WHERE id = %s", (topology_id,))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    topologia={
                        "id":result[0],
                        "tipo": result[1],
                        "subnetname": result[3],
                        "network": result[4],
                        "gateway": result[5],
                        "iprange": result[6],
                        "worker" : result[7] 
                    }
                    data = {"mensaje": "Se editó correctamente la topologia", "topology": topologia}
                    return JSONResponse(content=data, status_code=200)
                except psycopg2.Error as e:
                    print(e)
                    cur.close()
                    conn.close()
                    data = {"mensaje": "No se pudo editar la topologia"}
                    return JSONResponse(content=data, status_code=400)
        else:
            data = {"mensaje": "Se enviaron campos incorrectos"}
            return JSONResponse(content=data, status_code=400)
        
@app.get("/listarTopologias/")
async def listar_topologias():
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM topologia WHERE estado = 1")
        result = cur.fetchall()
        cur.close()
        conn.close()
        topologias = []
        for row in result:
            topologia = {
                "id":row[0],
                "tipo": row[1],
                "subnetname": row[3],
                "network": row[4],
                "gateway": row[5],
                "iprange": row[6],
                "worker" : row[7]
            }
            topologias.append(topologia)
        data = {"mensaje": "Lista de topologias", "topologias": topologias}
        return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la lista de topologias"}
        return JSONResponse(content=data, status_code=400)
    
@app.get("/getTopology/{topology_id}")
async def get_user(topology_id: int = Path(..., description="ID del usuario a buscar")):
    if topology_id is None:
        data = {"mensaje": "No se proporcionó el ID de la topologia"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM topologia WHERE id = %s AND estado = 1", (topology_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is None:
            data = {"mensaje": "No se encontró a la topologia con el ID proporcionado o ha sido eliminado"}
            return JSONResponse(content=data, status_code=404)
        else:
            topologia = {
                "id":result[0],
                "tipo": result[1],
                "subnetname": result[3],
                "network": result[4],
                "gateway": result[5],
                "iprange": result[6],
                "worker": result[7]
            }
            data = {"mensaje": "Se encontró a la topologia exitosamente", "topologia": topologia}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener a la topologia"}
        return JSONResponse(content=data, status_code=400)
    
@app.delete("/deleteTopology/{topology_id}")
async def delete_user(topology_id: int = Path(..., description="ID del usuario a eliminar")):
    if topology_id is None:
        data = {"mensaje": "No se proporcionó el ID de la topologia"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM topologia WHERE id = %s AND estado = 1", (topology_id,))
        result = cur.fetchone()

        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró la topologia con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE topologia SET estado = 0 WHERE id = %s", (topology_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "Topologia con id "+str(topology_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar a la Topologia"}
        return JSONResponse(content=data, status_code=400)

###### Vinculo de Topologia y Proyecto ######

@app.post("/createLinkTopoProyecto/")
async def createLinkTopoProyecto(body: dict):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'proyecto' in body and 'topologia' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO proyecto_topologia (estado,proyecto,topologia) VALUES (1, %s, %s)",(body['proyecto'],body['topologia'],))
                cur.execute("SELECT currval('proyecto_topologia_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo vincular la topologia con el proyecto!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se vinculo la topologia con el proyecto de manera exitosa",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se pudo crear el vinculo!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.put("/editLinkTopoProyecto/{topology_id}/{project_id}")
async def editLinkTopoProyecto(topology_id: int = Path(..., description="ID de la topologia a editar"),project_id: int = Path(..., description="ID del proyecto a editar"),body: dict=None):
    if topology_id is None or project_id is None:
        data = {"mensaje": "No se envió datos en el path"}
        return JSONResponse(content=data, status_code=400)
    else:
        if 'proyecto' in body and 'topologia' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM proyecto_topologia WHERE proyecto = %s AND topologia = %s AND estado=1", (project_id,topology_id))
            result = cur.fetchone()
            if result is None:
                cur.close()
                conn.close()
                data = {"mensaje": "No se encontró el vinculo con el ID proporcionado"}
                return JSONResponse(content=data, status_code=404)
            else:
                try:
                    cur.execute("UPDATE proyecto_topologia SET proyecto = %s, topologia = %s WHERE proyecto = %s AND topologia = %s",
                                (body['proyecto'],body['topologia'], project_id ,topology_id,))
                    conn.commit()
                    cur.execute("SELECT * FROM proyecto_topologia WHERE proyecto = %s AND topologia = %s", (body['proyecto'],body['topologia'],))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    vinculo={
                        "id":result[0],
                        "proyecto": result[2],
                        "topologia": result[3],
                    }
                    data = {"mensaje": "Se editó correctamente el vinculo", "vinculo": vinculo}
                    return JSONResponse(content=data, status_code=200)
                except psycopg2.Error as e:
                    print(e)
                    cur.close()
                    conn.close()
                    data = {"mensaje": "No se pudo editar el vinculo"}
                    return JSONResponse(content=data, status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400) 
        
@app.get("/listarlinksTopoProyectos/")
async def listar_topologias():
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT proyecto_topologia.id,proyecto.id,proyecto.nombre,topologia.id,topologia.tipo,topologia.subnetname from proyecto_topologia JOIN proyecto on proyecto_topologia.proyecto = proyecto.id JOIN topologia on proyecto_topologia.topologia = topologia.id where proyecto_topologia.estado = 1 and topologia.estado = 1 and proyecto.estado=1;")
        result = cur.fetchall()
        cur.close()
        conn.close()
        vinculos = []
        for row in result:
            vinculo = {
                "id":row[0],
                "proyecto": row[1],
                "nombre": row[2],
                "topologia": row[3],
                "tipo": row[4],
                "subnet": row[5]
            }
            vinculos.append(vinculo)
        data = {"mensaje": "Lista de vinculos", "vinculos": vinculos}
        return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la lista de vinculos"}
        return JSONResponse(content=data, status_code=400)
    
@app.delete("/deleteLinkTopoProyecto/{topology_id}/{project_id}")
async def delete_user(topology_id: int = Path(..., description="ID de la topologia a editar"),project_id: int = Path(..., description="ID del proyecto a editar")):
    if topology_id is None and project_id is None:
        data = {"mensaje": "No se proporcionó el ID de la topologia o del proyecto"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM proyecto_topologia WHERE topologia = %s AND proyecto = %s AND estado=1", (topology_id,project_id,))
        result = cur.fetchone()
        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró el vinculo con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE proyecto_topologia SET estado = 0 WHERE topologia = %s AND proyecto = %s", (topology_id,project_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "Vinculo con Topologia "+str(topology_id)+" y Proyecto "+str(project_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar a la Topologia"}
        return JSONResponse(content=data, status_code=400)

###### Vinculo de Topologia y VM ######

@app.post("/addVmTopology/")
async def createLinkTopoVM(body: dict):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'vm' in body and 'topologia' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO topologia_vm (estado,topologia,vm) VALUES (1, %s, %s)",(body['topologia'],body['vm'],))
                cur.execute("SELECT currval('topologia_vm_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo vincular la vm con la topologia!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se vinculo la vm con la topologia de manera exitosa",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se pudo crear el vinculo!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.put("/editLinkTopoVM/{topology_id}/{vm_id}")
async def editLinkTopoVM(topology_id: int = Path(..., description="ID de la topologia a editar"),vm_id: int = Path(..., description="ID del proyecto a editar"),body: dict=None):
    if topology_id is None or vm_id is None:
        data = {"mensaje": "No se envió datos en el path"}
        return JSONResponse(content=data, status_code=400)
    else:
        if 'vm' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM topologia_vm WHERE topologia = %s AND vm = %s AND estado=1", (topology_id,vm_id))
            result = cur.fetchone()
            if result is None:
                cur.close()
                conn.close()
                data = {"mensaje": "No se encontró el vinculo con el ID proporcionado"}
                return JSONResponse(content=data, status_code=404)
            else:
                try:
                    cur.execute("UPDATE topologia_vm SET vm = %s WHERE topologia = %s AND vm = %s",
                                (body['vm'], topology_id ,vm_id,))
                    conn.commit()
                    cur.execute("SELECT * FROM topologia_vm WHERE topologia = %s AND vm = %s", (topology_id,body['vm'],))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    vinculo={
                        "id":result[0],
                        "topologia": result[2],
                        "vm": result[3],
                    }
                    data = {"mensaje": "Se editó correctamente el vinculo", "vinculo": vinculo}
                    return JSONResponse(content=data, status_code=200)
                except psycopg2.Error as e:
                    print(e)
                    cur.close()
                    conn.close()
                    data = {"mensaje": "No se pudo editar el vinculo"}
                    return JSONResponse(content=data, status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400) 
        
@app.get("/getVmsporTopologia/{topology_id}")
async def getVmxTopo(topology_id: int = Path(..., description="ID del usuario a buscar")):
    if topology_id is None:
        data = {"mensaje": "No se proporcionó el ID de la topologia"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("select vm.id,vm.imagen,vm.vncport from topologia_vm join topologia on topologia.id=topologia_vm.topologia join vm on vm.id = topologia_vm.vm where topologia.id=%s and topologia.estado=1 and vm.estado=1 and topologia_vm.estado=1;", (topology_id,))
        result = cur.fetchall()
        cur.close()
        conn.close()
        vinculos = []
        if len(result)==0:
                    data = {"mensaje": "No se encontró VM's asociadas a esta topologia", "vinculos": vinculos}
                    return JSONResponse(content=data, status_code=200)
        else:
            for row in result:
                vinculo = {
                    "id":row[0],
                    "imagen": row[1],
                    "vncport": row[2],
                }
                vinculos.append(vinculo)
            data = {"mensaje": "Lista de vinculos", "vinculos": vinculos}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener a la topologia"}
        return JSONResponse(content=data, status_code=400)
    
@app.delete("/deleteLinkVmTopo/{topology_id}/{vm_id}")
async def deleteVMxTopo(topology_id: int = Path(..., description="ID de la topologia a editar"),vm_id: int = Path(..., description="ID del proyecto a editar")):
    if topology_id is None and vm_id is None:
        data = {"mensaje": "No se proporcionó el ID de la topologia o de la vm"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM topologia_vm WHERE topologia = %s AND vm = %s AND estado=1", (topology_id,vm_id,))
        result = cur.fetchone()
        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró el vinculo con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE topologia_vm SET estado = 0 WHERE topologia = %s AND vm = %s", (topology_id,vm_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "Vinculo con Topologia "+str(topology_id)+" y vm "+str(vm_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar el vinculo entre la VM y la topologia"}
        return JSONResponse(content=data, status_code=400)

###### Vinculo entre Usuario, Rol y Proyecto ######

@app.post("/addUserProjectRole/")
async def createLinkUserProjectRole(body: dict):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'usuario' in body and 'proyecto' in body and 'rol' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO usuario_proyecto_rol (estado,usuario,proyecto,rol) VALUES (1, %s, %s, %s)",(body['usuario'],body['proyecto'],body['rol']))
                cur.execute("SELECT currval('usuario_proyecto_rol_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo vincular la vm con el rol y el usuario!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se vinculo al usuario con el proyecto y su rol",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se pudo crear el vinculo!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.put("/editUserProjectRole/{user_id}/{project_id}/{role_id}")
async def editLinkTopoVMUser(user_id: int = Path(..., description="ID de la topologia a editar"),project_id: int = Path(..., description="ID del proyecto a editar"),role_id: int = Path(..., description="ID del proyecto a editar"),body: dict=None):
    if user_id is None or project_id is None or role_id is None:
        data = {"mensaje": "No se envió datos en el path"}
        return JSONResponse(content=data, status_code=400)
    else:
        if 'usuario' in body and 'proyecto' in body and 'rol' in body:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario_proyecto_rol WHERE usuario = %s AND proyecto = %s AND rol = %s AND estado=1", (user_id,project_id,role_id,))
            result = cur.fetchone()
            if result is None:
                cur.close()
                conn.close()
                data = {"mensaje": "No se encontró el vinculo con el ID proporcionado"}
                return JSONResponse(content=data, status_code=404)
            else:
                try:
                    cur.execute("UPDATE usuario_proyecto_rol SET usuario = %s, proyecto = %s, rol = %s WHERE usuario = %s AND proyecto = %s AND rol = %s AND estado=1",
                                (body['usuario'],body['proyecto'],body['rol'], user_id ,project_id,role_id,))
                    conn.commit()
                    cur.execute("SELECT * FROM usuario_proyecto_rol WHERE usuario = %s AND proyecto = %s AND rol = %s AND estado=1", (body['usuario'],body['proyecto'],body['rol'],))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    vinculo={
                        "id":result[0],
                        "usuario": result[2],
                        "proyecto": result[3],
                        "rol": result[4],
                    }
                    data = {"mensaje": "Se editó correctamente el vinculo", "vinculo": vinculo}
                    return JSONResponse(content=data, status_code=200)
                except psycopg2.Error as e:
                    print(e)
                    cur.close()
                    conn.close()
                    data = {"mensaje": "No se pudo editar el vinculo"}
                    return JSONResponse(content=data, status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400) 

#Listado de Proyecto y Rol por Usuario

@app.get("/getRoleProjectPorUser/{user_id}")
async def get_user(user_id: int = Path(..., description="ID del usuario a buscar")):
    if user_id is None:
        data = {"mensaje": "No se proporcionó el ID de la topologia"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("select proyecto.id,proyecto.nombre,rol.nombre from usuario_proyecto_rol join usuario on usuario.id = usuario_proyecto_rol.usuario join proyecto on proyecto.id = usuario_proyecto_rol.proyecto join rol on usuario_proyecto_rol.rol = rol.id where usuario.id = %s and usuario.estado=1 and rol.estado=1 and proyecto.estado=1 and usuario_proyecto_rol.estado=1;", (user_id,))
        result = cur.fetchall()
        cur.close()
        conn.close()
        vinculos = []
        if len(result)==0:
                    data = {"mensaje": "No se encontró proyectos o roles asociados a ese usuario", "vinculos": vinculos}
                    return JSONResponse(content=data, status_code=200)
        else:
            for row in result:
                vinculo = {
                    "id_proyecto":row[0],
                    "proyecto": row[1],
                    "rol": row[2],
                }
                vinculos.append(vinculo)
            data = {"mensaje": "Lista de vinculos", "vinculos": vinculos}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener los vinculos"}
        return JSONResponse(content=data, status_code=400)

#Listado de Proyecto y Rol por Usuario

@app.get("/getRoleProjectPorUser")
async def get_user():
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("select proyecto.id,proyecto.nombre,rol.nombre from usuario_proyecto_rol join usuario on usuario.id = usuario_proyecto_rol.usuario join proyecto on proyecto.id = usuario_proyecto_rol.proyecto join rol on usuario_proyecto_rol.rol = rol.id where usuario.estado=1 and rol.estado=1 and proyecto.estado=1 and usuario_proyecto_rol.estado=1;")
        result = cur.fetchall()
        cur.close()
        conn.close()
        vinculos = []
        if len(result)==0:
                    data = {"mensaje": "No se encontró proyectos o roles asociados aún", "vinculos": vinculos}
                    return JSONResponse(content=data, status_code=200)
        else:
            for row in result:
                vinculo = {
                    "id_proyecto":row[0],
                    "proyecto": row[1],
                    "rol": row[2],
                }
                vinculos.append(vinculo)
            data = {"mensaje": "Lista de vinculos", "vinculos": vinculos}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener los vinculos"}
        return JSONResponse(content=data, status_code=400)

@app.delete("/deleteRolProjectUser/{role_id}/{project_id}/{user_id}")
async def delete_rol_project_user(role_id: int = Path(..., description="ID de la topologia a editar"),project_id: int = Path(..., description="ID del proyecto a editar"),user_id: int = Path(..., description="ID del proyecto a editar")):
    if role_id is None and user_id is None and project_id is None :
        data = {"mensaje": "No se proporciono los parámetros para la eliminación de manera correcta"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario_proyecto_rol WHERE rol = %s AND usuario = %s AND proyecto = %s AND estado=1", (role_id,user_id,project_id,))
        result = cur.fetchone()
        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró el vinculo con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE usuario_proyecto_rol SET estado = 0 WHERE rol = %s AND usuario = %s AND proyecto = %s AND estado=1", (role_id,user_id,project_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "Vinculo entre el  rol "+str(role_id)+", proyecto "+str(project_id)+" y usuario "+str(user_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar el vinculo entre el usuario, el proyecto y el rol"}
        return JSONResponse(content=data, status_code=400)

#Listado de roles

@app.get("/listarRoles/")
async def listar_Roles():
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM rol WHERE estado = 1")
        result = cur.fetchall()
        cur.close()
        conn.close()
        roles = []
        for row in result:
            rol = {
                "id": row[0],
                "nombre": row[2],
            }
            roles.append(rol)
        data = {"mensaje": "Lista de roles", "roles": roles}
        return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la lista de roles"}
        return JSONResponse(content=data, status_code=400)

## Espacio para implementaciones futuras ##
## CRUD de Imagenes ##
@app.post("/addImagen/{user_id}/{project_id}")
async def add_Imagen(project_id: int = Path(..., description="ID del proyecto"),user_id: int = Path(..., description="ID del usuario"),body: dict=None):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'imagen' in body and project_id is not None and user_id is not None:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO imagen (estado,imagen,proyecto,usuario) VALUES (1,%s,%s,%s)",(body['imagen'],project_id,user_id,))
                cur.execute("SELECT currval('imagen_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo añadir la imagen!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se añadio la imagen con los parámetros especificados",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se puede añadir la imagen!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.get("/listarImagenesxProyecto/{project_id}")
async def listar_Proyecto(project_id: int = Path(..., description="ID del proyecto")):
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    if project_id is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM imagen WHERE estado = 1 and proyecto = %s",(project_id,))
            result = cur.fetchall()
            cur.close()
            conn.close()
            imagenes = []
            for row in result:
                imagen = {
                    "id": row[0],
                    "imagen": row[2]
                }
                imagenes.append(imagen)
            data = {"mensaje": "Lista de imagenes", "imagenes": imagenes}
            return JSONResponse(content=data, status_code=200)
        except psycopg2.Error as e:
            print(e)
            data = {"mensaje": "No se pudo obtener la lista de imagenes"}
            return JSONResponse(content=data, status_code=400)
    else:
        data = {"mensaje": "Se enviaron parámetros vacíos"}
        return JSONResponse(content=data, status_code=400)

@app.delete("/deleteImagen/{imagen_id}")
async def delete_user(imagen_id: int = Path(..., description="ID de la imagen")):
    if imagen_id is None:
        data = {"mensaje": "No se proporcionó el ID del proyecto o ID del usuario"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM imagen WHERE id = %s and estado=1", (imagen_id,))
        result = cur.fetchone()
        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró la imagen con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE imagen SET estado = 0 WHERE id = %s", (imagen_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "imagen con id "+str(imagen_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar la imagen"}
        return JSONResponse(content=data, status_code=400)
## CRUD de Flavors ##
@app.post("/addFlavor/{user_id}/{project_id}")
async def add_Flavor(project_id: int = Path(..., description="ID del proyecto"),user_id: int = Path(..., description="ID del usuario"),body: dict=None):
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'cpu' in body and 'descripcion' in body and 'memoria' in body and 'disco' in body and project_id is not None and user_id is not None:
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO flavor (estado,descripcion,cpu,memoria,disco,proyecto,usuario) VALUES (1,%s,%s,%s,%s,%s,%s)",(body['descripcion'],body['cpu'],body['memoria'],body['disco'],project_id,user_id,))
                cur.execute("SELECT currval('flavor_id_seq')")
                result = cur.fetchone()
                cur.close()
                conn.commit()
                conn.close()
                if result is None:
                    data = {"mensaje": "No se pudo añadir el flavor!",
                            "id": 0}
                    return JSONResponse(content=data,status_code=400)
                else:
                    data = {"mensaje": "se añadio el flavor con los parámetros especificados",
                            "id": result[0]}
                    return JSONResponse(content=data,status_code=200)
            except psycopg2.Error as e:
                print(e)
                data = {"mensaje": "No se puede añadir el flavor!"}
                return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
        
@app.get("/listarFlavors/{project_id}")
async def listar_Proyecto(project_id: int = Path(..., description="ID del proyecto")):
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    if project_id is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM flavor WHERE estado = 1 and proyecto = %s",(project_id,))
            result = cur.fetchall()
            cur.close()
            conn.close()
            flavors = []
            for row in result:
                flavor = {
                    "id": row[0],
                    "descripcion": row[2],
                    "cpu": row[3],
                    "memoria": row[4],
                    "disco": row[5],
                }
                flavors.append(flavor)
            data = {"mensaje": "Lista de flavors", "flavors": flavors}
            return JSONResponse(content=data, status_code=200)
        except psycopg2.Error as e:
            print(e)
            data = {"mensaje": "No se pudo obtener la lista de flavors"}
            return JSONResponse(content=data, status_code=400)
    else:
        data = {"mensaje": "Se enviaron parámetros vacíos"}
        return JSONResponse(content=data, status_code=400)

@app.delete("/deleteFlavor/{flavor_id}")
async def delete_flavor(flavor_id: int = Path(..., description="ID del flavor")):
    if flavor_id is None:
        data = {"mensaje": "No se proporcionó el ID del proyecto o ID del usuario"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM flavor WHERE id = %s and estado = 1", (flavor_id,))
        result = cur.fetchone()
        if result is None:
            cur.close()
            conn.close()
            data = {"mensaje": "No se encontró el flavor con el ID proporcionado"}
            return JSONResponse(content=data, status_code=404)
        else:
            cur.execute("UPDATE flavor SET estado = 0 WHERE id = %s", (flavor_id,))
            conn.commit()
            cur.close()
            conn.close()
            data = {"mensaje": "flavor con id "+str(flavor_id)+" eliminado exitosamente"}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo eliminar la imagen"}
        return JSONResponse(content=data, status_code=400)

@app.put("/editflavor/{flavor_id}")
async def edit_flavor(flavor_id: int = Path(..., description="ID de la topologia a editar"),
                    body: dict = None):
    if body is None:
        data = {"mensaje": "No se envió datos en el body"}
        return JSONResponse(content=data, status_code=400)
    else:
        if 'descripcion' in body and 'cpu' in body and 'memoria' in body and 'disco':
            conn = psycopg2.connect(
                host="10.0.0.10",
                database="linuxorch",
                user="ubuntu",
                password="ubu"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM flavor WHERE id = %s AND estado=1", (flavor_id,))
            result = cur.fetchone()
            if result is None:
                cur.close()
                conn.close()
                data = {"mensaje": "No se encontró la topologia con el ID proporcionado"}
                return JSONResponse(content=data, status_code=404)
            else:
                try:
                    cur.execute("UPDATE flavor SET descripcion = %s, cpu = %s, memoria = %s, disco = %s WHERE id = %s",
                                (body['descripcion'],body['cpu'],body['memoria'],body['disco'], flavor_id,))
                    conn.commit()
                    cur.execute("SELECT * FROM flavor WHERE id = %s", (flavor_id,))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    flavor={
                        "id":result[0],
                        "descripcion": result[2],
                        "cpu": result[3],
                        "memoria": result[4],
                        "disco": result[5],
                        "proyecto": result[6],
                        "usuario": result[7],
                    }
                    data = {"mensaje": "Se editó correctamente el flavor", "flavor": flavor}
                    return JSONResponse(content=data, status_code=200)
                except psycopg2.Error as e:
                    print(e)
                    cur.close()
                    conn.close()
                    data = {"mensaje": "No se pudo editar el flavor"}
                    return JSONResponse(content=data, status_code=400)
        else:
            data = {"mensaje": "Se enviaron campos incorrectos"}
            return JSONResponse(content=data, status_code=400)

@app.get("/getFlavor/{flavor_id}")
async def get_flavor(flavor_id: int = Path(..., description="ID del flavor a buscar")):
    if flavor_id is None:
        data = {"mensaje": "No se proporcionó el ID del flavor"}
        return JSONResponse(content=data, status_code=404)
    conn = psycopg2.connect(
        host="10.0.0.10",
        database="linuxorch",
        user="ubuntu",
        password="ubu"
    )
    try:
        cur = conn.cursor()
        cur.execute("select * from flavor where id=%s and estado=1", (flavor_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is None:
            data = {"mensaje": "No se encontró el flavor con el ID proporcionado o ha sido eliminada"}
            return JSONResponse(content=data, status_code=404)
        else:
            flavor = {
                "id": result[0],
                "descripcion": result[2],
                "cpu": result[3],
                "memoria": result[4],
                "disco": result[5]
            }
            data = {"mensaje": "Se encontró el flavor exitosamente", "vm": flavor}
            return JSONResponse(content=data, status_code=200)
    except psycopg2.Error as e:
        print(e)
        data = {"mensaje": "No se pudo obtener la vm"}
        return JSONResponse(content=data, status_code=400)
## FIN ##
if __name__ == "__main__":
    import uvicorn
    #Inicalizando servicio de API
    uvicorn.run("OrchLinux:app",host="10.0.0.10",port=7070,reload=True)