from app.services.embedding_service import get_embedding
from app.services.chroma_service import search_memories


user_id = 1

question = "What career am I preparing for?"


print("Question:")
print(question)


# Convert question into a vector
query_embedding = get_embedding(question)

print("\nQuery embedding generated!")
print("Vector length:", len(query_embedding))


# Search ChromaDB
results = search_memories(
    embedding=query_embedding,
    user_id=user_id,
    n_results=5
)


print("\nSearch completed!")

print("\nDocuments found:")

for document in results["documents"][0]:
    print("-", document)