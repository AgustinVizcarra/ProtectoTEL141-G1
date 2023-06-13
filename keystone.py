import requests
import time
import json

class KeystoneAuth(object):
    def __init__(self,username, password):
        self.auth_url = "http://10.20.12.48:5000/v3"
        self.username = username
        self.password = password
        self.token = None
        self.headers = {'Content-Type': 'application/json'}
        self.UserID = None
        self.ProjectID = None
        self.RolName = None
        
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
        
    def getRolName(self):
        return self.RolName
    
    def setRolName(self,RolName):
        self.RolName = RolName
        
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
                            'domain': {'name': 'Default'}
                        }
                    }
                },
                "scope": {
                    "system":{
                        "all": True
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
    
    #Actualizar Token
    def updateToken(self):
        auth_data = {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': "admin", 
                            'password': "ronny", 
                            'domain': {'name': 'Default'}
                        }
                    }
                },
                "scope": {
                    "system":{
                        "all": True
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
            print("[*] El token se actualizó correctamente\n")
        else:
            print("[*] Error al actualizar el token, verifique las credenciales\n")

        return self.token
        
    #Obtener listado de proyectos en los que se encuentra asignado el usuario con su rol
    def getListProjects(self):
        response = requests.get(self.auth_url + '/users/' + self.UserID + "/projects",
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        proyectos = []
        roles = []
        if response.status_code == 200:
            response = response.json()
            for project in response["projects"]:
                proyecto = []
                proyecto.append(project["id"])
                proyecto.append(project["name"])
                proyectos.append(proyecto)
            
            for proyectito in proyectos:
                url='{}/projects/{}/users/{}/roles'.format(self.auth_url,proyectito[0],self.UserID)
                headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token
                }
        
                response = requests.get(url, headers=headers)
                rolName = response.json()['roles'][0]['name']
                roles.append(rolName)
        else:
            print("[*] Error al obtener la lista de proyectos del usuario\n")

        return proyectos, roles
    
    #Crear Usuario
    def crear_usuario(self, username, password, email):
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
                print("[*] Usuario creado exitosamente\n")
 
            else:
                print("[*] Ha ocurrido un error al crear el usuario\n")


    #Asignar usuario a un proyecto
    def asignarUsuarioProyecto(self,username):
        #obtenemos el ID del usuario
        response = requests.get(self.auth_url + '/users?name=' + username,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        user_id = None
        if response.status_code == 200:
            users = response.json()['users']
            if len(users)!=0:
                user_id = users[0]['id']

        #btenemos el ID del rol 'usuario'
        response = requests.get(self.auth_url + '/roles?name=usuario',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        role_id = None
        if response.status_code == 200:
            roles = response.json()['roles']
            if len(roles)!=0:
                role_id = roles[0]['id']
        
        
        if (user_id is not None) and (role_id is not None):
            url='{}/projects/{}/users/{}/roles/{}'.format(self.auth_url,self.ProjectID,user_id,role_id)
            headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token
            }

            response = requests.put(url, headers=headers)  
            if response.status_code == 204:
                print("[*] Se ha asignado al usuario "+username+" al proyecto "+nameProject + " correctamente con el rol de usuario\n")
            
            else:
                print("[*] Ha ocurrido un error al asignar al usuario al proyecto\n")  
        
        else:
            print("[*] No se encontró el usuario y/o rol\n")
      

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
            print("[*] No se encontró un usuario con dicho username\n")
                
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
                    print("[*] Usuario actualizado exitosamente\n")
                else:
                    print("[*] Ha ocurrido un error al actualizar el usuario\n")
            

    #Eliminar usuario de un proyecto
    def eliminarUsuarioProyecto(self,username):
        #obtenemos el ID del usuario
        response = requests.get(self.auth_url + '/users?name=' + username,
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        user_id = None
        if response.status_code == 200:
            users = response.json()['users']
            if len(users)!=0:
                user_id = users[0]['id']

      
        #obtenemos el ID del rol 'usuario'
        response = requests.get(self.auth_url + '/roles?name=usuario',
                                headers={'Content-Type': 'application/json',
                                        'X-Auth-Token': self.token})
        role_id = None
        if response.status_code == 200:
            roles = response.json()['roles']
            if len(roles)!=0:
                role_id = roles[0]['id']
        
        
        if (user_id is not None) and (role_id is not None):
            url='{}/projects/{}/users/{}/roles/{}'.format(self.auth_url,self.ProjectID,user_id,role_id)
            headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.token
            }

            response = requests.delete(url, headers=headers)  
            if response.status_code == 204:
                print("[*] Se ha eliminado al usuario "+username+" del proyecto "+nameProject + " correctamente")
            
            else:
                print("[*] Ha ocurrido un error al eliminar al usuario del proyecto\n") 
        
        else:
            print("[*] No se encontró el usuario y/o rol\n")

    #Listar usuarios por proyecto
    def listarProyectosUsuarios(self):
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
                if response.status_code == 200:
                    response = response.json()
                    for project in response["projects"]:
                        if(project["id"] == self.ProjectID):
                            proyectos_usuario.append(user_name)
                            break
                       
                else:
                    proyectos.append("[*] Ha ocurrido un problema al listar los proyectos del usuario\n")
                                       
        else:
            print("[*] Ha ocurrido un problema al listar los usuarios\n")
        
        return proyectos_usuario



