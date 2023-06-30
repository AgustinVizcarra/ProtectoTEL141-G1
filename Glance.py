import requests
import time
import json

#########################################GLANCE###################################################
class GlanceClient(object):
    def __init__(self,auth_token):
        self.auth_token = auth_token
        self.glance_url = "http://10.20.12.188:9292/v2"
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

        extension = ruta_archivo.split('.')[-1]
        

        formatos_compatibles = {
            'qcow2': ['qcow2'],
            'vmdk': ['vmdk'],
            'raw': ['img', 'bin', 'raw'],
            'ami': ['ami'],
            'vdi': ['vdi'],
            'vhd': ['vhd'],
            'iso': ['iso']
            
            # Agrega aquí otros formatos compatibles y sus correspondientes extensiones
        }

        formato = None
        for fmt, extensiones in formatos_compatibles.items():
            if extension in extensiones:
                formato = fmt
                break

        if formato is None:
            print("Formato de imagen no compatible.")
            return

        url = f"{self.glance_url}/images"

        data = {
            'name': nombre,
            'visibility': 'public',
            'disk_format': formato,
            'container_format': 'bare',
        }

        #DISK-FORMAT
        #ami: Formato de imagen utilizado por el servicio de Amazon Machine Image (AMI) en Amazon Web Services (AWS).
        #vdi: Formato de disco utilizado por el hipervisor VirtualBox.  
        #vhd: Formato de disco utilizado por el hipervisor Hyper-V de Microsoft.
        #vmdk: Formato de disco utilizado por VMware.
        #raw: Imagen sin formato, que puede ser utilizada por varios hipervisores.

        # Crear la imagen
        response = requests.post(url, headers=self.headers, json=data)
        #print(response.json)

        if response.status_code == 201:
            print("[*] Imagen creada exitosamente.")
            image_id = response.json()['id']

            # Subir los datos de la imagen
            url = f"{self.glance_url}/images/{image_id}/file"

            self.headers['Content-Type'] = 'application/octet-stream'
            with open(ruta_archivo, 'rb') as f:
                response = requests.put(url, headers=self.headers, data=f)

            if response.status_code == 204:
                print("[*] Datos de la imagen cargados exitosamente.")
            else:
                print("[*] Error al cargar los datos de la imagen:", response.status_code)
        else:
            print("[*] Error al crear la imagen:", response.status_code)

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

    
    def eliminar_imagen(self, imagen_name):
        imagen_id=self.obtenerIdImagen(imagen_name)

        if imagen_id is not None:
            url = f"{self.glance_url}/images/{imagen_id}"
            response = requests.delete(url, headers=self.headers)
        

            if response.status_code == 204:
                print("Imagen eliminada exitosamente.")
            else:
                print("Error al eliminar la imagen:", response.status_code)
        else:
            print("La imagen no existe")

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


    def obtenerIdImagen(self, image_name):
        url = f"{self.glance_url}/images"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            images = response.json().get('images', [])
            # Buscar la imagen por nombre
            for image in images:
                if image['name'] == image_name:
                    image_id = image['id']
                    return image_id
            return None
        else:
            print("Error al obtener las imágenes:", response.status_code)
            return None
