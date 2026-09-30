import json
import re

from app.providers.gemini_provider import GeminiProvider


# ============================================================
# GEMINI PROVIDER
# ============================================================

gemini = GeminiProvider()


# ============================================================
# FAST MEMORY EXTRACTION
# ============================================================

def fast_extract_memory(message: str):

    text = message.strip()
    lower = text.lower()

    # ========================================================
    # NAME
    # ========================================================

    name_match = re.match(
        r"^(?:my name is|i am|i'm)\s+([A-Za-z][A-Za-z0-9 _-]{1,40})[.!]?$",
        text,
        re.IGNORECASE
    )

    if name_match and lower.startswith(
        ("my name is", "i am ", "i'm ")
    ):

        name = name_match.group(1).strip()

        # Avoid treating common sentences as names
        blocked = {
            "learning",
            "studying",
            "working",
            "building",
            "using",
            "trying"
        }

        if name.lower() not in blocked:

            return {
                "should_remember": True,
                "memories": [
                    {
                        "content": f"User's name is {name}",
                        "memory_type": "PERSONAL_INFO",
                        "importance": 5
                    }
                ]
            }


    # ========================================================
    # CURRENT LEARNING
    # ========================================================

    learning_patterns = [
        r"i am learning (.+)",
        r"i'm learning (.+)",
        r"iam learning (.+)",
        r"i am currently learning (.+)",
        r"i'm currently learning (.+)",
        r"i started learning (.+)",
        r"i am studying (.+)",
        r"i'm studying (.+)",
        r"i am practicing (.+)",
        r"i'm practicing (.+)"
    ]

    for pattern in learning_patterns:

        match = re.match(
            pattern,
            lower
        )

        if match:

            skills_text = match.group(1).strip()

            skills_text = re.sub(
                r"[.!?]+$",
                "",
                skills_text
            )

            # Multiple skills
            skills = re.split(
                r",|\band\b",
                skills_text
            )

            memories = []

            for skill in skills:

                skill = skill.strip()

                if not skill:
                    continue

                memories.append({
                    "content": f"User is learning {skill}",
                    "memory_type": "SKILL",
                    "importance": 8
                })

            if memories:

                return {
                    "should_remember": True,
                    "memories": memories
                }


    # ========================================================
    # CURRENT JOB / PROFESSION
    # ========================================================

    profession_patterns = [
        r"i am working as (.+)",
        r"i'm working as (.+)",
        r"i currently work as (.+)",
        r"i am a (.+) developer",
        r"i'm a (.+) developer"
    ]

    for pattern in profession_patterns:

        match = re.match(
            pattern,
            lower
        )

        if match:

            profession = match.group(1).strip()

            profession = re.sub(
                r"[.!?]+$",
                "",
                profession
            )

            return {
                "should_remember": True,
                "memories": [
                    {
                        "content": f"User works as {profession}",
                        "memory_type": "PROFESSION",
                        "importance": 9
                    }
                ]
            }


    # ========================================================
    # PROJECT
    # ========================================================

    project_patterns = [
        r"i am building (.+)",
        r"i'm building (.+)",
        r"i created (.+)",
        r"i built (.+)",
        r"i am working on (.+)",
        r"i'm working on (.+)"
    ]

    for pattern in project_patterns:

        match = re.match(
            pattern,
            lower
        )

        if match:

            project = match.group(1).strip()

            project = re.sub(
                r"[.!?]+$",
                "",
                project
            )

            return {
                "should_remember": True,
                "memories": [
                    {
                        "content": f"User is working on {project}",
                        "memory_type": "PROJECT",
                        "importance": 8
                    }
                ]
            }


    # ========================================================
    # NO FAST MATCH
    # ========================================================

    return None


# ============================================================
# GEMINI MEMORY EXTRACTION
# ============================================================

def extract_memories(message: str):

    # ========================================================
    # FAST PATH
    # ========================================================

    fast_result = fast_extract_memory(message)

    if fast_result is not None:

        print(
            "\n========== FAST MEMORY EXTRACTION =========="
        )

        print(
            fast_result
        )

        return fast_result


    # ========================================================
    # GEMINI FALLBACK
    # ========================================================

    print(
        "\n========== GEMINI MEMORY EXTRACTION =========="
    )

    prompt = f"""
You are a STRICT user-memory extraction system.

Extract ONLY useful factual information explicitly
stated by the user.

Allowed memory types:

GOAL
SKILL
INTEREST
PROJECT
PROFESSION
PREFERENCE
PERSONAL_INFO

Rules:

1. Only remember information explicitly stated by the user.
2. Never guess.
3. Never create memories from questions.
4. Never create memories from general requests.
5. Keep memories short and specific.
6. If the user explicitly says they are learning,
   studying, practicing, or using a technology,
   classify it as SKILL.
7. A future career direction is GOAL.
8. A current or past job is PROFESSION.
9. A project the user is building or built is PROJECT.
10. Personal facts such as name are PERSONAL_INFO.
11. If multiple skills are explicitly mentioned,
    create separate memories.
12. Return only valid JSON.

Examples:

"I am learning Python"

{{
    "should_remember": true,
    "memories": [
        {{
            "content": "User is learning Python",
            "memory_type": "SKILL",
            "importance": 8
        }}
    ]
}}

"I want to become a Java developer"

{{
    "should_remember": true,
    "memories": [
        {{
            "content": "User wants to become a Java developer",
            "memory_type": "GOAL",
            "importance": 9
        }}
    ]
}}

"What is Python?"

{{
    "should_remember": false,
    "memories": []
}}

USER MESSAGE:

{message}
"""

    try:

        response = gemini.generate_response(
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = json.loads(response)

        if not isinstance(result, dict):

            return {
                "should_remember": False,
                "memories": []
            }

        if not result.get("should_remember"):

            return {
                "should_remember": False,
                "memories": []
            }

        memories = result.get(
            "memories",
            []
        )

        if not isinstance(memories, list):

            return {
                "should_remember": False,
                "memories": []
            }

        valid_memories = []

        allowed_types = {
            "GOAL",
            "SKILL",
            "INTEREST",
            "PROJECT",
            "PROFESSION",
            "PREFERENCE",
            "PERSONAL_INFO"
        }

        forbidden_phrases = [
            "[your name]",
            "[user_name]",
            "[user name]",
            "not specified",
            "not mentioned",
            "unknown"
        ]

        for memory in memories:

            if not isinstance(memory, dict):
                continue

            content = str(
                memory.get("content", "")
            ).strip()

            memory_type = str(
                memory.get(
                    "memory_type",
                    ""
                )
            ).upper().strip()

            importance = memory.get(
                "importance",
                5
            )

            if not content:
                continue

            if memory_type not in allowed_types:
                continue

            lower_content = content.lower()

            if any(
                phrase in lower_content
                for phrase in forbidden_phrases
            ):
                continue

            try:

                importance = int(
                    importance
                )

            except (
                ValueError,
                TypeError
            ):

                importance = 5

            importance = max(
                1,
                min(10, importance)
            )

            valid_memories.append({
                "content": content,
                "memory_type": memory_type,
                "importance": importance
            })

        if not valid_memories:

            return {
                "should_remember": False,
                "memories": []
            }

        return {
            "should_remember": True,
            "memories": valid_memories
        }

    except Exception as e:

        print(
            f"Gemini memory extraction failed: {e}"
        )

        return {
            "should_remember": False,
            "memories": []
        }