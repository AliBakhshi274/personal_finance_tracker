from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.config import SessionLocal
from models.transaction import Transaction
from models.transaction_model import TransactionModel


class TransactionRepo:
    def __init__(self, session: Session):
        self.session = session

    def add_transaction(self, transaction: Transaction):
        db_transaction = TransactionModel(
            amount=transaction.amount,
            currency=transaction.currency,
            category=transaction.category,
            description=transaction.description,
            date=transaction.date,
            user_id= transaction.user_id
        )
        self.session.add(db_transaction)
        self.session.commit()
        self.session.refresh(db_transaction)
        return db_transaction

    def get_all(self, user_id: int):
        return self.session.query(TransactionModel).filter_by(user_id=user_id).all()

    def get_by_category(self, category: str):
        return self.session.query(TransactionModel).filter(
            TransactionModel.category == category
        ).all()

    def delete_transaction(self, user_id: int):
        transactions = self.session.query(TransactionModel).filter(TransactionModel.user_id==user_id).all()
        if not transactions:
            return []
        for transaction in transactions:
            self.session.delete(transaction)
        self.session.commit()
        return transactions

    def get_daily_summary(self, user_id: int):
        return (
            self.session.query(
                func.date(TransactionModel.date).label('day'),
                func.sum(TransactionModel.amount).label('total_amount'),
            )
            .filter(TransactionModel.user_id == user_id)
            .group_by(func.date(TransactionModel.date))
            .order_by(func.date(TransactionModel.date))
            .all()
        )

    def get_monthly_summary(self, user_id: int):
        return (
            self.session.query(
                func.extract('year', TransactionModel.date).label('year'),
                func.extract('month', TransactionModel.date).label('month'),
                func.sum(TransactionModel.amount).label('total_amount'),
            )
            .filter(TransactionModel.user_id == user_id)
            .group_by(
                func.extract('year', TransactionModel.date),
                func.extract('month', TransactionModel.date)
                      )
            .order_by(func.extract('year', TransactionModel.date), func.extract('month', TransactionModel.date))
            .all()
        )


if __name__ == "__main__":
    db = SessionLocal()
    transaction_repo = TransactionRepo(db)
    # transaction = Transaction(
    #     amount=45.55,
    #     currency="EUR",
    #     category="Cloth",
    #     description="for my friend's party",
    #     date=datetime.today(),
    #     user_id=1
    # )
    # transaction_repo.add_transaction(transaction)
    foods = transaction_repo.get_by_category(category='Food')
    for food in foods:
        print(f"amount: {food.amount}, category: {food.category}")
