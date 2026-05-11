from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import settings
from src.core.sources import SourceType


def load_and_split_pdf(file_path: str):
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {path}")

    loader = PyPDFLoader(str(path))
    docs = loader.load()

    for doc in docs:
        doc.metadata.update(
            {
                "type": SourceType.PDF.value,
                "source": str(path),
                "source_name": path.name,
            }
        )
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    return text_splitter.split_documents(docs)
