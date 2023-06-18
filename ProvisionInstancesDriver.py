import requests

class ProvisionInstancesManager:
    def __init__(self):
        self.base_url = "http://10.20.12.48:7070"

    def add_vm(self, imagen_id, flavor_id):
        if not imagen_id or not flavor_id:
            return {"msg": "Se deben proporcionar valores válidos para 'imagen' y 'vncport'"}    
        endpoint = f"{self.base_url}/addVM/"
        body = {
            "imagen": imagen_id,
            "flavor": flavor_id
        }
        response = requests.post(endpoint, json=body)
        return response.json()

    def edit_vm(self, vm_id, imagen_id,flavor_id):
        if not vm_id or not imagen_id or not flavor_id:
            return {"msg": "Se deben proporcionar valores válidos para 'vm_id', 'imagen' y 'vncport'"}
        endpoint = f"{self.base_url}/editVM/{vm_id}"
        body = {
            "imagen": imagen_id,
            "flavor": flavor_id
        }
        response = requests.put(endpoint, json=body)
        return response.json()

    def delete_vm(self, vm_id):
        if not vm_id:
            return {"msg": "Se debe proporcionar un ID de VM válido"}
        
        endpoint = f"{self.base_url}/deleteVm/{vm_id}"
        response = requests.delete(endpoint)
        return response.json()

    def listar_vms(self):
        endpoint = f"{self.base_url}/listarVms/"
        response = requests.get(endpoint)
        return response.json()

    def get_vm(self, vm_id):
        if not vm_id:
            return {"msg": "Se debe proporcionar un ID de VM válido"}
        endpoint = f"{self.base_url}/getVM/{vm_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def listar_imagenes(self):
        endpoint = f"{self.base_url}/listarImagenes/"
        response = requests.get(endpoint)
        return response.json()
    
    ## Imagenes ##
    
    def add_imagen(self, user_id, project_id,imagen):
        if not imagen or not user_id or not project_id:
            return {"msg": "Se deben proporcionar valores válidos para 'imagen' y 'vncport'"}    
        endpoint = f"{self.base_url}/addImagen/{user_id}/{project_id}"
        body = {
            "imagen": imagen,
            "usuario": user_id,
            "proyecto": project_id,
        }
        response = requests.post(endpoint, json=body)
        return response.json()
    
    def listar_imagenes_project(self,project_id):
        endpoint = f"{self.base_url}/listarImagenesxProyecto/{project_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def delete_imagen(self, imagen_id):
        if not imagen_id:
            return {"msg": "Se debe proporcionar un ID de imagen válido"}
        endpoint = f"{self.base_url}/deleteImagen/{imagen_id}"
        response = requests.delete(endpoint)
        return response.json()
    
    ## Flavors ##
    
    def add_flavor(self, user_id, project_id,descripcion, cpu,memoria,disco):
        if not descripcion or not user_id or not project_id or not cpu or not memoria or not disco:
            return {"msg": "Se deben proporcionar valores válidos para 'imagen' y 'vncport'"}    
        endpoint = f"{self.base_url}/addFlavor/{user_id}/{project_id}"
        body = {
            "descripcion": descripcion,
            "cpu": cpu,
            "memoria": memoria,
            "disco": disco
        }
        response = requests.post(endpoint, json=body)
        return response.json()
    
    def listar_flavor_project(self,project_id):
        endpoint = f"{self.base_url}/listarFlavors/{project_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def delete_flavor(self, flavor_id):
        if not flavor_id:
            return {"msg": "Se debe proporcionar un ID de flavor válido"}
        endpoint = f"{self.base_url}/deleteFlavor/{flavor_id}"
        response = requests.delete(endpoint)
        return response.json()

    def edit_flavor(self, flavor_id,descripcion,cpu,memoria,disco):
        if not flavor_id or not descripcion or not cpu or not memoria or not disco:
            return {"msg": "Se deben proporcionar valores válidos para el flavor (no deben ser nulos)"}
        endpoint = f"{self.base_url}/editflavor/{flavor_id}"
        body = {
            "descripcion": descripcion,
            "cpu": cpu,
            "memoria": memoria,
            "disco": disco
        }
        response = requests.put(endpoint, json=body)
        return response.json()
    
    def get_flavor(self, flavor_id):
        if not flavor_id:
            return {"msg": "Se debe proporcionar un ID de flavor válido"}
        endpoint = f"{self.base_url}/getFlavor/{flavor_id}"
        response = requests.get(endpoint)
        return response.json()