import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")


if not API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY is missing in .env")

if not VOICE_ID:
    raise RuntimeError("ELEVENLABS_VOICE_ID is missing in .env")


def text_to_speech(text: str) -> bytes:

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_flash_v2_5",
        "output_format": "mp3_22050_32"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"ElevenLabs API error {response.status_code}: "
            f"{response.text}"
        )

    return response.content