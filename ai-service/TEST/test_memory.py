from app.services.memory_extractor import extract_memories


message = "I am preparing for a Java backend developer job."

result = extract_memories(message)

print(result)