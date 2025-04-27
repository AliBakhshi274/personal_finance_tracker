from datetime import datetime, timezone
from sqlalchemy.orm import Session
from database.config import SessionLocal
from models.transaction import Transaction
from repositories.transaction_repo import TransactionRepo
from utils.currency import get_exchange_rate
from utils.emailer import send_email


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

        if currency.upper() != "EUR":
            try:
                rate = get_exchange_rate(base_currency=currency.upper(), target_currency="EUR")
                amount_in_eur = amount * rate
                currency = "EUR"
            except Exception as e:
                raise ValueError(f"Invalid currency or error in get_exchange_rate: {str(e)}")
        else:
            amount_in_eur = amount

        transaction = Transaction(
            amount=amount_in_eur,
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

    def daily_summary(self, user_id: int):
        return self.repo.get_daily_summary(user_id)

    def monthly_summary(self, user_id: int):
        return self.repo.get_monthly_summary(user_id)

    def email_monthly_summary(self, user_id: int, user_email: str):
        summary = self.repo.get_monthly_summary(user_id=user_id)
        print(summary)

        if not summary:
            raise Exception("there is no data for monthly report!")

        body = "There is a MONTHLY report:<br>"
        for year, month, total in summary:
            body += f"{int(year)}-{int(month)}: {total} EUR <br>"
        send_email(
            receiver_email=user_email,
            subject="Monthly Report",
            body=body
        )

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



