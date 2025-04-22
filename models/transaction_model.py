from sqlalchemy import Column, Integer, Numeric, String, DateTime, func, ForeignKey, modifier
from sqlalchemy.orm import relationship
from models.user_model import UserModel
from database.config import Base


class TransactionModel(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, default='EUR')
    category = Column(String, nullable=False)
    description = Column(String, default='None')
    date = Column(DateTime, nullable=False, default=func.now())

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('UserModel', back_populates='transactions', lazy=True)