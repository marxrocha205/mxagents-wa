import logging
from .base_handler import MessageHandler
from src.infrastructure.evolution.messaging_client import MessagingClient

logger = logging.getLogger(__name__)

class TextMessageHandler(MessageHandler):
    """Processa mensagens de texto puro."""
    
    def __init__(self):
        self.messaging_client = MessagingClient()

    async def process(self, phone_number: str, message_content: dict):
        # O WhatsApp manda texto em dois lugares diferentes dependendo de como foi digitado
        text = message_content.get("conversation") or message_content.get("extendedTextMessage", {}).get("text", "")
        
        if not text:
            logger.warning(f"Nenhum texto extraível recebido de {phone_number}.")
            return

        logger.info(f"Processando texto de {phone_number}: {text}")

        
        resposta = f"Sistema base ativo. Você enviou: '{text}'. Aguardando módulo de IA."
        
        await self.messaging_client.send_text(number=phone_number, text=resposta)