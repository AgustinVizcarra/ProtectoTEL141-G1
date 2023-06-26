from Nova import NovaClient
from Neutron import NeutronClient
from Classes.VM import VM
from Classes.Network import Network

class VMConstructor:
    def createVM(VM: VM,networks,neutron: NeutronClient,nova: NovaClient):
        ##Networks es una listas con los nombres de las redes a las cuales se deben crear
        nova.create_instance_with_multiple_networks(nombre=VM.name,flavorID = VM.flavorID, imageID = VM.imageID, keyPairID = VM.keyPairID, securitygroupID = VM.securitygroupID, networks = networks)

    def editVM(VM: VM,network,neutron: NeutronClient,nova: NovaClient):
        pass

    
