import requests

class PlacementManager:
    
    def __init__(self):
        self.base_url = "http://10.20.12.39:7070"

    ## Gestion de Colocaciones de VM's ##
    
    def add_vm_topology(self, body):
        if not body:
            return {"msg": "No se envió ningún dato en el cuerpo de la solicitud"}
        endpoint = f"{self.base_url}/addVmTopology/"
        response = requests.post(endpoint, json=body)
        return response.json()
    
    def edit_link_topo_vm(self, topology_id, vm_id, body):
        if not all([topology_id, vm_id, body]):
            return {"msg": "Se deben proporcionar valores válidos para 'topology_id', 'vm_id' y 'body'"}
        endpoint = f"{self.base_url}/editLinkTopoVM/{topology_id}/{vm_id}"
        response = requests.put(endpoint, json=body)
        return response.json()
    
    def get_vms_por_topologia(self, topology_id):
        if not topology_id:
            return {"msg": "Se debe proporcionar un ID de topología válido"}
        endpoint = f"{self.base_url}/getVmsporTopologia/{topology_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def delete_link_vm_topo(self, topology_id, vm_id):
        if not all([topology_id, vm_id]):
            return {"msg": "Se deben proporcionar valores válidos para 'topology_id' y 'vm_id'"}
        endpoint = f"{self.base_url}/deleteLinkVmTopo/{topology_id}/{vm_id}"
        response = requests.delete(endpoint)
        return response.json()