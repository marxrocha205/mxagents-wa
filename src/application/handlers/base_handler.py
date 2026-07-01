from abc import ABC, abstractmethod

class MessageHandler(ABC):
    """
    Contrato base para todos os processadores de mensagem.
    Garante que qualquer novo tipo de mensagem implemente o método process.
    """
    @abstractmethod
    async def process(self, phone_number: str, message_content: dict):
        pass