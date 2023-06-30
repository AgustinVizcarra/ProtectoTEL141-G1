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
        return resultado2
    else:
        print(f"Se produjo un error: {error.decode()}")
        return []

    

def escoger_vm(lista: list):
    return max(lista, key=lambda x: float(x[1]))

app.get("/")
async def soplonVMs():
    pass


if __name__ == "__main__":
    import uvicorn
    #Inicializando servicio de socket
    #Inicalizando servicio de API
    uvicorn.run(app,host="localhost",port=13001)
    