import socket
import json
import threading
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Instaciacion Variables globales
# CPU
estimacion_core_0_percent=0
estimacion_core_1_percent=0
estimacion_core_2_percent=0
estimacion_core_3_percent=0
# memoria
estimacion_memoria_usada_gb=0
estimacion_memoria_disponible_mb=0
# disco
estimacion_disco_usado_gb=0
estimacion_disco_usado_percent=0

collection={
    "10.0.0.30":"worker1"
    "10.0.0.40":"worker2"
    "10.0.0.50":"worker3"
}

def socket_listener(IP):
    # Llamado de variables globales
    global estimacion_core_0_percent,estimacion_core_1_percent,estimacion_core_2_percent,estimacion_core_3_percent
    global estimacion_memoria_usada_gb,estimacion_memoria_disponible_mb
    global estimacion_disco_usado_gb,estimacion_disco_usado_percent
    # Instancia TCP-IP Socket
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
        # Procesamos la información para crear los hilos respectivos
        # CPU
        input_core_0_percent = informacion['Core0(%)']
        input_core_1_percent = informacion['Core1(%)']
        input_core_2_percent = informacion['Core2(%)']
        input_core_3_percent = informacion['Core3(%)']
        # Memoria
        input_memoria_usada_GB = informacion['MemoriaUsada(Gb)']
        input_memoria_diponible_MB = informacion['MemoriaDisponible(Mb)']
        # Disco
        input_almacenamiento_usado_GB = informacion['AlmacenamientoUsado(Gb)']
        input_almacenamiento_usado_percent = informacion['AlmacenamientoUsado(%)']
        # Llamo a las funciones para realizar la estimación respectiva y los lanzo por medio de hilos
        estimacion_CPU = threading.Thread(target=estimarCPU,args=(input_core_0_percent,input_core_1_percent,input_core_2_percent,input_core_3_percent))
        estimacion_memoria = threading.Thread(target=estimarMemoria,args=(input_memoria_usada_GB,input_memoria_diponible_MB))
        estimacion_almacenamiento = threading.Thread(target=estimarAlmacenamiento,args=(input_almacenamiento_usado_GB,input_almacenamiento_usado_percent))
        # Defino los hilos para la ejecucuion en paralelo
        hilos = [estimacion_CPU,estimacion_memoria,estimacion_almacenamiento]
        # Ejecucion
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join()
        #Responde
        # Una vez obtenido todos los datos se arma el body
        body={}
        # CPU
        body['Core0(%)'] = estimacion_core_0_percent
        body['Core1(%)'] = estimacion_core_1_percent
        body['Core2(%)'] = estimacion_core_2_percent
        body['Core3(%)'] = estimacion_core_3_percent
        # Memoria
        body['MemoriaUsada(Gb)'] = estimacion_memoria_usada_gb
        body['MemoriaDisponible(Mb)'] = estimacion_memoria_disponible_mb
        # Disco
        body['AlmacenamientoUsado(Gb)'] = estimacion_disco_usado_gb
        body['AlmacenamientoUsado(%)'] = estimacion_disco_usado_percent
        # Formulacion
        data = {collection[IP],body}
        response = json.dumps(data)
        client_socket.sendall(response.encode('utf-8'))
        #Cerramos la conexion
        client_socket.close()

def estimarCPU(input_core_0_percent,input_core_1_percent,input_core_2_percent,input_core_3_percent):
    ## ARFIMA
    global estimacion_core_0_percent,estimacion_core_1_percent,estimacion_core_2_percent,estimacion_core_3_percent
    ## Para el core 0 (%)
    train = input_core_0_percent
    # Se entrena el modelo ARIMA fraccionario
    model = ARIMA(train, order=(1, 0.5, 1))
    model_fit = model.fit(disp=0)
    # Se realiza la predicción del valor siguiente a las listas de entrada
    estimacion_core_0_percent = model_fit.forecast()[0]
    ## Para el core 1 (%)
    train = input_core_1_percent
    model = ARIMA(train, order=(1, 0.5, 1))
    model_fit = model.fit(disp=0)
    estimacion_core_1_percent = model_fit.forecast()[0]
    ## Para el core 2 (%)
    train = input_core_2_percent
    model = ARIMA(train, order=(1, 0.5, 1))
    model_fit = model.fit(disp=0)
    estimacion_core_2_percent = model_fit.forecast()[0]
    ## Para el core 3 (%)
    train = input_core_3_percent
    model = ARIMA(train, order=(1, 0.5, 1))
    model_fit = model.fit(disp=0)
    estimacion_core_3_percent = model_fit.forecast()[0]
    
def estimarMemoria(input_memoria_usada_GB,input_memoria_diponible_MB):
    ## ARIMA
    global estimacion_memoria_usada_gb,estimacion_memoria_disponible_mb
    # Para la memoria usada en GB
    train = input_memoria_usada_GB
    # Se entrena el modelo ARIMA simple
    model = ARIMA(train, order=(1, 1, 1))
    model_fit = model.fit(disp=0)
    estimacion_memoria_usada_gb = model_fit.forecast()[0]
    # Para la memoria disponle en MB
    train = input_memoria_disponible_MB
    model = ARIMA(train, order=(1, 1, 1))
    model_fit = model.fit(disp=0)
    estimacion_memoria_disponible_mb = model_fit.forecast()[0]
    
def estimarAlmacenamiento(input_almacenamiento_usado_GB,input_almacenamiento_usado_percent):
    ## Suavizado Exponencial
    global estimacion_disco_usado_gb,estimacion_disco_usado_percent
    # Para el almacenamiento usado en GB
    train = input_almacenamiento_usado_GB
    # Se utiliza el método de suavizado exponencial
    model = ExponentialSmoothing(train)
    model_fit = model.fit(disp=0)
    estimacion_disco_usado_gb = model_fit.forecast()[0]
    # Para el almacenamiento usado en %
    train = input_almacenamiento_usado_percent
    model = ExponentialSmoothing(train)
    model_fit = model.fit(disp=0)
    estimacion_disco_usado_percent = model_fit.forecast()[0]

if __name__ == "__main__":
    IP = input("Ingrese la dirección IP de este nodo de la red de management (x.x.x.x):")
    socket_listener(IP)