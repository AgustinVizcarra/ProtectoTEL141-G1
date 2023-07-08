########################################## NOVA ##################################################
import requests
from Glance import GlanceClient
from Neutron import NeutronClient
import json
import paramiko
import os
import ipaddress
from funcioncitas import validar_direccion_ip2
##########FLAVOR###########
class NovaClient(object):
    def __init__(self, auth_token,username, password):
        self.auth_url = "http://10.20.12.188:5000/v3"
        self.auth_token = auth_token
        self.username = username
        self.password = password
        self.IdProject = None  # Agregar propiedad IdProject
        self.nova_url = "http://10.20.12.188:8774"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }
        self.providerNetworkID = "794ca462-47ec-4f90-8d1e-8be57004378a"
   
    def list_flavors(self):
        url=f"{self.nova_url}/v2.1/flavors"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            flavors = response.json().get('flavors', [])
            flavor_info = []
            for flavor in flavors:
                flavorcito=self.obtenerDetallesFlavor(flavor['id'])
                flavor_info.append([flavorcito['flavor']['id'], flavorcito['flavor']['name'], flavorcito['flavor']['ram'], flavorcito['flavor']['disk'], flavorcito['flavor']['vcpus']])
            return flavor_info
        else:
            raise Exception('Error al listar los flavors. Código de estado: {}'.format(response.status_code))

    def create_flavor(self, name, ram, vcpus, disk):
        url=f"{self.nova_url}/v2.1/flavors"
        

        while True:
            verificar=self.verificarFlavor(name)

            if verificar is True:

                flavor_data = {
                    'flavor': {
                        'name': name,
                        'ram': ram,
                        'vcpus': vcpus,
                        'disk': disk
                    }
                }
            
                response = requests.post(url, json=flavor_data, headers=self.headers)

                if response.status_code == 200:
                    flavor = response.json()['flavor']
                    print("[*] Flavor creado exitosamente")
                    return flavor
                else:
                    raise Exception('Failed to create flavor. Status code: {}'.format(response.status_code))
            else:
                name = input("Por favor, introduce un nombre diferente para el flavor: ")

    def get_flavor(self, flavor_id):
        response = requests.get(self.nova_url + '/flavors/{}'.format(flavor_id), headers=self.headers)

        if response.status_code == 200:
            flavor = response.json()['flavor']
            return flavor
        else:
            raise Exception('Failed to get flavor. Status code: {}'.format(response.status_code))

    def update_flavor(self,new_name, new_ram, new_vcpus, new_disk):

        flavor_id=self.obtenerIdFlavor(new_name)



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

    def delete_flavor(self, name):
        flavor_id=self.obtenerIdFlavor(name)
        
        if flavor_id is not None:
            url = f"{self.nova_url}/v2.1/flavors/{flavor_id}"
            response = requests.delete(url, headers=self.headers)
            

            if response.status_code == 202:
                print("[*] Flavoy eliminado exitosamente\n")
                return True
            else:
                print("El flavor que intenta borrar no existe")
                

    def obtenerDetallesFlavor(self, flavor_id):
        url = f"{self.nova_url}/v2.1/flavors/{flavor_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener los detalles del Flavor:", response.status_code)
    
    def verificarFlavor(self,flavor_name):
        url=f"{self.nova_url}/v2.1/flavors"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            flavors = response.json().get('flavors', [])
            # Buscar el flavor por nombre
            for flavor in flavors:
                if flavor['name'] == flavor_name:
                    print("El flavor ya existe:", flavor['name'])
                    return False
            
            return True
        else:
            print("Error al obtener los flavors:", response.status_code, response.json())

    def obtenerIdFlavor(self,flavor_name):
        url=f"{self.nova_url}/v2.1/flavors"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            flavors = response.json().get('flavors', [])
            # Buscar el flavor por nombre
            for flavor in flavors:
                if flavor['name'] == flavor_name:
                    flavor_id=flavor['id']
                    return flavor_id
            return None
        else:
            print("Error al obtener los flavors:", response.status_code, response.json())
        


##########KEYPAIR###########
#Crear Keypair
    def crearKeyPair(self, name,ruta):
        url = f"{self.nova_url}/v2/os-keypairs"
        
        
        while True:
            
            data = {
                'keypair': {
                    'name': name,
                    #'user_id': user_id
                }
            }

            
            response = requests.post(url, json=data, headers=self.headers)
            

            if response.status_code == 200:
                keypair = response.json().get('keypair', {})
                keypair_name = keypair.get('name')
                keypair_key = keypair.get('public_key')
                keypair_id = keypair.get('user_id')
                print("[*] Keypair creado exitosamente\n")
                
                llave_name=keypair_name
                
                # Extraer la clave pública de la respuesta JSON
                
                public_key = keypair_key
                
                # Generar el nombre del archivo
                nombre_archivo = llave_name + "_public_key.pem"
                
                # Ruta completa al directorio de destino
                carpeta_destino = ruta #RUTA EN ESPECIFICO QUE SE LE PUEDE PEDIR AL USUARIO
                
                # Ruta completa al archivo
                ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)

                # Guardar la clave pública en un archivo
                with open(ruta_archivo, "a") as file:
                    file.write(public_key)
                    print("[*] Clave pública guardada correctamente\n")
                    
                    break
            elif response.status_code==409:
                existing_name = response.json().get('conflictingRequest', {}).get('message')
                print("[*] La llave que está intentando crear ya existe\n")
                name = input("Escoja otro nombre: ")
                if not name:
                    print("[*] Nombre inválido. Saliendo del programa\n")
                    break
            
            else:
                print("[*] Error al crear el Keypair:", response.status_code)

#Importar keypair
    def importarKeyPair(self,nombre, llave_publica):
        
        url = f"{self.nova_url}/v2/os-keypairs"
        
        data = {
            'keypair': {
                'name': nombre,
                'public_key': llave_publica
            }
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            print("[*] Par de claves creado exitosamente\n")
        else:
            print("[*] Error al crear el par de claves\n")



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
                return info
            else:
                #print("[*] No se encontró el Keypair especificado")
                return []
        else:
            print("[*] Error al obtener la información del Keypair\n")
            return []
    
#Listar keypairs
    def listarKeyPair(self,user):
        url = f"{self.nova_url}/v2.1/os-keypairs"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])
            if len(keypairs) == 0:
                #print("[*] No cuenta con ninguna keypair, por favor cree una")
                return []
            
            else:
                keypair_names = []
                for keypair in keypairs:
                    keypair_name = keypair['keypair']['name']
                    url = f"{self.nova_url}/v2.1/os-keypairs/{keypair_name}"
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 200:
                        keypair = response.json().get('keypair', [])
                        if keypair['user_id'] == user and keypair['name'] == keypair_name:
                            usuario = keypair['user_id']
                            if usuario == user:
                                keypair_names.append(keypair_name)

                if len(keypair_names) == 0:
                    #print("[*] No se encontraron keypairs para el usuario:", user)
                    return []
                
                #else:
                    #print("Keypairs del usuario:")
                    #for name in keypair_names:
                    #    print("- Nombre del Keypair:", name)

                return keypair_names
        else:
            print("[*] Error al listar los Keypairs\n")
            return []
        
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
                    print("[*] Keypair eliminado exitosamente\n")
                else:
                    print("[*] Error al eliminar el Keypair\n")
                return
        else:
            print("[*] No se encontró el Keypair especificado\n")

#Obtener ID de keypair
    def obtenerIDKeyPair(self,keypair,userId):
        url = f"{self.nova_url}/v2/os-keypairs"
        response = requests.get(url, headers=self.headers)
        #print(keypair)

        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])
            for kp in keypairs:
                if kp['keypair']['name'] == keypair:
                    #print("Nombre de la Keypair:", kp['keypair']['name'])
                    return kp['keypair']['name']
            print("No se encontró el Keypair especificado")
        else:
            print("Error al obtener el nombre de la Keypair:", response.status_code)

##########SECURITY GROUP###########
#Crear securitygroup
    def crearSecurityGroup(self,name,descripcion):
        url = f"{self.nova_url}/v2.1/os-security-groups"
        data = {
            'security_group': {
                'name': name,
                'description': descripcion
            }
        }

        # Obtener el token específico del proyecto
        #token = self.get_token_project(IdProject)

        # Verificar si se obtuvo el token correctamente
        #if token is None:
        #    print("Error al obtener el token del proyecto.")

        # Establecer el encabezado con el token
        #self.headers_security = {
        #    'Content-Type': 'application/json',
        #    'X-Auth-Token': self.auth_token
        #}

        response = requests.post(url, json=data, headers=self.headers)
    

        if response.status_code == 200:
            security_group = response.json().get('security_group', {})
            print("[*] Grupo de seguridad creado exitosamente")
        else:
            print("[*] Error al crear el Grupo de seguridad:", response.status_code)
    
#Listar securitygroup
    def listarSecurityGroup(self):
        #token_project = self.get_token_project(IdProject)  # Obtener el token del proyecto utilizando el método get_token_project
        #self.headers_security = {
        #    'Content-Type': 'application/json',
            #'X-Auth-Token': token_project
        #    'X-Auth-Token': self.auth_token
        #}
        url = f"{self.nova_url}/v2.1/os-security-groups"
        response = requests.get(url, headers=self.headers)
    
        
        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            
            if len(security_groups) == 0:
                print("[*] No se encontraron security groups")
                return []
            
            #print("Lista de Grupos de Seguridad:")
            lista_sg = []
            for sg in security_groups:
                #print("Nombre:", sg['name'])
                #print("Descripción:", sg['description'])
                #print("ID:", sg['id'])
                #print("----------")
                lista_sg.append([sg['name'], sg['description']])
            return lista_sg
        else:
            print(" [*] Error al listar los Grupos de Seguridad:", response.status_code)
            return []
    
#Editar securitygroup
    def editarSecurityGroup(self,name,nuevoname,descripcion):
        id_security,description=self.obtenerIDSecurityGroup(name)
    

        if id_security==None:
            print("[*] No existe el Grupo de seguridad especificado")
        else:
            url_editar = f"{self.nova_url}/v2.1/os-security-groups/{id_security}"
            #descripcion = None
            if descripcion is not None and nuevoname is not None:
                data = {
                    'security_group': {
                        'name': nuevoname,
                        'description': descripcion
                    }
                }

            elif nuevoname is None and descripcion is not None:

                data = {
                    'security_group': {
                        'name': name,
                        'description': descripcion
                    }
                }

            elif  descripcion is None and nuevoname is not None:

                data = {
                    'security_group': {
                        'name': nuevoname,
                        'description':description
                    }
                }

                
            #else:
            #    data = {
            #        'security_group': {
            #            'name': nuevoname,
            #            'description':''
            #        }
            #    }

              
           
                
            response_editar = requests.put(url_editar, json=data, headers=self.headers)
            if response_editar.status_code == 200:
                print("[*] Grupo de seguridad editado exitosamente")
            else:
                print("Error al editar el Grupo de seguridad:", response_editar.status_code)
            return

       
    
#Eliminar securitygroup
    def eliminarSecurityGroup(self,name):
        id_security=self.obtenerIDSecurityGroupSDK(name)
        #print(id_security)

        if id_security==None:
            print("No existe el Grupo de seguridad especificado")
        else:

            url_eliminar = f"{self.nova_url}/v2.1/os-security-groups/{id_security}"
           
            response_eliminar = requests.delete(url_eliminar, headers=self.headers)
        
        
            if response_eliminar.status_code == 202:
                print("[*] Grupo de seguridad eliminado exitosamente")
            else:
                print("[*] Error al eliminar el Grupo de seguridad")
            return
    


#Obtener ID de securitygroup para funcion menu
    def obtenerIDSecurityGroup(self,securitygroup):
        
        url = f"{self.nova_url}/v2.1/os-security-groups"
        response = requests.get(url, headers=self.headers)
        

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            for sg in security_groups:
                if sg['name'] == securitygroup:

                    return sg['id'],sg['description']
            #print("No se encontró el Grupo de seguridad especificado")
            return None
        else:
            print("Error al obtener el ID del Grupo de seguridad:", response.status_code)

#Obtener ID de securitygroup solo para SDK
    def obtenerIDSecurityGroupSDK(self,securitygroup):
        
        url = f"{self.nova_url}/v2.1/os-security-groups"
        response = requests.get(url, headers=self.headers)
        

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            for sg in security_groups:
                if sg['name'] == securitygroup:

                    return sg['id']
            #print("No se encontró el Grupo de seguridad especificado")
            return None
        else:
            print("Error al obtener el ID del Grupo de seguridad:", response.status_code)

#Listar Reglas
    def infoSecurityGroupRules(self,nombre):
        self.neutron_url = "http://10.20.12.188:9696"
        url = f"{self.neutron_url}/v2.0/security-group-rules"
        response = requests.get(url, headers=self.headers)
        id=self.obtenerIDSecurityGroupSDK(nombre)
        rules=[]
        if response.status_code == 200:
            security_group_rules = response.json().get('security_group_rules', [])
            for rule in security_group_rules:
                if rule['security_group_id'] == id:
                    rules.append([rule['id'],rule['direction'],rule['protocol'],rule['port_range_max'],rule['port_range_min']])
            return rules

    
#Agregar regla
    def agregarRegla(self,nombre,protocol_ip,from_port,dest_port,cidr):
        description='ssh'
        self.neutron_url = "http://10.20.12.188:9696"
       
        id_security=self.obtenerIDSecurityGroupSDK(nombre)

        url = f"{self.nova_url}/v2/os-security-group-rules"


        data = {
            'security_group_rule': {
                'parent_group_id': id_security,
                'direction': 'ingress',
                'ethertype': 'IPv4',
                'ip_protocol': protocol_ip,
                'description':description,
                'from_port': from_port,
                'to_port': dest_port,
                'remote_ip_prefix': cidr
                
                
            }
        }

        response = requests.post(url, json=data, headers=self.headers)
        

        if response.status_code == 200:
            security_group_rule = response.json().get('security_group_rule', {})
            print("[*] Regla de seguridad agregada exitosamente")
            #print("|-----------------------------------------------------|")
            #print("Regla de seguridad agregada exitosamente:")
            #print("Nombre del grupo de seguridad:", nombre)
            #print("Protocolo:", security_group_rule['ip_protocol'])
            #print("Puerto origen:", security_group_rule['from_port'])
            #print("Puerto destino:", security_group_rule['to_port'])
            #print("CIDR:", security_group_rule['ip_range']['cidr'])
            #print("|-----------------------------------------------------|")
        else:
            print("[*] Error al agregar la regla de seguridad:", response.status_code)

#Eliminar regla
    def eliminarRegla(self,id):

        #self.neutron_url = "http://10.20.12.188:9696"

        #id=self.obtenerIDSecurityGroupSDK(id)

        #url = f"{self.neutron_url}/v2.0/security-group-rules"
        #response = requests.get(url, headers=self.headers)
        #print(response.status_code)
        #rule_id=''
        #if response.status_code == 200:
        #    security_group_rules = response.json().get('security_group_rules', [])
        #    for rule in security_group_rules:
        #        if rule['security_group_id'] == id:
        #            print(rule)
        #            rule_id=rule['id']
                    
        url_eliminar = f"{self.nova_url}/v2.1/os-security-group-rules/{id}"
        response_eliminar = requests.delete(url_eliminar, headers=self.headers)
        

        if response_eliminar.status_code == 202:
            print("[*] Regla de seguridad eliminada exitosamente")
        else:
            print("[*] Error al eliminar la regla de seguridad:", response_eliminar.status_code)



#################MAQUINA VM (opciones)#######################
# Listar las instancias de VM
    def list_instances(self,project_id):
        response = requests.get(self.nova_url + '/v2.1/servers', headers=self.headers)

        if response.status_code == 200:
            vm_names=[]
            instances = response.json().get('servers',[])
            
            if len(instances) == 0:
                print("[*] No hay instancias creadas")
                return []
            
            for instance in instances:
                vm_names.append(instance['name'])
            return vm_names
        else:
            print("[*] Error al listar las instancias")
            return []
        
    # Crear una instancia de VM
    def create_instance(self, name, flavor_id, image_id, network_id,keypairID,securitygroupID):
        
        network_interfaces = []
        interface = {'uuid': network_id}
        network_interfaces.append(interface)


        instance_data = {
            'server': {
                'name': name,
                'flavorRef': flavor_id,
                'imageRef': image_id,
                'key_name': keypairID,
                "security_groups": [
                    {
                    "name": securitygroupID
                    }
                ],
                'networks': network_interfaces
            }
        }

        response = requests.post(self.nova_url + '/v2.1/servers', json=instance_data, headers=self.headers)

        if response.status_code == 202:
            instance = response.json()['server']
            id_instance = instance['id']
            while True:
                estado = self.get_instance_estado(id_instance)
                if estado == "active":
                    break
            print("[*] Instancia creada de manera exitosa")
            return instance
        else:
            raise Exception('Failed to create instance. Status code: {}'.format(response.status_code))
        
    # Crear una instancia de VM
    def create_instance_internet(self, name, flavor_id, image_id, network_id,keypairID,securitygroupID, SalidaInternet,AccesoInternet,listaPuertos):
        
        network_interfaces = []

        if SalidaInternet==1:
            internet="643a290f-4061-4fb1-9403-c39ae1d42693"
            interface = {'uuid': internet}
            network_interfaces.append(interface)



        interface = {'uuid': network_id}
        network_interfaces.append(interface)


        instance_data = {
            'server': {
                'name': name,
                'flavorRef': flavor_id,
                'imageRef': image_id,
                'key_name': keypairID,
                "security_groups": [
                    {
                    "name": securitygroupID
                    }
                ],
                'networks': network_interfaces
            }
        }

        response = requests.post(self.nova_url + '/v2.1/servers', json=instance_data, headers=self.headers)

        if response.status_code == 202:
            instance = response.json()['server']
            id_instance = instance['id']
            puertos={}
            puerto_http=None
            puerto_https=None
            puerto_ssh=None
            puerto_telnet=None
            while True:
                estado = self.get_instance_estado(id_instance)
                if estado == "active":
                    IP4=self.get_instance_ip(id_instance)
    
                    if SalidaInternet ==1 and AccesoInternet == 1:
                        for i in listaPuertos:
                            
                            #Uso de SSH paramiko
                            hostname = '10.20.12.188'
                            username = 'ubuntu'
                            password = 'ubuntu'
                            port = 22
                            command1 = "echo ubuntu | sudo -S ./puertos_libres.sh "
                
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            try:
                                ssh.connect(hostname, port, username, password)
                                #AL ejecutar ese comando se recibirá un puerto libre
                                stdin, stdout, stderr = ssh.exec_command(command1)
                                puerto_libre=stdout.read().decode()
                                puerto_libre=puerto_libre[:-1]
                                #print(puerto_libre)

                            
                                if i == 22:
                                    puerto_ssh = puerto_libre
                                    
                                elif i == 23:
                                    puerto_telnet = puerto_libre
                                    
                                elif i == 80:
                                    puerto_http= puerto_libre
                                elif i == 443:
                                    puerto_https = puerto_libre
                                elif i!=22 and i!=23 and i!=80 and i!=443:
                                    puertos[i]=puerto_libre
                                    

                                
                                command3=f"echo ubuntu | sudo -S ./port_forwarding_gateway.sh {puerto_libre}"+ " " + "CREAR"
                                ssh.exec_command(command3)
                                #print(i)
                                
                                #Uso de SSH paramiko
                                port = 5001
                                command2 = "echo ubuntu | sudo -S ./port_forwarding_controller.sh" + " " + str(puerto_libre) + " " + str(IP4) + " " + str(i)+ " " + "CREAR"
                                #print(command2)
                                ssh = paramiko.SSHClient()
                                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                
                                try:
                                    ssh.connect(hostname, port, username, password)

                                    #AL ejecutar ese comando se recibirá un puerto libre
                                    stdin, stdout, stderr=ssh.exec_command(command2)
                                    C2=stdout.read().decode()
                                #    print(C2)

                                except paramiko.AuthenticationException:

                                    print("Error de autenticación. Verifica las credenciales de SSH.")

                                except paramiko.SSHException as ssh_exception:

                                    print("Error de conexión SSH:", str(ssh_exception))

                                finally:

                                    ssh.close()
                            
                            except paramiko.AuthenticationException:

                                print("Error de autenticación. Verifica las credenciales de SSH.")

                            except paramiko.SSHException as ssh_exception:

                                print("Error de conexión SSH:", str(ssh_exception))

                            finally:

                                ssh.close()
                        
                        #self.ssh_connect(hostname, username, password, port,command)
                        #self.ssh_connect(hostname,username,password,port,command)
                        #thread = threading.Thread(target=subprocess.call(command, shell=True), args=(command,))
                        #thread.start()

                    elif SalidaInternet==0 and AccesoInternet==1:
                        print("Debe tener Salida a la red (Publica)")
                    break
            if puerto_ssh !=None:
                print("[*] Comando para acceder desde Internet a la VM con ssh: ssh {usuario}@10.20.12.188 -p "+str(puerto_ssh))
            if puerto_telnet !=None:
                print("[*] Puerto para acceder desde Internet a la VM con Telnet: "+str(puerto_telnet))
            if puerto_http !=None:
                print("[*] Puerto para acceder desde Internet a la VM con http: "+str(puerto_http))
            if puerto_https !=None:
                print("[*] Puerto para acceder desde Internet a la VM con https: "+str(puerto_https))
            if puertos !=None:
                print("[*] Puertos habilitados para las conexiones que desea realizar "+str(puertos))    
            print("[*] Instancia creada de manera exitosa")
            return instance
        else:
            raise Exception('Failed to create instance. Status code: {}'.format(response.status_code))
        
    # Obtener detalles de una instancia de VM
    def get_instance(self, server_id):
        url = f"{self.nova_url}/v2.1/servers/{server_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            server_details = response.json().get('server', {})
            print("Detalles del servidor:")
            print("Nombre:", server_details.get('name'))
            print("Flavor:")
            flavor = server_details.get('flavor', {})
            id_flavor=flavor.get('id')
            self.obtenerDetallesFlavor(id_flavor)

            print("Imagen:")
            image = server_details.get('image', {})
            id_image=image.get('id') 

            glance = GlanceClient(self.UserID,self.ProjectName,self.token)  # Crear una instancia de la clase GlanceClass
            glance.obtenerDetallesImagen(id_image)

            print("Llave:")
            keypair = server_details.get('key_name')
            print("  - Nombre:", keypair)
            print("Red:")
            addresses = server_details.get('addresses', {})
            
            for network, ip_list in addresses.items():
                print(f"  - {network}:")
                for ip in ip_list:
                    print(f"    - IP: {ip.get('addr')}")
        else:
            print("Error al obtener los detalles del servidor:", response.status_code)

    # Obtener detalles de una IP de VM
    def get_instance_ip(self, server_id):
        url = f"{self.nova_url}/v2.1/servers/{server_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            server_details = response.json().get('server', {})
            addresses = server_details.get('addresses', {})
            for network, ip_list in addresses.items():
                for ip in ip_list:
                    if validar_direccion_ip2(ip.get('addr')):
                        IP=ip.get('addr')
                        return IP

    
        else:
            print("Error al obtener los detalles del servidor:", response.status_code)
            
    # Obtener ESTADO de una instancia de VM
    def get_instance_estado(self, server_id):
        url = f"{self.nova_url}/v2.1/servers/{server_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            server_details = response.json()
            return server_details['server']['OS-EXT-STS:vm_state']
        else:
            print("[*] Error al obtener el estado del servidor:", response.status_code)

    # Actualizar una instancia de VM
    def update_instance(self, name, newname, descripcion,project):
        instance_id=self.get_instance_id(name)
        instance_data = {
            'server': {
                'name': newname
            }
        }
        response = requests.put(self.nova_url + '/v2.1/servers/{}'.format(instance_id), json=instance_data, headers=self.headers)

        if response.status_code == 200:
            instance = response.json()['server']
            return instance
        else:
            raise Exception('Failed to update instance. Status code: {}'.format(response.status_code))

    # Eliminar una instancia de VM
    def delete_instance(self, name):
        instance_id=self.get_instance_id(name)
        ipv4=self.get_instance_ip(instance_id)
        response = requests.delete(self.nova_url + '/v2.1/servers/{}'.format(instance_id), headers=self.headers)
        
        
        if response.status_code == 204:
            while True:
                #Uso de SSH paramiko
                hostname = '10.20.12.188'
                username = 'ubuntu'
                password = 'ubuntu'
                port = 5001
                

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(hostname, port, username, password)
                    command1 = "echo ubuntu | sudo -S ./filter_iptables_ip.sh" + " " + str(ipv4)
                    #AL ejecutar ese comando se recibirá un puerto libre
                    stdin, stdout, stderr = ssh.exec_command(command1)
                    #print(command1)
                    puerto_libre=stdout.read().decode().replace("[sudo] password for ubuntu: ","")
                    #print(puerto_libre)
                    if puerto_libre == '\n':
                        break
                    else:
                        puerto_libre=puerto_libre.split(" ")
                    #print(puerto_libre)
                    
                    puerto_libre[1] = puerto_libre[1].replace("\n","")
                    #print(puerto_libre)
            
                    
                    command2 = "echo ubuntu | sudo -S ./port_forwarding_controller.sh" + " " + str(puerto_libre[0]) + " " + str(ipv4) + " " + str(puerto_libre[1])+ " " + "DELETE"
                    #print(command2)
                    ssh.exec_command(command2)

                    #Uso de SSH paramiko
                    port = 22
                    command3=f"echo ubuntu | sudo -S ./port_forwarding_gateway.sh {puerto_libre[0]}"+ " " + "DELETE"
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    
                    try:
                        ssh.connect(hostname, port, username, password)

                        #AL ejecutar ese comando se recibirá un puerto libre
                        stdin, stdout, stderr=ssh.exec_command(command3)
                        #C2=stdout.read().decode()
                        #ssh.exec_command(command3)
                    #    print(command3)

                    except paramiko.AuthenticationException:

                        print("Error de autenticación. Verifica las credenciales de SSH.")

                    except paramiko.SSHException as ssh_exception:

                        print("Error de conexión SSH:", str(ssh_exception))

                    finally:

                        ssh.close()
            
                
                except paramiko.AuthenticationException:

                    print("Error de autenticación. Verifica las credenciales de SSH.")

                except paramiko.SSHException as ssh_exception:

                    print("Error de conexión SSH:", str(ssh_exception))

                finally:

                    ssh.close()

            
        else:
            raise Exception('Failed to delete instance. Status code: {}'.format(response.status_code))
    
    #  Obtener la cantida de nodos que tiene una red provider
    def cantidadNodos(self,project_id,network_id):
        pass
    
    
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
        response = requests.post(self.nova_url + '/v2.1/servers/{}/action'.format(instance_id), json=action_data, headers=self.headers)

        if response.status_code == 202:
            return True
        else:
            raise Exception('Failed to reboot instance. Status code: {}'.format(response.status_code))
        
    def get_instance_id(self, vm_name):
        url = f"{self.nova_url}/v2.1/servers"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            servers = response.json().get('servers', [])
            for server in servers:
                if server['name'] == vm_name:
                    return server['id']
            print("No se encontró la VM especificada")
        else:
            print("Error al obtener el ID de la VM:", response.status_code)

    # Crear una instancia con múltiples interfaces de red
    def create_instance_with_multiple_interfaces(self, nombre, flavor_id, imagen_id, keypair_id, security_group_id, interfaces):
        
        network_interfaces = []
        for interface in interfaces:
            network_id = interface['network_id']
            port_id = interface['port_id']
            interface_data = {
                'net-id': network_id,
                'port-id': port_id
            }
            network_interfaces.append(interface_data)

        instance_data = {
            'server':{
                
            
                'name': nombre,
                'flavorRef': flavor_id,
                'imageRef': imagen_id,
                'key_name': keypair_id,
                'security_groups': [{'name': security_group_id}],
                'networks': network_interfaces
            }
        }
            

        url = f"{self.nova_url}/v2.1/servers"
        response = requests.post(url, headers=self.headers, json=instance_data)

        if response.status_code == 202:
            instance_id = response.json()['server']['id']
            return instance_id
        else:
            print("Error al crear la instancia:", response.status_code)
            return None


    # Crear una instancia con varias redes
    
    def create_instance_with_multiple_networks(self, nombre, flavor_id, imagen_id, keypair_id, security_group_id, networks):

        network_interfaces = []
        SalidaInternet=1
        AccesoInternet=1
        Listapuertos=[22]
        internet="643a290f-4061-4fb1-9403-c39ae1d42693"
        interface = {'uuid': internet}
        network_interfaces.append(interface)

        for network_id in networks:
            interface = {'uuid': network_id}
            network_interfaces.append(interface)

        instance_data = {
            'server':{
                
                'name': nombre,
                'flavorRef': flavor_id,
                'imageRef': imagen_id,
                'key_name': keypair_id,
                'security_groups': [{'name': security_group_id}],
                'networks': network_interfaces
            }
        }

       

        url = f"{self.nova_url}/v2.1/servers"
        response = requests.post(url, headers=self.headers, json=instance_data)
        

        if response.status_code == 202:
            instance_id = response.json()['server']['id']
            while True:
                estado = self.get_instance_estado(instance_id)
                if estado == "active":
                    IP4=self.get_instance_ip(instance_id)
                    if SalidaInternet ==1 and AccesoInternet == 1:
                        for i in Listapuertos:
                            #Uso de SSH paramiko
                            hostname = '10.20.12.188'
                            username = 'ubuntu'
                            password = 'ubuntu'
                            port = 22
                            command1 = "echo ubuntu | sudo -S ./puertos_libres.sh "
                
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            try:
                                ssh.connect(hostname, port, username, password)
                                #AL ejecutar ese comando se recibirá un puerto libre
                                stdin, stdout, stderr = ssh.exec_command(command1)
                                puerto_libre=stdout.read().decode()
                                puerto_libre=puerto_libre[:-1]
                                #print(puerto_libre)
                                
                                command3=f"echo ubuntu | sudo -S ./port_forwarding_gateway.sh {puerto_libre}"+ " " + "CREAR"
                                ssh.exec_command(command3)
                                #print(i)
                                
                                #Uso de SSH paramiko
                                port = 5001
                                command2 = "echo ubuntu | sudo -S ./port_forwarding_controller.sh" + " " + str(puerto_libre) + " " + str(IP4) + " " + str(i)+ " " + "CREAR"
                                #print(command2)
                                ssh = paramiko.SSHClient()
                                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                
                                try:
                                    ssh.connect(hostname, port, username, password)

                                    #AL ejecutar ese comando se recibirá un puerto libre
                                    stdin, stdout, stderr=ssh.exec_command(command2)
                                    C2=stdout.read().decode()
                                #    print(C2)

                                except paramiko.AuthenticationException:

                                    print("Error de autenticación. Verifica las credenciales de SSH.")

                                except paramiko.SSHException as ssh_exception:

                                    print("Error de conexión SSH:", str(ssh_exception))

                                finally:

                                    ssh.close()
                            
                            except paramiko.AuthenticationException:

                                print("Error de autenticación. Verifica las credenciales de SSH.")

                            except paramiko.SSHException as ssh_exception:

                                print("Error de conexión SSH:", str(ssh_exception))

                            finally:

                                ssh.close()
                        
                        #self.ssh_connect(hostname, username, password, port,command)
                        #self.ssh_connect(hostname,username,password,port,command)
                        #thread = threading.Thread(target=subprocess.call(command, shell=True), args=(command,))
                        #thread.start()

                    elif SalidaInternet==0 and AccesoInternet==1:
                        print("Debe tener Salida a la red (Publica)")
                    break
            print("[*] Comando para acceder desde Internet a la VM: ssh {usuario}@10.20.12.188 -p "+str(puerto_libre))
            print("[*] Instancia creada de manera exitosa")

            return instance_id
        else:
            print("Error al crear la instancia:", response.status_code)
            return None
        

    #Agregar una interfaz    
    def agregar_interfaz_to_VM(self, vm_id, network_id):
        
        url = f"{self.nova_url}/v2.1/servers/{vm_id}/os-interface"
        data = {
            "interfaceAttachment": {
                "net_id": network_id
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        

        if response.status_code == 200:
            print("Interfaz añadida correctamente.")
        else:
            print("Error al añadir la interfaz:", response.status_code)
            
    #Agregar una interfaz a la VM br_provider
    def agregar_interfaz_to_VM_br_provider(self, vm_id):
        url = f"{self.nova_url}/v2.1/servers/{vm_id}/os-interface"
        data = {
            "interfaceAttachment": {
                "net_id": self.providerNetworkID
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            #port_id = response.json()['interfaceAttachment']['port_id']
            #print(port_id)
            #url2 = f"{self.nova_url}/v2.1/servers/{vm_id}/os-interface/{port_id}"
            #response = requests.put(url2, headers=self.headers, json={'interfaceAttachment': {'port_state': 'ACTIVE'}})
            #print(response.json())
            #if response.status_code == 200:
            #    print('[*] La interfaz se ha establecido como ACTIVA correctamente.')   
            print("[*] Interfaz añadida correctamente.")
        else:
            print("[*] Error al añadir la interfaz:", response.status_code)

#MIGRAR

    #Migracion en Frio    
    def cold_migrate_instance(self, id, target_host):
        
        #instance_id=self.get_instance_id(name)
        url = f"{self.nova_url}/servers/{id}/action"

        data = {
            "os-migrateLive": {
                "host": target_host,
                "block_migration": False,
                "disk_over_commit": False
            }
        }
        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 202:
            print("Migración en frío iniciada correctamente.")
        else:
            print("Error al iniciar la migración en frío:", response.status_code)
        return response.status_code


    #Migracion en Caliente
    def live_migrate_instance(self, name, target_host):
        instance_id=self.get_instance_id(name)
        url = f"{self.nova_url}/servers/{instance_id}/action"
        data = {
            "os-migrateLive": {
                "host": target_host,
                "block_migration": True,
                "disk_over_commit": False
            }
        }
        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 202:
            print("Migración en caliente iniciada correctamente.")
        else:
            print("Error al iniciar la migración en caliente:", response.status_code)
        return response.status_code


#Borrar Componentes del proyecto (Slice)

    def delete_all_vms_and_networks(self):
        # Eliminar todas las instancias
        response = requests.get(self.nova_url + '/v2.1/servers', headers=self.headers)

        if response.status_code == 200:
            instances = response.json().get('servers', [])

            if len(instances) == 0:
                print("[*] No hay instancias creadas")
            else:
                for instance in instances:
                    instance_id = instance['id']
                    delete_response = requests.delete(self.nova_url + f'/v2.1/servers/{instance_id}', headers=self.headers)
                    if delete_response.status_code == 204:
                        print(f"Instancia {instance_id} eliminada con éxito")
                    else:
                        print(f"Error al eliminar la instancia {instance_id}")

        else:
            print("[*] Error al listar las instancias")

        # Eliminar todas las redes
        response = requests.get(self.neutron_url + '/v2.0/networks', headers=self.headers)

        if response.status_code == 200:
            networks = response.json().get('networks', [])

            if len(networks) == 0:
                print("[*] No hay redes creadas")
            else:
                for network in networks:
                    network_id = network['id']
                    delete_response = requests.delete(self.neutron_url + f'/v2.0/networks/{network_id}', headers=self.headers)
                    if delete_response.status_code == 204:
                        print(f"Red {network_id} eliminada con éxito")
                    else:
                        print(f"Error al eliminar la red {network_id}")

        else:
            print("[*] Error al listar las redes")

        # Eliminar todos los grupos de seguridad
        response = requests.get(self.nova_url + '/v2.1/os-security-groups', headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])

            if len(security_groups) == 0:
                print("[*] No hay grupos de seguridad creados")
            else:
                for security_group in security_groups:
                    security_group_id = security_group['id']
                    delete_response = requests.delete(self.neutron_url + f'/v2.0/security-groups/{security_group_id}', headers=self.headers)
                    if delete_response.status_code == 204:
                        print(f"Grupo de seguridad {security_group_id} eliminado con éxito")
                    else:
                        print(f"Error al eliminar el grupo de seguridad {security_group_id}")

        else:
            print("[*] Error al listar los grupos de seguridad")

        # Eliminar todos los keypairs
        response = requests.get(self.nova_url + '/v2.1/os-keypairs', headers=self.headers)

        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])

            if len(keypairs) == 0:
                print("[*] No hay keypairs creados")
            else:
                for keypair in keypairs:
                    keypair_name = keypair['name']
                    delete_response = requests.delete(self.nova_url + f'/v2.1/os-keypairs/{keypair_name}', headers=self.headers)
                    if delete_response.status_code == 202:
                        print(f"Keypair {keypair_name} eliminado con éxito")
                    else:
                        print(f"Error al eliminar el keypair {keypair_name}")

        else:
            print("[*] Error al listar los keypairs")

