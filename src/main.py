from fastapi import FastAPI, Request, BackgroundTasks
import logging
from src.config.settings import settings
from src.application.services.message_handler import MessageHandlerService
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

# Instanciamos nosso serviço (Cérebro)
message_handler = MessageHandlerService()
router = MessageRouter()

@app.get("/")
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}

@app.post("/api/v1/webhooks/evolution")
async def evolution_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Recebe todos os eventos da Evolution API.
    Usamos BackgroundTasks para responder '200 OK' instantaneamente para a Evolution,
    enquanto processamos a mensagem em segundo plano.
    """
    payload = await request.json()
    
    # Adiciona a tarefa de processar a mensagem em uma thread separada
    background_tasks.add_task(message_handler.process_webhook_payload, payload)
    
    return {"status": "received"}