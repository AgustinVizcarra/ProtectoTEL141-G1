import requests

class ProvisionInstancesManager:
    def __init__(self):
        self.base_url = "http://10.20.12.39:7070"

    def add_vm(self, imagen, vncport):
        if not imagen or not vncport:
            return {"msg": "Se deben proporcionar valores válidos para 'imagen' y 'vncport'"}
        
        endpoint = f"{self.base_url}/addVM/"
        body = {
            "imagen": imagen,
            "vncport": vncport
        }
        response = requests.post(endpoint, json=body)
        return response.json()

    def edit_vm(self, vm_id, imagen, vncport):
        if not vm_id or not imagen or not vncport:
            return {"msg": "Se deben proporcionar valores válidos para 'vm_id', 'imagen' y 'vncport'"}
        
        endpoint = f"{self.base_url}/editVM/{vm_id}"
        body = {
            "imagen": imagen,
            "vncport": vncport
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

