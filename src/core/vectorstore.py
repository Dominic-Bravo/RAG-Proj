from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from src.config import settings

def get_vectorstore(chunks=None):
    # Pass the API key explicitly here
    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        task_type="retrieval_document",
        google_api_key=settings.GOOGLE_API_KEY 
    )
    
    if chunks:
        vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings,
            persist_directory=settings.VECTOR_DB_DIR
        )
    else:
        vectorstore = Chroma(
            persist_directory=settings.VECTOR_DB_DIR,
            embedding_function=embeddings
        )
        
    return vectorstore

# update the rpo chats retrieval 

# vectorstore = get_vectorstore(chunks, "pdf_db")
# vectorstore = get_vectorstore(chunks, "repo_db")

# def get_vectorstore(documents, collection_name: str):

#     embeddings = get_embeddings()

#     vectorstore = Chroma.from_documents(
#         documents=documents,
#         embedding=embeddings,
#         persist_directory=f"chroma_db/{collection_name}",
#         collection_name=collection_name
#     )

#     return vectorstore