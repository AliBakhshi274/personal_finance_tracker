from models.transaction_model import TransactionModel
from database.config import engine

def init_db():
    TransactionModel.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()