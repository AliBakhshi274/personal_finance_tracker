from models.transaction import Transaction

if __name__ == '__main__':
    transaction = Transaction(amount=20.54, category="Food", description="Lunch")
    print(transaction)