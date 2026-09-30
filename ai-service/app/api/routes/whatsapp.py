from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
import os


router = APIRouter(
    prefix="/api/whatsapp",
    tags=["WhatsApp"]
)


# ============================================================
# META WEBHOOK VERIFICATION
# ============================================================

@router.get("/webhook")
async def verify_webhook(request: Request):

    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    verify_token = os.getenv(
        "WHATSAPP_VERIFY_TOKEN"
    )

    if mode == "subscribe" and token == verify_token:
        return PlainTextResponse(challenge)

    return PlainTextResponse(
        "Verification failed",
        status_code=403
    )


# ============================================================
# RECEIVE WHATSAPP MESSAGE
# ============================================================

@router.post("/webhook")
async def receive_webhook(request: Request):

    data = await request.json()

    print("\n========== WHATSAPP WEBHOOK ==========")
    print(data)

    return {
        "status": "received"
    }