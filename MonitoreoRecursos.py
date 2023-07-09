import requests

#Funcion para obtener informacion remota de los servidores
def obtenerInfoRemoto():
    monitoringAPI = "http://10.20.12.188:9090/recursos"
    response = requests.get(monitoringAPI,headers={'Content-Type': 'application/json'})
    informacion = []
    if response.status_code == 200:
        output = response.json()
        workers  = output.keys()
        for worker in workers:
            servidor = []
            infoWorker = output[worker]
            servidor.append([worker.upper()])
            servidor.append(["Core0 : "+str(infoWorker["Core0(%)"])+"%"])
            servidor.append(["Core1 : "+str(infoWorker["Core1(%)"])+"%"])
            servidor.append(["Core2 : "+str(infoWorker["Core2(%)"])+"%"])
            servidor.append(["Core3 : "+str(infoWorker["Core3(%)"])+"%"])
            servidor.append(["Memoria Usada(Gb): "+str(infoWorker["MemoriaUsada(Gb)"])])
            servidor.append(["Memoria Disponible(Mb): "+str(infoWorker["MemoriaDisponible(Mb)"])])
            servidor.append(["Memoria Total(Gb): "+str(infoWorker["MemoriaTotal(Gb)"])])
            servidor.append(["Almacenamiento Usado(Gb): "+str(infoWorker["AlmacenamientoUsado(Gb)"])])
            servidor.append(["Almacenamiento Usado(%): "+str(infoWorker["AlmacenamientoUsado(%)"])])
            servidor.append(["Almacenamiento Total(Gb):"+ str(infoWorker["AlmacenamientoTotal(Gb)"])])
            servidor.append(["Interfaz ens3 (RX): "+str(infoWorker["ens3(RX)bps"])+"bps"])
            servidor.append(["Interfaz ens3 (TX): "+str(infoWorker["ens3(TX)bps"])+"bps"])
            servidor.append(["Interfaz ens4 (RX): "+str(infoWorker["ens4(RX)bps"])+"bps"])
            servidor.append(["Interfaz ens4 (TX): "+str(infoWorker["ens4(TX)bps"])+"bps"])
            informacion.append(servidor)
    return informacion
   