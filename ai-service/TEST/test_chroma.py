from app.services.embedding_service import get_embedding

from app.services.chroma_service import (
    add_memory_to_chroma,
    get_memory_count,
    memory_collection
)


memory_id = 1
user_id = 1

content = "I am preparing for a Java backend developer job."

memory_type = "GOAL"
importance = 9


# Generate embedding
embedding = get_embedding(content)

print("Embedding generated!")
print("Vector length:", len(embedding))

print("\nFirst 10 generated vector values:")
print(embedding[:10])


# Store in ChromaDB
add_memory_to_chroma(
    memory_id=memory_id,
    user_id=user_id,
    content=content,
    embedding=embedding,
    memory_type=memory_type,
    importance=importance
)

print("\nMemory stored in ChromaDB!")


# Count memories
count = get_memory_count()

print("\nChromaDB memory count:", count)


# Get stored data from ChromaDB
results = memory_collection.get(
    ids=[str(memory_id)],
    include=[
        "documents",
        "metadatas",
        "embeddings"
    ]
)


print("\nNumber of memories:", len(results["ids"]))


for i in range(len(results["ids"])):

    print("\n-----------------------------")

    print("Chroma ID:")
    print(results["ids"][i])

    print("\nMemory:")
    print(results["documents"][i])

    print("\nMetadata:")
    print(results["metadatas"][i])

    print("\nVector length:")
    print(len(results["embeddings"][i]))

    print("\nFirst 10 vector values:")
    print(results["embeddings"][i][:10])