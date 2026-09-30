from datetime import datetime

from app.services.embedding_service import get_embedding
from app.services.chroma_service import search_memories
from app.services.query_intent_service import classify_query_intent

from app.database.connection import SessionLocal
from app.database.models import Memory


# ============================================================
# CONFIGURATION
# ============================================================

MAX_DISTANCE = 1.20


# ============================================================
# GET SKILLS FROM MYSQL
# ============================================================

def get_skills_from_mysql(
    user_id: int,
    recent_only: bool = False
):
    """
    Get skill memories directly from MySQL.

    MySQL is the source of truth for long-term memories.
    """

    db = SessionLocal()

    try:

        query = (
            db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.memory_type == "SKILL",
                Memory.active == True
            )
        )

        # ====================================================
        # RECENT SKILLS
        # ====================================================

        if recent_only:

            query = query.order_by(
                Memory.created_at.desc()
            )

            memories = query.limit(3).all()

        # ====================================================
        # ALL SKILLS
        # ====================================================

        else:

            query = query.order_by(
                Memory.created_at.asc()
            )

            memories = query.all()

        result = []

        for memory in memories:

            result.append({

                "content": memory.content,

                "memory_type": memory.memory_type,

                "importance": memory.importance,

                "created_at": memory.created_at,

                "distance": 0.0,

                "similarity_score": 1.0,

                "importance_score":
                    memory.importance / 10,

                "recency_score": 0.0,

                "final_score": 1.0
            })

        return result

    finally:

        db.close()


# ============================================================
# RETRIEVE RELEVANT MEMORIES
# ============================================================

def retrieve_relevant_memories(
    question: str,
    user_id: int,
    n_results: int = 5
):
    """
    Retrieve memories based on query intent.
    """

    try:

        # ========================================================
        # 1. CLASSIFY QUERY INTENT
        # ========================================================

        intent = classify_query_intent(
            question
        )

        print(
            f"\n========== QUERY INTENT: {intent} ==========\n"
        )

        # ========================================================
        # 2. GENERAL QUERY
        # ========================================================
        #
        # IMPORTANT:
        # General questions do not need RAG.
        #
        # Example:
        #   hii
        #   hello
        #   how are you
        #   what is Java
        #
        # Skip embedding + Chroma search.
        # ========================================================

        if intent == "GENERAL":

            print(
                "\n========== GENERAL QUERY =========="
            )

            print(
                "Skipping memory retrieval."
            )

            return []

        # ========================================================
        # 3. RECENT SKILLS
        # ========================================================

        if intent == "RECENT_SKILLS":

            memories = get_skills_from_mysql(
                user_id=user_id,
                recent_only=True
            )

            print(
                "\n========== RECENT SKILLS ==========\n"
            )

            for memory in memories:

                print(
                    f"Skill: {memory['content']}"
                )

                print(
                    f"Created: {memory['created_at']}"
                )

                print(
                    "-----------------------------------"
                )

            return memories

        # ========================================================
        # 4. ALL SKILLS
        # ========================================================

        if intent == "ALL_SKILLS":

            memories = get_skills_from_mysql(
                user_id=user_id,
                recent_only=False
            )

            print(
                "\n========== ALL USER SKILLS ==========\n"
            )

            for memory in memories:

                print(
                    f"Skill: {memory['content']}"
                )

                print(
                    f"Created: {memory['created_at']}"
                )

                print(
                    "-----------------------------------"
                )

            return memories

        # ========================================================
        # 5. NORMAL SEMANTIC RAG
        # ========================================================

        question_embedding = get_embedding(
            question
        )

        results = search_memories(
            embedding=question_embedding,
            user_id=user_id,
            n_results=n_results
        )

        documents = results.get(
            "documents",
            [[]]
        )

        distances = results.get(
            "distances",
            [[]]
        )

        metadatas = results.get(
            "metadatas",
            [[]]
        )

        if not documents or not documents[0]:

            return []

        memories = []

        # ========================================================
        # 6. PROCESS CHROMA RESULTS
        # ========================================================

        for i, document in enumerate(
            documents[0]
        ):

            distance = distances[0][i]

            metadata = metadatas[0][i]

            memory_type = metadata.get(
                "memory_type",
                "GENERAL"
            )

            # ====================================================
            # INTENT FILTERING
            # ====================================================

            if intent == "GOALS":

                if memory_type != "GOAL":
                    continue

            elif intent == "PROJECTS":

                if memory_type != "PROJECT":
                    continue

            elif intent == "PROFESSION":

                if memory_type != "PROFESSION":
                    continue

            # ====================================================
            # DISTANCE FILTERING
            # ====================================================

            if distance > MAX_DISTANCE:

                continue

            # ====================================================
            # IMPORTANCE
            # ====================================================

            importance = int(
                metadata.get(
                    "importance",
                    5
                )
            )

            # ====================================================
            # CREATED AT
            # ====================================================

            created_at = metadata.get(
                "created_at"
            )

            # ====================================================
            # RECENCY SCORE
            # ====================================================

            recency_score = 0.0

            if created_at:

                try:

                    created_date = (
                        datetime.fromisoformat(
                            str(created_at)
                        )
                    )

                    now = datetime.now()

                    age_days = (
                        now - created_date
                    ).total_seconds() / 86400

                    recency_score = max(
                        0.0,
                        1.0 - (
                            age_days / 365
                        )
                    )

                except Exception:

                    recency_score = 0.0

            # ====================================================
            # SIMILARITY SCORE
            # ====================================================

            similarity_score = max(
                0.0,
                1.0 - distance
            )

            # ====================================================
            # IMPORTANCE SCORE
            # ====================================================

            importance_score = (
                importance / 10
            )

            # ====================================================
            # FINAL SCORE
            # ====================================================

            final_score = (
                similarity_score * 0.60
                +
                importance_score * 0.25
                +
                recency_score * 0.15
            )

            memories.append({

                "content": document,

                "distance": distance,

                "memory_type": memory_type,

                "importance": importance,

                "created_at": created_at,

                "similarity_score":
                    similarity_score,

                "importance_score":
                    importance_score,

                "recency_score":
                    recency_score,

                "final_score":
                    final_score
            })

        # ========================================================
        # 7. SORT MEMORIES
        # ========================================================

        memories.sort(
            key=lambda memory:
                memory["final_score"],
            reverse=True
        )

        # ========================================================
        # 8. PRINT MEMORY RANKING
        # ========================================================

        print(
            "\n========== MEMORY RANKING ==========\n"
        )

        for memory in memories:

            print(
                f"Memory: "
                f"{memory['content']}"
            )

            print(
                f"Type: "
                f"{memory['memory_type']}"
            )

            print(
                f"Distance: "
                f"{memory['distance']}"
            )

            print(
                f"Final Score: "
                f"{memory['final_score']}"
            )

            print(
                "-----------------------------------"
            )

        return memories

    except Exception as e:

        print(
            f"Memory retrieval failed: {e}"
        )

        return []


# ============================================================
# BUILD MEMORY CONTEXT
# ============================================================

def build_memory_context(
    question: str,
    user_id: int,
    n_results: int = 5
):
    """
    Build verified memory context for the AI model.
    """

    memories = retrieve_relevant_memories(
        question=question,
        user_id=user_id,
        n_results=n_results
    )

    # ========================================================
    # NO MEMORY FOUND
    # ========================================================

    if not memories:

        return (
            "No relevant memory was found "
            "for this question."
        )

    # ========================================================
    # DETERMINE INTENT
    # ========================================================

    # We do NOT call classify_query_intent() again here.
    #
    # retrieve_relevant_memories() already classified it.
    #
    # For now we determine the special context by checking
    # the retrieved memory structure.
    # ========================================================

    first_memory = memories[0]

    # ========================================================
    # RECENT / ALL SKILLS
    # ========================================================

    if all(
        memory.get("memory_type") == "SKILL"
        for memory in memories
    ):

        context = "\n".join(
            f"- {memory['content']}"
            for memory in memories
        )

        return (
            "VERIFIED USER SKILLS:\n"
            f"{context}\n\n"
            "These are verified user skill memories. "
            "Use them directly when relevant."
        )

    # ========================================================
    # NORMAL CONTEXT
    # ========================================================

    context = "\n".join(
        f"- {memory['content']}"
        for memory in memories
    )

    return context