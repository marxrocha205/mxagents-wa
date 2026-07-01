import httpx
import logging
from .base_client import EvolutionBaseClient
from src.config.settings import settings

logger = logging.getLogger(__name__)

class BusinessClient(EvolutionBaseClient):
    """
    Cliente exclusivo para operações do WhatsApp Business 
    (Catálogos, Coleções, Produtos).
    """

    async def _get(self, endpoint: str, params: dict = None) -> dict:
        """Método auxiliar para requisições GET (Catálogos e Produtos)."""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, params=params, timeout=15.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Erro HTTP {e.response.status_code} na Evolution API: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Erro de conexão com a Evolution API: {str(e)}")
                raise

    async def get_catalog(self, catalog_owner_number: str) -> dict:
        """
        Busca todos os produtos do catálogo de um número Business.
        catalog_owner_number deve ser o seu número ou o número do cliente (sem o @s.whatsapp.net)
        """
        endpoint = f"/chat/fetchCatalog/{self.instance}"
        params = {
            "remoteJid": f"{catalog_owner_number}@s.whatsapp.net"
        }
        logger.info(f"Buscando catálogo de produtos de {catalog_owner_number}...")
        return await self._get(endpoint, params=params)

    async def get_collections(self, catalog_owner_number: str) -> dict:
        """
        Busca as coleções (categorias) cadastradas no catálogo do Business.
        """
        endpoint = f"/chat/fetchCollections/{self.instance}"
        params = {
            "remoteJid": f"{catalog_owner_number}@s.whatsapp.net"
        }
        logger.info(f"Buscando coleções de {catalog_owner_number}...")
        return await self._get(endpoint, params=params)