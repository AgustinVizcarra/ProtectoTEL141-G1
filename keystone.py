import requests
import time
import json

class KeystoneAuth(object):
    def __init__(self,username, password):
        self.auth_url = "http://10.20.12.39:5000/v3"
        self.username = username
        self.password = password
        self.token = None
        self.headers = {'Content-Type': 'application/json'}
        self.UserID = None
        self.ProjectID = None
        self.RolID = None
        
    def getUserID(self):
        return self.UserID
    
    def setUserID(self,UserID):
        self.UserID = UserID
            
    def getProjectID(self):
        return self.ProjectID
    
    def setProjectID(self,ProjectID):
        self.ProjectID = ProjectID
        
    def getUsername(self):
        return self.username
    
    def setUsername(self,username):
        self.username = username
        
    def getRolID(self):
        return self.RolID
    
    def setRolID(self,RolID):
        self.RolID = RolID
        
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
            self.UserID = response.json()["token"]["user"]['id']
            print("[*]La solicitud se completó correctamente")
            print("")
            
        elif response.status_code == 401:
            print("[*]Error de autorización, verifique credenciales")
            print("")
            
        else:
            print(response)
            print("[*]Se produjo un error. Codigo de estado: ", response.status_code)
            print("")

        return self.token
    
    #Obtener TOKEN de ADMIN
    def get_token_admin(self):
        auth_data = {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': "admin",
                            'password': "admin",
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

        self.token = response.headers['X-Subject-Token']
    
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
 
            else:
                print("[*] Ha ocurrido un error al crear el usuario")
            



    #Editar usuario
    def editar_usuario(self, username, password, email):
        # Primero, obtenemos el ID del usuario
        response = requests.get(self.auth_url + '/users?name=' + username,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        user_id = None
        if response.status_code == 200:
            users = response.json()['users']
            if len(users)!=0:
                user_id = users[0]['id']

        if user_id is None:
            print("[*]No se encontró un usuario con dicho username")
                
        else:
            # Actualizamos el email y/o contraseña del usuario si se especificaron
            if ( (password is not None) or (email is not None)):
                user_data = {'user': {}}
                if password is not None:
                    user_data['user']['password'] = password
                if email is not None:
                    user_data['user']['email'] = email
                
                response = requests.patch(self.auth_url + '/users/'+ user_id,
                                    json=user_data,
                                    headers={'Content-Type': 'application/json',
                                            'X-Auth-Token': self.token})

                if response.status_code == 200:
                    print("[*]Usuario actualizado exitosamente")
                else:
                    print("[*] Ha ocurrido un error al actualizar el usuario")
            
                
    #Eliminar usuario
    def delete_user(self,username):
        # Primero, obtenemos el ID del usuario
        response = requests.get(self.auth_url + '/users?name=' + username,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        user_id = None
        if response.status_code == 200:
            users = response.json()['users']
            if len(users)!=0:
                user_id = users[0]['id']

        if user_id is None:
            print("[*]No se encontró un usuario con dicho username")
                
        else:
            # Eliminamos al usuario
            response=requests.delete(self.auth_url+'/users/'+user_id,headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
            if response.status_code == 204:
                print("[*]Usuario eliminado exitosamente")
            else:
                print("[*] Ha ocurrido un error al eliminar el usuario")
        
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
            print(json.dumps(response.json().get('roles', []), indent=2))
        
        else:
            print(f"Error al listar los roles: {response.status_code} - {response.text}")


    # Obtener lista de usuarios
    def list_users(self):
        #Usuarios como json
        response = requests.get(self.auth_url + '/users',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
    
        print(json.dumps(response.json(), indent=2))
        print("")
        
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
            print("Usuarios con rol en el proyecto:")
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
       
    
    #Obtener listado de proyectos en los que se encuentra asignado el usuario
    def getListProjects(self):
        response = requests.get(self.auth_url + '/users/' + self.UserID + "/projects",
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        proyectos = []
        if response.status_code == 200:
            response = response.json()
            for project in response["projects"]:
                proyecto = []
                proyecto.append(project["id"])
                proyecto.append(project["name"])
                proyectos.append(proyecto)
        
        else:
            print("[*]Error al obtener la lista de proyectos del usuario\n")

        return proyectos
    
    #Obtener rol de un usuario en un proyecto
    def getUserRol(self):
        rolsito = ""
        
        url='{}/projects/{}/users/{}/roles'.format(self.auth_url,self.ProjectID,self.UserID)
        headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token
                }
        
        response = requests.get(url, headers=headers)  
        if response.status_code == 200:
            rolsito = response.json()['roles'][0]['name']
            self.RolID = response.json()['roles'][0]['id']
            
        else:
           print("[*]Error al obtener el rol del usuario en el proyecto")

        return rolsito

    #Seteamos el ID del rol 'usuario' al usuario
    def setUserRol(self):
        #Puede ser por esta consulta en general , o por el rol del usuario en el proyecto que seria lo mismo
        response = requests.get(self.auth_url + '/roles?name=usuario',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        if response.status_code == 200:
            roles = response.json()['roles']
            self.RolID = response.json()['roles'][0]['id']


    #Asignar usuario a un proyecto
    def asignarUsuarioProyecto(self,username,nameProject):
        # Primero, obtenemos el ID del usuario
        response = requests.get(self.auth_url + '/users?name=' + username,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        user_id = None
        if response.status_code == 200:
            users = response.json()['users']
            if len(users)!=0:
                user_id = users[0]['id']

        #Segundo, obtenemos el ID del proyecto
        response = requests.get(self.auth_url + '/projects?name=' + nameProject,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        project_id = None
        if response.status_code == 200:
            projects = response.json()['projects']
            if len(projects)!=0:
                user_id = projects[0]['id']
        
        #Tercero, obtenemos el ID del rol 'usuario'
        response = requests.get(self.auth_url + '/roles?name=usuario',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        role_id = None
        if response.status_code == 200:
            roles = response.json()['roles']
            if len(roles)!=0:
                role_id = roles[0]['id']
        
        
        if (user_id is not None) and (project_id is not None):
            url='{}/projects/{}/users/{}/roles/{}'.format(self.auth_url,project_id,user_id,role_id)
            headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token
            }

            response = requests.put(url, headers=headers)  
            if response.status_code == 204:
                print("[*] Se ha asignado al usuario "+username+" al proyecto "+nameProject + " correctamente")
            
            else:
                print("[*] Ha ocurrido un error al asignar al usuario al proyecto")  
        
        else:
            print("[*]No se encontró el usuario y/o el proyecto")
        

    #Eliminar usuario de un proyecto
    def eliminarUsuarioProyecto(self,username,nameProject):
        # Primero, obtenemos el ID del usuario
        response = requests.get(self.auth_url + '/users?name=' + username,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        user_id = None
        if response.status_code == 200:
            users = response.json()['users']
            if len(users)!=0:
                user_id = users[0]['id']

        #Segundo, obtenemos el ID del proyecto
        response = requests.get(self.auth_url + '/projects?name=' + nameProject,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        project_id = None
        if response.status_code == 200:
            projects = response.json()['projects']
            if len(projects)!=0:
                user_id = projects[0]['id']
        
        #Tercero, obtenemos el ID del rol 'usuario'
        response = requests.get(self.auth_url + '/roles?name=usuario',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        role_id = None
        if response.status_code == 200:
            roles = response.json()['roles']
            if len(roles)!=0:
                role_id = roles[0]['id']
        
        
        if (user_id is not None) and (project_id is not None):
            url='{}/projects/{}/users/{}/roles/{}'.format(self.auth_url,project_id,user_id,role_id)
            headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token
            }

            response = requests.delete(url, headers=headers)  
            if response.status_code == 204:
                print("[*] Se ha eliminado al usuario "+username+" del proyecto "+nameProject + " correctamente")
            
            else:
                print("[*] Ha ocurrido un error al eliminar al usuario del proyecto") 
        
        else:
            print("[*]No se encontró el usuario y/o el proyecto")

    #Listar usuarios por proyecto
    def listarProyectosUsuarios(self):
        #obtener lista de usuarios
        response = requests.get(self.auth_url + '/users',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        
        proyectos_usuario = []
        
        if response.status_code == 200:
            users = response.json()['users']
            for user in users:
                user_id = user['id']
                user_name = user['name']
                
                #Consultamos los proyectos que tiene ese usuario
                response = requests.get(self.auth_url + '/users/' + user_id+ "/projects",
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
                proyectos = []
                if response.status_code == 200:
                    response = response.json()
                    for project in response["projects"]:
                        proyecto = []
                        proyecto.append(project["id"])
                        proyecto.append(project["name"])
                        proyectos.append(proyecto)
                else:
                    proyectos.append("|     [*]Ha ocurrido un problema al listar los proyectos del usuario |")
                
                proyectos_usuario.append([user_name,proyectos])            
                       
            print("[*]Se han listado todos los proyectos de los usuarios")
        
        else:
            print("[*]Ha ocurrido un problema al listar los usuarios")
        
        return proyectos_usuario

        