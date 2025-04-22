from models.user_model import UserModel
from models.transaction_model import TransactionModel
from database.config import engine

def init_db():
    TransactionModel.metadata.drop_all(engine)
    UserModel.metadata.drop_all(engine)
    TransactionModel.metadata.create_all(bind=engine)
    UserModel.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()

