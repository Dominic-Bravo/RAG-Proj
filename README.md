 # AI RAG-Python Assistant 🤖

A modular, scalable Retrieval-Augmented Generation (RAG) system built with **Python**, **LangChain**, and **Google Gemini**. This project implements a professional **Service Layer** architecture, featuring persistent vector storage and contextual conversation history. Perfect for developers looking to understand production-grade RAG implementation.

---

## 🚀 Features

*   **Persistent Vector Store:** Uses ChromaDB to save document embeddings locally, avoiding redundant API calls and reducing latency.
*   **Contextual Memory:** Remembers previous interactions in a session using LangChain's `chat_history`.
*   **Modular Architecture:** Clean separation of concerns between data ingestion, vector management, and the RAG engine.
*   **Type Safety & Config:** Robust environment variable handling and validation managed via Pydantic Settings.
*   **Production Ready:** Includes a comprehensive suite of unit and integration tests powered by `pytest`.

---

## 🛠️ Tech Stack

*   **LLM:** Google Gemini 2.5 Flash
*   **Embeddings:** Google Gemini Embedding (001)
*   **Orchestration:** LangChain Expressive Language (LCEL)
*   **Vector Database:** ChromaDB
*   **Environment Management:** `uv` (Fast Python package installer and resolver)

---

## ⚙️ Setup & Installation

### 1. Configure Environment
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here

    ## 📁 Project Structure

    ```text
    rag_project/
    ├── src/
    │   ├── core/
    │   │   ├── ingestion.py    # PDF loading and text splitting
    │   │   ├── vectorstore.py  # ChromaDB & Embedding initialization
    │   │   └── engine.py       # LCEL Chain and RAG logic
    │   ├── config.py           # Global settings via Pydantic
    │   └── main.py             # Entry point (Interactive CLI)
    ├── tests/                  # Pytest suite
    ├── .env                    # API Keys (Git ignored)
    ├── pyproject.toml          # Project dependencies & tool config
    └── chroma_db/              # Persistent vector storage directory