from Neutron import NeutronClient
from Classes.Network import Network 
class NetworkConstructor:
    def createNetwork(network: Network,neutron: NeutronClient,nova):
        neutron.create_network_topology(cidr=network.CIDR,red=network.nameNetwork,subred=network.nameSubnet)
    
