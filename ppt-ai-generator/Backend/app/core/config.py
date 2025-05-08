from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    openai_api_key: str
    database_url: str
    redis_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
