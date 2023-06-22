import uuid
from Classes.Network import Network
from NetworkHandler import NetworkConstructor
from VMHandler import VMConstructor
class TopoConstructor:
    def lineConstructor(VMs,CIDR,neutron,nova):
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
    
    def ringConstructor(VMs,CIDR,neutron,nova):
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
    

    def busConstructor(VMs,CIDR,neutron,nova):
        numberNetworks = 1
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
            VMConstructor.createVM(VMs[i],[networks[0]],neutron,nova)
        return 1


    def meshConstructor(VMs,CIDR,neutron,nova):
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


