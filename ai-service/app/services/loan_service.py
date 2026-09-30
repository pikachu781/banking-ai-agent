from sqlalchemy.orm import Session

from app.database.models import Loan


def get_loan_status(
    db: Session,
    user_id: int
) -> dict | None:

    loan = (
        db.query(Loan)
        .filter(
            Loan.user_id == user_id
        )
        .first()
    )

    if loan is None:
        return None

    return {
        "loan_type": loan.loan_type,
        "principal_amount": float(loan.principal_amount),
        "interest_rate": float(loan.interest_rate),
        "tenure_months": loan.tenure_months,
        "outstanding_amount": float(loan.outstanding_amount),
        "status": loan.status
    }