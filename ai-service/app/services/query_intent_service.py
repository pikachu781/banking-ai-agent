import json
import ollama


ALLOWED_INTENTS = {
    "RECENT_SKILLS",
    "ALL_SKILLS",
    "GOALS",
    "PROJECTS",
    "PROFESSION",
    "GENERAL"
}


# ============================================================
# FAST GENERAL QUERY DETECTION
# ============================================================

def is_obviously_general(question: str) -> bool:

    text = question.lower().strip()

    casual_messages = {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "hey there",
        "good morning",
        "good afternoon",
        "good evening",
        "good night",
        "thanks",
        "thank you",
        "ok",
        "okay",
        "bye",
        "goodbye",
        "yo"
    }

    if text in casual_messages:
        return True

    general_phrases = [
        "how are you",
        "how are you doing",
        "what's up",
        "whats up",
        "who are you",
        "what can you do",
        "tell me about yourself"
    ]

    for phrase in general_phrases:

        if phrase in text:
            return True

    return False


# ============================================================
# FAST PERSONAL INTENT DETECTION
# ============================================================

def fast_personal_intent(question: str):

    text = question.lower().strip()

    print(
        "\n========== FAST INTENT CHECK =========="
    )

    print(
        f"Question: {text}"
    )

    # --------------------------------------------------------
    # RECENT SKILLS
    # --------------------------------------------------------

    recent_skill_phrases = [

        "what am i learning",
        "what am i currently learning",
        "what am i learning currently",
        "what am i learning now",
        "what am i learning recently",

        "what am i currently learn",
        "what am i curently learn",
        "what am i learn",

        "which skills am i learning",
        "which technology am i learning",
        "which technologies am i learning",

        "what skills am i learning",
        "what technologies am i learning"
    ]

    for phrase in recent_skill_phrases:

        if phrase in text:

            print(
                "Detected intent: RECENT_SKILLS"
            )

            return "RECENT_SKILLS"


    # --------------------------------------------------------
    # TYPING MISTAKE / FLEXIBLE LEARNING DETECTION
    # --------------------------------------------------------

    if "learn" in text or "learning" in text:

        learning_words = [
            "currently",
            "curently",
            "recently",
            "recent",
            "now"
        ]

        for word in learning_words:

            if word in text:

                print(
                    "Detected intent: RECENT_SKILLS"
                )

                return "RECENT_SKILLS"


    # --------------------------------------------------------
    # ALL SKILLS
    # --------------------------------------------------------

    all_skill_phrases = [

        "what technologies do i know",
        "what technology do i know",
        "what skills do i know",
        "what are my skills",
        "what are all my skills",

        "what programming languages do i know",
        "what frameworks do i know",

        "list my skills",
        "show my skills",
        "show all my skills",
        "list all my skills"
    ]

    for phrase in all_skill_phrases:

        if phrase in text:

            print(
                "Detected intent: ALL_SKILLS"
            )

            return "ALL_SKILLS"


    # --------------------------------------------------------
    # GOALS
    # --------------------------------------------------------

    goal_phrases = [

        "what are my goals",
        "what is my goal",
        "what are my future goals",

        "what do i want to learn",
        "what do i want to achieve",

        "what am i planning to learn",
        "what am i planning to achieve"
    ]

    for phrase in goal_phrases:

        if phrase in text:

            print(
                "Detected intent: GOALS"
            )

            return "GOALS"


    # --------------------------------------------------------
    # PROJECTS
    # --------------------------------------------------------

    project_phrases = [

        "what are my projects",
        "what projects am i working on",
        "what projects do i have",

        "show my projects",
        "list my projects",
        "tell me about my projects"
    ]

    for phrase in project_phrases:

        if phrase in text:

            print(
                "Detected intent: PROJECTS"
            )

            return "PROJECTS"


    # --------------------------------------------------------
    # PROFESSION / CAREER
    # --------------------------------------------------------

    profession_phrases = [

        "what is my career",
        "what is my career goal",
        "what career am i preparing for",

        "what job am i preparing for",
        "what role am i preparing for",

        "what profession am i preparing for",

        "what do i want to become",
        "what job do i want"
    ]

    for phrase in profession_phrases:

        if phrase in text:

            print(
                "Detected intent: PROFESSION"
            )

            return "PROFESSION"


    # --------------------------------------------------------
    # NOTHING MATCHED
    # --------------------------------------------------------

    print(
        "No fast intent detected."
    )

    return None


# ============================================================
# QUERY INTENT CLASSIFICATION
# ============================================================

def classify_query_intent(question: str) -> str:

    # ========================================================
    # FAST GENERAL
    # ========================================================

    if is_obviously_general(question):

        print(
            "\n========== FAST GENERAL DETECTION =========="
        )

        print(
            "Skipping Ollama intent classification."
        )

        return "GENERAL"


    # ========================================================
    # FAST PERSONAL
    # ========================================================

    fast_intent = fast_personal_intent(question)

    if fast_intent:

        print(
            "\n========== FAST PERSONAL INTENT =========="
        )

        print(
            f"Detected intent: {fast_intent}"
        )

        print(
            "Skipping Ollama intent classification."
        )

        return fast_intent


    # ========================================================
    # OLLAMA FALLBACK
    # ========================================================

    print(
        "\n========== OLLAMA INTENT CLASSIFICATION =========="
    )

    prompt = f"""
You are a query intent classifier for a personal AI assistant.

Classify the user's question into exactly ONE intent.

Allowed intents:

RECENT_SKILLS
- Questions asking what the user is learning recently,
  currently learning, or started learning most recently.

ALL_SKILLS
- Questions asking about all technologies, skills,
  programming languages, frameworks, or concepts the user knows.

GOALS
- Questions about the user's goals, plans, or what
  they want to learn or achieve.

PROJECTS
- Questions about the user's projects or applications.

PROFESSION
- Questions about the user's career, profession,
  job direction, or role.

GENERAL
- Questions that do not match the above categories.

Return ONLY JSON:

{{
    "intent": "GENERAL"
}}

USER QUESTION:
{question}
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

        result = json.loads(
            response["message"]["content"]
        )

        intent = result.get(
            "intent",
            "GENERAL"
        ).upper()

        if intent not in ALLOWED_INTENTS:

            return "GENERAL"

        return intent

    except Exception as e:

        print(
            f"Query intent classification failed: {e}"
        )

        return "GENERAL"