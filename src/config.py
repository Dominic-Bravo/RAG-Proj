from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    LLM_MODEL: str = "gemini-2.5-flash"

    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 100
    REPO_CHUNK_SIZE: int = 1500
    REPO_CHUNK_OVERLAP: int = 200

    VECTOR_DB_DIR: str = "./chroma_db"
    CLONED_REPOS_DIR: str = "./data/repos"
    DEFAULT_K: int = 5
    REPO_K: int = 8

    SUPPORTED_CODE_EXTENSIONS: tuple[str, ...] = (
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".cs",
        ".json",
        ".html",
        ".css",
        ".md",
        ".toml",
        ".yaml",
        ".yml",
    )
    IGNORE_FOLDERS: tuple[str, ...] = (
        ".git",
        ".pytest_cache",
        ".venv",
        "__pycache__",
        "bin",
        "build",
        "chroma_db",
        "dist",
        "node_modules",
        "obj",
    )

    SYSTEM_PROMPT: str = """
You are an expert AI assistant.

Use only the provided context to answer the user's question.

Rules:
- Be accurate and concise.
- Cite file paths, PDF names, or page numbers when available.
- If the answer is not in the context, say that the information is not available.
- Do not invent files, functions, requirements, or personal details.
"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
