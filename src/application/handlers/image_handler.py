import logging
from .base_handler import MessageHandler
from src.infrastructure.evolution.messaging_client import MessagingClient

logger = logging.getLogger(__name__)

class ImageMessageHandler(MessageHandler):
    def __init__(self):
        self.messaging_client = MessagingClient()

    async def process(self, phone_number: str, message_content: dict):
        image_data = message_content.get("imageMessage", {})
        caption = image_data.get("caption", "")
        
        logger.info(f"Imagem recebida de {phone_number}. Legenda: {caption}")
        
        # FUTURO: Aqui chamaremos a Evolution para baixar o base64 da imagem
        # e enviaremos para o Qwen-VL (Visão) analisar.
        
        resposta = "Recebi sua imagem! O módulo de visão computacional será ativado em breve."
        await self.messaging_client.send_text(phone_number, resposta)