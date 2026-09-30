from app.database.connection import SessionLocal
from app.database.models import Memory

from app.services.chroma_service import memory_collection


db = SessionLocal()

try:

    memories = db.query(Memory).all()

    print("\n========== CHROMA MIGRATION ==========\n")

    for memory in memories:

        memory_id = str(memory.id)

        # Check if memory exists in Chroma
        result = memory_collection.get(
            ids=[memory_id],
            include=["documents", "metadatas"]
        )

        if not result["ids"]:
            print(
                f"Memory {memory.id} not found in Chroma"
            )
            continue

        # Get existing Chroma metadata
        metadata = result["metadatas"][0]

        # Add/update created_at
        metadata["created_at"] = str(
            memory.created_at
        )

        # Keep existing values
        metadata["memory_id"] = memory.id
        metadata["user_id"] = memory.user_id
        metadata["memory_type"] = memory.memory_type
        metadata["importance"] = memory.importance

        # Update Chroma metadata
        memory_collection.update(
            ids=[memory_id],
            metadatas=[metadata]
        )

        print(
            f"Updated memory {memory.id}"
        )

    print("\nMigration completed!")

finally:

    db.close()