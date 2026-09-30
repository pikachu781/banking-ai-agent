from app.database.connection import SessionLocal
from app.database.models import Memory

from app.services.chroma_service import memory_collection


# Memories that were identified as invalid
BAD_MEMORY_IDS = [
    8,
    11,
    13,
    14,
    15,
    16,
    17,
    18
]


db = SessionLocal()

try:

    print("\n========== MEMORY CLEANUP ==========\n")

    for memory_id in BAD_MEMORY_IDS:

        # ------------------------------------------
        # 1. Find memory in MySQL
        # ------------------------------------------

        memory = (
            db.query(Memory)
            .filter(
                Memory.id == memory_id
            )
            .first()
        )

        if not memory:

            print(
                f"Memory {memory_id} "
                f"not found in MySQL"
            )

            continue

        print(
            f"Deleting memory {memory_id}:"
        )

        print(
            f"  {memory.content}"
        )

        # ------------------------------------------
        # 2. Delete from MySQL
        # ------------------------------------------

        db.delete(memory)

        # ------------------------------------------
        # 3. Delete from ChromaDB
        # ------------------------------------------

        memory_collection.delete(
            ids=[str(memory_id)]
        )

        print(
            "  Deleted from MySQL + ChromaDB"
        )

        print(
            "-----------------------------------"
        )

    # ------------------------------------------
    # 4. Save MySQL changes
    # ------------------------------------------

    db.commit()

    print(
        "\nCleanup completed successfully!"
    )

except Exception as e:

    db.rollback()

    print(
        f"\nCleanup failed: {e}"
    )

finally:

    db.close()