import uuid
import math
from Classes.Network import Network
from NetworkHandler import NetworkConstructor
from VMHandler import VMConstructor
class TopoConstructor:
    def lineConstructor(self,VMs,CIDR,neutron,nova):
        numberNetworks = len(VMs) - 1
        networks = []
        #Create Networks
        for i in range(numberNetworks):
            nameNetwork = str(uuid.uuid4())
            networks.append(nameNetwork)
            nameSubnet = str(uuid.uuid4())
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova) 
        #Create VMs
        for i in range(len(VMs)):
            if i == 0:
                VMConstructor.createVM(VMs[i],[networks[i]],neutron,nova)
            elif i == (len(VMs) - 1):
                VMConstructor.createVM(VMs[i],[networks[i-1]],neutron,nova)
            else:
                VMConstructor.createVM(VMs[i],[networks[i-1],networks[i]],neutron,nova)
        return 1
    
    def ringConstructor(self,VMs,CIDR,neutron,nova):
        numberNetworks = len(VMs)
        networks = []
        #Create Networks
        for i in range(numberNetworks):
            nameNetwork = str(uuid.uuid4())
            networks.append(nameNetwork)
            nameSubnet = str(uuid.uuid4())
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova)
        #Create VMs
        for i in range(len(VMs)):
            VMConstructor.createVM(VMs[i],[networks[i-1],networks[i]],neutron,nova)
        return 1
    

    def busConstructor(self,VMs,CIDR,neutron,nova):
        numberNetworks = 1
        networks = [] 
        #Create Networks
        for i in range(numberNetworks):
            nameNetwork = str(uuid.uuid4())
            networks.append(nameNetwork) # network = ["asxcsda","asdqoi","foiwenfweip"]
            nameSubnet = str(uuid.uuid4())
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova)
        #Create VMs
        for i in range(len(VMs)):
            VMConstructor.createVM(VMs[i],[networks[0]],neutron,nova)
        return 1

    def linkConstructor(VMs, network,neutron, nova, CIDR):
        #Crear enlace entre dos vms
        if len(network) == 0 and len(VMs) == 2:
            networkC = networkConstructor(CIDR=CIDR,neutron=neutron,nova=nova)
            for vm in VMs:
                VMConstructor.editVM(VM=vm,network=networkC.nameNetwork,neutron=neutron,nova=nova)
            return 1
        elif len(network) == 1 and len(VMs) == 1:
            VMConstructor.editVM(VM=VMs[0],network=network[0],neutron=neutron,nova=nova)
            return 1
        else:
            return 1
        
    def linkDestructor(VM, network, neutron, nova):
        pass
        


    def meshConstructor(self,VMs,CIDR,neutron,nova):
        n = len(VMs)
        numberNetworksPerimetrales = n 
        diagonalexArista = n - 3
        diagonales = ((n*(n-3))/2)
        networks = []
        Ndiagonales = []
        #Create Networks
        for i in range(numberNetworksPerimetrales):
            nameNetwork = str(uuid.uuid4())
            networks.append(nameNetwork)
            nameSubnet = str(uuid.uuid4())
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova)
        for i in range(diagonales):
            nameNetwork = str(uuid.uuid4())
            Ndiagonales.append(nameNetwork)
            nameSubnet = str(uuid.uuid4())
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova)
        #Create VMs
        for i in range(len(VMs)):
            VMConstructor.createVM(VMs[i],[networks[i-1],networks[i]],neutron,nova)
        return 1
        pass
    
    #Para crear el árbol
    def arbolConstructor(self,VMs,CIDR,neutron,nova):
        pass
    
    def meshConstructorV2(self,VMs,CIDR,neutron,nova):
        ### Primero debemos mapear la relación entre VM's y el número de vertices de una red MESH
        ## para eso se realiza lo siguiente:
        mapVMVertice = {}
        ## Enlaces mapean los valores contiguos
        enlacesContiguos = {}
        enlacesCruzados = {}
        mapVMNetwork = {}
        i = 1
        for vm in VMs:
            mapVMVertice[i] = vm
            i+=1
        ## Esto se mapea de la siguiente manera p.e {Vertice: 1, VM: VM1}
        ## Ahora si quere mapear los enlaces perimetrales se hace de la siguiente manera
        ## Si la secuencia a nivel de vertices es 1-2-3-4-5-6-1 (Para tener una figura cerrada) (Siendo N=6)
        for iterador in mapVMVertice.keys():
            ##Definimos los casos aislado
            if iterador == 1:
                ## para este caso los enlaces adyacentes son N-1 y 1-2 por lo que se define la creacion de esos enlaces
                ## Será bueno usar una colección que permita mapear la VM junto con las redes creadas
                enlacesContiguos[iterador] = [len(mapVMVertice),iterador + 1]
                ## Solo se mapea la creacion del valor con el nodo vecino inferior o sea 6-1/1-2/2-3/... etc
                mapVMNetwork[iterador] = networkConstructor(CIDR,neutron,nova)
            elif iterador == len(mapVMVertice):
                ## En la logica generica ya se mapea el escenario del ultimo enlace N-1 y N, sin embargo añadimos los adyacentes
                enlacesContiguos[iterador] = [iterador-1,1]
                ## Creacion del enlace N-1-N
                mapVMNetwork[iterador] = networkConstructor(CIDR,neutron,nova)
            else:
                ## Logica generica: enlaces n-1_n y n_n+1
                enlacesContiguos[iterador]=[iterador-1,iterador+1]
                ## Creacion del enlace n-1-n
                mapVMNetwork[iterador] = networkConstructor(CIDR,neutron,nova)
        ## Una vez que tenemos mapeados los enlaces contiguos ahora podemos crear los enlaces cruzados (o sea los valores que no son contiguos)
        for v in enlacesContiguos.keys():
            ## Verificamos los enlaces que no sean contiguos
            ## Siendo i {1,2,3,...,N}
            for i in mapVMVertice.keys():
                ## Enlaces contiguos v {1:[6,2]}
                if i not in enlacesContiguos[v]:
                    ## Verificamos que no sea un enlace repetido 1-4 / 4-1:
                    if len(enlacesCruzados.keys()) ==0:
                        ## Quiere decir que el diccionario está vacío
                        enlacesCruzados[[v,i]] = networkConstructor(CIDR,neutron,nova)
                    else:
                        for j in enlacesCruzados.keys():
                            # Siendo J una lista de enlaces [1,4],[1,5]
                            if i not in j:
                                ## Añadimos el enlace junto con la creacion
                                enlacesCruzados[[v,i]] = networkConstructor(CIDR,neutron,nova)
        ## Finalmente procedemos a la creacion de las VMs junto con sus redes contiguos y cruzadas
        for i in mapVMVertice.keys():
            ## Definimos un vector auxiliar que contenga todas las redes para la creacion de la VM
            aux = []
            ## Verificamos los enlaces contiguos
            for j in enlacesContiguos.keys():
                if j == i:
                    ## Verificamos el contenido de los enlaces contiguos
                    aux.append(mapVMNetwork[i]) ## enlace n-1 y n
                    aux.append(mapVMNetwork[i+1]) ## enlace
                if j == len(enlacesContiguos):
                    aux.append(mapVMNetwork[i])
                    ## Cierro el contorno de la figura
                    aux.append(mapVMNetwork[1])
            for k in enlacesCruzados.keys():
                if i in k:
                    ## Verifico que i se encuentre en la dupla k o sea si i es 1 y k es [1,4] verifico que esté ahí
                    aux.append(mapVMNetwork[k])
            ## Una vez tenido todas las redes creadas se procede a crear las vm's junto con sus redes contiguas y cruzadas
            VMConstructor.createVM(mapVMVertice[i],aux,neutron,nova)

        def treeConstructor(self,VMs,CIDR,neutron,nova,niveles):
            # Definimos la cantidad de Vm's por nivel para eso consideramos lo siguiente
            if(niveles>=3):
                # Realizo la numeración
                numeracion = {}
                i = 1
                for vm in VMs:
                    numeracion[i] = vm
                    i+=1
                cantidad_vms = len(VMs) 
                # Nos basamos que la razon de la progresion geometrica no puede ser mayor a la mitad del número de VM's
                # Aplicando la division entera
                aux_mitad = cantidad_vms//niveles
                # Usamos un diccionario que permita guardar la desviacion entre la suma de potencias y la cantidad de VM's
                map_diferencias = {}
                for i in range(2,aux_mitad+1):
                    # No se considera el 1 puesto que no se tendría una serie geométrica y no se podría sumar los términos
                    suma=int((1 * (math.pow(i, niveles )-1)) / (i-1))
                    # Hallamos el valor que más se acerca a la cantidad de vms para ello
                    diferencia= cantidad_vms-suma
                    map_diferencias[i]=diferencia
                # hallo el indice de la cantidad de nodos por nivel y la diferencia que este tiene con respecto a la cantidad de VM's
                cantidad_nodos_vm = min(map_diferencias,key=abs(map_diferencias.get))
                # Ahora tenemos 2 casuisticas de
                if(map_diferencias[cantidad_nodos_vm]==0):
                    # Quiere decir que la suma de la progresion geométrica cuya razon es la cantidad de nodos por VM es la cantidad de nodos o vms en total
                    enlaces = {}
                    for n in range(niveles):
                        j=0
                        for k in range(cantidad_nodos_vm**n):
                            if(k==0 and n==0):
                                nodo = 1
                                for i in range(cantidad_nodos_vm):
                                    vecino = cantidad_nodos_vm**n + i + 1
                                    # Creo una red que almacene la conexión entre el nodo y el vecino
                                    nameNetwork = str(uuid.uuid4())
                                    nameSubnet = str(uuid.uuid4())
                                    network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
                                    enlaces[network]=[nodo,vecino]
                            elif(n>0 and n < (niveles-1)):
                                nodo = int(((cantidad_nodos_vm**n-1)/(cantidad_nodos_vm-1))+k+1)
                                for i in range(cantidad_nodos_vm):
                                    vecino = nodo+cantidad_nodos_vm**n+i+j*(cantidad_nodos_vm-1)
                                    nameNetwork = str(uuid.uuid4())
                                    nameSubnet = str(uuid.uuid4())
                                    network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
                                    enlaces[network]=[nodo,vecino]
                                j+=1
                        # Una vez que conozco en que nodo me encuentro procedo a ver los vecinos
                        nodo_enlace = {}    
                        # Posteriormente
                        for vm_index in numeracion:
                            # Instancio
                            nodo_enlace[vm_index] = []
                            for network in enlaces:
                                if enlaces[network][0]==vm_index:
                                    # Red de nodo
                                    nodo_enlace[vm_index].append(network)
                                elif enlaces[network][1]==vm_index:
                                    # Red de vecino
                                    nodo_enlace[vm_index].append(network)
                        # Finalmente con el mapeo creo la red
                        for nodo in nodo_enlace:
                            VMConstructor.createVM(numeracion[nodo],nodo_enlace[nodo],neutron,nova)
                else:   
                    # Quiere decir que la suma no cuadra con la cantidad de nodos
                    # Primero analizamos la suma total más proxima a la cantidad de nodos
                    nodos_general=int((1 * (cantidad_nodos_vm**niveles)-1)/(cantidad_nodos_vm-1))
                    if(map_diferencias[cantidad_nodos_vm]<0):
                        # Quiere decir que tengo una cantidad que es menor a mi total con esto en cuenta
                        enlaces = {}
                        for n in range(niveles):
                            j=0
                            for k in range(cantidad_nodos_vm**n):
                                if(k==0 and n==0):
                                    nodo = 1
                                    for i in range(cantidad_nodos_vm):
                                        vecino = cantidad_nodos_vm**n + i + 1
                                        # Creo una red que almacene la conexión entre el nodo y el vecino
                                        if (vecino in numeracion.keys()):
                                            nameNetwork = str(uuid.uuid4())
                                            nameSubnet = str(uuid.uuid4())
                                            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
                                            enlaces[network]=[nodo,vecino]
                                elif(n>0 and n < (niveles-1)):
                                    nodo = int(((cantidad_nodos_vm**n-1)/(cantidad_nodos_vm-1))+k+1)
                                    for i in range(cantidad_nodos_vm):
                                        vecino = nodo+cantidad_nodos_vm**n+i+j*(cantidad_nodos_vm-1)
                                        if (vecino in numeracion.keys()):
                                            # Quiere decir que si se encuentra dentro del rango (caso contrario no la añado)
                                            nameNetwork = str(uuid.uuid4())
                                            nameSubnet = str(uuid.uuid4())
                                            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
                                            enlaces[network]=[nodo,vecino]
                                    j+=1
                        # Una vez que conozco en que nodo me encuentro procedo a ver los vecinos
                        nodo_enlace = {}    
                        # Posteriormente
                        for vm_index in numeracion:
                            # Instancio
                            nodo_enlace[vm_index] = []
                            for network in enlaces:
                                if enlaces[network][0]==vm_index:
                                    # Red de nodo
                                    nodo_enlace[vm_index].append(network)
                                elif enlaces[network][1]==vm_index:
                                    # Red de vecino
                                    nodo_enlace[vm_index].append(network)
                        # Finalmente con el mapeo creo la red
                        for nodo in nodo_enlace:
                            VMConstructor.createVM(numeracion[nodo],nodo_enlace[nodo],neutron,nova)                        
                    else:
                        enlaces = {}
                        for n in range(niveles):
                            j=0
                            for k in range(cantidad_nodos_vm**n):
                                if(k==0 and n==0):
                                    nodo = 1
                                    for i in range(cantidad_nodos_vm):
                                        vecino = cantidad_nodos_vm**n + i + 1
                                        # Creo una red que almacene la conexión entre el nodo y el vecino
                                        nameNetwork = str(uuid.uuid4())
                                        nameSubnet = str(uuid.uuid4())
                                        network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
                                        enlaces[network]=[nodo,vecino]
                                elif(n>0 and n < (niveles-1)):
                                    nodo = int(((cantidad_nodos_vm**n-1)/(cantidad_nodos_vm-1))+k+1)
                                    for i in range(cantidad_nodos_vm):
                                        vecino = nodo+cantidad_nodos_vm**n+i+j*(cantidad_nodos_vm-1)
                                        nameNetwork = str(uuid.uuid4())
                                        nameSubnet = str(uuid.uuid4())
                                        network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
                                        enlaces[network]=[nodo,vecino]
                                    j+=1
                        # Hasta aquí se tendría el mapeo de los nodos en general (ahora adicionalmente):
                        # Tener en cuenta lo siguiente la cantidad de nodos máxima de nodos queda definida en un factor n+1
                        # Puesto que considerando la suma de n niveles para N+1 siendo N la cantidad de nodos por nivel
                        # Difiere en un factor de N+1 del punto de medio de la suma de los n cuadrados con razón N
                        # ¿ Y esto por qué? -> Puesto que si se tiene más nodos que el valor del punto medio entonces estamos en 
                        # la situacion en donde se debe aumentar el número de nodos 
                        # Para tener un mejor entendimiento plantiemos el siguiente ejemplo
                        # Supongamos que el usuario ingresa una cantidad de nodos igual a 10 y una cantidad de niveles igual a 3
                        # El algoritmo mapeará en donde se tenga una menor diferencia dado que se tendrá lo siguiente
                        # En un inicio se mapeará una cantidad máxima según esta premisa de hasta 10 considerando una base de 7
                        # Si se tuviera una cantidad de nodos = 11 se mapearía a la cantidad proxima que en este caso sería 13 para n=3 (o sea máximo se puede tener una rama adicional)
                        # Punto y aparte mapeamos 
                        k = 2
                        # Reenumeramos los nodos restantes
                        reOrdenamiento={}
                        for nodoExtra in range(nodos_general+1,len(VMs)+1):
                            reOrdenamiento[k]= nodoExtra
                            k+=1
                        for n in range(niveles):
                            j=0
                            for k in range(cantidad_nodos_vm**n):
                                if(k==0 and n==0):
                                    nodo = 1
                                    for i in range(cantidad_nodos_vm):
                                        vecino = cantidad_nodos_vm**n + i + 1
                                        # Creo una red que almacene la conexión entre el nodo y el vecino
                                        try:
                                            if (reOrdenamiento[vecino] in reOrdenamiento.values()):
                                                nameNetwork = str(uuid.uuid4())
                                                nameSubnet = str(uuid.uuid4())
                                                network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
                                                enlaces[network]=[nodo,reOrdenamiento[vecino]]
                                        except:
                                            pass
                                elif(n>0 and n < (niveles-1)):
                                    nodo = int(((cantidad_nodos_vm**n-1)/(cantidad_nodos_vm-1))+k+1)
                                    for i in range(cantidad_nodos_vm):
                                        vecino = nodo+cantidad_nodos_vm**n+i+j*(cantidad_nodos_vm-1)
                                        try:
                                            if (reOrdenamiento[vecino] in reOrdenamiento.values()):
                                                nameNetwork = str(uuid.uuid4())
                                                nameSubnet = str(uuid.uuid4())
                                                network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
                                                enlaces[network]=[reOrdenamiento[nodo],reOrdenamiento[vecino]]
                                        except:
                                            pass
                                    j+=1
                        # Una vez que conozco en que nodo me encuentro procedo a ver los vecinos
                        nodo_enlace = {}    
                        # Posteriormente
                        for vm_index in numeracion:
                            # Instancio
                            nodo_enlace[vm_index] = []
                            for network in enlaces:
                                if enlaces[network][0]==vm_index:
                                    # Red de nodo
                                    nodo_enlace[vm_index].append(network)
                                elif enlaces[network][1]==vm_index:
                                    # Red de vecino
                                    nodo_enlace[vm_index].append(network)
                        # Finalmente
                        for nodo in nodo_enlace:
                            VMConstructor.createVM(numeracion[nodo],nodo_enlace[nodo],neutron,nova)
            else:
                print("[*] Debe ingresar una cantidad de niveles mayor o igual a 3")
                
def networkConstructor(CIDR,neutron,nova):
        nameNetwork = str(uuid.uuid4())
        nameSubnet = str(uuid.uuid4())
        network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
        NetworkConstructor.createNetwork(network,neutron,nova)
        return network            


