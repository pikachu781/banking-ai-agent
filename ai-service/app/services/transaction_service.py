from sqlalchemy.orm import Session

from app.database.models import BankAccount, Transaction


def get_recent_transactions(
    db: Session,
    user_id: int,
    limit: int = 5
) -> list[dict]:

    # Find the user's bank account
    account = (
        db.query(BankAccount)
        .filter(
            BankAccount.user_id == user_id
        )
        .first()
    )

    if account is None:
        return []

    # Get recent transactions
    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.account_id == account.id
        )
        .order_by(
            Transaction.transaction_date.desc()
        )
        .limit(limit)
        .all()
    )

    result = []

    for transaction in transactions:

        result.append({
            "transaction_type": transaction.transaction_type,
            "amount": float(transaction.amount),
            "description": transaction.description,
            "transaction_date": transaction.transaction_date
        })

    return result