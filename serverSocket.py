import pymongo
import requests
import socket
import json
from fastapi import FastAPI
import threading

"""
collection={
    "10.0.1.10":"worker1",
    "10.0.1.20":"worker2",
    "10.0.1.30":"worker3"
}
"""
collection={
    "10.0.0.30":"worker1",
    "10.0.0.40":"worker2",
    "10.0.0.50":"worker3"
}

app = FastAPI(title = "Servidor de monitoreo",
              description = "Corriendo servidor!",
              version = "1.0.1")

def socket_listener():
    #Instancia TCP-IP
    print("Servicio de escucha inicializado en el puerto 9898")
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Estadisticas"]
    #Direccionamos con la direccion IP correspondiente a la red interna
    server_add = ('10.0.1.1',9898)
    #Indicamos por donde quiere que escuche
    server_socket.bind(server_add)
    print("Escuchando...")
    server_socket.listen()
    #Aceptamos las conexiones
    while True:
        client_socket, client_add = server_socket.accept()
        print("Conexione entrante de "+str(client_add[0])+ ":"+str(client_add[1]))
        #Recibiendo con buffer 1024 bytes
        data = client_socket.recv(1024).decode('utf-8')
        print(json.loads(data))
        #Almacenamiento de datos en mongo
        mycol = mydb[collection[client_add[0]]]
        x = mycol.insert_one(json.loads(data))
        #Responde
        response = 'Data Received'
        client_socket.sendall(response.encode('utf-8'))
        #Cerramos la conexion
        client_socket.close()

def limpiarBaseDeDatos():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Estadisticas"]
    longitudes={}
    for workerIP in collection:
        col = mydb[collection[workerIP]]
        result= col.find()
        longitudes[collection[workerIP]] = len(result)
    # Se debe eliminar la información
    print(longitudes)
    if longitudes['worker1']>200 and longitudes['worker2']>200 and longitudes['worker3']>200:
        for workerIP in collection:
            col = mydb[collection[workerIP]]
            result = collection.delete_many({}).limit(100)
            print(result.delet_count)

@app.on_event('startup')
async def startup():
    print("Iniciando el API de Monitoreo")
    print("Esperando solicitudes")
    
@app.get("/recursos")
def get_recursos():
    #Obtener los ultimos recursos de cada worker
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
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
    uvicorn.run(app,host="10.0.0.10",port=9090)