from app.services.embedding_service import get_embedding
from app.services.chroma_service import search_memories


question = "What am I learning now?"

user_id = 2


embedding = get_embedding(question)


results = search_memories(
    embedding=embedding,
    user_id=user_id,
    n_results=10
)


print("\n========== RAW CHROMA RESULT ==========\n")

print("Documents:")
print(results.get("documents"))

print("\nDistances:")
print(results.get("distances"))

print("\nMetadata:")
print(results.get("metadatas"))

print("\nIDs:")
print(results.get("ids"))