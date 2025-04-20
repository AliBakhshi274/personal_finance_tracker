from datetime import datetime

class Transaction:
    def __init__(self,
                 amount: float,
                 currency: str = "EUR",
                 category: str = None,
                 description: str = "",
                 date: datetime = datetime.now(),
                 ):
        self.amount = amount
        self.currency = currency
        self.category = category
        self.description = description
        self.date = date

    def __repr__(self):
        return f"< Transaction {self.amount} {self.currency} \nin {self.category} Category \non {self.date.strftime('%Y-%m-%d')} \ndescription is: {self.description} >"