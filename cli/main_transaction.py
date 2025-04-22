'''
python -m cli.main add 74.254 USD Clothes  sweater
python -m cli.main get-all
'''

from database.config import SessionLocal
from services.transaction_service import TransactionService
import typer

app = typer.Typer()


@app.command()
def add(amount: float,
        currency: str,
        category: str,
        description: str):
    db = SessionLocal()
    transaction_service = TransactionService(db)
    transaction_service.add_transaction(
        amount=amount,
        currency=currency,
        category=category,
        description=description
    )
    typer.echo(f"Transaction added to database successfully.")
    db.close()


@app.command()
def get_all():
    db = SessionLocal()
    transaction_service = TransactionService(db)
    items = transaction_service.get_all()
    for item in items:
        typer.echo(f"{item.amount} {item.currency} {item.category} {item.date.strftime('%d/%m/%Y')}")
    typer.echo(f"operation was successful.")
    db.close()


@app.command()
def get_by_category(category: str):
    db = SessionLocal()
    transaction_service = TransactionService(db)
    items = transaction_service.get_by_category(category)
    for item in items:
        typer.echo(f"{item.amount} {item.currency} {item.category} {item.date.strftime('%d/%m/%Y')}")
    typer.echo(f"operation was successful.")
    db.close()

if __name__ == "__main__":
    app()