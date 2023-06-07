###########################################NEUTRON###############################################
###############RED################## 

class NeutronClient(object):

    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.neutron_url = "http://10.20.12.39:9696/v2.0/"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }

    def list_networks(self):
        response = requests.get(self.neutron_url + 'networks', headers=self.headers)

        if response.status_code == 200:
            networks = response.json()['networks']
            return networks
        else:
            raise Exception('Failed to list networks. Status code: {}'.format(response.status_code))

    def create_network(self, name):
        network_data = {
            'network': {
                'name': name
            }
        }
        response = requests.post(self.neutron_url + 'networks', json=network_data, headers=self.headers)

        if response.status_code == 201:
            network = response.json()['network']
            return network
        else:
            raise Exception('Failed to create network. Status code: {}'.format(response.status_code))

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

##############GRUPO DE SEGURIDAD##################
    def list_security_groups(self):
        response = requests.get(self.neutron_url + 'security-groups', headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json()['security_groups']
            return security_groups
        else:
            raise Exception('Failed to list security groups. Status code: {}'.format(response.status_code))

    def create_security_group(self, name, description):
        security_group_data = {
            'security_group': {
                'name': name,
                'description': description
            }
        }
        response = requests.post(self.neutron_url + 'security-groups', json=security_group_data, headers=self.headers)

        if response.status_code == 201:
            security_group = response.json()['security_group']
            return security_group
        else:
            raise Exception('Failed to create security group. Status code: {}'.format(response.status_code))

    def get_security_group(self, security_group_id):
        response = requests.get(self.neutron_url + 'security-groups/{}'.format(security_group_id), headers=self.headers)

        if response.status_code == 200:
            security_group = response.json()['security_group']
            return security_group
        else:
            raise Exception('Failed to get security group. Status code: {}'.format(response.status_code))

    def update_security_group(self, security_group_id, new_name, new_description):
        security_group_data = {
            'security_group': {
                'name': new_name,
                'description': new_description
            }
        }
        response = requests.put(self.neutron_url + 'security-groups/{}'.format(security_group_id),
                                json=security_group_data, headers=self.headers)

        if response.status_code == 200:
            security_group = response.json()['security_group']
            return security_group
        else:
            raise Exception('Failed to update security group. Status code: {}'.format(response.status_code))

    def delete_security_group(self, security_group_id):
        response = requests.delete(self.neutron_url + 'security-groups/{}'.format(security_group_id), headers=self.headers)

        if response.status_code == 204:
            return True
        else:
            raise Exception('Failed to delete security group. Status code: {}'.format(response.status_code))


###################PUERTOS - TEMA A TRATAR ###################################