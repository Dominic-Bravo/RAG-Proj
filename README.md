# RAG Python

todo
refactor codes and ui

A small Retrieval-Augmented Generation app focused on two source types:

- PDF documents
- Local repositories or GitHub repository URLs

The project is structured so each source type can grow independently without mixing PDF facts and code context in the same vector collection.

## Run

```powershell
uv run python -m src.main
```

Or, from the existing virtual environment:

```powershell
.\.venv\Scripts\python.exe -m src.main
```

## Configure

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
DEFAULT_PDF_PATH=Dominic Ian bravo.pdf
```

Optional settings can also be overridden in `.env`:

```env
EMBEDDING_MODEL=models/gemini-embedding-001
LLM_MODEL=gemini-2.5-flash
VECTOR_DB_DIR=./chroma_db
CLONED_REPOS_DIR=./data/repos
CHUNK_SIZE=700
CHUNK_OVERLAP=100
REPO_CHUNK_SIZE=1500
REPO_CHUNK_OVERLAP=200
```

## Architecture

```text
src/
  config.py              App settings and source scanning defaults
  main.py                CLI entry point
  repo_chat.py           Repository chat workflow
  core/
    engine.py            RAG prompt and chain builder
    ingestion.py         PDF loading and chunking
    repo_ingestion.py    Repository loading, cloning, scanning, and chunking
    sources.py           Source type definitions
    vectorstore.py       Embeddings and source-specific Chroma stores
```

## Source Separation

PDF and repository chunks are stored separately:

```text
chroma_db/
  pdf/
  repo/
```

Each chunk is tagged with metadata:

- `type`: `pdf` or `repo`
- `source`: absolute file path
- `source_name`: PDF filename when available
- `relative_path`: repository-relative file path when available
- `language`: code file extension when available

This keeps retrieval focused and makes future source types easier to add.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The engine tests use an injected fake LLM, so they do not require a live API call.
