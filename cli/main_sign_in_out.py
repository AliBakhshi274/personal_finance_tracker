import json
import typer
from pathlib import Path
from database.config import SessionLocal
from services.transaction_service import TransactionService
from services.user_service import UserService
import utils.plotter as plotter

app = typer.Typer()

SESSION_FILE = Path("user_session.json")


def save_session(user_id: int):
    with open(SESSION_FILE, "w") as file:
        json.dump({"user_id": user_id}, file)


def load_session():
    if not SESSION_FILE.exists():
        raise FileNotFoundError(f"Session file does not exist: {SESSION_FILE}")
    with open(SESSION_FILE, "r") as file:
        return json.load(file).get("user_id")


@app.command()
def register(user: str, email: str, password: str):
    db = SessionLocal()
    service = UserService(db)

    try:
        user = service.sign_up(user, email, password)
        typer.echo(f"New user added Successfully: {user.username}")
    except ValueError or Exception as e:
        typer.echo(str(e))
    finally:
        db.close()


@app.command()
def login(email: str, password: str):
    db = SessionLocal()
    service = UserService(db)
    try:
        user = service.sign_in(email, password)
        typer.echo(f"Login Successfully: {user.username}")
        save_session(user.id)
    except ValueError as e:
        typer.echo(str(e))
    finally:
        db.close()


@app.command()
def add_transaction(amount: float,
                    currency: str = "EUR",
                    category: str = None,
                    description: str = "",
                    ):
    db = SessionLocal()
    try:
        user_id = load_session()
        if user_id is None:
            return typer.echo("No user found")
        service = TransactionService(db)
        service.add_transaction(amount=amount, currency=currency, category=category, description=description,
                                user_id=user_id)
        typer.echo("Transaction was successfully added")
    except Exception as e:
        typer.echo(str(e))
    finally:
        db.close()


@app.command()
def get_transactions():
    user_id = load_session()
    db = SessionLocal()
    service = TransactionService(db)
    try:
        transactions = service.get_all(user_id=user_id)
        for transaction in transactions:
            typer.echo(
                f"<{transaction.amount} \n{transaction.currency} \n{transaction.category} \n{transaction.description}>")
    except ValueError as e:
        typer.echo(str(e))
    finally:
        db.close()


@app.command()
def sign_out():
    with open(f'user_session.json', 'w') as file:
        json.dump({"user_id": None}, file)
    typer.echo("Sign out successfully")


@app.command()
def delete_account():
    db = SessionLocal()
    user_id = load_session()
    user_service = UserService(db)
    if user_id is None:
        typer.echo("No user found or first be logged in")
        return None
    user = user_service.repo.get_user_by_id(user_id)
    if user is not None:
        sign_out()
    transactions_service = TransactionService(db)
    transactions_service.delete_by_user_id(user_id=user_id)
    typer.echo("Account deleted successfully")
    db.close()


@app.command()
def daily_summary():
    user_id = load_session()
    db = SessionLocal()
    service = TransactionService(db)
    summary = service.daily_summary(user_id=user_id)
    print(summary)
    for day, total in summary:
        typer.echo(f"{day}: {total}")
    db.close()


@app.command()
def monthly_summary():
    user_id = load_session()
    db = SessionLocal()
    service = TransactionService(db)
    summary = service.monthly_summary(user_id=user_id)
    print(summary)
    for year, month, total in summary:
        typer.echo(f"{year}-{month}: {total}")
    db.close()


@app.command()
def plot_daily():
    user_id = load_session()
    db = SessionLocal()
    service = TransactionService(db)
    summary = service.daily_summary(user_id=user_id)
    plotter.plot_daily_summary(summary)
    db.close()


@app.command()
def plot_monthly():
    user_id = load_session()
    db = SessionLocal()
    service = TransactionService(db)
    summary = service.monthly_summary(user_id=user_id)
    plotter.plot_monthly_summary(summary)
    db.close()

@app.command()
def email_monthly_report():
    user_id = load_session()
    db = SessionLocal()
    service_transaction = TransactionService(db)
    service_user = UserService(db)
    user_email = service_user.get_email(user_id=user_id)
    service_transaction.email_monthly_summary(user_id=user_id, user_email=user_email)
    db.close()

if __name__ == "__main__":
    # register("Amirali", "alibakhshi.bs@gmail.com", "amirali")
    # register("666", "666@gmail.com", "666")
    # login("alibakhshi.bs@gmail.com", "amirali")
    # login("555@gmail.com", "555")
    # login("345@gmail.com", "345")
    # add_transaction(amount=30, currency="IRR", category="Fruit", description="Banana")
    # add_transaction(amount=45, currency="USD", category="Fruit", description="Orange")
    # add_transaction(amount=45, category="Fruit", description="watermelon")
    # add_transaction(amount=45, category="Snacks", description="Chips")
    # daily_summary()
    print(".......................................................")
    # monthly_summary()
    print("################################")
    email_monthly_report()
    # plot_daily()
    # plot_monthly()
    # sign_out()
    # delete_account()