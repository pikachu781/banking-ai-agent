from app.services.memory_conflict_service import (
    classify_memory_conflict
)

existing_memory = (
    "I am preparing for a Java backend developer role."
)

new_memory = (
    "I have switched my career goal to becoming "
    "a Python data scientist."
)

result = classify_memory_conflict(
    existing_memory=existing_memory,
    new_memory=new_memory
)


print("\nExisting:")
print(existing_memory)

print("\nNew:")
print(new_memory)

print("\nDecision:")
print(result["decision"])

print("\nReason:")
print(result["reason"])