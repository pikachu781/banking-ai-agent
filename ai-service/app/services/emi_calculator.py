# ============================================================
# EMI CALCULATOR
# ============================================================

def calculate_emi(
    principal: float,
    annual_rate: float,
    years: float
) -> dict:

    # Convert annual interest rate to monthly rate
    monthly_rate = annual_rate / 12 / 100

    # Convert years to months
    months = int(years * 12)

    # EMI formula
    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return {
        "principal": round(principal, 2),
        "annual_rate": round(annual_rate, 2),
        "years": round(years, 2),
        "months": months,
        "emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2)
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = calculate_emi(
        principal=500000,
        annual_rate=8.5,
        years=5
    )

    print("\n========== EMI CALCULATOR ==========")
    print(f"Loan Amount: ₹{result['principal']:,.2f}")
    print(f"Interest Rate: {result['annual_rate']}%")
    print(f"Tenure: {result['years']} years")
    print(f"Months: {result['months']}")
    print(f"Monthly EMI: ₹{result['emi']:,.2f}")
    print(f"Total Interest: ₹{result['total_interest']:,.2f}")
    print(f"Total Payment: ₹{result['total_payment']:,.2f}")