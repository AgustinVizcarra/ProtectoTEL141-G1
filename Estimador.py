import pymongo
import time
import socket
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time
from datetime import datetime  
import threading
import requests

ready = False
worker_estimacion = {}
worker_info = {}
tiempo_espera = 0
collection={"worker1":6701,"worker2":6702, "worker3":6703}
collection_compute={"worker1":"10.0.1.10","worker2":"10.0.1.20", "worker3":"10.0.1.30"}
worker_sobrecargados = {}
worker_libre = {}


app = FastAPI(title = "Servidor de Estimación",
              description = "Corriendo servidor!",
              version = "1.0.1")

def socket_listener():
    #Instancia TCP-IP
    global tiempo_espera
    global ready
    print("Servicio de estimacion inicializado en el puerto 6767")
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Estadisticas"]
    while True:
        ## Ejecuto de manera continua el get de la base de datos para luego enviarlo a cada worker
        hilos = []
        ready = False
        inicio = time.perf_counter()
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
        final = time.perf_counter()
        ## Aqui ya se debe tener todas las colecciones como para poder guardarla en base de datos
        tiempo_espera = final - inicio
        ready = True
        ## alerto en caso haya sobrecarga
        alertarMigrador()
        ## Dejo que espere otros 5 segundos
        time.sleep(5)

def alertarMigrador():
    global worker_estimacion
    global worker_sobrecargados
    global worker_libre
    conteo_cpu = 0
    conteo_memoria = 0
    conteo_disco = 0
    for worker in worker_estimacion:
        # Hallamos el conteo por CPU (realizamos la suma)
        conteo_cpu = worker_estimacion[worker]['Est_Core0(%)']+worker_estimacion[worker]['Est_Core1(%)']+worker_estimacion[worker]['Est_Core2(%)']+worker_estimacion[worker]['Est_Core3(%)']
        # Hallamos el conteo por Memoria (consideramos los megas disponibles)
        conteo_memoria = worker_estimacion[worker]['Est_MemoriaDisponible(Mb)']
        # Hallamos el porcentaje de disco disponible (consideramos el porcentaje de disco)
        conteo_disco = worker_estimacion[worker]['Est_AlmacenamientoUsado(%)']
        # Realizamos el análisis
        if conteo_cpu >= 390 or conteo_memoria <= 200 or conteo_disco >= 98:
            # Se debe migrar urgentemente
            worker_sobrecargados[worker] = collection_compute[worker]
    # Renicio mis variables auxiliares
    conteo_cpu = 0
    conteo_memoria = 0
    conteo_disco = 0
    #Analizo para definir el worker libre
    cons_cpu =0
    cons_memoria=0
    cons_disco=0
    cons_worker=''
    if len(worker_sobrecargados)==0:
        # Quiere decir que no hay problemas
        pass
    else:
        # Quiere decir que si hay problemas
        if (len(worker_sobrecargados)==len(collection)):
            # No hay chance de migración todo el sistema se encuentra sobrecargado
            pass
        else:
            # Si hay chance de migracion para eso debemos identificar el worker libre en base a consolidacion
            for worker in worker_estimacion:
                # Verifico para no interar sobre los workers 
                if worker not in worker_sobrecargados.keys():
                    # Quiere decir que me encuentro en alguno de los workers que se encuentra libre
                    conteo_cpu = worker_estimacion[worker]['Est_Core0(%)']+worker_estimacion[worker]['Est_Core1(%)']+worker_estimacion[worker]['Est_Core2(%)']+worker_estimacion[worker]['Est_Core3(%)']
                    # Hallamos el conteo por Memoria (consideramos los megas disponibles)
                    conteo_memoria = worker_estimacion[worker]['Est_MemoriaDisponible(Mb)']
                    # Hallamos el porcentaje de disco disponible (consideramos el porcentaje de disco)
                    conteo_disco = worker_estimacion[worker]['Est_AlmacenamientoUsado(%)']
                    # Capacidad de migrar o un best effort (10% mas delta) o una hpc (100% de un core)
                    if conteo_cpu>cons_cpu and conteo_memoria>cons_memoria and conteo_disco>cons_disco and conteo_cpu<290 and conteo_memoria>200 and conteo_disco<95:
                        #Busco los valores que permitan la consolidacion
                        cons_cpu=conteo_cpu
                        cons_memoria=conteo_memoria
                        cons_disco=conteo_disco
                        cons_worker=worker
            # Una vez acabado el ciclo iterativo
            worker_libre[cons_worker]= collection_compute[cons_worker]
            # Realizar el envío de información al migrador
            for worker_sobrecargado in worker_sobrecargados:
                body={
                    "host_migrar": worker_sobrecargados[worker_sobrecargado],
                    "destino": worker_libre[cons_worker]
                }
                endpoint = "http://localhost:13000/migrar"
                response = requests.post(endpoint, json=body)
        
def getInfoPorWorker(worker,connection):
    global worker_info
    data = connection.find().sort("$natural",-1).limit(100)
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
    #timestamps = []
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
        #timestamps.append(value['timestamp'])
    ## Armamos la estructura
    ## CPU
    cpu_0_percent.reverse()
    cpu_1_percent.reverse()
    cpu_2_percent.reverse()
    cpu_3_percent.reverse()
    info['Core0(%)'] = cpu_0_percent
    info['Core1(%)'] = cpu_1_percent
    info['Core2(%)'] = cpu_2_percent
    info['Core3(%)'] = cpu_3_percent
    ## Memoria
    memoriaUsadaGB.reverse()
    memoriaDisponibleMB.reverse()
    info['MemoriaUsada(Gb)'] = memoriaUsadaGB
    info['MemoriaDisponible(Mb)'] = memoriaDisponibleMB
    ## Disco
    almacenamientoUsadoGB.reverse()
    almacenamientoUsadoPercent.reverse()
    info['AlmacenamientoUsado(Gb)'] = almacenamientoUsadoGB
    info['AlmacenamientoUsado(%)'] = almacenamientoUsadoPercent
    #timestamps.reverse()
    #print(timestamps)
    worker_info[worker] = info

def sendDataToCompute(dataSegment,worker,port):
    ## Referencia de la variable global
    global worker_estimacion
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(('10.20.12.48',port))
    informacion=dataSegment
    ## Envío la información al nodo de computo
    data = json.dumps(informacion)
    client_socket.sendall(data.encode('utf-8'))
    ## Recibo la respuesta
    response = client_socket.recv(1024)
    data = json.loads(response.decode('utf-8'))
    print(data)         
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
    aux['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    worker_estimacion[worker] = aux
    
    
@app.on_event('startup')
async def startup():
    print("Iniciando el API de Estimación")
    print("Esperando solicitudes...")
    
@app.get("/estimacion")
async def get_recursos():
    #Obtener los ultimos recursos de cada worker
    ## Proximamente
    global ready
    body_response = {}
    if ready:
        # Quiere decir que la informacion se encuentra lista para ser enviada
        body_response["mensaje"] = "Estimacion ejecutada exitosamente"
        body_response["estimacion"] = worker_estimacion
        body_response["tiempo_respuesta"] = tiempo_espera
        return JSONResponse(content=body_response,status_code=200)
    else:
        # La informacion no se encuentra lista para enviarse por lo que debe esperar
        while True:
            if ready:
                # Quiere decir que la info se encuentra lista para enviarse
                # Al dar un return es como si diera un break
                body_response["mensaje"] = "Estimacion ejecutada exitosamente"
                body_response["estimacion"] = worker_estimacion
                body_response["tiempo_respuesta"] = tiempo_espera
                return JSONResponse(content=body_response,status_code=200)

@app.post("/allocate")
async def allocateVM(body: dict):
    global ready
    global worker_estimacion
    if not body:
        #Si en caso no se tiene valores dentro del body
        data = {"mensaje": "Se debe proveer un body para realizar el allocation de la VM"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'flavor' in body and 'estilo' in body:
            # Aquí se tiene dos casuisticas si en caso se tiene 
            conteo_cpu = 0
            conteo_memoria = 0
            conteo_disco = 0
            cons_worker = ''
            if body['estilo'] == 'besteffort':
                # Dimensionamos en funcion de best effort
                # Para la cantidad de vCPU's*10 + 10 (hipervisor + I/O)
                cpu_requirement = body['flavor']['vcpus']*10 + 10
                # Para la cantidad de memoria (1Gb memoria) -> 10% 1Gb del Host
                memory_requirement = body['flavor']['memory']*0.1
                # Para el disco (relacion 1:1)
                disco_requirement = body['flavor']['storage']
                if ready:
                    # Quiere decir que la informacion se encuentra lista para ser el analisis
                    for worker in worker_estimacion:
                        # Analizamos el candidato mediante consolidacion
                        conteo_cpu = worker_estimacion[worker]['Est_Core0(%)']+worker_estimacion[worker]['Est_Core1(%)']+worker_estimacion[worker]['Est_Core2(%)']+worker_estimacion[worker]['Est_Core3(%)']+cpu_requirement
                        conteo_memoria = worker_estimacion[worker]['Est_MemoriaUsada(Gb)']+memory_requirement
                        conteo_disco = worker_estimacion[worker]['Est_AlmacenamientoUsado(Gb)']+disco_requirement
                        if conteo_cpu>cons_cpu and conteo_memoria>cons_memoria and conteo_disco>cons_disco and conteo_cpu<390 and conteo_memoria<4.08 and conteo_disco<9.4:
                            #Busco los valores que permitan la consolidacion
                            cons_cpu=conteo_cpu
                            cons_memoria=conteo_memoria
                            cons_disco=conteo_disco
                            cons_worker=worker
                    if cons_worker != '':
                        body_response={"destino":collection_compute[cons_worker]}
                    else:
                        body_response={"destino":"Sistema saturado"}
                    return JSONResponse(content=body_response,status_code=200)
                else:
                    # La informacion no se encuentra lista para enviarse por lo que debe esperar
                    while True:
                        if ready:
                            # Quiere decir que la info se encuentra lista para el analisis
                            for worker in worker_estimacion:
                                # Analizamos el candidato mediante consolidacion
                                conteo_cpu = worker_estimacion[worker]['Est_Core0(%)']+worker_estimacion[worker]['Est_Core1(%)']+worker_estimacion[worker]['Est_Core2(%)']+worker_estimacion[worker]['Est_Core3(%)']+cpu_requirement
                                conteo_memoria = worker_estimacion[worker]['Est_MemoriaUsada(Gb)']+memory_requirement
                                conteo_disco = worker_estimacion[worker]['Est_AlmacenamientoUsado(Gb)']+disco_requirement
                                if conteo_cpu>cons_cpu and conteo_memoria>cons_memoria and conteo_disco>cons_disco and conteo_cpu<390 and conteo_memoria<4.08 and conteo_disco<9.4:
                                    #Busco los valores que permitan la consolidacion
                                    cons_cpu=conteo_cpu
                                    cons_memoria=conteo_memoria
                                    cons_disco=conteo_disco
                                    cons_worker=worker
                            if cons_worker != '':
                                body_response={"destino":collection_compute[cons_worker]}
                            else:
                                body_response={"destino":"Sistema saturado"}
                            return JSONResponse(content=body_response,status_code=200)
            elif body['estilo'] == 'hpc':
                # Dimensionamos en funcion de HPC
                # Para la cantidad de vCPU's*100 + 10 (hipervisor + I/O)
                cpu_requirement = body['flavor']['vcpus']*100 + 10
                # Para la cantidad de memoria (1Gb memoria) -> 10% 1Gb del Host
                memory_requirement = body['flavor']['memory']*0.1
                # Para el disco (relacion 1:1)
                disco_requirement = body['flavor']['storage']
                if ready:
                    # Quiere decir que la informacion se encuentra lista para ser el analisis
                    for worker in worker_estimacion:
                        # Analizamos el candidato mediante consolidacion
                        conteo_cpu = worker_estimacion[worker]['Est_Core0(%)']+worker_estimacion[worker]['Est_Core1(%)']+worker_estimacion[worker]['Est_Core2(%)']+worker_estimacion[worker]['Est_Core3(%)']+cpu_requirement
                        conteo_memoria = worker_estimacion[worker]['Est_MemoriaUsada(Gb)']+memory_requirement
                        conteo_disco = worker_estimacion[worker]['Est_AlmacenamientoUsado(Gb)']+disco_requirement
                        if conteo_cpu>cons_cpu and conteo_memoria>cons_memoria and conteo_disco>cons_disco and conteo_cpu<390 and conteo_memoria<4.08 and conteo_disco<9.4:
                            #Busco los valores que permitan la consolidacion
                            cons_cpu=conteo_cpu
                            cons_memoria=conteo_memoria
                            cons_disco=conteo_disco
                            cons_worker=worker
                    if cons_worker != '':
                        body_response={"destino":collection_compute[cons_worker]}
                    else:
                        body_response={"destino":"Sistema saturado"}
                    return JSONResponse(content=body_response,status_code=200)
                else:
                    # La informacion no se encuentra lista para enviarse por lo que debe esperar
                    while True:
                        if ready:
                            # Quiere decir que la info se encuentra lista para el analisis
                            for worker in worker_estimacion:
                                # Analizamos el candidato mediante consolidacion
                                conteo_cpu = worker_estimacion[worker]['Est_Core0(%)']+worker_estimacion[worker]['Est_Core1(%)']+worker_estimacion[worker]['Est_Core2(%)']+worker_estimacion[worker]['Est_Core3(%)']+cpu_requirement
                                conteo_memoria = worker_estimacion[worker]['Est_MemoriaUsada(Gb)']+memory_requirement
                                conteo_disco = worker_estimacion[worker]['Est_AlmacenamientoUsado(Gb)']+disco_requirement
                                if conteo_cpu>cons_cpu and conteo_memoria>cons_memoria and conteo_disco>cons_disco and conteo_cpu<390 and conteo_memoria<4.08 and conteo_disco<9.4:
                                    #Busco los valores que permitan la consolidacion
                                    cons_cpu=conteo_cpu
                                    cons_memoria=conteo_memoria
                                    cons_disco=conteo_disco
                                    cons_worker=worker
                            if cons_worker != '':
                                body_response={"destino":collection_compute[cons_worker]}
                            else:
                                body_response={"destino":"Sistema saturado"}
                            return JSONResponse(content=body_response,status_code=200)
            else:
                data = {"mensaje": "no se tiene este estilo para el despliegue de VM"}
                return JSONResponse(content=data,status_code=400) 
        else:
            data = {"mensaje": "se enviaron campos incorrectos"}
            return JSONResponse(content=data,status_code=400)
            
if __name__ == "__main__":
    import uvicorn
    #Inicializando servicio de socket
    socket_thread = threading.Thread(target=socket_listener)
    socket_thread.start()
    #Inicalizando servicio de API
    uvicorn.run(app,host="10.0.0.10",port=8888)