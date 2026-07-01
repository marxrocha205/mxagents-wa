import logging
from .text_handler import TextMessageHandler
from .image_handler import ImageMessageHandler
from .audio_handler import AudioMessageHandler
from .document_handler import DocumentMessageHandler
from src.infrastructure.metrics.counters import MESSAGES_RECEIVED

# Importações da Base de Dados (NOVAS)
from src.infrastructure.database.connection import AsyncSessionLocal
from src.infrastructure.database.repositories.contact_repository import ContactRepository

logger = logging.getLogger(__name__)

class MessageRouter:
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
        
        # O WhatsApp envia o nome do perfil do utilizador como 'pushName'
        push_name = payload.get("data", {}).get("pushName", "")
        
        message_content = message_info.get("message", {})
        if not message_content:
            return

        # ==========================================
        # Registo do Utilizador na Base de Dados
        # ==========================================
        async with AsyncSessionLocal() as session:
            repo = ContactRepository(session)
            # O sistema agora memoriza o cliente antes de responder!
            contact = await repo.get_or_create(phone_number, push_name)
            logger.debug(f"Processando mensagem do cliente: {contact.name or contact.phone_number}")

        message_type = next(iter(message_content.keys()), None)
        
        if message_type:
            MESSAGES_RECEIVED.labels(message_type=message_type).inc()
        
        handler = self.strategies.get(message_type)
        
        if handler:
            await handler.process(phone_number, message_content)
        else:
            logger.warning(f"Nenhum handler configurado para o tipo: {message_type}")