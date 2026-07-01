import logging
from .base_client import EvolutionBaseClient

logger = logging.getLogger(__name__)

class MediaClient(EvolutionBaseClient):
    """
    Cliente responsável por interagir com os ficheiros e mídias do WhatsApp.
    """
    
    async def get_base64_from_message(self, message_object: dict) -> str | None:
        """
        Pede à Evolution API para descarregar a mídia e devolvê-la em formato Base64.
        O message_object é o dicionário 'message' exato que recebemos no webhook.
        """
        endpoint = f"/chat/getBase64FromMediaMessage/{self.instance}"
        payload = {
            "message": message_object
        }
        
        try:
            logger.debug("A solicitar Base64 da mídia à Evolution API...")
            response = await self._post(endpoint, payload)
            return response.get("base64")
        except Exception as e:
            logger.error(f"Falha ao descarregar mídia: {str(e)}")
            return None