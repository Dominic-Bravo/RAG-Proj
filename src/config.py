from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    LLM_MODEL: str = "gemini-2.5-flash"
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 100
    VECTOR_DB_DIR: str = "./chroma_db"

    # New V2 way to handle config
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()