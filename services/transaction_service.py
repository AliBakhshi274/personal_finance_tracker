from datetime import datetime

from sqlalchemy.orm import Session

from database.config import SessionLocal
from models.transaction import Transaction
from repositories.transaction_repo import TransactionRepo

class TransactionService:
    def __init__(self, db: Session):
        self.repo = TransactionRepo(session=db)

    def add_transaction(self,
                        amount: float,
                        currency: str = "EUR",
                        category: str = None,
                        description: str = "",
                        date: datetime = datetime.now()
                        ):
        if amount == 0:
            raise ValueError("Amount can't be zero")
        elif amount < 0:
            raise ValueError("Amount can't be negative")

        transaction = Transaction(
            amount=amount,
            currency=currency,
            category=category,
            description=description,
            date=date
        )

        return self.repo.add_transaction(transaction)

    def get_all(self):
        return self.repo.get_all()

    def get_by_category(self, category: str):
        return self.repo.get_by_category(category)

if '__main__' == __name__:
    session = SessionLocal()
    service = TransactionService(session)

    service.add_transaction(
        amount=85.65,
        currency="EUR",
        category="Shopping",
        description="a Suit",
        date=datetime.now()
    )

    print(service.get_all())
    print(service.get_by_category("Food"))

    session.close()



