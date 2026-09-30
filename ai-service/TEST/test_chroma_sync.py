from app.services.chroma_sync_service import (
    rebuild_chroma_from_mysql
)

from app.services.chroma_service import (
    get_memory_count
)


print("\nBefore rebuild:")
print(
    "Chroma count:",
    get_memory_count()
)

rebuild_chroma_from_mysql()

print("\nAfter rebuild:")
print(
    "Chroma count:",
    get_memory_count()
)