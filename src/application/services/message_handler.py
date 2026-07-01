import logging
from infrastructure.evolution.base_client import EvolutionClient

logger = logging.getLogger(__name__)

class MessageHandlerService:
    def __init__(self):
        self.evolution_client = EvolutionClient()

    async def process_webhook_payload(self, payload: dict):
        """
        Processa o JSON recebido da Evolution API e orquestra a resposta.
        """
        # A Evolution dispara vários eventos. Só queremos mensagens novas (upsert)
        if payload.get("event") != "messages.upsert":
            return

        data = payload.get("data", {})
        message_info = data.get("message", {})

        # Ignora mensagens enviadas pelo próprio bot (fromMe = True) ou status
        if message_info.get("fromMe") or message_info.get("isGroup"):
            return

        remote_jid = message_info.get("remoteJid", "")
        # Extrai apenas o número (tira o @s.whatsapp.net)
        phone_number = remote_jid.split("@")[0] 

        # A estrutura da mensagem muda se for texto puro, imagem com legenda, etc.
        # Vamos pegar o texto puro por enquanto
        conversation = message_info.get("message", {}).get("conversation", "")
        extended_text = message_info.get("message", {}).get("extendedTextMessage", {}).get("text", "")
        
        user_text = conversation or extended_text

        if not user_text:
            logger.debug("Mensagem sem texto identificável (pode ser áudio/imagem puro). Ignorando por enquanto.")
            return

        logger.info(f"Mensagem recebida de {phone_number}: {user_text}")

        # ==========================================
        # Aqui no futuro entrará a inteligência (RAG / OpenRouter)
        # Por enquanto, faremos um teste simples de "Echo"
        # ==========================================
        
        resposta_bot = f"Olá! Eu recebi sua mensagem: '{user_text}'. Em breve serei conectado à Inteligência Artificial!"
        
        # Dispara a resposta usando nosso client de infraestrutura
        await self.evolution_client.send_text_message(number=phone_number, text=resposta_bot)