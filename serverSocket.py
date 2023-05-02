import pymongo
import requests
import socket
import json
from fastapi import FastAPI
import threading

collection={
    "192.168.200.201":"worker1",
    "192.168.200.202":"worker2",
    "192.168.200.203":"worker3"
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
    server_add = ('192.168.200.200',9898)
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
@app.on_event('startup')
async def startup():
    print("Iniciando el API de Monitoreo")
    print("Esperando solicitudes")
    
if __name__ == "__main__":
    import uvicorn
    #Inicializando servicio de socket
    socket_thread = threading.Thread(target=socket_listener)
    socket_thread.start()
    #Inicalizando servicio de API
    uvicorn.run(app,host="10.0.0.10",port=9090)

    