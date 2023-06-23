from Nova import NovaClient
from Neutron import NeutronClient
from Classes.VM import VM
from Classes.Network import Network

class VMConstructor:
    def createVM(VM: VM,networks,neutron: NeutronClient,nova: NovaClient):
        ##Networks es una listas con los nombres de las redes a las cuales se deben crear
        nova.create_instance(flavor_id=,name=,keypairID=,network_id=,securitygroupID=)
        pass
    def editVM(VM,networks,neutron,nova):
        pass