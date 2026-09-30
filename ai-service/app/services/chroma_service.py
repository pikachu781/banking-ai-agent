import chromadb


# Create persistent ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Create or get the memories collection
memory_collection = client.get_or_create_collection(
    name="memories"
)


def add_memory_to_chroma(
    memory_id: int,
    user_id: int,
    content: str,
    embedding: list[float],
    memory_type: str,
    importance: int,
    created_at,
    active: bool = True
):
    """
    Store a memory and its embedding in ChromaDB.
    """

    memory_collection.upsert(
        ids=[str(memory_id)],
        embeddings=[embedding],
        documents=[content],
        metadatas=[
            {
                "memory_id": memory_id,
                "user_id": user_id,
                "memory_type": memory_type,
                "importance": importance,
                "created_at": str(created_at),
                "active": active
            }
        ]
    )



def get_memory_count():
    """
    Return the number of memories stored in ChromaDB.
    """

    return memory_collection.count()

def search_memories(
    embedding: list[float],
    user_id: int,
    n_results: int = 5
):
    """
    Search ChromaDB for memories similar to the given embedding.
    Only memories belonging to the specified user are returned.
    """

    results = memory_collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        where={
         "$and": [
             {"user_id": user_id},
              {"active": True}
           ]
       }
    )

    return results
def find_similar_memory(
    embedding: list[float],
    user_id: int,
    n_results: int = 1
):
    """
    Find memories similar to the given embedding
    for the same user.
    """

    results = memory_collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
       where={
        "$and": [
           {"user_id": user_id},
          {"active": True}
       ]
       }
    )

    return results
def update_memory_in_chroma(
    memory_id: int,
    user_id: int,
    content: str,
    embedding: list[float],
    memory_type: str,
    importance: int,
    created_at,
    active: bool = True
):
    """
    Update an existing memory in ChromaDB.

    ChromaDB uses the same memory_id as MySQL.
    """

    memory_collection.upsert(
        ids=[str(memory_id)],
        embeddings=[embedding],
        documents=[content],
        metadatas=[
            {
                "memory_id": memory_id,
                "user_id": user_id,
                "memory_type": memory_type,
                "importance": importance,
                "created_at": str(created_at),
                "active": active
            }
        ]
    )
def delete_memory_from_chroma(memory_id: int):
    """
    Delete a memory from ChromaDB using its memory ID.
    """

    memory_collection.delete(
        ids=[str(memory_id)]
    )