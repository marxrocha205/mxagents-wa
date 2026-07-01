import logging
from .base_handler import MessageHandler
from src.infrastructure.evolution.messaging_client import MessagingClient

logger = logging.getLogger(__name__)

class DocumentMessageHandler(MessageHandler):
    def __init__(self):
        self.messaging_client = MessagingClient()

    async def process(self, phone_number: str, message_content: dict):
        doc_data = message_content.get("documentMessage", {})
        filename = doc_data.get("fileName", "arquivo_desconhecido")
        
        logger.info(f"Documento recebido de {phone_number}: {filename}")
        
        
        
        resposta = f"Recebi o arquivo '{filename}'. A leitura de documentos será ativada em breve."
        await self.messaging_client.send_text(phone_number, resposta)