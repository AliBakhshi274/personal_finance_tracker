from sqlalchemy.orm import Session
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
        )
        self.session.add(db_transaction)
        self.session.commit()
        self.session.refresh(db_transaction)
        return db_transaction

    def get_all(self):
        return self.session.query(TransactionModel).all()

    def get_by_category(self, category: str):
        return self.session.query(TransactionModel).filter(
            TransactionModel.category == category
        ).all()

# if __name__ == "__main__":
#     db = SessionLocal()
#     transaction_repo = TransactionRepo(db)
#     transaction = Transaction(
#         amount=12.36,
#         currency="EUR",
#         category="Food",
#         description="Launch",
#         date=datetime.today()
#     )
#     transaction_repo.add_transaction(transaction)
#     print(transaction_repo.get_all())
