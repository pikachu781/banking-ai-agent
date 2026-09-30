# ============================================================
# NAVIGATION INTENT DETECTOR
# ============================================================

NAVIGATION_COMMANDS = [
    "open",
    "go to",
    "goto",
    "navigate to",
    "take me to",
    "show page",
    "open page",
    "view page",
    "visit",
]


def is_navigation_request(message: str) -> bool:
    """
    Determines whether the user is explicitly asking
    to navigate to a page.

    Returns:
        True  -> navigation request
        False -> normal banking/data request
    """

    if not message:
        return False

    text = message.lower().strip()

    # --------------------------------------------------------
    # Explicit navigation commands
    # --------------------------------------------------------

    for command in NAVIGATION_COMMANDS:

        if command in text:
            return True

    # --------------------------------------------------------
    # Explicit page/screen requests
    # --------------------------------------------------------

    if "page" in text:
        return True

    if "screen" in text:
        return True

    return False