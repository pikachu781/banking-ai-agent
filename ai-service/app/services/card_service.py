from sqlalchemy.orm import Session

from app.database.models import Card


def get_card_status(
    db: Session,
    user_id: int
) -> dict | None:

    card = (
        db.query(Card)
        .filter(
            Card.user_id == user_id
        )
        .first()
    )

    if card is None:
        return None

    return {
        "card_type": card.card_type,
        "card_number": card.card_number,
        "status": card.status
    }