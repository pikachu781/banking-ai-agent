from sqlalchemy.orm import Session

from app.services.chroma_service import (
    delete_memory_from_chroma
)

from app.database.models import (
    Conversation,
    Message,
    Memory
)


# ============================================================
# CONVERSATION
# ============================================================

def get_or_create_conversation(
    db: Session,
    user_id: int
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.id.desc()
        )
        .first()
    )

    if conversation:
        return conversation

    conversation = Conversation(
        user_id=user_id
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


# ============================================================
# MESSAGE
# ============================================================

def save_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str
):

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_history(
    db: Session,
    conversation_id: int
):

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.id.asc()
        )
        .all()
    )

    return [
        {
            "role": message.role,
            "content": message.content
        }
        for message in messages
    ]


# ============================================================
# LONG-TERM MEMORY
# ============================================================

def save_memory(
    db: Session,
    user_id: int,
    content: str,
    memory_type: str = "GENERAL",
    importance: int = 5
):
    """
    Save a new active memory to MySQL.

    New memories are active by default.
    """

    memory = Memory(
        user_id=user_id,
        content=content,
        memory_type=memory_type,
        importance=importance,
        active=True
    )

    # --------------------------------------------------------
    # Save to MySQL
    # --------------------------------------------------------

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


# ============================================================
# GET MEMORIES
# ============================================================

def get_memories(
    db: Session,
    user_id: int,
    active_only: bool = True
):
    """
    Get memories belonging to a user.

    By default, only active memories are returned.
    """

    query = (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id
        )
    )

    # --------------------------------------------------------
    # Only active memories
    # --------------------------------------------------------

    if active_only:

        query = query.filter(
            Memory.active == True
        )

    memories = (
        query
        .order_by(
            Memory.importance.desc(),
            Memory.id.desc()
        )
        .all()
    )

    return [
        {
            "id": memory.id,

            "content": memory.content,

            "memory_type": memory.memory_type,

            "importance": memory.importance,

            "active": memory.active
        }
        for memory in memories
    ]


# ============================================================
# DEACTIVATE MEMORY
# ============================================================

def deactivate_memory(
    db: Session,
    user_id: int,
    memory_id: int
):
    """
    Mark a memory as inactive.

    The memory remains in MySQL for historical purposes.

    It is also removed from ChromaDB so normal semantic
    search will not retrieve it.
    """

    # ========================================================
    # 1. FIND MEMORY
    # ========================================================

    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == user_id
        )
        .first()
    )

    if not memory:
        return False

    # ========================================================
    # 2. MARK INACTIVE
    # ========================================================

    memory.active = False

    db.commit()
    db.refresh(memory)

    # ========================================================
    # 3. REMOVE FROM CHROMADB
    # ========================================================

    delete_memory_from_chroma(
        memory_id=memory_id
    )

    return True


# ============================================================
# DELETE MEMORY
# ============================================================

def delete_memory(
    db: Session,
    user_id: int,
    memory_id: int
):
    """
    Permanently delete a memory.

    Use this only when the memory should be completely removed.
    """

    # ========================================================
    # 1. FIND MEMORY
    # ========================================================

    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == user_id
        )
        .first()
    )

    if not memory:
        return False

    # ========================================================
    # 2. DELETE FROM MYSQL
    # ========================================================

    db.delete(memory)
    db.commit()

    # ========================================================
    # 3. DELETE FROM CHROMADB
    # ========================================================

    delete_memory_from_chroma(
        memory_id=memory_id
    )

    return True


# ============================================================
# UPDATE MEMORY
# ============================================================

def update_memory(
    db: Session,
    user_id: int,
    memory_id: int,
    content: str,
    memory_type: str = "GENERAL",
    importance: int = 5
):
    """
    Update an existing memory.

    Updated memories remain active.
    """

    # ========================================================
    # 1. FIND MEMORY
    # ========================================================

    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == user_id
        )
        .first()
    )

    if not memory:
        return None

    # ========================================================
    # 2. UPDATE MEMORY
    # ========================================================

    memory.content = content

    memory.memory_type = memory_type

    memory.importance = importance

    # ========================================================
    # 3. MAKE SURE MEMORY IS ACTIVE
    # ========================================================

    memory.active = True

    # ========================================================
    # 4. SAVE
    # ========================================================

    db.commit()
    db.refresh(memory)

    return memory


# ============================================================
# ACTIVATE MEMORY
# ============================================================

def activate_memory(
    db: Session,
    user_id: int,
    memory_id: int
):
    """
    Reactivate an inactive memory.
    """

    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == user_id
        )
        .first()
    )

    if not memory:
        return False

    memory.active = True

    db.commit()
    db.refresh(memory)

    return memory
# ============================================================
# REPLACE MEMORY
# ============================================================

def replace_memory(
    db: Session,
    user_id: int,
    old_memory_id: int,
    new_content: str,
    memory_type: str = "GENERAL",
    importance: int = 5
):
    """
    Deactivate the old memory and create a new active memory.

    Old memory:
        active = False

    New memory:
        active = True
    """

    # ========================================================
    # 1. FIND OLD MEMORY
    # ========================================================

    old_memory = (
        db.query(Memory)
        .filter(
            Memory.id == old_memory_id,
            Memory.user_id == user_id
        )
        .first()
    )

    if not old_memory:
        return None

    # ========================================================
    # 2. DEACTIVATE OLD MEMORY
    # ========================================================

    old_memory.active = False

    db.commit()

    # ========================================================
    # 3. CREATE NEW MEMORY
    # ========================================================

    new_memory = Memory(
        user_id=user_id,
        content=new_content,
        memory_type=memory_type,
        importance=importance,
        active=True
    )

    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)

    # ========================================================
    # 4. REMOVE OLD MEMORY FROM CHROMADB
    # ========================================================

    delete_memory_from_chroma(
        memory_id=old_memory.id
    )

    # ========================================================
    # 5. RETURN NEW MEMORY
    # ========================================================

    return new_memory