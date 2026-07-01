import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from src.config.settings import settings

logger = logging.getLogger(__name__)

# O declarative_base é a classe mãe de todas as nossas tabelas
Base = declarative_base()

# Criação do "Motor" assíncrono que fala com o PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False, # Mude para True se quiser ver as queries SQL no terminal
    pool_pre_ping=True, # Garante que a conexão não caiu antes de usar
    pool_size=10,
    max_overflow=20
)

# Fábrica de sessões (o que usaremos para fazer os INSERTs e SELECTs)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    """
    Dependência para injetar a sessão da base de dados nas rotas do FastAPI.
    Garante que a conexão é fechada adequadamente após o uso.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()