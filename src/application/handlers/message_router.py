import logging
from .text_handler import TextMessageHandler
from .image_handler import ImageMessageHandler
from .audio_handler import AudioMessageHandler
from .document_handler import DocumentMessageHandler
from src.infrastructure.metrics.counters import MESSAGES_RECEIVED

logger = logging.getLogger(__name__)

class MessageRouter:
    """
    Roteador principal. Aplica o padrão Strategy para decidir
    quem vai processar a mensagem baseado no seu tipo.
    """
    def __init__(self):
        self.strategies = {
            "conversation": TextMessageHandler(),
            "extendedTextMessage": TextMessageHandler(),
            "imageMessage": ImageMessageHandler(),
            "audioMessage": AudioMessageHandler(),
            "documentMessage": DocumentMessageHandler(),
        }

    async def route(self, payload: dict):
        if payload.get("event") != "messages.upsert":
            return

        message_info = payload.get("data", {}).get("message", {})

        if message_info.get("fromMe") or message_info.get("isGroup"):
            return

        remote_jid = message_info.get("remoteJid", "")
        phone_number = remote_jid.split("@")[0]
        
        message_content = message_info.get("message", {})
        if not message_content:
            return

        message_type = next(iter(message_content.keys()), None)
        
        # Incrementa métricas
        if message_type:
            MESSAGES_RECEIVED.labels(message_type=message_type).inc()
        
        handler = self.strategies.get(message_type)
        
        if handler:
            logger.info(f"Roteando mensagem tipo '{message_type}' via {handler.__class__.__name__}")
            await handler.process(phone_number, message_content)
        else:
            logger.warning(f"Nenhum handler configurado para o tipo: {message_type}")