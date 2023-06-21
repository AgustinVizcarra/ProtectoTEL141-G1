import hashlib
import requests

def encrypt_sha256(data):
    """Encripta los datos utilizando SHA256."""
    encrypted_data = hashlib.sha256(data.encode()).hexdigest()
    return encrypted_data
class AuthenticationManager(object):
    
    ### Autenticacion y gestión de los usuarios ###
    
    def __init__(self):
        self.auth_url = "http://10.20.12.48:7070"
        
    def get_auth(self,nombre,pwd):
        if not nombre or not pwd:
            return {"msg": "Se deben proporcionar valores válidos para nombre, correo o contraseña. Si el error persiste contacte con el soport técnico"}
        endpoint = self.auth_url + "/auth/"
        body = {
            "nombre": nombre,
            "pwd": encrypt_sha256(pwd)
        }
        response = requests.post(endpoint, json=body)
        return response.json()
    def create_user(self, nombre, correo, pwd):
        if not nombre or not correo or not pwd:
            return {"msg": "Se deben proporcionar valores válidos para el nombre, correo o contraseña"}
        endpoint = self.auth_url + "/createUser/"
        body = {
            "nombre": nombre,
            "correo": correo,
            "pwd": encrypt_sha256(pwd)
        }
        response = requests.post(endpoint, json=body)
        return response.json()
    def edit_user(self, user_id, nombre, correo):
        if not user_id or not nombre or not correo:
            return {"msg": "Se deben proporcionar valores válidos para nombre, correo o ID"}
        endpoint = f"{self.auth_url}/editUser/{user_id}"
        body = {
            "nombre": nombre,
            "correo": correo
        }
        response = requests.put(endpoint, json=body)
        return response.json()
    def listar_usuarios(self):
        endpoint = f"{self.auth_url}/listarUsers/"
        response = requests.get(endpoint)
        return response.json()
    def delete_user(self, user_id):
        if not user_id:
            return {"msg": "Se debe proporcionar un ID de usuario válido"}
        endpoint = f"{self.auth_url}/deleteUser/{user_id}"
        response = requests.delete(endpoint)
        return response.json()
    def get_user_by_id(self, user_id):
        if not user_id:
            return {"msg": "Se debe proporcionar un ID de usuario"}
        endpoint = f"{self.auth_url}/getUser/{user_id}"
        response = requests.get(endpoint)
        return response.json()
    ## Gestion de los vinculos del usuario con sus proyectos y roles ##
    
    def add_user_project_role(self, usuario, proyecto, rol):
        if not all([usuario, proyecto, rol]):
            return {"msg": "Se deben proporcionar valores válidos para 'usuario', 'proyecto' y 'rol'"}

        endpoint = f"{self.auth_url}/addUserProjectRole/"
        body = {
            "usuario": usuario,
            "proyecto": proyecto,
            "rol": rol
        }
        response = requests.post(endpoint, json=body)
        return response.json()

    def edit_user_project_role(self, user_id, project_id, usuario, proyecto, rol):
        
        if not all([user_id, project_id, usuario, proyecto, rol]):
            return {"msg": "Se deben proporcionar valores válidos para 'user_id', 'project_id', 'usuario', 'proyecto' y 'rol'"}
        
        endpoint = f"{self.auth_url}/editUserProjectRole/{user_id}/{project_id}"
        body = {
            "usuario": usuario,
            "proyecto": proyecto,
            "rol": rol
        }
        response = requests.put(endpoint, json=body)
        return response.json()

    def get_role_project_por_user(self, user_id=None):
        if user_id is None:
            endpoint = f"{self.auth_url}/getRoleProjectPorUser"
        else:
            endpoint = f"{self.auth_url}/getRoleProjectPorUser/{user_id}"       
        response = requests.get(endpoint)
        return response.json()

    def delete_rol_project_user(self, project_id, user_id):
        if not all([ project_id, user_id]):
            return {"msg": "Se deben proporcionar valores válidos para 'project_id' y 'user_id'"}
        endpoint = f"{self.auth_url}/deleteRolProjectUser/{project_id}/{user_id}"
        response = requests.delete(endpoint)
        return response.json()

    ## Listado de Roles ##
    
    def listar_roles(self):
        endpoint = f"{self.auth_url}/listarRoles/"
        response = requests.get(endpoint)
        return response.json()

    def get_rol_topo(self, project_id, user_id,topo_id):
        if not all([ project_id, user_id,topo_id ]):
            return {"msg": "Se deben proporcionar valores válidos para 'project_id','user_id' y 'topo_id'"}
        endpoint = f"{self.auth_url}/getRolXTopo/{project_id}/{user_id}/{topo_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def get_rol_topoxuser(self,topo_id):
        if not all([ topo_id ]):
            return {"msg": "Se deben proporcionar valores válidos para  'topo_id'"}
        endpoint = f"{self.auth_url}/getRoleProjectPorUserPorTopo/{topo_id}"
        response = requests.get(endpoint)
        return response.json()
    
    ## Implementacion de notificación de envío de correo (Proximamente) ##
    