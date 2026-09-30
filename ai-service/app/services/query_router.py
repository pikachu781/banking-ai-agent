# ============================================================
# QUERY ROUTER
# ============================================================
#
# Main query classification:
#
# REALTIME   -> current/live banking information
# RETRIEVAL  -> user's stored memory / RAG information
# TASK       -> calculation or action/tool request
# GENERAL    -> normal conversation / knowledge question
#
# ============================================================


# ============================================================
# MAIN ROUTER
# ============================================================

def classify_query(query: str) -> str:
    """
    Classify the user's query into:

    REALTIME
    RETRIEVAL
    TASK
    GENERAL
    """

    text = query.lower().strip()

    print("\n========== QUERY ROUTER ==========")
    print(f"Question: {query}")

    # ========================================================
    # EMPTY QUERY
    # ========================================================

    if not text:
        print("Detected: GENERAL")
        return "GENERAL"

    # ========================================================
    # 1. REALTIME QUERY
    # ========================================================
    #
    # Information that can change and should come from
    # current/live banking data.
    # ========================================================

    realtime_words = [

        # Balance
        "current balance",
        "account balance",
        "available balance",
        "my balance",

        # Current status
        "current status",
        "account status",
        "card status",
        "loan status",
        "fd status",

        # Current transactions
        "latest transaction",
        "recent transaction",
        "last transaction",
        "today's transaction",
        "today transaction",
        "recent transactions",

       # Current banking information
     "current interest rate",
      "interest rate",
    "fd interest rate",
    "loan interest rate",
    "fixed deposit interest rate",
    "fixed deposit rate",
    "loan rate",
     "current fd rate",
     "current loan rate",
    "interest rate on my fd",
    "interest rate on my loan",
     "interest rate on my fixed deposit",

    # Card status
    "card status",
    "my card status",
    "is my card active",
    "is my card blocked",
    "card active",
    "card blocked",
    "debit card status",
    "credit card status",

    "card details",
    "my card details",
     "card number",
    "my card number",
   "what card do i have",
   "what type of card do i have",
  "debit or credit card",
    "debit card or credit card",


    #loan status

    "loan status",
    "my loan status",
    "loan balance",
     "loan outstanding",
     "outstanding loan",
     "outstanding loan amount",
    "loan outstanding amount",
    "how much loan do i have",
    "how much loan is left",
    "how much loan do i have left",
   "remaining loan",
   "remaining loan amount",
     "loan remaining",
        #account details
        "account details",
       "my account details",
        "account number",
       "ifsc",
        "branch"


     "account status",
    "my account status",
     "is my account active",
     "is my account blocked",
     "account active",
    "account blocked",
    "bank account status",
    "is my bank account active",

    ]

    for word in realtime_words:

        if word in text:

            print("Detected: REALTIME")
            return "REALTIME"

    # ========================================================
    # 2. TASK QUERY
    # ========================================================
    #
    # User wants the system to calculate or perform an action.
    # ========================================================

    task_words = [
         "fd",
       "fixed deposit",
       "fixed-deposit",
       "fd interest",
       "fixed deposit interest",
        "calculate fd",
        "calculate fd interest",

        # EMI
        "emi",
        "emi calculator",
        "calculate emi",
        "calculate loan emi",
        "loan emi",
        "calculate my emi",
        "calculate my loan emi",

          

        # Calculations
        "calculate",
        "calculate fd",
        "calculate interest",
        "calculate emi",
        "calculate maturity",
        "compute",
        "find emi",
        "find interest",

        # Banking actions
        "transfer",
        "send money",
        "pay",
        "payment",
        "create fd",
        "open fd",
        "close fd",
        "block card",
        "unblock card",
        "change pin",
        "add beneficiary",
        "remove beneficiary",

        # Account operations
        "book",
        "apply",
        "request",
        "cancel",
    ]

    for word in task_words:

        if word in text:

            print("Detected: TASK")
            return "TASK"

    # ========================================================
    # 3. RETRIEVAL QUERY
    # ========================================================
    #
    # Information that already exists in user's memory/RAG.
    # ========================================================

    retrieval_words = [

        # Skills
        "my skills",
        "what skills do i know",
        "what technologies do i know",
        "what technology do i know",
        "what programming languages do i know",
        "what frameworks do i know",

        # Learning
        "what am i learning",
        "what am i currently learning",
        "what am i learning recently",
        "what am i learning now",
        "what i am learning",
        "what do i learn",

        # Goals
        "my goals",
        "what are my goals",
        "what do i want to learn",
        "what do i want to achieve",

        # Projects
        "my projects",
        "what projects do i have",
        "what projects have i worked on",

        # Profession
        "my profession",
        "what is my profession",
        "what do i do",

        # Personal information
        "my name",
        "what is my name",
        "what's my name",

    ]

    for word in retrieval_words:

        if word in text:

            print("Detected: RETRIEVAL")
            return "RETRIEVAL"

    # ========================================================
    # RETRIEVAL FALLBACK WORDS
    # ========================================================

    # Questions clearly asking about the user's own stored data.

    personal_words = [
        "about me",
        "do you know me",
        "what do you know about me",
        "my information",
        "my details",
        "my profile",
    ]

    for word in personal_words:

        if word in text:

            print("Detected: RETRIEVAL")
            return "RETRIEVAL"

    # ========================================================
    # 4. GENERAL QUERY
    # ========================================================
    #
    # Everything else goes to general AI reasoning.
    # ========================================================

    print("Detected: GENERAL")

    return "GENERAL"


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_queries = [

        "What is my current balance?",

        "What skills do I know?",

        "What am I currently learning?",

        "What are my goals?",

        "What projects do I have?",

        "Calculate FD interest for 2 lakh",

        "Calculate my loan EMI",

        "Transfer 500 rupees to Rahul",

        "What is my name?",

        "Explain Java polymorphism",

        "Hello",

    ]

    print("\n\n==============================")
    print("QUERY ROUTER TEST")
    print("==============================")

    for question in test_queries:

        result = classify_query(question)

        print(
            f"Result: {result}"
        )

        print(
            "------------------------------"
        )
        