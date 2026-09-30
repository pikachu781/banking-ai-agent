# ============================================================
# FD CALCULATOR
# ============================================================

def calculate_fd(
    principal: float,
    rate: float,
    years: float
) -> dict:

    # Simple interest calculation
    interest = principal * (rate / 100) * years

    maturity_amount = principal + interest

    return {
        "principal": round(principal, 2),
        "rate": rate,
        "years": years,
        "interest": round(interest, 2),
        "maturity_amount": round(maturity_amount, 2)
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = calculate_fd(
        principal=200000,
        rate=7,
        years=2
    )

    print("\n========== FD CALCULATOR ==========")

    print(f"Principal: ₹{result['principal']:,.2f}")
    print(f"Interest Rate: {result['rate']}%")
    print(f"Tenure: {result['years']} years")
    print(f"Interest: ₹{result['interest']:,.2f}")
    print(f"Maturity Amount: ₹{result['maturity_amount']:,.2f}")