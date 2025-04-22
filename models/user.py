from datetime import datetime


class User:
    def __init__(self,
                 username: str,
                 email: str,
                 password: str,
                 register_date: datetime = None,
                 last_login: datetime = None,
                 ):
        self.username = username
        self.email = email
        self.password = password
        self.register_date = register_date
        self.last_login = last_login

    def __repr__(self):
        return (f"<User {self.username}\n"
                f"{self.email}\n"
                f"{self.password}\n"
                f"register_date: {self.register_date}\n"
                f"last login: {self.last_login}>")
