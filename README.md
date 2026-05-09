# Scalable RAG AI Agent Architecture (PDF + GitHub + Multi-Source)

python -m src.main

## Overview

This document describes a clean, scalable architecture for building a Retrieval-Augmented Generation (RAG) AI system that supports multiple data sources such as PDFs, GitHub repositories, and future document types.

The goal is to avoid context conflicts, improve retrieval accuracy, and enable long-term scalability similar to modern AI coding assistants like Cursor-style systems.

---

## Core Problem

When all data sources are stored in a single vector database:

* PDF content mixes with code
* Unrelated contexts are retrieved together
* AI generates inconsistent or incorrect answers
* System becomes hard to scale and debug

---

## Solution: Multi-Source RAG Architecture

Instead of mixing all embeddings, we separate data by source type and optionally route queries intelligently.

---

## Recommended Folder Structure

```
RAG-AI-Agent/
│
├── main.py
├── requirements.txt
├── .env
│
├── data/
│   ├── pdf/
│   ├── repos/
│   ├── docs/
│
├── storage/
│   ├── vectorstores/
│   │   ├── pdf_db/
│   │   ├── repo_db/
│   │   ├── docs_db/
│
├── src/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── core/
│   │   ├── engine.py
│   │   ├── vectorstore.py
│   │   ├── embeddings.py
│   │   ├── router.py
│   │
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── repo_loader.py
│   │   ├── base_loader.py
│   │
│   ├── retrieval/
│   │   ├── pdf_retriever.py
│   │   ├── repo_retriever.py
│   │   ├── unified_retriever.py
│   │
│   ├── chat/
│   │   ├── pdf_chat.py
│   │   ├── repo_chat.py
│   │   ├── unified_chat.py
│   │
│   ├── utils/
│       ├── file_utils.py
│       ├── logger.py
```

---

## Key Design Principles

### 1. Separation of Vector Stores

Each data source has its own vector database:

* PDF → pdf_db
* GitHub repo → repo_db
* Documents → docs_db

This prevents embedding conflicts.

---

### 2. Metadata Tagging

Each chunk must include metadata:

```python
metadata = {
    "type": "repo",  # or pdf, docs
    "source": "file path"
}
```

This allows filtering during retrieval.

---

### 3. Query Router (Optional but Powerful)

A router decides which knowledge base to use:

```python
if "code" in query:
    return "repo"
elif "pdf" in query:
    return "pdf"
else:
    return "repo"
```

---

### 4. Retrieval Layer Separation

Each source has its own retriever:

* PDFRetriever → PDF-only search
* RepoRetriever → Code-only search
* UnifiedRetriever → merges results intelligently

---

## Data Flow

### PDF Flow

```
PDF → Loader → Chunking → Embedding → pdf_db → PDF Retriever → LLM
```

### Repo Flow

```
GitHub Repo → File Scanner → Code Chunking → Embedding → repo_db → Repo Retriever → LLM
```

### Unified Flow

```
User Query → Router → Select Retriever → Context → LLM → Response
```

---

## Why This Architecture Works

* Prevents context pollution
* Improves retrieval accuracy
* Scales to multiple data sources
* Enables agent-like behavior
* Easier debugging and maintenance

---

## Common Mistakes to Avoid

❌ Mixing PDFs and code in one vector DB
❌ No metadata tagging
❌ No routing layer
❌ Rebuilding DB without clearing old embeddings

---

## Scaling Roadmap

### Phase 1

* Basic PDF + Repo RAG

### Phase 2

* Separate vector stores
* Metadata filtering

### Phase 3

* Query routing system
* Improved retrieval logic

### Phase 4

* AST parsing for code understanding
* Symbol-level search

### Phase 5

* Full AI coding agent
* File editing tools
* Git integration
* Terminal execution

---

## Final Idea

This architecture is the foundation of modern AI coding assistants and agentic systems.

It is the step between:

* Simple RAG chatbot

and

* Cursor-like AI coding assistant
* Devin-style autonomous agent

---

## Summary

The key principle is simple:

> One source type = one knowledge space

or

> Use routing + metadata filtering to control context
