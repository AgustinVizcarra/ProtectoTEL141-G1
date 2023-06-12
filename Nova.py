########################################## NOVA ##################################################
##########FLAVOR###########
class NovaClient(object):
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.nova_url = "http://10.20.12.39:8774/"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }
       
        

    def list_flavors(self):
        response = requests.get(self.nova_url + '/flavors', headers=self.headers)

        if response.status_code == 200:
            flavors = response.json()['flavors']
            return flavors
        else:
            raise Exception('Failed to list flavors. Status code: {}'.format(response.status_code))

    def create_flavor(self, name, ram, vcpus, disk):
        flavor_data = {
            'flavor': {
                'name': name,
                'ram': ram,
                'vcpus': vcpus,
                'disk': disk
            }
        }
        response = requests.post(self.nova_url + '/flavors', json=flavor_data, headers=self.headers)

        if response.status_code == 200:
            flavor = response.json()['flavor']
            return flavor
        else:
            raise Exception('Failed to create flavor. Status code: {}'.format(response.status_code))

    def get_flavor(self, flavor_id):
        response = requests.get(self.nova_url + '/flavors/{}'.format(flavor_id), headers=self.headers)

        if response.status_code == 200:
            flavor = response.json()['flavor']
            return flavor
        else:
            raise Exception('Failed to get flavor. Status code: {}'.format(response.status_code))

    def update_flavor(self, flavor_id, new_name, new_ram, new_vcpus, new_disk):
        flavor_data = {
            'flavor': {
                'name': new_name,
                'ram': new_ram,
                'vcpus': new_vcpus,
                'disk': new_disk
            }
        }
        response = requests.put(self.nova_url + '/flavors/{}'.format(flavor_id), json=flavor_data, headers=self.headers)

        if response.status_code == 200:
            flavor = response.json()['flavor']
            return flavor
        else:
            raise Exception('Failed to update flavor. Status code: {}'.format(response.status_code))

    def delete_flavor(self, flavor_id):
        response = requests.delete(self.nova_url + '/flavors/{}'.format(flavor_id), headers=self.headers)

        if response.status_code == 204:
            return True
        else:
            raise Exception('Failed to delete flavor. Status code: {}'.format(response.status_code))

##########KEYPAIR###########
#Crear Keypair
    def crearKeyPair(self,name,ubicacion,user):
        pass
    
#Listar keypairs
    def listarKeyPair(self,user):
        pass

#Info keypair
    def infoKeyPair(self,keypair,user):
        pass
    
#Borrar keypair
    def borrarKeyPair(self,keypair,user):
        pass

#Obtener ID de keypair
    def obtenerIDKeyPair(self,keypair):
        pass
##########SECURITY GROUP###########
#Crear securitygroup
    def crearSecurityGroup(self,name,descripcion):
        pass
    
#Listar securitygroup
    def listarSecurityGroup(self):
        pass

#Editar securitygroup
    def editarSecurityGroup(self,name,nuevoname,descripcion):
        pass
    
#Eliminar securitygroup
    def eliminarSecurityGroup(self,name):
        pass

#Obtener ID de securitygroup
    def obtenerIDSecurityGroup(self,securitygroup):
        pass
    
#Agregar regla
    def agregarRegla(self,nombre,protocol_ip,from_port,dest_port,cidr):
        pass

#Eliminar regla
    def eliminarRegla(self,ID):
        pass

#################MAQUINA VM (opciones)#######################
# Listar las instancias de VM
    def list_instances(self,project_id):
        response = requests.get(self.nova_url + '/servers', headers=self.headers)

        if response.status_code == 200:
            instances = response.json()['servers']
            return instances
        else:
            raise Exception('Failed to list instances. Status code: {}'.format(response.status_code))

    # Crear una instancia de VM
    def create_instance(self, name, flavor_id, image_id, network_id,keypairID,securitygroupID):
        instance_data = {
            'server': {
                'name': name,
                'flavorRef': flavor_id,
                'imageRef': image_id,
                'networks': [
                    {'uuid': network_id}
                ]
            }
        }
        response = requests.post(self.nova_url + '/servers', json=instance_data, headers=self.headers)

        if response.status_code == 202:
            instance = response.json()['server']
            return instance
        else:
            raise Exception('Failed to create instance. Status code: {}'.format(response.status_code))

    # Obtener detalles de una instancia de VM
    def get_instance(self, instance_id):
        response = requests.get(self.nova_url + '/servers/{}'.format(instance_id), headers=self.headers)

        if response.status_code == 200:
            instance = response.json()['server']
            return instance
        else:
            raise Exception('Failed to get instance. Status code: {}'.format(response.status_code))

    # Actualizar una instancia de VM
    def update_instance(self, name, newname, descripcion):
        instance_data = {
            'server': {
                'name': new_name
            }
        }
        response = requests.put(self.nova_url + '/servers/{}'.format(instance_id), json=instance_data, headers=self.headers)

        if response.status_code == 200:
            instance = response.json()['server']
            return instance
        else:
            raise Exception('Failed to update instance. Status code: {}'.format(response.status_code))

    # Eliminar una instancia de VM
    def delete_instance(self, instance_id):
        response = requests.delete(self.nova_url + '/servers/{}'.format(instance_id), headers=self.headers)

        if response.status_code == 204:
            return True
        else:
            raise Exception('Failed to delete instance. Status code: {}'.format(response.status_code))
    
     # Apagar una instancia de VM
    def stop_instance(self, instance_id):
        action_data = {
            'os-stop': None
        }
        response = requests.post(self.nova_url + '/servers/{}/action'.format(instance_id), json=action_data, headers=self.headers)

        if response.status_code == 202:
            return True
        else:
            raise Exception('Failed to stop instance. Status code: {}'.format(response.status_code))

    # Encender una instancia de VM
    def start_instance(self, instance_id):
        action_data = {
            'os-start': None
        }
        response = requests.post(self.nova_url + '/servers/{}/action'.format(instance_id), json=action_data, headers=self.headers)

        if response.status_code == 202:
            return True
        else:
            raise Exception('Failed to start instance. Status code: {}'.format(response.status_code))

    # Detener una instancia de VM
    def suspend_instance(self, instance_id):
        action_data = {
            'suspend': None
        }
        response = requests.post(self.nova_url + '/servers/{}/action'.format(instance_id), json=action_data, headers=self.headers)

        if response.status_code == 202:
            return True
        else:
            raise Exception('Failed to suspend instance. Status code: {}'.format(response.status_code))

    # Reiniciar una instancia de VM
    def reboot_instance(self, instance_id):
        action_data = {
            'reboot': {
                'type': 'SOFT'
            }
        }
        response = requests.post(self.nova_url + '/servers/{}/action'.format(instance_id), json=action_data, headers=self.headers)

        if response.status_code == 202:
            return True
        else:
            raise Exception('Failed to reboot instance. Status code: {}'.format(response.status_code))

#MIGRAR
