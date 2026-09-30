import json
import ollama


def classify_memory_conflict(
    existing_memory: str,
    new_memory: str
):
    """
    Compare an existing memory with a new memory.

    Returns:
    DUPLICATE
    UPDATE
    NEW
    """

    existing = existing_memory.lower().strip()
    new = new_memory.lower().strip()

    # ========================================================
    # RULE-BASED UPDATE DETECTION
    # ========================================================

    update_phrases = [
        "i have switched",
        "i switched",
        "i changed my",
        "i have changed my",
        "i changed from",
        "i have changed from",
        "i moved to",
        "i have moved to",
        "i no longer",
        "i don't use",
        "i do not use",
        "instead of",
        "replaced",
        "my new goal",
        "my current goal",
        "i am now preparing for",
        "i now want to become",
        "i now want to be",
        "changed career goal",
        "changed my career",
        "switched career",
        "switched my career"
    ]

    for phrase in update_phrases:

        if phrase in new:

            return {
                "decision": "UPDATE",
                "reason": (
                    "The new memory explicitly indicates "
                    "that the previous information has changed."
                )
            }

    # ========================================================
    # CAREER GOAL UPDATE DETECTION
    # ========================================================

    career_terms = [
        "career goal",
        "career",
        "become a",
        "become an",
        "want to become",
        "wants to become",
        "plan to become",
        "preparing for",
        "career direction",
        "future profession"
    ]

    existing_is_career = any(
        term in existing
        for term in career_terms
    )

    new_is_career = any(
        term in new
        for term in career_terms
    )

    if existing_is_career and new_is_career:

        return {
            "decision": "UPDATE",
            "reason": (
                "Both memories describe the user's "
                "career direction, so the new career "
                "goal replaces the previous one."
            )
        }

    # ========================================================
    # LLM CLASSIFICATION
    # ========================================================

    # ========================================================
    # LLM CLASSIFICATION
    # ========================================================

    prompt = f"""
You are a strict memory conflict classifier.

Compare the EXISTING MEMORY with the NEW MEMORY.

EXISTING MEMORY:
{existing_memory}

NEW MEMORY:
{new_memory}

Choose exactly ONE:

DUPLICATE
UPDATE
NEW

==================================================
DUPLICATE
==================================================

Choose DUPLICATE when both memories describe
essentially the SAME fact.

Examples:

Existing:
User is learning Python.

New:
User is currently learning Python.

Decision:
DUPLICATE


Existing:
User wants to become a Java developer.

New:
User wants to become a Java backend developer.

Decision:
DUPLICATE

==================================================
UPDATE
==================================================

Choose UPDATE when the new memory changes,
replaces, switches, abandons, or gives a new value
for the SAME type of user fact.

IMPORTANT:

A new value for the SAME user fact should be UPDATE
even if the new memory does not explicitly say
"changed" or "switched".

Examples:

Existing:
User wants to become a Java developer.

New:
User wants to become a Python developer.

Decision:
UPDATE

Reason:
Both are career goals and the new career direction
replaces the previous career goal.


Existing:
User is currently working as a Java developer.

New:
User is currently working as a Python developer.

Decision:
UPDATE

Reason:
Both describe the user's current profession,
but the profession changed.


Existing:
User's preferred programming language is Java.

New:
User prefers Python.

Decision:
UPDATE

Reason:
Both describe the same preference category,
but the preferred value changed.


Existing:
User's current project is a food management system.

New:
User's current project is a voice AI agent.

Decision:
UPDATE

Reason:
Both describe the user's current main project,
so the new project replaces the previous one.


Existing:
User's career goal is backend development.

New:
User's career goal is data science.

Decision:
UPDATE

==================================================
NEW
==================================================

Choose NEW when the new memory is a separate fact
and does NOT replace the existing memory.

Examples:

Existing:
User is learning Java.

New:
User is learning Python.

Decision:
NEW

Reason:
The user can learn both technologies.


Existing:
User wants to become a Java developer.

New:
User is learning Docker.

Decision:
NEW

Reason:
A career goal and a learning skill are different facts.


Existing:
User is working on a food management system.

New:
User is working on a voice AI agent.

Decision:
NEW

Reason:
The user can work on multiple projects.

==================================================
IMPORTANT RULES
==================================================

1. Do NOT treat every different value as UPDATE.

2. Different skills are normally NEW.

3. Different interests are normally NEW.

4. Different projects are normally NEW unless the
   memories clearly describe the SAME current/main
   project.

5. Different career goals are UPDATE when the new goal
   represents the user's new career direction.

6. Different professions are UPDATE when they describe
   the user's current profession/job and the new one
   replaces the old one.

7. If the user can have both facts at the same time,
   choose NEW.

8. If the new memory is essentially the same fact,
   choose DUPLICATE.

9. If the new memory changes the value of the same
   user fact, choose UPDATE.

10. Do not invent information.

Return ONLY valid JSON.

Format:

{{
    "decision": "DUPLICATE",
    "reason": "short explanation"
}}

Allowed values:

DUPLICATE
UPDATE
NEW
"""

    try:

        response = ollama.chat(
            model="mistral:latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json"
        )

        content = response["message"]["content"]

        result = json.loads(content)

        decision = result.get(
            "decision",
            "NEW"
        ).upper().strip()

        if decision not in [
            "DUPLICATE",
            "UPDATE",
            "NEW"
        ]:
            decision = "NEW"

        return {
            "decision": decision,
            "reason": result.get(
                "reason",
                ""
            )
        }

    except Exception as e:

        print(
            f"Memory conflict classification failed: {e}"
        )

        return {
            "decision": "NEW",
            "reason": "Memory conflict classification failed"
        }