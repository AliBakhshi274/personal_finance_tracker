from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.config import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    register_date = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=False)

    transactions = relationship("TransactionModel", back_populates="user", passive_deletes=True, lazy=True)
