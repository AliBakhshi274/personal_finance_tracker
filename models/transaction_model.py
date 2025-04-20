from sqlalchemy import Column, Integer, Numeric, String, DateTime, func
from database.config import Base


class TransactionModel(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, default='EUR')
    category = Column(String, nullable=False)
    description = Column(String, default='None')
    date = Column(DateTime, nullable=False, default=func.now())
