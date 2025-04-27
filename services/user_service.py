from datetime import datetime

import typer
from sqlalchemy.orm import Session

from database.config import SessionLocal
from models.user import User
from repositories.user_repo import UserRepo
from utils.auth import hash_password, verify_password


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepo(session=db)

    def sign_up(self,
                username: str,
                email: str,
                password: str,
                register_date: datetime = datetime.now(),
                last_login: datetime = datetime.now()):
        if username is None or email is None or password is None or register_date is None or last_login is None:
            raise ValueError("Username, email, password and register_date are required")
        existing_user = self.repo.get_user(email=email, password=password)
        typer.echo(existing_user)
        if existing_user is not None:
            raise ValueError("User already exists")

        hashed_password = hash_password(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            register_date=register_date,
            last_login=last_login
        )

        return self.repo.sign_up(user)


    def sign_in(self, email: str, password: str):
        if email is None or password is None:
            raise ValueError("email and password are required")

        user =  self.repo.sign_in(email=email)
        if not user or not verify_password(password, user.password):
            raise ValueError("Invalid password or email (Try again!)")

        self.repo.update_last_login(user.id)
        return user

    def delete_account(self, user_id: int):
        return self.repo.delete_account(user_id=user_id)

    def get_email(self, user_id: int):
        return self.repo.get_email(user_id)

if __name__ == "__main__":
    session = SessionLocal()
    service = UserService(db=session)

    result = service.sign_up(username="123",
                    email="<123>",
                    password="<PASSWORD>",
                    register_date=datetime.now(),
                    last_login=datetime.now()
                    )
    print(result)
    session.close()


