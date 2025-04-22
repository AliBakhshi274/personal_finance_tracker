from datetime import datetime, timezone

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
                        date: datetime = datetime.now(timezone.utc),
                        user_id: int = None,
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
            date=date,
            user_id=user_id,
        )

        return self.repo.add_transaction(transaction)

    def get_all(self, user_id: int):
        return self.repo.get_all(user_id=user_id)

    def get_by_category(self, category: str):
        return self.repo.get_by_category(category)

    def delete_by_user_id(self, user_id: int):
        return self.repo.delete_transaction(user_id)

if '__main__' == __name__:
    session = SessionLocal()
    service = TransactionService(session)

    service.add_transaction(
        amount=82.00,
        currency="EUR",
        category="Shopping",
        description="das Handtuch",
        date=datetime.now(),
        user_id=1
    )

    print(service.get_all())
    print(service.get_by_category("Food"))

    session.close()



