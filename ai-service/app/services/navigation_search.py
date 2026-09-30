from typing import Optional


# ============================================================
# AI NAVIGATION SEARCH
# ============================================================

NAVIGATION_INTENTS = {

    "dashboard": {
        "route": "/dashboard",
        "keywords": [
            "home",
            "home screen",
            "main screen",
            "main page",
            "banking home",
            "bank homepage",
            "homepage",
            "where do i start"
        ]
    },

    "account": {
        "route": "/account",
        "keywords": [
            "account information",
            "account info",
            "account details",
            "bank account",
            "my bank account",
            "account information page",
            "see my account"
        ]
    },

    "transactions": {
        "route": "/transactions",
        "keywords": [
            "spending",
            "spent",
            "money spent",
            "where my money went",
            "money going",
            "payments",
            "payment history",
            "money history",
            "expense history",
            "expenses",
            "spending history",
            "see my spending",
            "check my spending"
        ]
    },

    "cards": {
    "route": "/cards",
    "keywords": [
        "manage my cards",
        "manage cards",
        "my debit card",
        "debit card information",
        "debit card details",
        "card information",
        "card management",

        # Navigation commands
        "open card",
        "open cards",
        "open my card",
        "open my cards",
        "open card page",
        "open cards page",
        "open my card page",
        "open my cards page",
        "go to card",
        "go to cards",
        "go to my card",
        "go to my cards",
        "card page",
        "cards page"
    ]
},

    "credit_cards": {
        "route": "/credit-cards",
        "keywords": [
            "credit card information",
            "credit card details",
            "manage credit card",
            "my credit card",
            "credit card management"
        ]
    },

    "loans": {
        "route": "/loans",
        "keywords": [
            "loan information",
            "loan details",
            "my loan information",
            "manage my loan",
            "loan management",
            "check my loan",
            "see my loan"
        ]
    },

    "loan_details": {
        "route": "/loans/details",
        "keywords": [
            "detailed loan information",
            "loan full details",
            "loan detail page",
            "detailed information about my loan"
        ]
    },

    "fd": {
        "route": "/fd",
        "keywords": [
            "fixed deposit information",
            "my fixed deposit",
            "fixed deposit account",
            "fd information",
            "my fd",
            "manage my fd"
        ]
    },

    "fd_details": {
        "route": "/fd/details",
        "keywords": [
            "fixed deposit details",
            "fd detailed information",
            "fd full details",
            "detailed fd information"
        ]
    },

    "emi_calculator": {
        "route": "/emi-calculator",
        "keywords": [
            "loan calculator",
            "loan emi",
            "calculate loan payment",
            "monthly loan payment",
            "monthly payment calculator",
            "calculate monthly payment",
            "emi tool"
        ]
    },

    "kyc": {
        "route": "/kyc",
        "keywords": [
            "verification",
            "identity verification",
            "verify my identity",
            "verification details",
            "kyc information",
            "kyc verification",
            "check my kyc"
        ]
    },

    "profile": {
        "route": "/profile",
        "keywords": [
            "my personal information",
            "personal details",
            "personal information",
            "my details",
            "user profile",
            "profile information",
            "manage my profile"
        ]
    },

    "change_password": {
        "route": "/change-password",
        "keywords": [
            "update my password",
            "reset my password",
            "password settings",
            "password management",
            "change login password",
            "modify my password"
        ]
    },

    "support": {
        "route": "/support",
        "keywords": [
            "need help",
            "get help",
            "customer help",
            "talk to support",
            "contact customer service",
            "customer service",
            "banking help",
            "need assistance"
        ]
    },

    "offers": {
        "route": "/offers",
        "keywords": [
            "bank deals",
            "banking deals",
            "available offers",
            "available deals",
            "special deals",
            "discounts",
            "bank discounts",
            "promotions",
            "bank promotions"
        ]
    }
}


def search_navigation(message: str) -> Optional[dict]:

    if not message:
        return None

    text = message.lower().strip()

    # ========================================================
    # EXACT / PHRASE MATCH
    # ========================================================

    sorted_pages = sorted(
    NAVIGATION_INTENTS.items(),
    key=lambda x: len(
        max(x[1]["keywords"], key=len)
    ),
    reverse=True
)

    for page, data in sorted_pages:

        for keyword in data["keywords"]:

            if keyword in text:

                return {
                    "type": "NAVIGATION",
                    "page": page,
                    "route": data["route"],
                    "confidence": 0.90
                }

    # ========================================================
    # WORD-BASED FALLBACK
    # ========================================================

    words = set(text.split())

    # Spending / transaction intent
    if (
        "spending" in words
        or "expenses" in words
        or "spent" in words
        or ("money" in words and "went" in words)
    ):
        return {
            "type": "NAVIGATION",
            "page": "transactions",
            "route": "/transactions",
            "confidence": 0.80
        }

    # Help intent
    if (
        "help" in words
        or "assistance" in words
    ):
        return {
            "type": "NAVIGATION",
            "page": "support",
            "route": "/support",
            "confidence": 0.80
        }

    # Verification intent
    if (
        "verification" in words
        or "verify" in words
    ):
        return {
            "type": "NAVIGATION",
            "page": "kyc",
            "route": "/kyc",
            "confidence": 0.80
        }

    return None