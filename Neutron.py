###########################################NEUTRON###############################################
import requests
###############RED################## 

class NeutronClient(object):

    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.neutron_url = "http://10.20.12.48:9696/v2.0/"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }
        self.NetworkID = None
        
    def getNetworkID(self):
        return self.NetworkID
    
    def setNetworkID(self,NetworkID):
        self.NetworkID = NetworkID
        
    def list_networks(self):
        response = requests.get(self.neutron_url + 'networks', headers=self.headers)

        if response.status_code == 200:
            networks = response.json()['networks']
            return networks
        else:
            raise Exception('Failed to list networks. Status code: {}'.format(response.status_code))

    #Funcion que permite crear la redprovider
    def create_network(self, red,subred,cidr,gateway,project):
        network_data = {
            'network': {
                'name': red,
                'project_id ': project
            }
        }
        response = requests.post(self.neutron_url + 'networks', json=network_data, headers=self.headers)

        if response.status_code == 201:
            network_id = response.json()['network']['id']
            
            subnet_data = {
                'subnet': {
                    'name': subred,
                    'network_id': network_id,
                    'cidr': cidr,
                    'gateway_ip': gateway
                }
            }
            
            response = requests.post(self.neutron_url + 'subnets', json=subnet_data, headers=self.headers)
            if response.status_code == 201:
                self.NetworkID = network_id
                print("[*] Red Provider creada exitosamente\n")
            else:
                print("[*] Ha ocurrido un error al crear la redProvider\n")
        else:
            print("[*] Ha ocurrido un error al crear la redProvider\n")


    def get_network(self, network_id):
        response = requests.get(self.neutron_url + 'networks/{}'.format(network_id), headers=self.headers)

        if response.status_code == 200:
            network = response.json()['network']
            return network
        else:
            raise Exception('Failed to get network. Status code: {}'.format(response.status_code))

    def update_network(self, network_id, new_name):
        network_data = {
            'network': {
                'name': new_name
            }
        }
        response = requests.put(self.neutron_url + 'networks/{}'.format(network_id), json=network_data, headers=self.headers)

        if response.status_code == 200:
            network = response.json()['network']
            return network
        else:
            raise Exception('Failed to update network. Status code: {}'.format(response.status_code))

    def delete_network(self, network_id):
        response = requests.delete(self.neutron_url + 'networks/{}'.format(network_id), headers=self.headers)

        if response.status_code == 204:
            return True
        else:
            raise Exception('Failed to delete network. Status code: {}'.format(response.status_code))

    #Funcion para saber si ya existe una redprovider
    def existe_network(self,project_id):
        response = requests.get(self.neutron_url + 'networks?project_id='+project_id, headers=self.headers)
        if response.status_code == 200:
            networks = response.json()['networks']
            if len(networks) != 0:
                network_id = networks[0]['id']
                self.NetworkID =  network_id
                return True
        return False
        
        
    #Funcion que devuelve la info de una red y su subred
    def infoRedProvider(self):
        url = f"{self.nova_url}/os-networks"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            networks = response.json().get('networks', [])
            for network in networks:
                print("Información de la red y subred:")
                print("ID de la red:", network['id'])
                print("Nombre de la red:", network['label'])
                print("ID de la subred:", network['cidr'])
                print("Proveedor de la red:", network['provider'])
                return
            print("No se encontró información de la red y subred")
        else:
            print("Error al obtener la información de la red y subred:", response.status_code)    
        
###################SUBRED################## 

    def list_subnets(self):
        response = requests.get(self.neutron_url + 'subnets', headers=self.headers)

        if response.status_code == 200:
            subnets = response.json()['subnets']
            return subnets
        else:
            raise Exception('Failed to list subnets. Status code: {}'.format(response.status_code))

    def create_subnet(self, name, network_id, cidr, gateway_ip):
        subnet_data = {
            'subnet': {
                'name': name,
                'network_id': network_id,
                'cidr': cidr,
                'gateway_ip': gateway_ip
            }
        }
        response = requests.post(self.neutron_url + 'subnets', json=subnet_data, headers=self.headers)

        if response.status_code == 201:
            subnet = response.json()['subnet']
            return subnet
        else:
            raise Exception('Failed to create subnet. Status code: {}'.format(response.status_code))

    def get_subnet(self, subnet_id):
        response = requests.get(self.neutron_url + 'subnets/{}'.format(subnet_id), headers=self.headers)

        if response.status_code == 200:
            subnet = response.json()['subnet']
            return subnet
        else:
            raise Exception('Failed to get subnet. Status code: {}'.format(response.status_code))

    def update_subnet(self, subnet_id, new_name):
        subnet_data = {
            'subnet': {
                'name': new_name
            }
        }
        response = requests.put(self.neutron_url + 'subnets/{}'.format(subnet_id), json=subnet_data, headers=self.headers)

        if response.status_code == 200:
            subnet = response.json()['subnet']
            return subnet
        else:
            raise Exception('Failed to update subnet. Status code: {}'.format(response.status_code))

    def delete_subnet(self, subnet_id):
        response = requests.delete(self.neutron_url + 'subnets/{}'.format(subnet_id), headers=self.headers)

        if response.status_code == 204:
            return True
        else:
            raise Exception('Failed to delete subnet. Status code: {}'.format(response.status_code))

###################PUERTOS - TEMA A TRATAR ###################################