from app.services.embedding_service import get_embedding

from app.services.chroma_service import (
    find_similar_memory,
    update_memory_in_chroma
)

from app.services.memory_service import update_memory


# ============================================================
# CONFIGURATION
# ============================================================

DUPLICATE_THRESHOLD = 0.90


# ============================================================
# FIND SIMILAR MEMORY
# ============================================================

def find_existing_memory(
    content: str,
    user_id: int
):
    """
    Find an existing memory that is semantically
    similar to the new memory.
    """

    # Generate embedding for new memory
    embedding = get_embedding(content)

    # Search ChromaDB
    results = find_similar_memory(
        embedding=embedding,
        user_id=user_id,
        n_results=1
    )

    # No results
    if not results.get("documents"):
        return None

    if not results["documents"][0]:
        return None

    # Get distance
    distance = results["distances"][0][0]

    # Similar enough
    if distance <= (1 - DUPLICATE_THRESHOLD):

        memory_id = results["metadatas"][0][0]["memory_id"]

        return {
            "memory_id": memory_id,
            "distance": distance
        }

    return None


# ============================================================
# DUPLICATE CHECK
# ============================================================

def check_duplicate_memory(
    content: str,
    user_id: int
):
    """
    Check whether a similar memory already exists.
    """

    existing = find_existing_memory(
        content=content,
        user_id=user_id
    )

    if existing:

        return {
            "is_duplicate": True,
            "existing_memory_id": existing["memory_id"],
            "distance": existing["distance"]
        }

    return {
        "is_duplicate": False,
        "existing_memory_id": None,
        "distance": None
    }


# ============================================================
# UPDATE MEMORY
# ============================================================

def update_existing_memory(
    db,
    user_id: int,
    memory_id: int,
    content: str,
    memory_type: str,
    importance: int
):
    """
    Update memory in MySQL and synchronize ChromaDB.
    """

    # --------------------------------------------------------
    # 1. Update MySQL
    # --------------------------------------------------------

    updated_memory = update_memory(
        db=db,
        user_id=user_id,
        memory_id=memory_id,
        content=content,
        memory_type=memory_type,
        importance=importance
    )

    if not updated_memory:
        return None

    # --------------------------------------------------------
    # 2. Generate new embedding
    # --------------------------------------------------------

    embedding = get_embedding(
        updated_memory.content
    )

    # --------------------------------------------------------
    # 3. Update ChromaDB
    # --------------------------------------------------------

    update_memory_in_chroma(
        memory_id=updated_memory.id,
        user_id=updated_memory.user_id,
        content=updated_memory.content,
        embedding=embedding,
        memory_type=updated_memory.memory_type,
        importance=updated_memory.importance,
        created_at=updated_memory.created_at,
        active=updated_memory.active
    )

    return updated_memory