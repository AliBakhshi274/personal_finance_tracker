from datetime import datetime, timezone

import typer
from sqlalchemy.orm import Session
from database.config import SessionLocal
from models.transaction_model import TransactionModel
from models.user import User
from models.user_model import UserModel


class UserRepo:
    def __init__(self, session: Session):
        self.session = session

    def sign_up(self, user: User):
        db_user = UserModel(
            username=user.username,
            email=user.email,
            password=user.password,
            register_date=user.register_date,
            last_login=user.last_login,
        )
        self.session.add(db_user)
        self.session.commit()
        return db_user

    def get_user(self, email: str, password: str):
        user_model = self.session.query(UserModel).filter(UserModel.email == email and UserModel.password == password).first()
        if user_model is None:
            return None
        return User(
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
            register_date=user_model.register_date,
            last_login=user_model.last_login,
        )

    def get_user_by_id(self, id: int):
        user = self.session.query(UserModel).filter(UserModel.id == id).first()
        if user is None:
            typer.echo("User not found")
            return None
        self.session.delete(user)
        self.session.commit()
        return user
        # if user_model is None:
        #     return None
        # return User(
        #     username=user_model.username,
        #     email=user_model.email,
        #     password=user_model.password,
        #     register_date=user_model.register_date,
        #     last_login=user_model.last_login,
        # )

    def sign_in(self, email: str):
        return self.session.query(UserModel).filter(UserModel.email == email).first()

    def update_last_login(self, id: int):
        self.session.query(UserModel).filter(UserModel.id == id).update({"last_login": datetime.now(timezone.utc)}, synchronize_session=False)
        self.session.commit()

    def delete_account(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user is None:
            return None
        print(f"user: {user.username}")
        self.session.delete(user)
        self.session.commit()
        return user

if __name__ == "__main__":
    db = SessionLocal()
    user_repo = UserRepo(db)
    print("salam")
    user = User(
        username='Zahra',
        email='<EMAIL>',
        password='<PASSWORD>',
        register_date=datetime.now(),
        last_login=datetime.now(),
    )

    print(user.__repr__())
    user_repo.sign_up(user)
    db.close()