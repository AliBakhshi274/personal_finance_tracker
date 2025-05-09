from datetime import datetime, timezone


class Transaction:
    def __init__(self,
                 amount: float,
                 currency: str = "EUR",
                 category: str = None,
                 description: str = "",
                 date: datetime = datetime.now(timezone.utc),
                 user_id: int = None,
                 ):
        self.amount = amount
        self.currency = currency
        self.category = category
        self.description = description
        self.date = date
        self.user_id = user_id

    def __repr__(self):
        return f"< Transaction {self.amount} {self.currency} \nin {self.category} Category \non {self.date.strftime('%Y-%m-%d')} \ndescription is: {self.description} >"
