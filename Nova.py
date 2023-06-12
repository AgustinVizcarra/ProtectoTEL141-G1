########################################## NOVA ##################################################
import requests
##########FLAVOR###########
class NovaClient(object):
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.nova_url = "http://10.20.12.48:8774/v2.1"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }
       

    def list_flavors(self):
        response = requests.get(self.nova_url + '/flavors', headers=self.headers)

        if response.status_code == 200:
            flavors = response.json().get('flavors', [])
            flavor_info = []
            for flavor in flavors:
                flavor_info.append([flavor['id'], flavor['name'], flavor['ram'], flavor['disk'], flavor['vcpus']])
            return flavor_info
        else:
            raise Exception('Error al listar los flavors. Código de estado: {}'.format(response.status_code))

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
        url = f"{self.nova_url}/os-keypairs"
        data = {
            'keypair': {
                'name': name,
                'location': ubicacion,
                'user': user
            }
        }
        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 200:
            keypair = response.json().get('keypair', {})
            print("Keypair creado exitosamente:", keypair['name'])
        else:
            print("Error al crear el Keypair:", response.status_code)
    
#Listar keypairs
    def listarKeyPair(self,user):
        url = f"{self.nova_url}/os-keypairs"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])
            keypair_names=[]
            for keypair in keypairs:
                if keypair['user'] == user:
                    print("Nombre del Keypair:", keypair['name'])
                    keypair_names.append(keypair['name'])
                    return keypair_names
        else:
            print("Error al listar los Keypairs:", response.status_code)

#Info keypair
    def infoKeyPair(self,keypair,user):
        url = f"{self.nova_url}/os-keypairs"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])
            for kp in keypairs:
                if kp['user'] == user and kp['name'] == keypair:
                    print("Información del Keypair:")
                    print("Nombre:", kp['name'])
                    print("Ubicación:", kp['location'])
                    print("Usuario:", kp['user'])
                    info={
                        'nombre': kp['name'],
                        'tipo': kp['type'],
                        'fingerprint': kp['fingerprint'],
                        'fechacreacion': kp['created_at'],
                        'publickey': kp['public_key']
                    }
                    return info
            print("No se encontró el Keypair especificado")
        else:
            print("Error al obtener la información del Keypair:", response.status_code)
    
#Borrar keypair
    def borrarKeyPair(self,keypair,user):
        url = f"{self.nova_url}/os-keypairs"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])
            for kp in keypairs:
                if kp['user'] == user and kp['name'] == keypair:
                    url_keypair = f"{url}/{kp['id']}"
                    response_borrar = requests.delete(url_keypair, headers=self.headers)
                    if response_borrar.status_code == 204:
                        print("Keypair eliminado exitosamente")
                    else:
                        print("Error al eliminar el Keypair:", response_borrar.status_code)
                    return
            print("No se encontró el Keypair especificado")
        else:
            print("Error al eliminar el Keypair:", response.status_code)

#Obtener ID de keypair
    def obtenerIDKeyPair(self,keypair):
        url = f"{self.nova_url}/os-keypairs"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])
            for kp in keypairs:
                if kp['name'] == keypair:
                    print("ID del Keypair:", kp['id'])
                    return kp['id']
            print("No se encontró el Keypair especificado")
        else:
            print("Error al obtener el ID del Keypair:", response.status_code)

##########SECURITY GROUP###########
#Crear securitygroup
    def crearSecurityGroup(self,name,descripcion):
        url = f"{self.nova_url}/os-security-groups"
        data = {
            'security_group': {
                'name': name,
                'description': descripcion
            }
        }
        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 200:
            security_group = response.json().get('security_group', {})
            print("Grupo de seguridad creado exitosamente:", security_group['name'])
        else:
            print("Error al crear el Grupo de seguridad:", response.status_code)
    
#Listar securitygroup
    def listarSecurityGroup(self):
        url = f"{self.nova_url}/os-security-groups"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            print("Lista de Grupos de Seguridad:")
            lista_sg = []
            for sg in security_groups:
                print("Nombre:", sg['name'])
                print("Descripción:", sg['description'])
                #print("ID:", sg['id'])
                print("----------")
                lista_sg.append([sg['name'], sg['description']])
            return lista_sg
        else:
            print("Error al listar los Grupos de Seguridad:", response.status_code)

#Editar securitygroup
    def editarSecurityGroup(self,name,nuevoname,descripcion):
        url = f"{self.nova_url}/os-security-groups"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            for sg in security_groups:
                if sg['name'] == name:
                    url_editar = f"{url}/{sg['id']}"
                    data = {
                        'security_group': {
                            'name': nuevoname,
                            'description': descripcion
                        }
                    }
                    response_editar = requests.put(url_editar, json=data, headers=self.headers)
                    if response_editar.status_code == 200:
                        print("Grupo de seguridad editado exitosamente")
                    else:
                        print("Error al editar el Grupo de seguridad:", response_editar.status_code)
                    return
            print("No se encontró el Grupo de seguridad especificado")
        else:
            print("Error al obtener los Grupos de seguridad:", response.status_code)
    
#Eliminar securitygroup
    def eliminarSecurityGroup(self,name):
        url = f"{self.nova_url}/os-security-groups"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            for sg in security_groups:
                if sg['name'] == name:
                    url_eliminar = f"{url}/{sg['id']}"
                    response_eliminar = requests.delete(url_eliminar, headers=self.headers)
                    if response_eliminar.status_code == 204:
                        print("Grupo de seguridad eliminado exitosamente")
                    else:
                        print("Error al eliminar el Grupo de seguridad:", response_eliminar.status_code)
                    return
            print("No se encontró el Grupo de seguridad especificado")
        else:
            print("Error al obtener los Grupos de seguridad:", response.status_code)

#Obtener ID de securitygroup
    def obtenerIDSecurityGroup(self,securitygroup):
        url = f"{self.nova_url}/os-security-groups"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            for sg in security_groups:
                if sg['name'] == securitygroup:
                    print("ID del Grupo de seguridad:", sg['id'])
                    return sg['id']
            print("No se encontró el Grupo de seguridad especificado")
        else:
            print("Error al obtener el ID del Grupo de seguridad:", response.status_code)
    
#Agregar regla
    def agregarRegla(self,nombre,protocol_ip,from_port,dest_port,cidr):
        url = f"{self.nova_url}/os-security-group-rules"
        data = {
            'security_group_rule': {
                'security_group_name': nombre,
                'protocol': protocol_ip,
                'from_port': from_port,
                'to_port': dest_port,
                'cidr': cidr
            }
        }
        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 200:
            security_group_rule = response.json().get('security_group_rule', {})
            print("Regla de seguridad agregada exitosamente:")
            print("Nombre del grupo de seguridad:", security_group_rule['security_group_name'])
            print("Protocolo:", security_group_rule['protocol'])
            print("Puerto origen:", security_group_rule['from_port'])
            print("Puerto destino:", security_group_rule['to_port'])
            print("CIDR:", security_group_rule['cidr'])
        else:
            print("Error al agregar la regla de seguridad:", response.status_code)

#Eliminar regla
    def eliminarRegla(self,ID):
        url = f"{self.nova_url}/os-security-group-rules"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            security_group_rules = response.json().get('security_group_rules', [])
            for rule in security_group_rules:
                if rule['id'] == ID:
                    url_eliminar = f"{url}/{ID}"
                    response_eliminar = requests.delete(url_eliminar, headers=self.headers)
                    if response_eliminar.status_code == 204:
                        print("Regla de seguridad eliminada exitosamente")
                    else:
                        print("Error al eliminar la regla de seguridad:", response_eliminar.status_code)
                    return
            print("No se encontró la regla de seguridad especificada")
        else:
            print("Error al obtener las reglas de seguridad:", response.status_code)

#################MAQUINA VM (opciones)#######################
# Listar las instancias de VM
    def list_instances(self,project_id):
        response = requests.get(self.nova_url + '/servers', headers=self.headers)

        if response.status_code == 200:
            vm_names=[]
            instances = response.json().get('servers',[])
            for instance in instances:
                vm_names.append(instance['name'])
            return vm_names
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
                'name': newname
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
