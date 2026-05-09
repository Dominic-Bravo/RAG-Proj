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

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHROMA_DB_DIR = "chroma_db"

DEFAULT_K = 5

SUPPORTED_CODE_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".cs",
    ".json",
    ".html",
    ".css",
    ".md"
]

IGNORE_FOLDERS = [
    ".git",
    "node_modules",
    "__pycache__",
    "bin",
    "obj",
    ".venv",
    "dist",
    "build"
]

SYSTEM_PROMPT = """
You are an expert AI coding assistant.

Use the provided context to answer questions.

Rules:
- Be accurate
- Use file paths when available
- If code architecture exists, follow it
- Do not hallucinate files or functions
- If context is missing, say so
"""