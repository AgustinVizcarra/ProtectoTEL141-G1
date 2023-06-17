import requests
import time
import json

#########################################GLANCE###################################################
class GlanceClient(object):
    def __init__(self,auth_token):
        self.auth_token = auth_token
        self.glance_url = "http://10.20.12.48:9292/v2"
        self.headers = { 'Content-Type': 'application/json','X-Auth-Token': self.auth_token }
    
    def listar_imagenes(self):

        url = f"{self.glance_url}/images"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            imagenes = response.json().get('images', [])
            image_info=[]
            for image in imagenes:
                image_info.append([image['id'],image['name']])
            return image_info
        else:
            print("Error al listar las imágenes:", response.status_code)
            return []
    
    def cargar_imagen(self, nombre, ruta_archivo):

        url = f"{self.glance_url}/images"
        headers = {
            'X-Auth-Token': self.auth_token
        }
        archivo = open(ruta_archivo, 'rb')
        archivo_data = archivo.read()
        archivo.close()

        data = {
            'name': nombre,
            'visibility': 'public',  # Cambiar según sea necesario
            'disk_format': 'qcow2',  # Cambiar según el formato del archivo
            'container_format': 'bare',
        }

        #DISK-FORMAT
        #ami: Formato de imagen utilizado por el servicio de Amazon Machine Image (AMI) en Amazon Web Services (AWS).
        #vdi: Formato de disco utilizado por el hipervisor VirtualBox.  
        #vhd: Formato de disco utilizado por el hipervisor Hyper-V de Microsoft.
        #vmdk: Formato de disco utilizado por VMware.
        #raw: Imagen sin formato, que puede ser utilizada por varios hipervisores.

        files = {'file': (nombre, archivo_data)}

        response = requests.post(url, headers=headers, data=data, files=files)

        if response.status_code == 201:
            print("Imagen cargada exitosamente.")
        else:
            print("Error al cargar la imagen:", response.status_code)

    def obtener_informacion_imagen(self, imagen_id):

        url = f"{self.glance_url}/images/{imagen_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            informacion_imagen = response.json().get('image', {})
            return informacion_imagen
        else:
            print("Error al obtener información de la imagen:", response.status_code)
            return {}
    
    def actualizar_informacion_imagen(self, imagen_id, nuevos_metadatos):

        url = f"{self.glance_url}/images/{imagen_id}"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }
        data = {
            'image': nuevos_metadatos
        }

        response = requests.patch(url, json=data, headers=headers)

        if response.status_code == 200:
            print("Información de la imagen actualizada exitosamente.")
        else:
            print("Error al actualizar información de la imagen:", response.status_code)

    
    def eliminar_imagen(self, imagen_id):

        url = f"{self.glance_url}/images/{imagen_id}"
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 204:
            print("Imagen eliminada exitosamente.")
        else:
            print("Error al eliminar la imagen:", response.status_code)

    def compartir_imagen(self, imagen_id, proyectos):
        
        url = f"{self.glance_url}/images/{imagen_id}/members"

        data = {
            'memberships': [{'member_id': proyecto} for proyecto in proyectos]
        }

        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 201:
            print("Imagen compartida exitosamente.")
        else:
            print("Error al compartir la imagen:", response.status_code)
    

    def descargar_imagen(self, imagen_id, ruta_destino):

        url = f"{self.glance_url}/images/{imagen_id}/file"
        response = requests.get(url, headers=self.headers, stream=True)

        if response.status_code == 200:
            with open(ruta_destino, 'wb') as archivo:
                for chunk in response.iter_content(chunk_size=1024):
                    archivo.write(chunk)
            print("Imagen descargada exitosamente.")
        else:
            print("Error al descargar la imagen:", response.status_code)