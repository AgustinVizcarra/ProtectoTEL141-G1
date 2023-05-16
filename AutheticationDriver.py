class AuthenticationManager(object):
    def __init__(self,username,password):
        self.auth_url = "http://10.20.12.39:7070/"
        self.username = username
        self.password = password
    def get_auth_url(self):
        
        pass