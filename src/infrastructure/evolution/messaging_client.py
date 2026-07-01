import logging
from .base_client import EvolutionBaseClient

logger = logging.getLogger(__name__)

class MessagingClient(EvolutionBaseClient):
    """
    Cliente focado no envio de todos os formatos de mensagens.
    Respeita o Princípio de Responsabilidade Única (SRP).
    """
    
    async def send_text(self, number: str, text: str, delay: int = 1200) -> dict:
        endpoint = f"/message/sendText/{self.instance}"
        payload = {
            "number": number,
            "text": text,
            "delay": delay,
            "linkPreview": True
        }
        return await self._post(endpoint, payload)

    async def send_image(self, number: str, media_base64_or_url: str, caption: str = "", delay: int = 1500) -> dict:
        """Envia uma imagem (base64 ou URL pública) com ou sem legenda."""
        endpoint = f"/message/sendMedia/{self.instance}"
        payload = {
            "number": number,
            "mediatype": "image",
            "media": media_base64_or_url,
            "caption": caption,
            "delay": delay
        }
        logger.debug(f"Enviando imagem para {number}...")
        return await self._post(endpoint, payload)

    async def send_audio(self, number: str, audio_base64_or_url: str, delay: int = 2000) -> dict:
        """
        Envia um áudio. A Evolution API converte para o formato nativo do WhatsApp (ogg).
        O delay simula o 'gravando áudio...'.
        """
        endpoint = f"/message/sendWhatsAppAudio/{self.instance}"
        payload = {
            "number": number,
            "audio": audio_base64_or_url,
            "delay": delay
        }
        logger.debug(f"Enviando áudio para {number}...")
        return await self._post(endpoint, payload)

    async def send_document(self, number: str, doc_base64_or_url: str, filename: str, caption: str = "", delay: int = 1000) -> dict:
        """Envia arquivos (PDFs, planilhas, etc). Útil para envio de catálogos ou recibos."""
        endpoint = f"/message/sendMedia/{self.instance}"
        payload = {
            "number": number,
            "mediatype": "document",
            "media": doc_base64_or_url,
            "fileName": filename,
            "caption": caption,
            "delay": delay
        }
        logger.debug(f"Enviando documento {filename} para {number}...")
        return await self._post(endpoint, payload)