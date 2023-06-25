from Nova import NovaClient
from Neutron import NeutronClient
from Classes.VM import VM
from Classes.Network import Network

class VMConstructor:
    def createVM(VM: VM,networks,neutron: NeutronClient,nova: NovaClient):
        ##Networks es una listas con los nombres de las redes a las cuales se deben crear
        #nova.create_instance_v2(flavor_id=VM.flavorID,name=VM.name,keypairID=VM.keyPairID,network_id=networks,securitygroupID=VM.securitygroupID)


    def editVM(VM: VM,network,neutron: NeutronClient,nova: NovaClient):
        
        pass
