# ============================================================
# TASK SERVICE
# ============================================================

import re

from app.services.fd_calculator import calculate_fd


# ============================================================
# ACTIVE TASK STORAGE
# ============================================================

TASK_SESSIONS = {}


# ============================================================
# START FD TASK
# ============================================================

def start_fd_task(user_id: int) -> dict:

    TASK_SESSIONS[user_id] = {
        "task": "FD_CALCULATOR",
        "mode": None,
        "amount": None,
        "rate": None,
        "tenure": None
    }

    return TASK_SESSIONS[user_id]


# ============================================================
# GET ACTIVE TASK
# ============================================================

def get_active_task(user_id: int):

    return TASK_SESSIONS.get(user_id)


# ============================================================
# CHECK ACTIVE TASK
# ============================================================

def has_active_task(user_id: int) -> bool:

    return user_id in TASK_SESSIONS


# ============================================================
# UPDATE FD TASK
# ============================================================

def update_fd_task(
    user_id: int,
    mode=None,
    amount=None,
    rate=None,
    tenure=None
):

    task = TASK_SESSIONS.get(user_id)

    if not task:
        return None

    if mode is not None:
        task["mode"] = mode

    if amount is not None:
        task["amount"] = amount

    if rate is not None:
        task["rate"] = rate

    if tenure is not None:
        task["tenure"] = tenure

    return task


# ============================================================
# CLEAR TASK
# ============================================================

def clear_task(user_id: int):

    TASK_SESSIONS.pop(user_id, None)


# ============================================================
# PARSE AMOUNT
# ============================================================

def parse_amount(text: str):

    text = text.lower().replace(",", "").strip()

    # ========================================================
    # LAKH
    # ========================================================

    lakh_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs)",
        text
    )

    if lakh_match:

        value = float(
            lakh_match.group(1)
        )

        return value * 100000

    # ========================================================
    # CRORE
    # ========================================================

    crore_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:crore|crores|cr)",
        text
    )

    if crore_match:

        value = float(
            crore_match.group(1)
        )

        return value * 10000000

    # ========================================================
    # NORMAL AMOUNT
    # ========================================================

    amount_match = re.search(
        r"(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)",
        text
    )

    if amount_match:

        value = float(
            amount_match.group(1)
        )

        return value

    return None


# ============================================================
# PARSE INTEREST RATE
# ============================================================

def parse_rate(text: str):

    text = text.lower().strip()

    # ========================================================
    # EXPLICIT RATE
    # ========================================================
    # 8%
    # 8 percent
    # 8 per cent
    # 7.5%

    rate_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:%|percent|per\s*cent)",
        text
    )

    if rate_match:

        return float(
            rate_match.group(1)
        )

    # ========================================================
    # PLAIN NUMBER
    # ========================================================
    # 8
    # 7.5
    #
    # IMPORTANT:
    # This is used only when the current task field
    # is asking for the interest rate.

    plain_number = re.fullmatch(
        r"\s*(\d+(?:\.\d+)?)\s*",
        text
    )

    if plain_number:

        return float(
            plain_number.group(1)
        )

    return None


# ============================================================
# PARSE TENURE
# ============================================================

def parse_tenure(text: str):

    text = text.lower().strip()

    # ========================================================
    # YEARS
    # ========================================================
    # 2 years
    # 2 year
    # 2 yrs
    # 6year

    year_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:year|years|yr|yrs)",
        text
    )

    if year_match:

        return float(
            year_match.group(1)
        )

    # ========================================================
    # MONTHS
    # ========================================================
    # 24 months
    # 24 month
    # 24 mos
    # 24mo

    month_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:month|months|mo|mos)",
        text
    )

    if month_match:

        months = float(
            month_match.group(1)
        )

        return months / 12

    # ========================================================
    # PLAIN NUMBER
    # ========================================================
    # If the AI is asking:
    #
    # "What is the FD tenure?"
    #
    # and user says:
    #
    # 2
    #
    # treat it as 2 years.

    plain_number = re.fullmatch(
        r"\s*(\d+(?:\.\d+)?)\s*",
        text
    )

    if plain_number:

        return float(
            plain_number.group(1)
        )

    return None


# ============================================================
# DETECT MODE
# ============================================================

def detect_fd_mode(message: str):

    text = message.lower().strip()

    manual_words = [
        "manual",
        "manually",
        "calculator",
        "use calculator"
    ]

    automatic_words = [
        "automatic",
        "automatically",
        "calculate here",
        "you calculate"
    ]

    for word in manual_words:

        if word in text:
            return "manual"

    for word in automatic_words:

        if word in text:
            return "automatic"

    return None


# ============================================================
# PROCESS FD TASK
# ============================================================

def process_fd_task(
    user_id: int,
    message: str
):

    task = get_active_task(user_id)

    if not task:

        return False, None

    text = message.lower().strip()

    # ========================================================
    # CANCEL TASK
    # ========================================================

    cancel_words = [
        "cancel",
        "stop",
        "cancel task",
        "stop task"
    ]

    for word in cancel_words:

        if word in text:

            clear_task(user_id)

            return True, (
                "Okay. I cancelled the FD calculation."
            )

    # ========================================================
    # FD MODE SELECTION
    # ========================================================

    if task["mode"] is None:

        mode = detect_fd_mode(message)

        if mode is None:

            return True, (
                "Sure. Would you like to calculate "
                "it manually using the FD calculator, "
                "or should I calculate it for you here?"
            )

        update_fd_task(
            user_id,
            mode=mode
        )

        # ----------------------------------------------------
        # MANUAL
        # ----------------------------------------------------

        if mode == "manual":

            return True, (
                "Sure. Manual FD calculator selected. "
                "The FD calculator will open so you can "
                "enter the amount, interest rate and tenure."
            )

        # ----------------------------------------------------
        # AUTOMATIC
        # ----------------------------------------------------

        return True, (
            "Sure. I will calculate it for you. "
            "What amount would you like to invest?"
        )

    # ========================================================
    # MANUAL MODE
    # ========================================================

    if task["mode"] == "manual":

        return True, (
            "Manual FD calculator is selected. "
            "Please use the FD calculator."
        )

    # ========================================================
    # AUTOMATIC MODE
    # ========================================================

    if task["mode"] == "automatic":

        # ====================================================
        # STEP 1 — AMOUNT
        # ====================================================

        if task["amount"] is None:

            amount = parse_amount(message)

            if amount is None:

                return True, (
                    "What amount would you like "
                    "to invest in the FD?"
                )

            update_fd_task(
                user_id,
                amount=amount
            )

            # IMPORTANT:
            # Do NOT process this same message as rate.
            # Example:
            # user says 4000000
            # It must only become the amount.

            return True, (
                "What interest rate should I use "
                "for the FD?"
            )

        # ====================================================
        # STEP 2 — INTEREST RATE
        # ====================================================

        if task["rate"] is None:

            rate = parse_rate(message)

            if rate is None:

                return True, (
                    "What interest rate should I use "
                    "for the FD?"
                )

            update_fd_task(
                user_id,
                rate=rate
            )

            # IMPORTANT:
            # Do NOT process this same message as tenure.
            # Example:
            # user says 6
            # It becomes 6% only.

            return True, (
                "What is the FD tenure? "
                "For example, 2 years or 24 months."
            )

        # ====================================================
        # STEP 3 — TENURE
        # ====================================================

        if task["tenure"] is None:

            tenure = parse_tenure(message)

            if tenure is None:

                return True, (
                    "What is the FD tenure? "
                    "For example, 2 years or 24 months."
                )

            update_fd_task(
                user_id,
                tenure=tenure
            )

        # ====================================================
        # ALL DATA AVAILABLE
        # ====================================================

        task = get_active_task(user_id)

        if (
            task["amount"] is not None
            and task["rate"] is not None
            and task["tenure"] is not None
        ):

            result = calculate_fd(
                principal=task["amount"],
                rate=task["rate"],
                years=task["tenure"]
            )

            clear_task(user_id)

            return True, (
                f"Your FD calculation is complete.\n\n"
                f"Principal: ₹{result['principal']:,.2f}\n"
                f"Interest Rate: {result['rate']}%\n"
                f"Tenure: {result['years']} years\n"
                f"Interest: ₹{result['interest']:,.2f}\n"
                f"Maturity Amount: "
                f"₹{result['maturity_amount']:,.2f}"
            )

    return False, None



# ============================================================
# EMI TASK
# ============================================================


def start_emi_task(user_id):

    TASK_SESSIONS[user_id] = {
        "task": "EMI_CALCULATOR",
        "mode": None,
        "amount": None,
        "rate": None,
        "tenure": None,
        "tenure_unit": "years"
    }

    print(
        f"EMI task started for user {user_id}"
    )

    return TASK_SESSIONS[user_id]


# ============================================================
# EMI AMOUNT PARSER
# ============================================================

def parse_emi_amount(text):

    import re

    text = text.lower().strip()

    patterns = [
        ("crores", 10000000),
        ("crore", 10000000),
        ("cr", 10000000),

        ("lakhs", 100000),
        ("lakh", 100000),
        ("lacs", 100000),
        ("lac", 100000)
    ]

    for word, multiplier in patterns:

        if word in text:

            match = re.search(
                rf"(\d+(?:\.\d+)?)\s*{word}",
                text
            )

            if match:

                value = float(
                    match.group(1)
                )

                return value * multiplier

    match = re.search(
        r"(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)",
        text
    )

    if match:

        return float(
            match.group(1)
        )

    return None


# ============================================================
# EMI RATE PARSER
# ============================================================

def parse_emi_rate(text):

    import re

    text = text.lower()

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:%|percent|per\s*cent)",
        text
    )

    if match:

        return float(
            match.group(1)
        )

    return None


# ============================================================
# EMI TENURE PARSER
# ============================================================

def parse_emi_tenure(text):

    import re

    text = text.lower()

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        text
    )

    if match:

        return (
            float(match.group(1)),
            "years"
        )

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:months?|mos?)",
        text
    )

    if match:

        return (
            float(match.group(1)),
            "months"
        )

    return None, None


# ============================================================
# DETECT EMI MODE
# ============================================================

def detect_emi_mode(text):

    text = text.lower().strip()

    # --------------------------------------------------------
    # MANUAL / OPEN CALCULATOR
    # --------------------------------------------------------

    manual_words = [
        "manual",
        "manually",
        "open emi",
        "open calculator",
        "emi calculator",
        "use calculator",
        "open tool",
        "calculator"
    ]

    for word in manual_words:

        if word in text:

            return "manual"

    # --------------------------------------------------------
    # AUTOMATIC CALCULATION
    # --------------------------------------------------------

    automatic_words = [
        "automatic",
        "automatically",
        "calculate here",
        "you calculate",
        "calculate it",
        "calculate for me",
        "calculate",
        "calculate emi"
    ]

    for word in automatic_words:

        if word in text:

            return "automatic"

    return None


# ============================================================
# EMI TASK
# ============================================================

def process_emi_task(
    user_id,
    message
):

    from app.services.emi_calculator import calculate_emi

    task = get_active_task(
        user_id
    )

    if not task:

        return False, None

    if task.get("task") != "EMI_CALCULATOR":

        return False, None

    text = message.lower().strip()

    # ========================================================
    # CANCEL TASK
    # ========================================================

    cancel_words = [
        "cancel",
        "stop",
        "cancel task",
        "stop task",
        "never mind",
        "nevermind"
    ]

    if any(
        word in text
        for word in cancel_words
    ):

        clear_task(user_id)

        return (
            True,
            "Okay, I cancelled the EMI calculation."
        )

    # ========================================================
    # EXTRACT VALUES FIRST
    # ========================================================

    if task["amount"] is None:

        amount = parse_emi_amount(
            message
        )

        if amount is not None:

            task["amount"] = amount

            print(
                f"EMI amount detected: "
                f"{amount}"
            )

    if task["rate"] is None:

        rate = parse_emi_rate(
            message
        )

        if rate is not None:

            task["rate"] = rate

            print(
                f"EMI rate detected: "
                f"{rate}%"
            )

    if task["tenure"] is None:

        tenure, unit = parse_emi_tenure(
            message
        )

        if tenure is not None:

            task["tenure"] = tenure

            task["tenure_unit"] = unit

            print(
                f"EMI tenure detected: "
                f"{tenure} {unit}"
            )

    # ========================================================
    # DETECT MODE
    # ========================================================

    if task["mode"] is None:

        mode = detect_emi_mode(
            message
        )

        if mode:

            task["mode"] = mode

        # If all values are present,
        # automatically calculate.
        elif (
            task["amount"] is not None
            and task["rate"] is not None
            and task["tenure"] is not None
        ):

            task["mode"] = "automatic"

        # If values are present but incomplete,
        # automatically continue calculation.
        elif (
            task["amount"] is not None
            or task["rate"] is not None
            or task["tenure"] is not None
        ):

            task["mode"] = "automatic"

        else:

            return (
                True,
                "Sure. Would you like me to calculate the EMI here, or open the EMI calculator?"
            )

    # ========================================================
    # MANUAL MODE
    # ========================================================

    if task["mode"] == "manual":

        return (
            True,
            "Sure. Manual EMI calculator selected. The EMI calculator will open so you can enter the loan amount, interest rate and tenure."
        )

    # ========================================================
    # AUTOMATIC MODE
    # ========================================================

    if task["amount"] is None:

        return (
            True,
            "What is the loan amount?"
        )

    if task["rate"] is None:

        return (
            True,
            "What interest rate should I use?"
        )

    if task["tenure"] is None:

        return (
            True,
            "What is the loan tenure?"
        )

    # ========================================================
    # CONVERT TENURE TO YEARS
    # ========================================================

    years = task["tenure"]

    if task["tenure_unit"] == "months":

        years = task["tenure"] / 12

    # ========================================================
    # CALCULATE EMI
    # ========================================================

    print(
        "\n========== CALCULATING EMI =========="
    )

    print(
        f"Principal: {task['amount']}"
    )

    print(
        f"Rate: {task['rate']}%"
    )

    print(
        f"Years: {years}"
    )

    result = calculate_emi(
        principal=task["amount"],
        annual_rate=task["rate"],
        years=years
    )

    # ========================================================
    # CLEAR TASK
    # ========================================================

    clear_task(
        user_id
    )

    # ========================================================
    # RESPONSE
    # ========================================================

    response = (
        f"Your monthly EMI is "
        f"₹{result['emi']:,.2f}. "
        f"Total interest is "
        f"₹{result['total_interest']:,.2f}, "
        f"and total payment is "
        f"₹{result['total_payment']:,.2f}."
    )

    return (
        True,
        response
    )