from datetime import datetime

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


if __name__ == "__main__":
    db = SessionLocal()
    transaction_repo = TransactionRepo(db)
    transaction = Transaction(
        amount=45.55,
        currency="EUR",
        category="Cloth",
        description="for my friend's party",
        date=datetime.today(),
        user_id=1
    )
    transaction_repo.add_transaction(transaction)
    print(transaction_repo.get_all())
