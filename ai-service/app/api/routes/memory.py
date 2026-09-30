from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.memory_service import (
    save_memory,
    get_memories,
    delete_memory
)

router = APIRouter(
    prefix="/api/memory",
    tags=["Memory"]
)


# ============================================================
# CREATE MEMORY
# ============================================================

@router.post("/{user_id}")
def create_memory(
    user_id: int,
    content: str,
    memory_type: str = "GENERAL",
    importance: int = 5,
    db: Session = Depends(get_db)
):

    memory = save_memory(
        db=db,
        user_id=user_id,
        content=content,
        memory_type=memory_type,
        importance=importance
    )

    return {
        "success": True,
        "message": "Memory saved successfully",
        "memory": {
            "id": memory.id,
            "content": memory.content,
            "memory_type": memory.memory_type,
            "importance": memory.importance
        }
    }


# ============================================================
# GET USER MEMORIES
# ============================================================

@router.get("/{user_id}")
def read_memories(
    user_id: int,
    db: Session = Depends(get_db)
):

    memories = get_memories(
        db=db,
        user_id=user_id
    )

    return {
        "success": True,
        "count": len(memories),
        "memories": memories
    }


# ============================================================
# DELETE MEMORY
# ============================================================

@router.delete("/{user_id}/{memory_id}")
def remove_memory(
    user_id: int,
    memory_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_memory(
        db=db,
        user_id=user_id,
        memory_id=memory_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    return {
        "success": True,
        "message": "Memory deleted successfully"
    }