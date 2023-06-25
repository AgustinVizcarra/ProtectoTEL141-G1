from Neutron import NeutronClient
from Classes.Network import Network 
class NetworkConstructor:
    def createNetwork(network: Network,neutron: NeutronClient,nova):
        neutron.create_network(cidr,gateway,project,red,subred)
        pass
    
