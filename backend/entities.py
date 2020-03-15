class User:
    id: int
    login: str
    password: str
    eMail: str
    
    def __init__(self, id, login, password, eMail):
        super().__init__()
        self.id = id
        self.login = login
        self.password = password
        self.eMail = eMail
      
