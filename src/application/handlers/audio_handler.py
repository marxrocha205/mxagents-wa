import logging
from .base_handler import MessageHandler
from src.infrastructure.evolution.messaging_client import MessagingClient

logger = logging.getLogger(__name__)

class AudioMessageHandler(MessageHandler):
    def __init__(self):
        self.messaging_client = MessagingClient()

    async def process(self, phone_number: str, message_content: dict):
        logger.info(f"Áudio recebido de {phone_number}.")
        
        # FUTURO: Baixar o OGG via Evolution e mandar para Whisper/Qwen Audio para transcrição.
        
        resposta = "Recebi seu áudio! Estou sendo treinado para escutar e transcrever mensagens de voz."
        await self.messaging_client.send_text(phone_number, resposta)