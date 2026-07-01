import httpx
import logging
from src.config.settings import settings

logger = logging.getLogger(__name__)

class EvolutionBaseClient:
    """
    Classe base para comunicação com a Evolution API.
    Gerencia a construção de URLs, headers de autenticação e tratamento de erros HTTP.
    """
    def __init__(self):
        # rstrip('/') previne erros se a URL no .env terminar com barra
        self.base_url = settings.EVOLUTION_API_URL.rstrip('/')
        self.instance = settings.WHATSAPP_INSTANCE_NAME
        self.headers = {
            "Content-Type": "application/json",
            "apikey": settings.EVOLUTION_API_KEY
        }

    async def _post(self, endpoint: str, payload: dict) -> dict:
        """Método interno para padronizar todas as requisições POST."""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                # Timeout de 15s para evitar que a thread trave caso a Evolution engasgue
                response = await client.post(url, json=payload, headers=self.headers, timeout=15.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Erro HTTP {e.response.status_code} na Evolution API: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Erro de conexão com a Evolution API: {str(e)}")
                raise