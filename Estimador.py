import pymongo
import time
import requests
import socket
import json
from fastapi import FastAPI
import threading

ready = False
worker_estimacion = {}
worker_info = {}
collection={
    "worker1":"10.0.0.30",
    "worker2":"10.0.0.40",
    "worker3":"10.0.0.50"
}

app = FastAPI(title = "Servidor de Estimación",
              description = "Corriendo servidor!",
              version = "1.0.1")

def socket_listener():
    #Instancia TCP-IP
    print("Servicio de estimacion inicializado en el puerto 6767")
    myclient = pymongo.MongoClient("mongodb://10.20.12.188:27017/")
    mydb = myclient["Estadisticas"]
    while True:
        ## Ejecuto de manera continua el get de la base de datos para luego enviarlo a cada worker
        hilos = []
        for worker in collection:
            instancia = mydb[worker]    
            hilos.append(threading.Thread(target=getInfoPorWorker,args=(worker,instancia)))
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join()
        hilos = []
        for worker in worker_info:
            hilos.append(threading.Thread(target=sendDataToCompute,args=(worker_info[worker],worker,collection[worker])))
        for hilo in hilos:
            hilo.start()
        i = 0
        for hilo in hilos:
            hilo.join()
            i+=1
        ## Dejo que espere otros 5 segundos
        time.sleep(5)

def getInfoPorWorker(worker,connection):
    global worker_info
    data = connection.find().limit(100).sort("$natural",-1)
    info = {}
    ##Creamos los arreglos de listas
    cpu_0_percent =[]
    cpu_1_percent =[]
    cpu_2_percent=[]
    cpu_3_percent =[]
    memoriaUsadaGB =[]
    memoriaDisponibleMB =[]
    almacenamientoUsadoGB =[]
    almacenamientoUsadoPercent=[]
    for value in data:
        value.pop("_id")
        ## Segmentamos la data que es de utilidad para nosotros
        ## Para los CPUS
        cpu_0_percent.append(value['Core0(%)'])
        cpu_1_percent.append(value['Core1(%)'])
        cpu_2_percent.append(value['Core2(%)'])
        cpu_3_percent.append(value['Core3(%)'])
        ## Para la memoria
        memoriaUsadaGB.append(value['MemoriaUsada(Gb)'])
        memoriaDisponibleMB.append(value['MemoriaDisponible(Mb)'])
        ## Para el disco
        almacenamientoUsadoGB.append(value['AlmacenamientoUsado(Gb)'])
        almacenamientoUsadoPercent.append(value['AlmacenamientoUsado(%)'])
    ## Armamos la estructura
    ## CPU
    info['Core0(%)'] = cpu_0_percent
    info['Core1(%)'] = cpu_1_percent
    info['Core2(%)'] = cpu_2_percent
    info['Core3(%)'] = cpu_3_percent
    ## Memoria
    info['MemoriaUsada(Gb)'] = memoriaUsadaGB
    info['MemoriaDisponible(Mb)'] = memoriaDisponibleMB
    ## Disco
    info['AlmacenamientoUsado(Gb)'] = almacenamientoUsadoGB
    info['AlmacenamientoUsado(%)'] = almacenamientoUsadoPercent
    worker_info[worker] = info

def sendDataToCompute(dataSegment,worker,IP):
    ## Referencia de la variable global
    global worker_estimacion
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((IP,6767))
    informacion=dataSegment
    ## Envío la información al nodo de computo
    data = json.dumps(informacion)
    client_socket.sendall(data.encode('utf-8'))
    ## Recibo la respuesta
    response = client_socket.recv(1024)
    data = json.loads(response.decode('utf-8'))         
    client_socket.close()
    aux = {}
    ## CPU
    aux['Est_Core0(%)'] = data[worker]['Core0(%)']
    aux['Est_Core1(%)'] = data[worker]['Core1(%)']
    aux['Est_Core2(%)'] = data[worker]['Core2(%)']
    aux['Est_Core3(%)'] = data[worker]['Core3(%)']
    ## Memoria
    aux['Est_MemoriaUsada(Gb)'] = data[worker]['MemoriaUsada(Gb)'] 
    aux['Est_MemoriaDisponible(Mb)'] = data[worker]['MemoriaDisponible(Mb)'] 
    ## Disco
    aux['Est_AlmacenamientoUsado(Gb)'] = data[worker]['AlmacenamientoUsado(Gb)'] 
    aux['Est_AlmacenamientoUsado(%)'] = data[worker]['AlmacenamientoUsado(%)'] 
    ## Aqui proceso la informacion y la guardo en base de datos
    worker_estimacion[worker] = aux
    ## Proximamente
    
@app.on_event('startup')
async def startup():
    print("Iniciando el API de Estimación")
    print("Esperando solicitudes...")
    
@app.get("/estimacion")
def get_recursos():
    #Obtener los ultimos recursos de cada worker
    ## Proximamente
    myclient = pymongo.MongoClient("mongodb://10.20.12.188:27017/")
    mydb = myclient["Estadisticas"]
    info = {}
    for x in collection:
        mycol = mydb[collection[x]]
        data = mycol.find().limit(1).sort("$natural",-1)
        print(collection[x])
        print(data[0])
        infoW = data[0]
        infoW.pop("_id")
        print(infoW)
        info[collection[x]] = infoW
    return info

if __name__ == "__main__":
    import uvicorn
    #Inicializando servicio de socket
    socket_thread = threading.Thread(target=socket_listener)
    socket_thread.start()
    #Inicalizando servicio de API
    uvicorn.run(app,host="10.0.0.10",port=8888)