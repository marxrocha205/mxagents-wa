from fastapi import FastAPI, Request, BackgroundTasks, Response
import logging
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from src.config.settings import settings
from src.application.handlers.message_router import MessageRouter

# Configuração de log
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WhatsApp Agent Pro",
    description="Agente de mensageria assíncrono com RAG e IA",
    version="1.0.0"
)


router = MessageRouter()

@app.get("/")
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}

@app.get("/metrics")
async def metrics():
    """Endpoint para o Prometheus realizar o scrape das métricas."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/api/v1/webhooks/evolution")
async def evolution_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Recebe todos os eventos da Evolution API.
    Usamos BackgroundTasks para responder '200 OK' instantaneamente para a Evolution,
    enquanto roteamos e processamos a mensagem em segundo plano.
    """
    payload = await request.json()
    
    background_tasks.add_task(router.route, payload)
    
    return {"status": "received"}