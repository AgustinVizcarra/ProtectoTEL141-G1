import requests
import time

class KeystoneAuth(object):
    def __init__(self,username, password):
        self.auth_url = "http://10.20.12.39:5000/v3"
        self.username = username
        self.password = password
        self.token = None
        self.headers = {'Content-Type': 'application/json'}

    #Obtener TOKEN
    def get_token(self):
        auth_data = {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': self.username,
                            'password': self.password,
                            'domain': {'id': 'default'}
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "id": "default"
                        },
                        "name": "admin"
                    }
                }
            }
        }
        response = requests.post(self.auth_url+"/auth/tokens",
                                 json=auth_data,
                                 headers=self.headers)

        if response.status_code == 201:
            self.token = response.headers['X-Subject-Token']
            print("[*]La solicitud se completó correctamente")
            
        elif response.status_code == 401:
            print("[*]Error de autorización, verifique credenciales")
            
        else:
            print("[*]Se produjo un error. Codigo de estado;", response.status_code)

        return self.token
    
    
    #Crear rol
    def crear_Rol(self, name, description):
        roles = {
            'role': {
                'name': name,
                'description': description
            }
        }
        response = requests.post(self.auth_url + '/roles',
                                 json=roles,
                                headers={'Content-Type': 'application/json',
                                          'X-Auth-Token': self.token})
        
        if response.status_code == 201:
            print("[*]Rol creado exitosamente")
        else:
            print("[*]Error al crear el rol: {}".format(response.text))

        return response.json()




    #Crear Usuario
    def crear_usuario(self, username, password, email, rol_name):
        # Obtener el ID del rol a asignar
        response = requests.get(self.auth_url + '/roles',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})

        role_id = None
        if response.status_code == 200:
            roles = response.json()['roles']
            for role in roles:
                if role['name'] == rol_name:
                    role_id = role['id']
                    break

        if role_id is None:
            print("[*]No se encontró el rol especificado, por lo que no se creó usuario")

        else:
            # Crear el usuario con el rol asignado
            user_data = {
                'user': {
                    'name': username,
                    'password': password,
                    'email': email,
                    'enabled': True
                }
            }
            response = requests.post(self.auth_url + '/users',
                                    json=user_data,
                                    headers={'Content-Type': 'application/json',
                                            'X-Auth-Token': self.token})

            if response.status_code == 201:
                print("[*]Usuario creado exitosamente")

                # Obtener lista de usuarios
                url='{}/users'.format(self.auth_url)
                headers={
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token}

                response=requests.get(url,headers=headers)
                user_id=None

                if response.status_code == 200:

                    users = response.json()['users']
                    for user in users:
                        if user['name'] == username:
                            user_id=user['id']
                            break

                else:
                    print('Error al obtener usuarios: {}'.format(response.text))
                

                # Obtener lista de proyectos
                url = '{}/projects'.format(self.auth_url)
                headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token
                }

                response = requests.get(url, headers=headers)
                
                project_id = None
                project_name="admin"

                if response.status_code == 200:
                    # Imprimir id y nombre de cada proyecto
                    projects = response.json()['projects']
                    for project in projects:
                        if project['name'] == project_name:
                            project_id=project['id']
                            break

                else:
                    print('Error al listar proyectos: {}'.format(response.text))
                
                # Asignar el rol al usuario
                url = "{}/projects/{}/users/{}/roles/{}".format(self.auth_url,project_id,user_id,role_id)
                response = requests.put(url,
                                        json={'role':{'id':role_id}},
                                        headers={'Content-Type': 'application/json',
                                                'X-Auth-Token': self.token})
                
                if response.status_code == 204:
                    print("[*]Rol asignado exitosamente")
                        
                else:
                    print("[*]Error al asignar el rol: {}".format(response.text))
                
            else:
                print("Error al crear el usuario: {}".format(response.text))



    #Editar usuario y Rol
    def editar_usuario(self, username, rol_name, email, password):
        # Primero, obtenemos el ID del usuario
        response = requests.get(self.auth_url + '/users?name=' + username,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})

            
        user_id = None
        #print(len(response.json()['users']))   
        if response.status_code == 200:
            users = response.json()['users']
            if len(response.json()['users'])==0:
                user_id=None
            else:
                user_id = users[0]['id']

        if user_id is None:
            print("[*]No se encontró un usuario con el nombre especificado")
                
        else:    
            url="{}/users/{}/projects".format(self.auth_url,user_id)
            response = requests.get(url,headers={'Content-Type': 'application/json','X-Auth-Token': self.token})
            proyecto=response.json()['projects']
            project=proyecto[0]
            project_id = project['id']
            # Actualizamos el rol del usuario si se especificó
            if rol_name is not None:
                # Verificar si el usuario ya tiene un rol asignado en el proyecto
                response = requests.get(self.auth_url + '/projects/' + project_id + '/users/' + user_id + '/roles',
                                        headers={'Content-Type': 'application/json',
                                                'X-Auth-Token': self.token})
                if response.status_code == 200:
                    roles = response.json()['roles']
                    for role in roles:

                        response = requests.get(self.auth_url + '/roles', headers={'Content-Type': 'application/json','X-Auth-Token': self.token})
                       
                        if response.status_code == 200:
                            rolsitos=response.json().get('roles')
                            rol_exist=False
                            for rolsito in rolsitos:
                                if rolsito['name']==rol_name:
                                    rol_exist=True
                                    break
                            if rol_exist:
                                # Eliminar el rol anterior
                                url = self.auth_url + '/projects/' + project_id + '/users/' + user_id + '/roles/' + role['id']
                                response = requests.delete(url, headers={'X-Auth-Token': self.token})
                                if response.status_code == 204:
                                    print("[*]Rol eliminado exitosamente")
                                    
                                    '''# Obtenemos el ID del nuevo rol
                                    response = requests.get(self.auth_url + '/roles',
                                                            headers={'Content-Type': 'application/json',
                                                                    'X-Auth-Token': self.token})
                                    role_id = None 
                                    if response.status_code == 200:
                                        roles = response.json()['roles']
                                        for role in roles:
                                            #print(role['name'])
                                            if role['name'] == rol_name:
                                                role_id = role['id']
                                                break
                                                
                                    if role_id is None:
                                        print("[*]No se encontró el rol especificado")'''
                                                    
                                    '''else:'''
                                    # Actualizamos el rol del usuario
                                    url = "{}/projects/{}/users/{}/roles/{}".format(self.auth_url, project_id, user_id, rolsito['id'])
                                    response = requests.put(url,
                                                            headers={'Content-Type': 'application/json',
                                                                    'X-Auth-Token': self.token})
                                                                
                                    if response.status_code == 204:
                                        print("[*]Rol asignado exitosamente")
                                    else:
                                        print("[*]Error al asignar el rol: {}".format(response.text))
                            else:
                                print("El rol especificado no existe")
            # Actualizamos el email y/o contraseña del usuario si se especificaron
            if ((email is not None) or (password is not None)):
                user_data = {}
                if email is not None:
                    user_data['email'] = email
                if password is not None:
                    user_data['password'] = password
                url = "{}/users/{}".format(self.auth_url, user_id)
                response = requests.patch(url,
                                        headers={'Content-Type': 'application/json',
                                                'X-Auth-Token': self.token},
                                        json=user_data)
                if response.status_code == 200:
                    print("[*]Usuario actualizado exitosamente")
                else:
                    print("[*]Error al actualizar el usuario: {}".format(response.text))

    #Eliminar usuario
    def delete_user(self,username):
        response=requests.get(self.auth_url+'/users?name=' + username,
                              headers={'Content-Type':'application/json','X-Auth-Token':self.token})
        
        user_id=None

        if response.status_code==200:
            if len(response.json()['users'])==0:
                user_id=None
            else:
                user_id = users[0]['id']
        if user_id is not None:
            response=requests.delete(self.auth_url+'/users/'+user_id,headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
            if response.status_code == 204:
                print("[*]Usuario eliminado exitosamente")
            else:
                print("[*]Error al eliminar el usuario: {}".format(response.text))


    #Eliminar Rol
    def delete_rol(self, rol_name):
        # Obtener el ID del rol
        response = requests.get(self.auth_url + '/roles?name=' + rol_name,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        if response.status_code == 200:
            roles = response.json()['roles']
            if len(roles) == 0:
                print("[*]El rol especificado no existe")
                return
                
            role_id = roles[0]['id']
            # Verificar si hay usuarios asignados a este rol
            response = requests.get(self.auth_url + '/roles/' + role_id + '/users',
                                    headers={'Content-Type': 'application/json',
                                            'X-Auth-Token': self.token})

            
            if response.status_code == 200:
                users = response.json()['users']
                if len(users) > 0:
                    print("[*]Hay usuarios asignados a este rol. ¿Está seguro de que desea eliminar el rol? (s/n)")
                    respuesta = input()
                    if respuesta.lower() == 'n':
                        return
            
            # Eliminar el rol
            response = requests.delete(self.auth_url + '/roles/' + role_id,
                                    headers={'Content-Type': 'application/json',
                                                'X-Auth-Token': self.token})
            if response.status_code == 204:
                print("[*]Rol eliminado exitosamente")
            else:
                print("[*]Error al eliminar el rol: {}".format(response.text))
        else:
            print("[*]Error al obtener el ID del rol: {}".format(response.text))
    #Listar Roles
    def listar_roles(self):
        response = requests.get(self.auth_url + '/roles', headers={'Content-Type': 'application/json',
                                                    'X-Auth-Token': self.token})
        if response.status_code == 200:
            print(response.json().get('roles', []))
        
        else:
            print(f"Error al listar los roles: {response.status_code} - {response.text}")


    # Obtener lista de usuarios
    def list_users(self):
        #Usuarios como json
        response = requests.get(self.auth_url + '/users',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        print(response.json())
        # Obtener lista de proyectos
        url = '{}/projects'.format(self.auth_url)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.token
        }

        response = requests.get(url, headers=headers)
        
        project_id = None
        project_name="admin"

        if response.status_code == 200:
            # Imprimir id y nombre de cada proyecto
            projects = response.json()['projects']
            for project in projects:
                if project['name'] == project_name:
                    project_id=project['id']
                    break

        else:
            print('Error al listar proyectos: {}'.format(response.text))

        #obtener lista de usuarios
        response = requests.get(self.auth_url + '/users',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        if response.status_code == 200:
        # Imprimir id y nombre de cada usuario
            users = response.json()['users']
            for user in users:
                url='{}/projects/{}/users/{}/roles'.format(self.auth_url,project_id,user['id'])
                headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token
                }

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    roles = response.json()['roles']
                    for role in roles:
                        # Obtener detalles del usuario
                        user_url = '{}/users/{}'.format(self.auth_url, user['id'])
                        user_headers = {
                            'Content-Type': 'application/json',
                            'X-Auth-Token': self.token
                        }
                        user_response = requests.get(user_url, headers=user_headers)
                        if user_response.status_code == 200:
                            user_details = user_response.json()['user']
                            print('User: {}, Project: {}, Role: {}'.format(user_details['name'], project['name'], role['name']))
                        else:
                            print('Error al obtener los detalles del usuario: {}'.format(user_response.text))  
                else:
                    print("Error al obtener roles: {}".format(response.text))
        else:
            print(f"Error al listar a los usuarios: {response.status_code} - {response.text}")
       
    
    #Obtener rol de un determinado usuario
    def getUserRol(self,username):
        rolsito = ""
        #Usuarios como json
        response = requests.get(self.auth_url + '/users',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        # Obtener lista de proyectos
        url = '{}/projects'.format(self.auth_url)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.token
        }

        response = requests.get(url, headers=headers)
        
        project_id = None
        project_name="admin"

        if response.status_code == 200:
            # Imprimir id y nombre de cada proyecto
            projects = response.json()['projects']
            for project in projects:
                if project['name'] == project_name:
                    project_id=project['id']
                    break

        #else:
            #print('Error al listar proyectos: {}'.format(response.text))

        #obtener lista de usuarios
        response = requests.get(self.auth_url + '/users',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        if response.status_code == 200:
        # Imprimir id y nombre de cada usuario
            users = response.json()['users']
            for user in users:
                if(user['name']  == username):
                    url='{}/projects/{}/users/{}/roles'.format(self.auth_url,project_id,user['id'])
                    headers = {
                        'Content-Type': 'application/json',
                        'X-Auth-Token': self.token
                    }
                    response = requests.get(url, headers=headers)
                    
                    if response.status_code == 200:
                        roles = response.json()['roles']
                        rolsito = roles[0]['name']
                        break
                    
                    #else:
                        #print("Error al obtener roles: {}".format(response.text))
                        
                        
        #else:
        #    print(f"Error al listar a los usuarios: {response.status_code} - {response.text}")
       
        return rolsito










        