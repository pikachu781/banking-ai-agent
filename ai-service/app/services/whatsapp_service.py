import os
import httpx


# ============================================================
# WHATSAPP CONFIGURATION
# ============================================================

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

WHATSAPP_API_VERSION = os.getenv(
    "WHATSAPP_API_VERSION",
    "v26.0"
)


# ============================================================
# SEND TEXT MESSAGE
# ============================================================

async def send_whatsapp_message(
    phone_number: str,
    message: str
):

    if not WHATSAPP_ACCESS_TOKEN:
        raise Exception(
            "WHATSAPP_ACCESS_TOKEN is not configured."
        )

    if not WHATSAPP_PHONE_NUMBER_ID:
        raise Exception(
            "WHATSAPP_PHONE_NUMBER_ID is not configured."
        )

    url = (
        f"https://graph.facebook.com/"
        f"{WHATSAPP_API_VERSION}/"
        f"{WHATSAPP_PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": (
            f"Bearer {WHATSAPP_ACCESS_TOKEN}"
        ),
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

    if response.status_code >= 400:

        print(
            "WhatsApp API Error:",
            response.text
        )

        response.raise_for_status()

    return response.json()