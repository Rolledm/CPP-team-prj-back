API:
    GET
    /user?login=my_login&password=qwerty - пример запроса на логин. 
    вернется json:
    {
        id: int,
        login: str,
        password: str,
        eMail:str,
	Name:str
    } - если залогинился

    или 
    {
        result: "error"
    } - если логин/пароль неверные

 