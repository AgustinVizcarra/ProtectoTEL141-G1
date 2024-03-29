###########################################NEUTRON###############################################
import requests
import random
import paramiko
import re
import subprocess
import threading
###############RED################## 

vlan_tag = random.randint(1, 10000)

class NeutronClient(object):

    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.neutron_url = "http://10.20.12.188:9696/v2.0/"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }
        self.NetworkID = None
        
    def getNetworkID(self):
        return self.NetworkID
    
    def getNetworkIDbyName(self, name_red):
        url = f"{self.neutron_url}/networks"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            networks = response.json().get('networks', [])
            for network in networks:
                if network['name'] == name_red:
                    return network['id']
            return None
        else:
            print("Error al obtener la red:", response.status_code)
            return None
    
    def setNetworkID(self,NetworkID):
        self.NetworkID = NetworkID
        
    def list_networks(self,project_id):
        url = f"{self.neutron_url}/networks?project_id={project_id}"
        response = requests.get(url, headers=self.headers)
        informacion=[]
        if response.status_code == 200:
            networks = response.json()['networks']
            for network in networks:
                subnet_id = network.get('subnets', [''])[0]
                # Obtener información de la subred
                subnet_url = f"{self.neutron_url}/subnets/{subnet_id}"
                subnet_response = requests.get(subnet_url, headers=self.headers)
                if subnet_response.status_code == 200:
                    subnet = subnet_response.json().get('subnet', {})
                    subnet_info = {
                        'id': subnet.get('id', ''),
                        'name': subnet.get('name', ''),
                        'cidr': subnet.get('cidr', ''),
                        'gateway_ip': subnet.get('gateway_ip', '')
                    }

                    # Imprimir la información de la red y subred
        
                    informacion.append([network['name'],
                                        subnet_info['cidr'],
                                        subnet_info['gateway_ip'],network['id']])
            
            return informacion
        else:
            raise Exception('Failed to list networks. Status code: {}'.format(response.status_code))

    #Funcion que permite crear la redprovider
    def create_network(self,red,subred,cidr):
        vlan_tag = random.randint(1, 800)
        
        
        network_data = {
            'network': {
                "admin_state_up": True,
                "name": red,
                "shared": False,
                "provider:physical_network": "provider",
                "provider:network_type": "vlan",
                "provider:segmentation_id": vlan_tag
                #'project_id': project
            }
        }
        
        
        response = requests.post(self.neutron_url + 'networks', json=network_data, headers=self.headers)

        cidr_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$')
        

        if response.status_code == 201:
            network_id = response.json()['network']['id']

            # Mientras el CIDR sea '0.0.0.0/0', seguir pidiendo un nuevo CIDR
            while cidr == '0.0.0.0/0' or not cidr_regex.match(cidr):
                cidr = input("Por favor, introduce un CIDR válido de la forma 'x.x.x.x/x' que no sea '0.0.0.0/0': ")
            
            subnet_data = {
                'subnet': {
                    'network_id': network_id,
                    "name": subred,
                    "ip_version": 4,
                    'cidr': cidr,
                   
                }
            }
            
            
            response = requests.post(self.neutron_url + 'subnets', json=subnet_data, headers=self.headers)
            if response.status_code == 201:
                self.NetworkID = network_id
                
                '''#Uso de SSH paramiko
                hostname = '10.20.12.188'
                username = 'ubuntu'
                password = 'ubuntu'
                port = 5001
                command = "echo ubuntu | sudo -S ./configurar_vlan.sh "+str(vlan_tag)+" "+str(cidr)+" "+str(gateway)+" "+"CREAR"
                print(command)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(hostname, port, username, password)
                    print("Conexión SSH exitosa.")
                    # Realiza operaciones en la máquina virtual a través de la conexión SSH

                    # Ejemplo: Ejecutar un comando en la máquina virtual
                    #stdin, stdout, stderr = ssh.exec_command(command)
                    
                    # Cambiar al usuario root
                    #stdin, stdout, stderr = ssh.exec_command("sudo -i")
    
                    # Enviar la contraseña de root
                    #stdin.write("ubuntu" + '\n')
                    #stdin.flush()
                    #ssh.exec_command('echo' 'Hello world')
                    ssh.exec_command(command)
                    #print(stdout.read().decode())
                    
                except paramiko.AuthenticationException:

                    print("Error de autenticación. Verifica las credenciales de SSH.")

                except paramiko.SSHException as ssh_exception:

                    print("Error de conexión SSH:", str(ssh_exception))

                finally:

                    ssh.close()
                
                #self.ssh_connect(hostname, username, password, port,command)
                #self.ssh_connect(hostname,username,password,port,command)
                #thread = threading.Thread(target=subprocess.call(command, shell=True), args=(command,))
                #thread.start()'''
                
                print("[*] Red creada exitosamente\n")
                return True
            else:
                print("[*] Ha ocurrido un error al crear la red\n")
                return False
        else:
            print("[*] Ha ocurrido un error al crear la red\n")
            return False


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

    def delete_network(self,name ,project_id):
        # Primero, obtener la lista de todas las redes del proyecto
        url = self.neutron_url + 'networks?project_id=' + project_id
        response = requests.get(url, headers=self.headers)
        

        if response.status_code == 200:
            networks = response.json().get('networks', [])
            for network in networks:
                if network['name']==name:
                    network_id = network['id']  # Obtener el ID de la red
                    url_eliminar=self.neutron_url + 'networks/' + network_id
                    response = requests.delete(url_eliminar, headers=self.headers)
                    if response.status_code==204:
                        print("[*] La red",network['name'],"se ha eliminado exitosamente")
                        
                    elif response.status_code==409:
                        print("[*] La red", network['name'], "posee elementos en uso" )
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
        print(response.json())
        return False
    
    #Funcion que devuelve la info de una red y su subred
    def infoRedProvider(self, project_id):
        url = f"{self.neutron_url}/networks?project_id={project_id}"
        response = requests.get(url, headers=self.headers)
        información=[]

        if response.status_code == 200:
            networks = response.json().get('networks', [''])
            
            for network in networks :
                
                
                subnet_id = network.get('subnets', [''])[0]
                #subnet_id = subnet_id.strip("[]")
                
                # Obtener información de la subred
            
                subnet_url = f"{self.neutron_url}/subnets/{subnet_id}"
                
                subnet_response = requests.get(subnet_url, headers=self.headers)
            
                
                if subnet_response.status_code == 200:
                    subnet = subnet_response.json().get('subnet', {})
                    subnet_info = {
                        'id': subnet.get('id', ''),
                        'name': subnet.get('name', ''),
                        'cidr': subnet.get('cidr', ''),
                        'gateway_ip': subnet.get('gateway_ip', '')
                    }

                    # Imprimir la información de la red y subred

                    información.append([network['name'],
                                        network['description'],
                                        network['created_at'],
                                        subnet_info['cidr'],
                                        subnet_info['gateway_ip']])

                else:
                    print(" [*] Error al obtener la información de la subred:", subnet_response.status_code)
                    return []
        else:
            print(" [*] Error al obtener la información de la red y subred:", response.status_code)
            return []
            
        return información
            
       
    #Funcion que permite crear la redprovider para la topology
    def create_network_topology(self, red,subred,cidr):

        
        network_data = {
            'network': {
                
                "admin_state_up": True,
                "name": red,
                "shared": False,
                "provider:physical_network": "provider",
                "provider:network_type": "vlan",
                "provider:segmentation_id": random.randint(1, 1000)
                
            }
        }
        
        response = requests.post(self.neutron_url + 'networks', json=network_data, headers=self.headers)
        

        cidr_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$')
        

        if response.status_code == 201:
            network_id = response.json()['network']['id']

            # Mientras el CIDR sea '0.0.0.0/0', seguir pidiendo un nuevo CIDR
            while cidr == '0.0.0.0/0' or not cidr_regex.match(cidr):
                cidr = input("Por favor, introduce un CIDR válido de la forma 'x.x.x.x/x' que no sea '0.0.0.0/0': ")
            
            subnet_data = {
                'subnet': {
                    'network_id': network_id,
                    "name": subred,
                    "ip_version": 4,
                    'cidr': cidr,
                    #'gateway_ip': gateway
                }
            }
            
            response = requests.post(self.neutron_url + 'subnets', json=subnet_data, headers=self.headers)
            if response.status_code == 201:
                self.NetworkID = network_id
                print("[*] Red Provider creada exitosamente\n")
                return True
            else:
                print("[*] Ha ocurrido un error al crear la redProvider\n")
                return False
        else:
            print("[*] Ha ocurrido un error al crear la redProvider\n")
            return False
        

    
        
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

    def obtener_puerto_por_instancia(self,instancia_id):

        url = f"{self.neutron_url}/ports?device_id={instancia_id}"
        
        response = requests.get(url, headers=self.headers)
        

        if response.status_code == 200:
            puertos = response.json()['ports']
            if puertos:
                puerto = puertos[0]  # Tomamos el primer puerto asociado a la instancia
                print("ID del puerto:", puerto['id'])
                print("Estado del administrador:", puerto['admin_state_up'])
                print("Enlace: Tipo VNIC:", puerto['binding:vnic_type'])
                print("Puerto de seguridad:", puerto['port_security_enabled'])
            else:
                print("No se encontró ningún puerto asociado a la instancia.")
        else:
            print("Error al obtener los puertos:", response.status_code, response.text)

    def getNetworkIDbyName(self, name_red):
        url = f"{self.neutron_url}/networks"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            networks = response.json().get('networks', [])
            for network in networks:
                if network['name'] == name_red:
                    return network['id']
            return None
        else:
            print("Error al obtener la red:", response.status_code)
            return None
        
# SSH PARAMIKO
    def ssh_connect(hostname,username,password,port,command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(hostname, port, username, password)
            print("Conexión SSH exitosa.")
            # Realiza operaciones en la máquina virtual a través de la conexión SSH

            # Ejemplo: Ejecutar un comando en la máquina virtual
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            
        except paramiko.AuthenticationException:
            print("Error de autenticación. Verifica las credenciales de SSH.")
        except paramiko.SSHException as ssh_exception:
            print("Error de conexión SSH:", str(ssh_exception))
        except paramiko.ChannelException as channel_exception:
            print("Error de canal SSH:", str(channel_exception))
        finally:
            ssh.close()

    
