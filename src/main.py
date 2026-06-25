from fastapi import FastAPI, Request
import logging
from src.config.settings import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="MXAgents API",
    description="API para integração com o Evolution e envio de mensagens via WhatsApp.",
    version="1.0.0",
)

@app.get("/")
async def health_check():
    """
    Endpoint de verificação de saúde da API.
    Retorna um status 200 OK se a API estiver funcionando corretamente.
    """
    logger.info("Health check endpoint called.")
    return {"status": "ok", "message": "MXAgents API is running.", "environment": settings.ENVIRONMENT}

@app.post("/api/v1/webhooks/evolution")
async def evolution_webhook(request: Request):
    """
    Endpoint para receber webhooks do Evolution.
    """
    payload = await request.json()
    event_type = payload.get("event")
    instance = payload.get("instance")
    logger.info(f"A new webhook event has been received from Evolution.")
    logger.info(f"Instance: {instance}, Event Type: {event_type}")
    logger.info(f"Received webhook from Evolution: {payload}")


    return {"status": "received"}

    