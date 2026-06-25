from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"

    EVOLUTION_API_URL: str
    EVOLUTION_API_KEY: str
    WHATSAPP_INSTANCE_NAME: str

    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str | None = None

    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()