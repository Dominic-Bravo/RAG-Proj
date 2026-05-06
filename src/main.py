import os
from src.core.ingestion import load_and_split_pdf
from src.core.vectorstore import get_vectorstore
from src.core.engine import RAGEngine

def run_rag_pipeline(file_path: str, query: str, custom_prompt: str = None):
    # 1. Ingest document
    print(f"--- Processing: {file_path} ---")
    chunks = load_and_split_pdf(file_path)
    
    # 2. Setup Vector Store (Persistent)
    vectorstore = get_vectorstore(chunks)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # 3. Setup RAG Engine
    rag_engine = RAGEngine(custom_template=custom_prompt)
    chain = rag_engine.get_chain(retriever)
    
    # 4. Execute Query
    print(f"--- Querying AI ---")
    return chain.invoke(query)

if __name__ == "__main__":
    # DYNAMIC INPUTS
    PATH = r"C:\Users\63966\Documents\project\RAG-python\Dominic Ian bravo.pdf"
    QUERY = "List the technical skills for Dominic Ian Bravo and where he lives."
    
    # Example: You can pass a totally different prompt structure here
    PROMPT = "Context: {context} \n\n Task: Summarize skills and where he lives for {question}"

    response = run_rag_pipeline(PATH, QUERY, custom_prompt=PROMPT)
    print(f"\nRESULT:\n{response}")