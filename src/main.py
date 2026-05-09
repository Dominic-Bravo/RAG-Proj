import os
from dotenv import load_dotenv
# Corrected import path
from langchain_core.messages import AIMessage, HumanMessage 
from src.core.ingestion import load_and_split_pdf
from src.core.vectorstore import get_vectorstore
from src.core.engine import RAGEngine

load_dotenv()

# Global Config for ease of use
PATH = r"C:\Users\63966\Documents\project\RAG-python\Dominic Ian bravo.pdf"

def run_single_query(file_path: str, query: str, custom_prompt: str = None):
    """Runs a one-time RAG query without history."""
    chunks = load_and_split_pdf(file_path)
    vectorstore = get_vectorstore(chunks)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    engine = RAGEngine(custom_template=custom_prompt)
    chain = engine.get_chain(retriever)
    
    # Must pass as dict because engine now expects "question" and "chat_history"
    return chain.invoke({"question": query, "chat_history": []})

def start_interactive_chat(file_path: str):
    """Starts a continuous chat session with memory."""
    print(f"--- Loading Document: {os.path.basename(file_path)} ---")
    chunks = load_and_split_pdf(file_path)
    vectorstore = get_vectorstore(chunks)
    retriever = vectorstore.as_retriever()
    
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
    
if __name__ == "__main__":
    # Choose your mode:
    # 1. For a single response:
    # result = run_single_query(PATH, "What are his top 3 skills?")
    # print(result)

    # 2. For the interactive experience (recommended for testing memory):
    # start_interactive_chat(PATH)
    
    print("==== RAG AI SYSTEM ====")
    print("1. PDF Chat")
    print("2. Repo Coding Assistant")

    choice = input("\nChoose option: ")
    
    if choice == "1":
        start_interactive_chat(PATH)
    elif choice == "2":
        from src.repo_chat import start_repo_chat
        repo_path = input("Enter repo path: ")
        start_repo_chat(repo_path)
    else:
        print("Invalid choice. Exiting.")