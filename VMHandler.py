from Nova import NovaClient
from Neutron import NeutronClient
from Classes.VM import VM
from Classes.Network import Network

class VMConstructor:
    def createVM(VM: VM,networks,neutron: NeutronClient,nova: NovaClient):
        ##Networks es una listas con los nombres de las redes a las cuales se deben crear
        net_id = []
        for n in networks:
            net_id.append(neutron.getNetworkIDbyName(n))

        nova.create_instance_with_multiple_networks(nombre=VM.name,flavorID = VM.flavorID, imageID = VM.imageID, keyPairID = VM.keyPairID, securitygroupID = VM.securitygroupID, networks = net_id)

    def editVM(VM: VM,network: Network,neutron: NeutronClient,nova: NovaClient):
        vm_id = nova.get_instance_id(vm_name=VM.name)
        network_id = neutron.getNetworkIDbyName(network)
        nova.agregar_interfaz_to_VM(network_id=network_id,vm_id=vm_id)


