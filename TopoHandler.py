import uuid
from Classes.Network import Network
from NetworkHandler import NetworkConstructor
from VMHandler import VMConstructor
class TopoConstructor:
    def lineConstructor(self,VMs,CIDR,neutron,nova):
        numberNetworks = len(VMs) - 1
        networks = []
        #Create Networks
        for i in range(numberNetworks):
            nameNetwork = str(uuid.uuid4)
            networks.append(nameNetwork)
            nameSubnet = str(uuid.uuid4)
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
            nameNetwork = str(uuid.uuid4)
            networks.append(nameNetwork)
            nameSubnet = str(uuid.uuid4)
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
            nameNetwork = str(uuid.uuid4)
            networks.append(nameNetwork) # network = ["asxcsda","asdqoi","foiwenfweip"]
            nameSubnet = str(uuid.uuid4)
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
                VMConstructor.editVM(VM=vm,networks=[networkC],neutron=neutron,nova=nova)
            return 1
        elif len(network) == 1 and len(VMs) == 1:
            VMConstructor.editVM(VM=vm,networks=network,neutron=neutron,nova=nova)
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
            nameNetwork = str(uuid.uuid4)
            networks.append(nameNetwork)
            nameSubnet = str(uuid.uuid4)
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova)
        for i in range(diagonales):
            nameNetwork = str(uuid.uuid4)
            Ndiagonales.append(nameNetwork)
            nameSubnet = str(uuid.uuid4)
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova)
        #Create VMs
        for i in range(len(VMs)):
            VMConstructor.createVM(VMs[i],[networks[i-1],networks[i]],neutron,nova)
        return 1
        pass

    def meshConstructorV2(VMs,CIDR,neutron,nova):
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
            
def networkConstructor(CIDR,neutron,nova):
        nameNetwork = str(uuid.uuid4)
        nameSubnet = str(uuid.uuid4)
        network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
        NetworkConstructor.createNetwork(network,neutron,nova)
        return network            


