import random
from faker import Faker
from database.config import SessionLocal
from models.transaction_model import TransactionModel
from services.transaction_service import TransactionService

fake = Faker()


def create_fake_transactions(user_id: int, count: int = 1000):
    db = SessionLocal()
    service = TransactionService(db)

    categories = [
        'Food',
        'Shopping',
        'Health',
        'Travel',
        'Sports',
    ]

    currency = ['EUR', 'USD', 'IRR']

    for _ in range(count):
        amount = round(random.uniform(10, 500), 2)
        category = random.choice(categories)
        currency = random.choice(currency)
        fake_date = fake.date_time_between_dates(datetime_start='-3y', datetime_end='now')

        transaction = TransactionModel(
            amount=amount,
            currency=currency,
            category=category,
            description=category,
            date=fake_date,
            user_id=user_id
        )

        db.add(transaction)
    db.commit()
    db.close()


if __name__ == '__main__':
    create_fake_transactions(user_id=27)
