from app.services.chroma_service import memory_collection


results = memory_collection.get(
    include=["documents", "metadatas"]
)


print("\n========== CHROMA MEMORIES ==========\n")


for i in range(len(results["ids"])):

    print("ID:", results["ids"][i])

    print(
        "Content:",
        results["documents"][i]
    )

    print(
        "Metadata:",
        results["metadatas"][i]
    )

    print("-----------------------------------")