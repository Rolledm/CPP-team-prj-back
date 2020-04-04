class User:
    id: int
    login: str
    password: str
    eMail: str
    name: str
    taskId: int
    
    def __init__(self, id, login, password, eMail, name):
        super().__init__()
        self.id = id
        self.login = login
        self.password = password
        self.eMail = eMail
        self.name = name
        self.taskId = 0
      

class Task:
    id: int
    name: str
    description: str
    answer: str

    def __init__(self, id, name, description, answer):
        super().__init__()
        self.id = id
        self.name = name
        self.description = description
        self.answer = answer
        