import logging
from .base_client import EvolutionBaseClient

logger = logging.getLogger(__name__)

class MessagingClient(EvolutionBaseClient):
    """
    Cliente focado no envio de todos os formatos de mensagens.
    Respeita o Princípio de Responsabilidade Única (SRP).
    """
    
    
    async def send_presence(self, number: str, presence: str = "composing", delay: int = 1500) -> dict:
        """
        Envia o estado de presença antes da mensagem para humanizar o bot.
        presence: 'composing' (digitando...), 'recording' (gravando áudio...)
        """
        endpoint = f"/chat/sendPresence/{self.instance}"
        payload = {
            "number": number,
            "presence": presence,
            "delay": delay
        }
        logger.debug(f"Simulando presença ({presence}) para {number}...")
        return await self._post(endpoint, payload)
    
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
    
    async def send_contact(self, number: str, contact_number: str, contact_name: str) -> dict:
        """Envia um cartão de contacto (vCard)."""
        endpoint = f"/message/sendContact/{self.instance}"
        payload = {
            "number": number,
            "contact": {
                "fullName": contact_name,
                "wuid": contact_number # O número do contacto sem @s.whatsapp.net
            }
        }
        return await self._post(endpoint, payload)

    async def send_location(self, number: str, lat: float, lng: float, name: str = "", address: str = "") -> dict:
        """Envia um pino de localização do GPS."""
        endpoint = f"/message/sendLocation/{self.instance}"
        payload = {
            "number": number,
            "name": name,
            "address": address,
            "latitude": lat,
            "longitude": lng
        }
        return await self._post(endpoint, payload)

    async def send_poll(self, number: str, question: str, options: list[str], selectable_count: int = 1) -> dict:
        """Envia uma enquete. Ótimo para menus interativos sem risco de ban."""
        endpoint = f"/message/sendPoll/{self.instance}"
        payload = {
            "number": number,
            "name": question,
            "options": options,
            "selectableCount": selectable_count
        }
        return await self._post(endpoint, payload)

    async def send_reaction(self, number: str, message_id: str, emoji: str) -> dict:
        """Reage a uma mensagem específica do cliente com um emoji."""
        endpoint = f"/message/sendReaction/{self.instance}"
        payload = {
            "number": number,
            "reactionMessage": {
                "key": {
                    "id": message_id,
                    "remoteJid": f"{number}@s.whatsapp.net",
                    "fromMe": False
                },
                "reaction": emoji
            }
        }
        return await self._post(endpoint, payload)
    
    async def send_buttons(self, number: str, text: str, title: str, footer: str, buttons: list[dict]) -> dict:
        """
        Envia botões interativos.
        Exemplo de button: {"type": "reply", "reply": {"id": "btn_1", "title": "Sim"}}
        """
        endpoint = f"/message/sendButtons/{self.instance}"
        payload = {
            "number": number,
            "text": text,
            "title": title,
            "footer": footer,
            "buttons": buttons
        }
        logger.warning(f"Atenção: Uso de botões em conexão QR Code para {number} pode gerar instabilidade.")
        return await self._post(endpoint, payload)

    async def send_list(self, number: str, title: str, description: str, button_text: str, sections: list[dict]) -> dict:
        """
        Envia uma lista interativa (Menu).
        """
        endpoint = f"/message/sendList/{self.instance}"
        payload = {
            "number": number,
            "title": title,
            "description": description,
            "buttonText": button_text,
            "sections": sections
        }
        logger.warning(f"Atenção: Uso de listas em conexão QR Code para {number} pode gerar instabilidade.")
        return await self._post(endpoint, payload)