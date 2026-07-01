import logging
from .base_client import EvolutionBaseClient

logger = logging.getLogger(__name__)

class MessagingClient(EvolutionBaseClient):
    """
    Cliente focado exclusivamente no envio de mensagens (Texto, Imagem, Áudio, etc).
    Respeita o Princípio de Responsabilidade Única (SRP).
    """
    
    async def send_text(self, number: str, text: str, delay: int = 1200) -> dict:
        """
        Envia uma mensagem de texto puro.
        O delay simula o 'digitando...' para evitar banimentos (anti-spam).
        """
        endpoint = f"/message/sendText/{self.instance}"
        payload = {
            "number": number,
            "text": text,
            "delay": delay,
            "linkPreview": True
        }
        
        logger.debug(f"Preparando envio de texto para {number}...")
        return await self._post(endpoint, payload)