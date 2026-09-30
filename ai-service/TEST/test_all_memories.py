from app.database.connection import SessionLocal
from app.database.models import Memory


db = SessionLocal()

try:

    memories = (
        db.query(Memory)
        .filter(Memory.user_id == 2)
        .order_by(Memory.id)
        .all()
    )

    print("\n========== MYSQL MEMORIES ==========\n")

    for memory in memories:

        print("ID:", memory.id)
        print("Content:", memory.content)
        print("Type:", memory.memory_type)
        print("Importance:", memory.importance)
        print("-----------------------------------")

finally:
    db.close()