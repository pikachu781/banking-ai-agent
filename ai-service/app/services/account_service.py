from sqlalchemy.orm import Session

from app.database.models import BankAccount


def get_account_details(
    db: Session,
    user_id: int
) -> dict | None:

    account = (
        db.query(BankAccount)
        .filter(
            BankAccount.user_id == user_id
        )
        .first()
    )

    if account is None:
        return None

    return {
        "account_number": account.account_number,
        "account_type": account.account_type,
        "branch_name": account.branch_name,
        "ifsc_code": account.ifsc_code
    }