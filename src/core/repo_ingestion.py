import os
import re
import subprocess
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import settings
from src.core.sources import SourceType


GITHUB_URL_PATTERN = re.compile(
    r"^(https?://)?(www\.)?github\.com/[^/\s]+/[^/\s]+/?$"
)


def is_github_url(value: str) -> bool:
    return bool(GITHUB_URL_PATTERN.match(value.strip()))


def clone_github_repo(repo_url: str, destination_root: str | Path | None = None) -> Path:
    destination_root = Path(destination_root or settings.CLONED_REPOS_DIR).resolve()
    destination_root.mkdir(parents=True, exist_ok=True)

    repo_name = repo_url.rstrip("/").removesuffix(".git").split("/")[-1]
    destination = destination_root / repo_name

    if destination.exists():
        return destination

    clone_url = repo_url if repo_url.endswith(".git") else f"{repo_url.rstrip('/')}.git"
    subprocess.run(
        ["git", "clone", "--depth", "1", clone_url, str(destination)],
        check=True,
        capture_output=True,
        text=True,
    )
    return destination


def resolve_repo_path(repo_path_or_url: str) -> Path:
    value = repo_path_or_url.strip()
    if is_github_url(value):
        return clone_github_repo(value)

    path = Path(value).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"Repository folder not found: {path}")
    return path


def read_file(file_path: str | Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_repo(repo_path_or_url: str):
    repo_path = resolve_repo_path(repo_path_or_url)
    documents = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in settings.IGNORE_FOLDERS]

        for file in files:
            file_path = Path(root) / file
            ext = file_path.suffix.lower()

            if ext not in settings.SUPPORTED_CODE_EXTENSIONS:
                continue

            try:
                content = read_file(file_path)
            except UnicodeDecodeError:
                continue
            except OSError as exc:
                print(f"Error reading {file_path}: {exc}")
                continue

            relative_path = file_path.relative_to(repo_path)
            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "type": SourceType.REPO.value,
                        "source": str(file_path),
                        "repo_root": str(repo_path),
                        "relative_path": str(relative_path),
                        "file_name": file,
                        "language": ext.lstrip("."),
                    },
                )
            )

    return documents


def split_repo(repo_path_or_url: str):

    documents = load_repo(repo_path_or_url)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.REPO_CHUNK_SIZE,
        chunk_overlap=settings.REPO_CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(documents)

    return chunks
