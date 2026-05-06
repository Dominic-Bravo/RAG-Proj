This is a professional README.md designed to showcase your project's architecture and technical stack—perfect for your portfolio.

AI RAG-Python Assistant 🤖
A modular, scalable Retrieval-Augmented Generation (RAG) system built with Python, LangChain, and Google Gemini. This project implements a professional "Service Layer" architecture, allowing for persistent vector storage and contextual conversation history.

🚀 Features
Persistent Vector Store: Uses ChromaDB to save document embeddings locally, avoiding redundant API calls.

Contextual Memory: Remembers previous interactions in a session using LangChain's chat_history.

Modular Architecture: Clean separation between data ingestion, vector management, and the RAG engine.

Type Safety & Config: Managed via Pydantic Settings for robust environment variable handling.

Production Ready: Includes a full suite of pytest unit and integration tests.

🛠️ Tech Stack
LLM: Google Gemini 2.5 Flash

Embeddings: Google Gemini Embedding (001)

Orchestration: LangChain (LCEL)

Vector Database: ChromaDB

Environment Management: uv (Fast Python package installer)

📁 Project Structure
Plaintext
rag_project/
├── src/
│   ├── core/
│   │   ├── ingestion.py    # PDF loading and text splitting
│   │   ├── vectorstore.py  # ChromaDB & Embedding initialization
│   │   └── engine.py       # LCEL Chain and RAG logic
│   ├── config.py           # Global settings via Pydantic
│   └── main.py             # Entry point (Interactive CLI)
├── tests/                  # Pytest suite
├── .env                    # API Keys (git ignored)
├── pyproject.toml          # Project dependencies
└── chroma_db/              # Persistent vector storage
⚙️ Setup & Installation
1. Prerequisites
Ensure you have uv installed (or use pip).

2. Environment Setup
Create a .env file in the root directory:

Code snippet
GOOGLE_API_KEY=your_gemini_api_key_here
3. Install Dependencies
PowerShell
uv pip install -e .
🎮 Usage
To start the interactive AI chatbot using your local document as context:

PowerShell
python -m src.main
The system will:

Load the PDF defined in main.py.

Chunk and embed the text into a local database.

Start a chat loop where you can ask questions and follow-ups.

🧪 Testing
The project uses pytest for quality assurance. To run the tests:

PowerShell
python -m pytest
The test suite covers:

Ingegstion: Verifies PDF parsing and chunking logic.

Configuration: Ensures environment variables are correctly mapped.

Engine: Validates the LangChain sequence construction using Mocks.

🛡️ Best Practices Implemented
Decoupling: The UI (main.py) is separated from the business logic (engine.py).

Persistence: Data is stored on disk, not just in RAM.

Scalability: The RAGEngine class can be imported directly into a FastAPI or Django project.

Extensibility: Easily swap Gemini for OpenAI or Chroma for Pinecone by modifying the core modules.

Developed by: Dominic Ian Bravo