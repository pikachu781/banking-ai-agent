# ============================================================
# REALTIME INTENT SERVICE
# ============================================================


def detect_realtime_intent(message: str) -> str:

    message_lower = message.lower().strip()

    # ============================================
    # TRANSACTIONS
    # ============================================

    transaction_keywords = [
        "transaction",
        "transactions",
        "recent transaction",
        "recent transactions",
        "latest transaction",
        "latest transactions",
        "last transaction",
        "last transactions",
        "transaction history",
        "payment history"
    ]

    if any(
        keyword in message_lower
        for keyword in transaction_keywords
    ):
        return "TRANSACTIONS"

    # ============================================
    # BALANCE
    # ============================================

    balance_keywords = [
        "balance",
        "account balance",
        "current balance",
        "available balance"
    ]

    if any(
        keyword in message_lower
        for keyword in balance_keywords
    ):
        return "BALANCE"

    # ============================================
    # INTEREST RATE
    # ============================================

    interest_keywords = [
        "interest rate",
        "current interest",
        "fd rate",
        "fd interest",
        "fd interest rate",
        "fixed deposit rate",
        "fixed deposit interest",
        "fixed deposit interest rate",
        "loan rate",
        "loan interest",
        "loan interest rate",
        "current fd rate",
        "current loan rate"
    ]

    if any(
        keyword in message_lower
        for keyword in interest_keywords
    ):
        return "INTEREST_RATE"

    # ============================================
    # ACCOUNT DETAILS
    # ============================================

    account_keywords = [
        "account details",
        "my account details",
        "account number",
        "ifsc",
        "branch"
    ]

    if any(
        keyword in message_lower
        for keyword in account_keywords
    ):
        return "ACCOUNT_DETAILS"

    # ============================================
    # CARD STATUS
    # ============================================

    card_keywords = [
        "card status",
        "my card status",
        "is my card active",
        "is my card blocked",
        "card active",
        "card blocked",
        "debit card status",
        "credit card status"
    ]

    if any(
        keyword in message_lower
        for keyword in card_keywords
    ):
        return "CARD_STATUS"


    # ============================================
# CARD DETAILS
# ============================================
    card_details_keywords = [
    "card details",
    "my card details",
    "card number",
    "my card number",
    "what card do i have",
    "what type of card do i have",
    "debit or credit card",
    "debit card or credit card"
]

    if any(
    keyword in message_lower
    for keyword in card_details_keywords
):
      return "CARD_DETAILS"

        # ============================================
    # LOAN STATUS
    # ============================================

    loan_status_keywords = [
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
        "loan remaining"
    ]

    if any(
        keyword in message_lower
        for keyword in loan_status_keywords
    ):
        return "LOAN_STATUS"


    # ============================================
# ACCOUNT STATUS
# ============================================

    account_status_keywords = [
    "account status",
    "my account status",
    "is my account active",
    "is my account blocked",
    "account active",
    "account blocked",
    "bank account status",
    "is my bank account active"
]

    if any(
    keyword in message_lower
    for keyword in account_status_keywords
):
       return "ACCOUNT_STATUS"

    # ============================================
    # UNKNOWN REALTIME QUERY
    # ============================================

    return "UNKNOWN"


# ============================================================
# INTEREST RATE TYPE
# ============================================================


def detect_interest_rate_type(message: str) -> str:

    message_lower = message.lower().strip()

    # ============================================
    # FIXED DEPOSIT
    # ============================================

    fd_keywords = [
        "fd",
        "fixed deposit",
        "fixed deposits",
        "fd interest",
        "fd rate",
        "fixed deposit interest",
        "fixed deposit rate"
    ]

    if any(
        keyword in message_lower
        for keyword in fd_keywords
    ):
        return "FD"

    # ============================================
    # LOAN
    # ============================================

    loan_keywords = [
        "loan",
        "loans",
        "loan interest",
        "loan rate",
        "personal loan",
        "home loan",
        "car loan",
        "education loan"
    ]

    if any(
        keyword in message_lower
        for keyword in loan_keywords
    ):
        return "LOAN"


    

    # ============================================
    # UNKNOWN
    # ============================================

    return "UNKNOWN"