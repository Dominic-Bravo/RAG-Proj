from pathlib import Path

from langchain_chroma import Chroma

from src.config import settings
from src.core.sources import COLLECTION_NAMES, SourceType


def get_embeddings():
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is required to create embeddings.")

    return GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        task_type="retrieval_document",
        google_api_key=settings.GOOGLE_API_KEY,
    )


def get_vectorstore(
    chunks=None,
    source_type: SourceType | str = SourceType.PDF,
    collection_name: str | None = None,
    embedding_function=None,
):
    source_type = SourceType(source_type)
    embeddings = embedding_function or get_embeddings()
    persist_directory = Path(settings.VECTOR_DB_DIR) / source_type.value
    persist_directory.mkdir(parents=True, exist_ok=True)
    collection_name = collection_name or COLLECTION_NAMES[source_type]

    if chunks is not None:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(persist_directory),
            collection_name=collection_name,
        )
    else:
        vectorstore = Chroma(
            persist_directory=str(persist_directory),
            embedding_function=embeddings,
            collection_name=collection_name,
        )

    return vectorstore
