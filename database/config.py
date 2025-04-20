import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def get_connection():
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            os.getenv("DB_USERNAME"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
    )


try:
    SECRET_KEY = os.getenv("SECRET_KEY")
    engine = get_connection()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    print(
        f"Connection to the {engine.name} for user {engine} created successfully.")
except Exception as ex:
    print("Connection could not be made due to the following error: \n", ex)
