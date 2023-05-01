import requests


class KeystoneAuth(object):

    def __init__(self,username, password):
        self.auth_url = "http://10.20.12.39:5000/v3/auth/tokens"
        self.username = username
        self.password = password
        self.token = None
        self.headers = {'Content-Type': 'application/json'}

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
                }
            }
        }
        response = requests.post(self.auth_url,
                                 json=auth_data,
                                 headers=self.headers)

        if response.status_code == 201:
            self.token = response.headers['X-Subject-Token']
            print("La solicitud se completó correctamente")
            
        elif response.status_code == 401:
            print("Error de autorización, verifique credenciales")
            
        else:
            print("Se produjo un error. Codigo de estado;", response.status_code)

        return self.token













class KeystoneClient(object):
    def __init__(self, auth_url, username, password, project_name):
        self.auth = KeystoneAuth(auth_url, username, password, project_name)
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth.get_token()
        }

    def list_users(self):
        response = requests.get(self.auth.auth_url + '/users',
                                headers=self.headers)
        return response.json()

    def create_user(self, name, password, email):
        user_data = {
            'user': {
                'name': name,
                'password': password,
                'email': email,
                'enabled': True
            }
        }
        response = requests.post(self.auth.auth_url + '/users',
                                 json=user_data,
                                 headers=self.headers)
        return response.json()

    # Métodos similares para otros recursos de Keystone y OpenStack
