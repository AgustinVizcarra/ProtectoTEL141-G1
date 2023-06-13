########################################## NOVA ##################################################
import requests
##########FLAVOR###########
class NovaClient(object):
    def __init__(self, auth_token,username, password):
        self.auth_url = "http://10.20.12.48:5000/v3"
        self.auth_token = auth_token
        self.username = username
        self.password = password
        self.IdProject = None  # Agregar propiedad IdProject
        self.nova_url = "http://10.20.12.48:8774"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }


#Obtener TOKEN por proyecto
    def get_token_project(self,IdProject):
        auth_data = {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': self.username, 
                            'password': self.password, 
                            'domain': {'name': 'Default'}
                        }
                    }
                },
                "scope": {
                    "project":{
                        "id": IdProject
                    }
                }
            }
        }
        
        
        response = requests.post(self.auth_url+"/auth/tokens",
                                 json=auth_data,
                                 headers=self.headers)

        if response.status_code == 201:
            self.token = response.headers['X-Subject-Token']
            self.UserID = response.json()["token"]["user"]['id']
            print("[*] La solicitud se completó correctamente\n")
            
        else:
            print("[*] Error de autorización, verifique credenciales\n")
        
        return self.token

   
       

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
    def crearKeyPair(self, name):
        url = f"{self.nova_url}/v2.1/os-keypairs"
        data = {
            'keypair': {
                'name': name,
            }
        }
        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 200:
            keypair = response.json().get('keypair', {})
            keypair_name = keypair.get('name')
            keypair_key = keypair.get('public_key')
            keypair_id = keypair.get('user_id')
            print("Keypair creado exitosamente:")
            print("Nombre: ", keypair_name)
            print("Llave pública: ", keypair_key)
            print("ID de usuario: ", keypair_id)
        else:
            print("Error al crear el Keypair:", response.status_code)


#Info keypair
    def infoKeyPair(self,keypair_name,user):
        url = f"{self.nova_url}/v2.1/os-keypairs/{keypair_name}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            keypair = response.json().get('keypair', [])
            info=[]
            if keypair['user_id'] == user and keypair['name'] == keypair_name:
        
                info.append(keypair['name'])
                info.append("ssh")
                info.append(keypair['fingerprint'])
                info.append(keypair['created_at'])
                info.append(keypair['public_key'])
                info.append(keypair['user_id'])
                
                return info
            else:
                print("No se encontró el Keypair especificado")
        else:
            print("Error al obtener la información del Keypair:", response.status_code)

    
#Listar keypairs
    def listarKeyPair(self, user):
        url = f"{self.nova_url}/v2.1/os-keypairs"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])
            if len(keypairs) == 0:
                print("No cuenta con ninguna keypair, por favor cree una")
                return None
            else:
                keypair_names = []
                for keypair in keypairs:
                    keypair_name = keypair['keypair']['name']
                    info = self.infoKeyPair(keypair_name, user)
                    if info[5] == user:
                        keypair_names.append(keypair_name)

                if len(keypair_names) == 0:
                    print("No se encontraron keypairs para el usuario:", user)
                else:
                    print("Keypairs del usuario", user, ":")
                    for name in keypair_names:
                        print("- Nombre del Keypair:", name)

                return keypair_names
        else:
            print("Error al listar los Keypairs:", response.status_code)
    
#Borrar keypair
    def borrarKeyPair(self,keypair_name,user):
        url = f"{self.nova_url}/v2.1/os-keypairs/{keypair_name}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            keypair = response.json().get('keypair', [])

            if keypair['user_id'] == user and keypair['name'] == keypair_name:
                url_keypair = f"{url}"
                response_borrar = requests.delete(url_keypair, headers=self.headers)
                if response_borrar.status_code == 202:
                    print("Keypair eliminado exitosamente")
                else:
                    print("Error al eliminar el Keypair:", response_borrar.status_code)
                return
        else:
            print("No se encontró el Keypair especificado")

#Obtener ID de keypair
    def obtenerIDKeyPair(self,keypair):
        url = f"{self.nova_url}/v2.1/os-keypairs"
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
    def crearSecurityGroup(self,name,descripcion,IdProject):
        url = f"{self.nova_url}/v2.1/os-security-groups"
        data = {
            'security_group': {
                'name': name,
                'description': descripcion
            }
        }

        # Obtener el token específico del proyecto
        token = self.get_token_project(IdProject)

        # Verificar si se obtuvo el token correctamente
        if token is None:
            print("Error al obtener el token del proyecto.")

        # Establecer el encabezado con el token
        self.headers_security = {
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        }

        response = requests.post(url, json=data, headers=self.headers_security)

        if response.status_code == 200:
            security_group = response.json().get('security_group', {})
            print("Grupo de seguridad creado exitosamente:", security_group['name'])
        else:
            print("Error al crear el Grupo de seguridad:", response.status_code)
    
#Listar securitygroup
    def listarSecurityGroup(self,IdProject):
        token_project = self.get_token_project(IdProject)  # Obtener el token del proyecto utilizando el método get_token_project
        self.headers_security = {
            'Content-Type': 'application/json',
            'X-Auth-Token': token_project
        }
        url = f"{self.nova_url}/v2.1/os-security-groups"
        response = requests.get(url, headers=self.headers_security)
    

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
    def editarSecurityGroup(self,name,nuevoname,descripcion,IdProject):
        id_security=self.obtenerIDSecurityGroup(name,IdProject)

        if id_security==None:
            print("No existe el Grupo de seguridad especificado")
        else:
            url_editar = f"{self.nova_url}/v2.1/os-security-groups/{id_security}"
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

       
    
#Eliminar securitygroup
    def eliminarSecurityGroup(self,name,IdProject):
        id_security=self.obtenerIDSecurityGroup(name,IdProject)

        if id_security==None:
            print("No existe el Grupo de seguridad especificado")
        else:

            url_eliminar = f"{self.nova_url}/v2.1/os-security-groups/{id_security}"
            #response = requests.get(url, headers=self.headers)

            #if response.status_code == 200:
            #    security_groups = response.json().get('security_groups', [])
            #    for sg in security_groups:
            #        if sg['name'] == name:
                        #url_eliminar = f"{url}/{sg['id']}"
            response_eliminar = requests.delete(url_eliminar, headers=self.headers)
            if response_eliminar.status_code == 202:
                print("Grupo de seguridad eliminado exitosamente")
            else:
                print("Error al eliminar el Grupo de seguridad:", response_eliminar.status_code)
                print("Lalalala")
            return
    


#Obtener ID de securitygroup
    def obtenerIDSecurityGroup(self,securitygroup,IdProject):
        token_project1 = self.get_token_project(IdProject)  # Obtener el token del proyecto utilizando el método get_token_project
        self.headers_security1 = {
            'Content-Type': 'application/json',
            'X-Auth-Token': token_project1
        }
        url = f"{self.nova_url}/v2.1/os-security-groups"
        response = requests.get(url, headers=self.headers_security1)
        

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            for sg in security_groups:
                if sg['name'] == securitygroup:
                    print("ID del Grupo de seguridad:", sg['id'])
                    return sg['id']
            #print("No se encontró el Grupo de seguridad especificado")
            return None
        else:
            print("Error al obtener el ID del Grupo de seguridad:", response.status_code)
            print("Lalalala3")
    
#Agregar regla
    def agregarRegla(self,nombre,protocol_ip,from_port,dest_port,cidr,IdProject):
        token_project_rule = self.get_token_project(IdProject)  # Obtener el token del proyecto utilizando el método get_token_project
        self.headers_security_rule = {
            'Content-Type': 'application/json',
            'X-Auth-Token': token_project_rule
        }

        id_security=self.obtenerIDSecurityGroup(nombre,IdProject)

        url = f"{self.nova_url}/v2.1/os-security-group-rules"
        data = {
            'security_group_rule': {
                'parent_group_id': id_security,
                'ip_protocol': protocol_ip,
                'from_port': from_port,
                'to_port': dest_port,
                'cidr': cidr
            }
        }
        response = requests.post(url, json=data, headers=self.headers_security_rule)
        if response.status_code == 200:
            security_group_rule = response.json().get('security_group_rule', {})
            print("Regla de seguridad agregada exitosamente:")
            print("Nombre del grupo de seguridad:", nombre)
            print("Protocolo:", security_group_rule['ip_protocol'])
            print("Puerto origen:", security_group_rule['from_port'])
            print("Puerto destino:", security_group_rule['to_port'])
            print("CIDR:", security_group_rule['ip_range']['cidr'])
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
