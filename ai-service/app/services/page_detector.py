from typing import Optional


PAGE_MAP = {
    "dashboard": "/dashboard",
    "account": "/account",
    "transactions": "/transactions",
    "cards": "/cards",
    "credit_cards": "/credit-cards",
    "loans": "/loans",
    "loan_details": "/loans/details",
    "fd": "/fd",
    "fd_details": "/fd/details",
    "emi_calculator": "/emi-calculator",
    "kyc": "/kyc",
    "profile": "/profile",
    "change_password": "/change-password",
    "support": "/support",
    "offers": "/offers"
}


def detect_page(message: str) -> Optional[dict]:

    text = message.lower().strip()

    # Dashboard
    if any(word in text for word in [
        "dashboard",
        "home page",
        "home screen",
        "main page"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "dashboard",
            "route": PAGE_MAP["dashboard"]
        }

    # Account
    if any(word in text for word in [
        "my account",
        "account details",
        "account information",
        "account page"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "account",
            "route": PAGE_MAP["account"]
        }

    # Transactions
    if any(word in text for word in [
        "transactions",
        "transaction history",
        "transaction page",
        "payment history",
        "recent transactions"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "transactions",
            "route": PAGE_MAP["transactions"]
        }

    # Debit Cards
    if any(word in text for word in [
        "my card",
        "my cards",
        "debit card",
        "debit cards",
        "card page"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "cards",
            "route": PAGE_MAP["cards"]
        }

    # Credit Cards
    if any(word in text for word in [
        "credit card",
        "credit cards",
        "credit card page"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "credit_cards",
            "route": PAGE_MAP["credit_cards"]
        }

    # Loans
    if any(word in text for word in [
        "my loan",
        "my loans",
        "loan page",
        "loans page"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "loans",
            "route": PAGE_MAP["loans"]
        }

    # Loan Details
    if any(word in text for word in [
        "loan details",
        "loan information",
        "loan detail"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "loan_details",
            "route": PAGE_MAP["loan_details"]
        }

    # Fixed Deposit
    if any(word in text for word in [
        "fixed deposit",
        "fixed deposits",
        "fd",
        "my fd"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "fd",
            "route": PAGE_MAP["fd"]
        }

    # FD Details
    if any(word in text for word in [
        "fd details",
        "fd information",
        "fixed deposit details"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "fd_details",
            "route": PAGE_MAP["fd_details"]
        }

    # EMI Calculator
    if any(word in text for word in [
        "emi calculator",
        "calculate emi",
        "emi calculation",
        "calculate my emi"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "emi_calculator",
            "route": PAGE_MAP["emi_calculator"]
        }

    # KYC
    if any(word in text for word in [
        "kyc",
        "kyc page",
        "kyc details",
        "verification page"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "kyc",
            "route": PAGE_MAP["kyc"]
        }

    # Profile
    if any(word in text for word in [
        "my profile",
        "profile page",
        "profile"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "profile",
            "route": PAGE_MAP["profile"]
        }

    # Change Password
    if any(word in text for word in [
    "change password",
    "change my password",
    "update password",
    "update my password",
    "password page",
    "change the password"
      ]):
      
     return {
            "type": "NAVIGATION",
            "page": "change_password",
            "route": PAGE_MAP["change_password"]
        }

    # Support
    if any(word in text for word in [
        "support",
        "help page",
        "customer support",
        "contact support"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "support",
            "route": PAGE_MAP["support"]
        }

    # Offers
    if any(word in text for word in [
        "offers",
        "offer page",
        "special offers",
        "bank offers"
    ]):
        return {
            "type": "NAVIGATION",
            "page": "offers",
            "route": PAGE_MAP["offers"]
        }

    return None