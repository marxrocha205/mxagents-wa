import logging
from .text_handler import TextMessageHandler

logger = logging.getLogger(__name__)

class MessageRouter:
    """
    Roteador principal. Aplica o padrão Strategy para decidir
    quem vai processar a mensagem baseado no seu tipo.
    """
    def __init__(self):
        # Mapeamento dos tipos nativos do WhatsApp para nossas classes de negócio
        self.strategies = {
            "conversation": TextMessageHandler(),
            "extendedTextMessage": TextMessageHandler(),
            # No futuro:
            # "audioMessage": AudioMessageHandler(),
            # "imageMessage": ImageMessageHandler(),
            # "documentMessage": DocumentMessageHandler(),
        }

    async def route(self, payload: dict):
        """Avalia o payload do webhook e aciona a estratégia correta."""
        if payload.get("event") != "messages.upsert":
            return

        message_info = payload.get("data", {}).get("message", {})

        # Prevenção de loop infinito: ignorar mensagens que o próprio bot enviou
        if message_info.get("fromMe") or message_info.get("isGroup"):
            return

        remote_jid = message_info.get("remoteJid", "")
        phone_number = remote_jid.split("@")[0]
        
        message_content = message_info.get("message", {})
        if not message_content:
            return

        # O WhatsApp envia o tipo da mensagem como a primeira chave do dicionário
        # Ex: {"audioMessage": {...}} ou {"conversation": "..."}
        message_type = next(iter(message_content.keys()), None)
        
        handler = self.strategies.get(message_type)
        
        if handler:
            logger.info(f"Roteando mensagem tipo '{message_type}' via {handler.__class__.__name__}")
            await handler.process(phone_number, message_content)
        else:
            logger.warning(f"Nenhum handler configurado para o tipo: {message_type}")