import os

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    SUPPORTED_CODE_EXTENSIONS,
    IGNORE_FOLDERS,
    SYSTEM_PROMPT
)

# from src.ingestion.loaders import read_file

def read_file(file_path: str):

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_repo(repo_path: str):

    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_FOLDERS
        ]

        for file in files:

            ext = os.path.splitext(file)[1]

            if ext not in SUPPORTED_CODE_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:

                content = read_file(file_path)

                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": file_path,
                            "file_name": file,
                            "language": ext
                        }
                    )
                )

            except Exception as e:

                print(f"Error reading {file_path}: {e}")

    return documents


def split_repo(repo_path: str):

    documents = load_repo(repo_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    return chunks