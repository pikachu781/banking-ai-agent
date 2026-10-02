from fastapi import FastAPI

from app.database.connection import Base, engine
from app.database import models
from app.api.routes.fd import router as fd_router
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.memory import router as memory_router
from app.api.routes.emi import router as emi_router
from app.api.routes.whatsapp import router as whatsapp_router
from app.api.routes.voice import router as voice_router

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Voice AI Service",
    version="1.0.0"
)


app.include_router(
    health_router,
    prefix="/api"
)


app.include_router(
    chat_router,
    prefix="/api/ai"
)
app.include_router(
    memory_router,
    prefix="/api"
)

app.include_router(
    fd_router,
    prefix="/api/ai/fd"
)
app.include_router(
    emi_router,
    prefix="/api/ai/emi"
)
app.include_router(
    whatsapp_router
)
app.include_router(
    voice_router,
    prefix="/api/voice"
)