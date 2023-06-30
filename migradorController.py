from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

app = FastAPI(title="Servidor de migración",
              description="Corriendo servidor responsable de realizar las migraciones correspondientes",
              version="1.0.0"
             )
            
hosts= {
    "10.0.1.10":"compute1",
    "10.0.1.20":"compute2",
    "10.0.1.30":"compute3"
}

def migrarVM(id,hostDestino):
    pass

def obtener_ID_VM(vm_name):
    #A partir del nombre de la VM obtenida de la función padre de esta obtendremos el id de la vm, para posteriormente mmigrar
    pass

def obtener_VM_cargada(vm):
    r = requests.get(f'http://{vm}:13001/')
    if r.status_code == 200:
        data = r.json()
        id_vm = obtener_ID_VM(data["id"])
        return id_vm
    elif r.status_code == 404:
        raise Exception("Mano mira si tus servidores estan vivos en los nodos de computo")
    else:
        raise Exception("Mano no tengo mapeado que error pudo haber salido asi que suerte")

    
#host_migrar: "10.0.1.x", destino: "10.0.1.y"


app.post("/migrar")
async def chamoDeVMs(body: dict):
    if not body:
        resp = {"mensaje": "papi para que me mandas tus webadas?"}
    else:
        if "host_migrar" in body and "destino" in body:
            id_vm = obtener_VM_cargada(body["host_migrar"])
            migrarVM(id_vm,hosts["destino"])


if __name__ == "__main__":
    import uvicorn
    #Inicializando servicio de socket
    #Inicalizando servicio de API
    uvicorn.run(app,host="localhost",port=13000)