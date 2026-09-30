import ollama


MODEL = "nomic-embed-text"


def get_embedding(text: str):
    response = ollama.embed(
        model=MODEL,
        input=text
    )

    return response["embeddings"][0]


text1 = "I am preparing for a Java backend developer job."

text2 = "I want to become a Java backend engineer."

text3 = "I love eating pizza."


embedding1 = get_embedding(text1)
embedding2 = get_embedding(text2)
embedding3 = get_embedding(text3)


print("Embedding 1 length:", len(embedding1))
print("Embedding 2 length:", len(embedding2))
print("Embedding 3 length:", len(embedding3))