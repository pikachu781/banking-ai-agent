from app.services.navigation_search import search_navigation


TEST_CASES = [

    (
        "Where can I see my spending?",
        "/transactions"
    ),

    (
        "I want to check where my money went",
        "/transactions"
    ),

    (
        "Where can I see my account information?",
        "/account"
    ),

    (
        "I want to manage my cards",
        "/cards"
    ),

    (
        "Where can I see my credit card information?",
        "/credit-cards"
    ),

    (
        "I want to check my loan",
        "/loans"
    ),

    (
        "Show me my fixed deposit information",
        "/fd"
    ),

    (
        "I want to calculate my monthly loan payment",
        "/emi-calculator"
    ),

    (
        "Where can I verify my identity?",
        "/kyc"
    ),

    (
        "I want to see my personal information",
        "/profile"
    ),

    (
        "Where can I update my password?",
        "/change-password"
    ),

    (
        "I need help with banking",
        "/support"
    ),

    (
        "Are there any bank deals?",
        "/offers"
    )
]


print("\n========== AI NAVIGATION SEARCH TEST ==========\n")


for message, expected_route in TEST_CASES:

    result = search_navigation(message)

    print(f"User: {message}")
    print(f"Detected: {result}")

    if result and result["route"] == expected_route:
        print("✅ PASS")
    else:
        print(
            f"❌ FAIL - Expected: {expected_route}"
        )

    print("-" * 60)


from app.services.navigation_intent import is_navigation_request


def test_navigation_intent():

    navigation_tests = [
        "Open my account",
        "Go to my card",
        "Open my card page",
        "Navigate to transactions",
        "Show account page",
        "Go to my profile",
        "Open dashboard",
    ]

    data_tests = [
        "Show my balance",
        "What is my balance?",
        "Show my card",
        "Is my card active?",
        "Show my card details",
        "Show my transactions",
        "What is my account information?",
    ]

    for message in navigation_tests:

        result = is_navigation_request(message)

        print(
            f"{message} -> {result}"
        )

        assert result is True


    for message in data_tests:

        result = is_navigation_request(message)

        print(
            f"{message} -> {result}"
        )

        assert result is False


if __name__ == "__main__":

    test_navigation_intent()

    print("\nAll navigation intent tests passed.")