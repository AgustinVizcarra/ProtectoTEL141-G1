import requests

class NetworkingManager: 
    
    def __init__(self):
        self.base_url = "http://10.20.12.48:7070"
        
    ## Gestion de Proyectos (Slices) ##
    
    def add_proyecto(self, nombre):
        if not nombre:
            return {"msg": "Se debe proporcionar un valor válido para 'nombre'"}
        endpoint = f"{self.base_url}/addProyecto/"
        body = {
            "nombre": nombre
        }
        response = requests.post(endpoint, json=body)
        return response.json()

    def edit_proyecto(self, proyecto_id, nombre):
        if not proyecto_id or not nombre:
            return {"msg": "Se deben proporcionar valores válidos para 'proyecto_id' y 'nombre'"}
        endpoint = f"{self.base_url}/editProyecto/{proyecto_id}"
        body = {
            "nombre": nombre
        }
        response = requests.put(endpoint, json=body)
        return response.json()

    def delete_proyecto(self, proyecto_id):
        if not proyecto_id:
            return {"msg": "Se debe proporcionar un ID de proyecto válido"}
        endpoint = f"{self.base_url}/deleteProyecto/{proyecto_id}"
        response = requests.delete(endpoint)
        return response.json()

    def listar_proyectos(self):
        endpoint = f"{self.base_url}/listarProyecto/"
        response = requests.get(endpoint)
        return response.json()

    def get_proyecto(self, proyecto_id):
        if not proyecto_id:
            return {"msg": "Se debe proporcionar un ID de proyecto válido"}
        endpoint = f"{self.base_url}/getProyecto/{proyecto_id}"
        response = requests.get(endpoint)
        return response.json()
    
    ## Gestion de topologias ##
    
    def create_topology(self, tipo, subnetname, network, gateway, iprange, worker):
        if not all([tipo, subnetname, network, gateway, iprange, worker]):
            return {"mensaje": "Se deben proporcionar valores válidos para 'tipo', 'subnetname', 'network', 'gateway', 'iprange' y 'worker'"}
        body = {
            "tipo": tipo,
            "subnetname": subnetname,
            "network": network,
            "gateway": gateway,
            "iprange": iprange,
            "worker": worker
        }
        endpoint = f"{self.base_url}/createTopology/"
        response = requests.post(endpoint, json=body)
        return response.json()
    
    def edit_topology(self, topology_id, tipo, subnetname, network, gateway, iprange, worker):
        if not all([topology_id, tipo, subnetname, network, gateway, iprange, worker]):
            return {"msg": "Se deben proporcionar valores válidos para 'topology_id', 'tipo', 'subnetname', 'network', 'gateway', 'iprange' y 'worker'"}
        body = {
            "tipo": tipo,
            "subnetname": subnetname,
            "network": network,
            "gateway": gateway,
            "iprange": iprange,
            "worker": worker
        }
        endpoint = f"{self.base_url}/editTopology/{topology_id}"
        response = requests.put(endpoint, json=body)
        return response.json()
    
    def listar_topologias(self):
        endpoint = f"{self.base_url}/listarTopologias/"
        response = requests.get(endpoint)
        return response.json()
    
    def get_topology(self, topology_id):
        if not topology_id:
            return {"msg": "Se debe proporcionar un ID de topología válido"}
        endpoint = f"{self.base_url}/getTopology/{topology_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def delete_topology(self, topology_id):
        if not topology_id:
            return {"msg": "Se debe proporcionar un ID de topología válido"}
        endpoint = f"{self.base_url}/deleteTopology/{topology_id}"
        response = requests.delete(endpoint)
        return response.json()
    
    ## Gestion de Vinculos de Topologia y Proyecto ##
    
    def create_link_topo_proyecto(self, proyecto, topologia):
        if not proyecto or not topologia:
            return {"msg": "Se deben proporcionar valores válidos para 'proyecto' y 'topologia'"}
        body = {
            "proyecto": proyecto,
            "topologia": topologia
        }
        endpoint = f"{self.base_url}/createLinkTopoProyecto/"
        response = requests.post(endpoint, json=body)
        return response.json()
    
    def edit_link_topo_proyecto(self, topology_id, project_id, proyecto, topologia):
        if not all([topology_id, project_id, proyecto, topologia]):
            return {"msg": "Se deben proporcionar valores válidos para 'topology_id', 'project_id', 'proyecto' y 'topologia'"}
        body = {
            "proyecto": proyecto,
            "topologia": topologia
        }
        endpoint = f"{self.base_url}/editLinkTopoProyecto/{topology_id}/{project_id}"
        response = requests.put(endpoint, json=body)
        return response.json()
    
    def listar_links_topo_proyectos(self):
        endpoint = f"{self.base_url}/listarlinksTopoProyectos/"
        response = requests.get(endpoint)
        return response.json()
    
    def get_link_topo_proyecto(self, project_id):
        endpoint = f"{self.base_url}/getLinksTopoProyecto/{project_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def delete_link_topo_proyecto(self, topology_id, project_id):
        if not topology_id or not project_id:
            return {"msg": "Se deben proporcionar valores válidos para 'topology_id' y 'project_id'"}
        endpoint = f"{self.base_url}/deleteLinkTopoProyecto/{topology_id}/{project_id}"
        response = requests.delete(endpoint)
        return response.json()
    
    def get_users_topo_rol(self,project_id):
        if not project_id:
            return {"msg": "Se deben proporcionar valor válido para 'topology_id' "}
        endpoint = f"{self.base_url}/getUsersXTopo/{project_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def get_user_topo_rol(self,user_id):
        if not user_id:
            return {"msg": "Se deben proporcionar valores válidos para 'user_id "}
        endpoint = f"{self.base_url}/getTopoXUserXRol/{user_id}"
        response = requests.get(endpoint)
        return response.json()
    
    def get_detalle_user_topo(self,user_id):
        if not user_id:
            return {"msg": "Se deben proporcionar valores válidos para 'user_id "}
        endpoint = f"{self.base_url}/getDetalleTopoXUser/{user_id}"
        response = requests.get(endpoint)
        return response.json()