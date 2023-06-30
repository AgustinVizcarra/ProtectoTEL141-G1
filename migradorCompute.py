from fastapi import FastAPI
from fastapi.responses import JSONResponse
import subprocess

app = FastAPI(title="Servidor de cliente",
              description="Corriendo servidor responsable de darte el nombre de la VM mas pesada con respecto a recursos",
              version="1.0.0"
             )
    
#host_migrar: "10.0.1.x", destino: "10.0.1.y"

#ps aux | grep 'libvirt+.*qemu' | awk '{match($0, /uuid=([^,]+)/, uuid); match($0, /[0-9]+/); print uuid[1], substr($0, RSTART, RLENGTH)}'

def obtener_uuids_pids():
    comando = "ps aux | grep 'libvirt+.*qemu' | awk '{match($0, /uuid=([^,]+)/, uuid); match($0, /[0-9]+/); print uuid[1], substr($0, RSTART, RLENGTH)}'"
    proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, error = proceso.communicate()

    if proceso.returncode == 0:
        lineas = salida.decode().split('\n')[:-2]  # Eliminar la última línea 
        resultado = [linea.split(':') for linea in lineas]
        resultado.pop(-1)
        resultado2 = []
        for i in resultado:
            aux = i[0].split(" ")
            resultado2.append(aux)
        #devuelve esto [[uuid,pid], ....]
        return resultado

    else:
        print(f"Se produjo un error: {error.decode()}")
        return []


def obtener_cpu_mem():
    pass

def obtener_Vm_migrar():
    uwu = obtener_uuids_pids()
    uwu1 = []
    for i in uwu:
        aux = obtener_cpu_mem()
        #aux = [%cpu,%mem]
        uwu1.append([i[0],aux[0],aux[1]])


app.get("/")
async def soplonVMs():
    uuid = obtener_Vm_migrar()
    data = {"uuid":uuid}
    return JSONResponse(content=data,status_code=200)


if __name__ == "__main__":
    import uvicorn
    #Inicializando servicio de socket
    #Inicalizando servicio de API
    uvicorn.run(app,host="localhost",port=13001)