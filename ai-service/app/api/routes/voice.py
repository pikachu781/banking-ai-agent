from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from app.services.elevenlabs_service import text_to_speech


router = APIRouter()


class SpeakRequest(BaseModel):
    text: str


@router.post("/speak")
def speak(request: SpeakRequest):

    try:

        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )

        audio = text_to_speech(request.text)

        return Response(
            content=audio,
            media_type="audio/mpeg"
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )