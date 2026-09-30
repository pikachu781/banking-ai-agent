from app.database.connection import SessionLocal
from app.database.models import Memory

from app.services.embedding_service import get_embedding

from app.services.chroma_service import (
    memory_collection,
    add_memory_to_chroma
)


def rebuild_chroma_from_mysql():
    """
    Rebuild ChromaDB from MySQL.

    MySQL is the source of truth.

    Only active memories are stored in ChromaDB.
    Inactive memories remain in MySQL for history.
    """

    db = SessionLocal()

    try:

        print(
            "\n========== CHROMA REBUILD ==========\n"
        )

        # ====================================================
        # 1. GET ALL MEMORIES FROM MYSQL
        # ====================================================

        memories = (
            db.query(Memory)
            .order_by(
                Memory.id.asc()
            )
            .all()
        )

        print(
            f"Found {len(memories)} memories in MySQL."
        )

        # ====================================================
        # 2. CLEAR OLD CHROMA RECORDS
        # ====================================================

        print(
            "Clearing old ChromaDB records..."
        )

        if memory_collection.count() > 0:

            existing = memory_collection.get()

            existing_ids = existing.get(
                "ids",
                []
            )

            if existing_ids:

                memory_collection.delete(
                    ids=existing_ids
                )

        print(
            "Old ChromaDB records cleared."
        )

        # ====================================================
        # 3. SYNC ACTIVE MEMORIES
        # ====================================================

        active_count = 0
        inactive_count = 0

        for memory in memories:

            print(
                f"Checking Memory ID: {memory.id} "
                f"| active={memory.active}"
            )

            # ------------------------------------------------
            # SKIP INACTIVE MEMORY
            # ------------------------------------------------

            if not memory.active:

                inactive_count += 1

                print(
                    f"Skipping inactive Memory ID: "
                    f"{memory.id}"
                )

                continue

            # ------------------------------------------------
            # CREATE EMBEDDING
            # ------------------------------------------------

            embedding = get_embedding(
                memory.content
            )

            # ------------------------------------------------
            # ADD TO CHROMADB
            # ------------------------------------------------

            add_memory_to_chroma(
                memory_id=memory.id,
                user_id=memory.user_id,
                content=memory.content,
                embedding=embedding,
                memory_type=memory.memory_type,
                importance=memory.importance,
                created_at=memory.created_at,
                active=memory.active
            )

            active_count += 1

        # ====================================================
        # 4. RESULT
        # ====================================================

        print(
            "\n===================================="
        )

        print(
            f"Active memories synced: "
            f"{active_count}"
        )

        print(
            f"Inactive memories skipped: "
            f"{inactive_count}"
        )

        print(
            f"ChromaDB total: "
            f"{memory_collection.count()}"
        )

        print(
            "ChromaDB rebuild completed."
        )

        print(
            "====================================\n"
        )

    except Exception as e:

        print(
            f"ChromaDB rebuild failed: {e}"
        )

        raise

    finally:

        db.close()