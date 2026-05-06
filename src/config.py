from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    LLM_MODEL: str = "gemini-2.5-flash"
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 100
    # THIS WAS MISSING:
    VECTOR_DB_DIR: str = "./chroma_db" 

    class Config:
        env_file = ".env"
        # This tells pydantic to ignore extra fields in .env if any
        extra = "ignore" 

settings = Settings()