import socket
import json

def socket_listener(IP):
    #Instancia TCP-IP
    print("Servicio de escucha inicializado en el puerto 9898")
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Direccionamos con la direccion IP correspondiente a la red interna
    server_add = (IP,6767)
    #Indicamos por donde quiere que escuche
    server_socket.bind(server_add)
    print("Escuchando Peticiones...")
    server_socket.listen()
    #Aceptamos las conexiones
    while True:
        client_socket, client_add = server_socket.accept()
        print("Conexione entrante de "+str(client_add[0])+ ":"+str(client_add[1]))
        #Recibiendo con buffer 1024 bytes
        data = client_socket.recv(1024)
        data = data.decode('utf-8')
        informacion = json.loads(data)
        #Responde
        message = {'msg':'Data Received'}
        response = json.dumps(message)
        client_socket.sendall(response.encode('utf-8'))
        #Cerramos la conexion
        client_socket.close()
        
if __name__ == "__main__":
    IP = input("Ingrese la dirección IP de este nodo de la red de management (x.x.x.x):")
    socket_listener(IP)