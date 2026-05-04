🧠 Document Intelligence RAG System
A high-performance Retrieval-Augmented Generation (RAG) pipeline built to turn static PDF documents into actionable intelligence. This system leverages semantic search to provide accurate, grounded responses based strictly on provided technical documents, effectively eliminating LLM hallucinations.

🚀 Technical Highlights
Modern Python Tooling: Managed with uv for lightning-fast dependency resolution and reproducible environments.

Advanced Orchestration: Built using LangChain Expression Language (LCEL) for a modular and transparent data pipeline.

State-of-the-Art Models: Utilizes Gemini 2.5 Flash for reasoning and gemini-embedding-001 for high-dimensional vector search.

Vector Infrastructure: Implements ChromaDB as a vector store for efficient semantic retrieval.

🛠 Tech Stack
Core: Python 3.12+

Framework: LangChain

LLM & Embeddings: Google Gemini API

Vector Store: ChromaDB

Environment: uv & python-dotenv

📋 System Architecture
Ingestion: Parses local PDFs using PyPDFLoader.

Transformation: Breaks text into 700-character chunks with 100-character overlap using RecursiveCharacterTextSplitter to preserve semantic context.

Embedding: Converts text chunks into vectors using Google’s retrieval-optimized embedding models.

Retrieval: Performs a similarity search to extract the most relevant context for any given query.

Generation: Augments the LLM prompt with retrieved context to ensure responses are "grounded" in the source material.

⚙️ Setup & Installation
1. Clone the environment:

Bash
cd RAG-python
2. Install dependencies with uv:

Bash
uv sync
uv add langchain langchain-google-genai langchain-chroma langchain-community pypdf python-dotenv
3. Configure Environment:
Create a .env file in the root directory:

Plaintext
GOOGLE_API_KEY=your_gemini_api_key_here
4. Run the Pipeline:

Bash
uv run python main.py
🛡 Security & Best Practices
Credential Management: API keys are managed via .env variables and are excluded from version control via .gitignore.

Factual Integrity: The system is configured with temperature: 0 and strict prompt constraints to ensure output is strictly derivative of the input document.