from app.services.page_detector import detect_page


tests = [
    "Show my transactions",
    "Open my account",
    "Show my debit card",
    "Open credit card",
    "Show my loan",
    "Show loan details",
    "Open my fixed deposit",
    "Calculate EMI",
    "Show my KYC",
    "Open my profile",
    "Change my password",
    "I need customer support",
    "Show me offers"
]


for message in tests:
    result = detect_page(message)

    print(f"\nUser: {message}")
    print(f"AI:   {result}")