from app.services.embedding_service import get_embedding


text = "I am preparing for a Java backend developer job."


embedding = get_embedding(text)


print("Text:")
print(text)

print("\nEmbedding generated successfully!")

print("Vector type:")
print(type(embedding))

print("\nVector length:")
print(len(embedding))

print("\nFirst 10 values:")
print(embedding[:10])