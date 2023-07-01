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

def obtener_cpu_memoria(pid: str):
    comand = f'top -p {pid} -b -n 2 -d 0.2'
    comand = comand +  "| tail -1 | awk '{print $9 \" \" $10}'"
    proceso = subprocess.Popen(comand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, error = proceso.communicate()
    if proceso.returncode == 0:
        lineas = salida.decode()[:-1]
        lineas = lineas.split(" ")
        return lineas

    else:
        print(f"Se produjo un error: {error.decode()}")
        return []

def escoger_vm(lista: list):
    return max(lista, key=lambda x: float(x[1]))

app.get("/")
async def soplonVMs():
    uuid_pid = obtener_uuids_pids()
    uwu = []
    for i in uuid_pid:
        aux = obtener_cpu_memoria(i[1])
        uwu.append([i[0],aux[0],aux[1]])
    uuid = escoger_vm(uwu)[0]
    data = {
        "uuid": uuid        
    }    
    return JSONResponse(content=data,status_code=200)


if __name__ == "__main__":
    import uvicorn
    #Inicializando servicio de socket
    #Inicalizando servicio de API
    uvicorn.run(app,host="localhost",port=13001)
    