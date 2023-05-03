import requests
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
        # Primero creamos el usuario
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
            
            # Después, obtenemos el ID del rol a asignar
            response = requests.get(self.auth_url + '/roles',
                                headers={'Content-Type': 'application/json',
                                         'X-Auth-Token': self.token})

            role_id = None
            if response.status_code == 201:
                roles = response.json()['roles']
                for role in roles:
                    if role['name'] == rol_name:
                        role_id = role['id']
                        break

            if role_id is None:
                print("[*]No se encontró el rol especificado")
                
            else:
                # Finalmente, asignamos el rol al usuario
                url = "{}/roles/{}/users/{}".format(self.auth_url, role_id, username)
                response = requests.put(url,
                                        headers={'Content-Type': 'application/json',
                                                'X-Auth-Token': self.token})

                if response.status_code == 201:
                    print("[*]Rol asignado exitosamente")
                    
                else:
                    print("[*]Error al asignar el rol: {}".format(response.text))
            
        else:
            print("Error al crear el usuario: {}".format(response.text))


    #Editar usuario y Rol
    def editar_usuario(self, username, password=None, email=None, rol_name=None):
        # Primero, obtenemos el ID del usuario
        response = requests.get(self.auth_url + '/users?name=' + username,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        
        user_id = None
        
        if response.status_code == 200:
            users = response.json()['users']
            user_id = users[0]['id']
            
        if user_id is None:
            print("[*]No se encontró un usuario con el nombre especificado")
            
<<<<<<< HEAD
            if response.status_code == 200:
                roles = response.json()['roles']
                for role in roles:
                    if role['name'] == rol_name:
                        role_id = role['id']
                        break
=======
        else:
            # Luego, actualizamos los campos del usuario
            user_data = {
                'user': {
                    'id': user_id,
                }
            }
>>>>>>> 3fb919534a6bd93e05e25e16572c2db7a9ac2eeb
            
            if password is not None:
                user_data['user']['password'] = password
                
            if email is not None:
                user_data['user']['email'] = email
            
            if rol_name is not None:
                # Obtenemos el ID del nuevo rol
                response = requests.get(self.auth_url + '/roles',
                                        headers={'Content-Type': 'application/json',
                                                'X-Auth-Token': self.token})
                
                role_id = None
                
                if response.status_code == 201:
                    roles = response.json()['roles']
                    for role in roles:
                        if role['name'] == rol_name:
                            role_id = role['id']
                            break
                
                if role_id is None:
                    print("[*]No se encontró el rol especificado")
                    
                else:
                    # Asignamos el nuevo rol al usuario
                    url = "{}/roles/{}/users/{}".format(self.auth_url, role_id, username)
                    response = requests.put(url,
                                            headers={'Content-Type': 'application/json',
                                                    'X-Auth-Token': self.token})
                    
                    if response.status_code == 201:
                        print("[*]Rol asignado exitosamente")
                        
                        response = requests.patch(self.auth_url + '/users/' + user_id,
                                    json=user_data,
                                    headers={'Content-Type': 'application/json',
                                            'X-Auth-Token': self.token})
            
<<<<<<< HEAD
            if response.status_code == 201:
                print("Rol asignado exitosamente")
            else:
                print("Error al asignar el rol: {}".format(response.text))
                return
        
        response = requests.patch(self.auth_url + '/users/' + user_id,
                                json=user_data,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        
        if response.status_code == 200:
            print("Usuario actualizado exitosamente")
        else:
            print("Error al actualizar el usuario: {}".format(response.text))
=======
                        if response.status_code == 201:
                            print("[*]Usuario actualizado exitosamente")
                            print("[*]Se cerrará la aplicación.Vuelva a iniciar sesión nuevamente.")
                        else:
                            print("[*]Error al actualizar el usuario: {}".format(response.text))
                         
                    else:
                        print("[*]Error al asignar el rol: {}".format(response.text))
>>>>>>> 3fb919534a6bd93e05e25e16572c2db7a9ac2eeb


    #Listar Roles
    def listar_roles(self):
        response = requests.get(self.auth_url + '/roles', headers={'Content-Type': 'application/json',
                                                    'X-Auth-Token': self.token})
        if response.status_code == 200:
            print(response.json().get('roles', []))
            
        else:
            print(f"Error al listar los roles: {response.status_code} - {response.text}")

    #Listar Usuario
    def list_users(self):
        response = requests.get(self.auth_url + '/users',
                                headers={'Content-Type': 'application/json',
                                                    'X-Auth-Token': self.token})
        print(response.json())





