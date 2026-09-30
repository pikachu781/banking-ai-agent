
from app.providers.gemini_provider import GeminiProvider


# ============================================================
# GENERATE RESPONSE
# ============================================================

def generate_response(
    message: str,
    history: list,
    memory_context: str = "",
    query_type: str = "GENERAL"
) -> str:

    print(
        f"\n========== AI RESPONSE TYPE: {query_type} =========="
    )

    # ========================================================
    # 1. REALTIME QUERY
    # ========================================================

    if query_type == "REALTIME":

        print(
            "\n========== REALTIME QUERY =========="
        )

        return (
            "Realtime banking services are not connected yet."
        )

    # ========================================================
    # 2. TASK QUERY
    # ========================================================

    if query_type == "TASK":

        print(
            "\n========== TASK QUERY =========="
        )

        return (
            "Banking task tools are not connected yet."
        )

    # ========================================================
    # 3. RETRIEVAL QUERY
    # ========================================================

    if query_type == "RETRIEVAL":

        print(
            "\n========== RETRIEVAL QUERY =========="
        )

        return generate_memory_response(
            message=message,
            memory_context=memory_context
        )

    # ========================================================
    # 4. GENERAL QUERY
    # ========================================================

    if query_type == "GENERAL":

        print(
            "\n========== GENERAL QUERY =========="
        )

        return generate_general_response(
            message=message,
            history=history
        )

    # ========================================================
    # SAFETY FALLBACK
    # ========================================================

    return generate_general_response(
        message=message,
        history=history
    )


# ============================================================
# GENERAL AI RESPONSE
# ============================================================

def generate_general_response(
    message: str,
    history: list
) -> str:

    messages = []

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    system_prompt = """
You are a helpful AI assistant.

Answer the user's question using your general knowledge.

IMPORTANT RULES:

1. Answer the question directly.

2. You may explain general concepts such as:
   - Java
   - Python
   - programming
   - mathematics
   - technology
   - education
   - general knowledge

3. Do NOT require user memory to answer a general question.

4. Do NOT say that you lack user memories when the question
   is a general knowledge question.

5. Do NOT mention internal systems, RAG, embeddings,
   databases, routing, or implementation details.

6. Give a clear and useful answer suitable for the user's
   question.

7. If the user asks for an explanation, explain it simply
   with an example when useful.
"""

    messages.append({
        "role": "system",
        "content": system_prompt
    })

    # ========================================================
    # ADD RECENT CONVERSATION HISTORY
    # ========================================================

    if history:

        for item in history:

            role = item.get("role")
            content = item.get("content")

            if role in ["user", "assistant"] and content:

                messages.append({
                    "role": role,
                    "content": content
                })

    # ========================================================
    # CURRENT QUESTION
    # ========================================================

    messages.append({
        "role": "user",
        "content": message
    })

    # ========================================================
    # GEMINI
    # ========================================================

    provider = GeminiProvider()

    response = provider.generate_response(
        messages
    )

    return response


# ============================================================
# RETRIEVAL / MEMORY RESPONSE
# ============================================================

def generate_memory_response(
    message: str,
    memory_context: str
) -> str:

    messages = []

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    system_prompt = """
You are a helpful AI assistant.

You may receive verified long-term memories about the user.

IMPORTANT RULES:

1. Use ONLY the verified long-term memories provided
   in the current prompt for user-specific questions.

2. Do NOT use previous conversation history as a source
   of verified user facts.

3. Do NOT invent user-specific information.

4. If there is not enough relevant verified memory,
   clearly say that you do not have enough information.

5. Do NOT use unrelated memories.

6. Do NOT mention internal memory systems, embeddings,
   databases, RAG, or implementation details.

============================================================
SKILL QUESTIONS
============================================================

If the user asks:

"What technologies do I know?"

"What are my skills?"

"What programming languages do I know?"

"What frameworks do I know?"

Then:

- List ALL relevant skills present in the verified memories.
- Do NOT mention only one skill.
- Do NOT ignore other supplied skills.
- Do NOT invent skills that are not present.

============================================================
RECENT LEARNING QUESTIONS
============================================================

If the user asks:

"What am I learning recently?"

"What am I currently learning?"

"What am I learning now?"

Then use the memories supplied for recent/current learning.

Do NOT include future goals unless the user explicitly asks
about goals.

============================================================
GOAL QUESTIONS
============================================================

If a memory says:

"User wants to learn Docker in the future"

then this is a GOAL.

Do NOT describe Docker as a technology the user currently
knows or is currently learning.

============================================================
GENERAL RULE
============================================================

Use the verified memories as the source of truth.

Never guess.

Never add information that is not present.
"""

    messages.append({
        "role": "system",
        "content": system_prompt
    })

    # ========================================================
    # USER PROMPT
    # ========================================================

    user_prompt = f"""
VERIFIED LONG-TERM USER MEMORIES:

{memory_context}

CURRENT USER QUESTION:

{message}

============================================================
ANSWERING INSTRUCTIONS
============================================================

Answer the current question using ONLY the relevant
verified memories above.

If this is an ALL-SKILLS question, include EVERY relevant
skill from the provided memories.

If this is a RECENT-LEARNING question, include the relevant
recent/current learning memories only.

Do not use unrelated memories.

Do not guess.

Do not invent information.
"""

    messages.append({
        "role": "user",
        "content": user_prompt
    })

    # ========================================================
    # GEMINI
    # ========================================================

    provider = GeminiProvider()

    response = provider.generate_response(
        messages
    )

    return response

