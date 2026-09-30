from sqlalchemy.orm import Session

from app.database.models import FixedDeposit, Loan


def get_fd_interest_rate(
    db: Session,
    user_id: int
) -> dict | None:

    fd = (
        db.query(FixedDeposit)
        .filter(
            FixedDeposit.user_id == user_id,
            FixedDeposit.status == "ACTIVE"
        )
        .first()
    )

    if fd is None:
        return None

    return {
        "interest_rate": float(fd.interest_rate),
        "principal_amount": float(fd.principal_amount),
        "tenure_months": fd.tenure_months
    }


def get_loan_interest_rate(
    db: Session,
    user_id: int
) -> dict | None:

    loan = (
        db.query(Loan)
        .filter(
            Loan.user_id == user_id,
            Loan.status == "ACTIVE"
        )
        .first()
    )

    if loan is None:
        return None

    return {
        "interest_rate": float(loan.interest_rate),
        "loan_type": loan.loan_type,
        "principal_amount": float(loan.principal_amount),
        "tenure_months": loan.tenure_months
    }