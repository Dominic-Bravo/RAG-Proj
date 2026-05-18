import os
from pathlib import Path
from dotenv import load_dotenv

from .repo_chat import start_repo_chat
from langchain_core.messages import AIMessage, HumanMessage 
from src.core.ingestion import load_and_split_pdf
from src.core.vectorstore import get_vectorstore
from src.core.engine import RAGEngine
from src.core.sources import SourceType
from src.config import settings

"""Main entry point for the RAG AI system. Provides a simple CLI to interact with either PDF documents or GitHub repositories.
The user can choose to start a chat session with a PDF or a repo, and the system will load the relevant data, create a vector store, and use a RAG engine to answer questions based on the content. The system also supports a one-time query mode for quick questions without maintaining chat history.
test
"""
load_dotenv()

DEFAULT_PDF_PATH = Path(os.getenv("DEFAULT_PDF_PATH", "Dominic Ian bravo.pdf"))

def run_single_query(file_path: str, query: str, custom_prompt: str = None):
    """Runs a one-time RAG query without history."""
    chunks = load_and_split_pdf(file_path)
    vectorstore = get_vectorstore(chunks, source_type=SourceType.PDF)
    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.DEFAULT_K})
    
    engine = RAGEngine(custom_template=custom_prompt)
    chain = engine.get_chain(retriever)
    
    # Must pass as dict because engine now expects "question" and "chat_history"
    return chain.invoke({"question": query, "chat_history": []})

def start_interactive_chat(file_path: str):
    """Starts a continuous chat session with memory."""
    print(f"--- Loading Document: {os.path.basename(file_path)} ---")
    chunks = load_and_split_pdf(file_path)
    vectorstore = get_vectorstore(chunks, source_type=SourceType.PDF)
    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.DEFAULT_K})
    
    engine = RAGEngine()
    chain = engine.get_chain(retriever)
    
    chat_history = []
    
    print("\n[AI Chatbot Ready! Type 'exit' to quit]\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']: 
            break
        
        response = chain.invoke({
            "question": user_input,
            "chat_history": chat_history
        })
        
        print(f"\nAI: {response}\n")
        
        chat_history.extend([
            HumanMessage(content=user_input),
            AIMessage(content=response)
        ])
    
def main():
    print("==== RAG AI SYSTEM ====")
    print("1. PDF Chat")
    print("2. Repo Coding Assistant")

    choice = input("\nChoose option: ")
    
    if choice == "1":
        pdf_path = input(f"Enter PDF path [{DEFAULT_PDF_PATH}]: ").strip()
        start_interactive_chat(pdf_path or str(DEFAULT_PDF_PATH))
    elif choice == "2":
        
        repo_path = input("Enter repo path or GitHub URL: ")
        start_repo_chat(repo_path)
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
