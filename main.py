import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma 
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURATION ---
# Load environment variables from the .env file
load_dotenv()

# --- 1. DATA INGESTION ---
# Load the PDF from your local directory
file_path = r"C:\Users\63966\Documents\project\RAG-python\Dominic Ian bravo.pdf"
loader = PyPDFLoader(file_path)
docs = loader.load()

# --- 2. DOCUMENT CHUNKING ---
# Split the document into small, manageable pieces for the AI
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700, 
    chunk_overlap=100
)
chunks = text_splitter.split_documents(docs)

# sample chunking configuration with custom separators (uncomment if needed)
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=100,
#     separators=[
#         "\n\n",  # paragraphs
#         "\n",    # lines
#         ".",     # sentences
#         " ",     # words
#     ]
# )

# sample chunking configuration for markdown documents (uncomment if needed)
# from langchain.text_splitter import MarkdownHeaderTextSplitter

# headers_to_split_on = [
#     ("#", "Header 1"),
#     ("##", "Header 2"),
#     ("###", "Header 3"),
# ]

# splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
# chunks = splitter.split_text(markdown_text)


# --- 3. VECTOR STORAGE ---
# gemini-embedding-001 is the stable standard for 2026 RAG pipelines
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    task_type="retrieval_document"
)

# Initialize the vector database (in-memory)
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
retriever = vectorstore.as_retriever()

# --- 4. PROMPT ENGINEERING ---

template = """Answer the question based strictly on the provided document context:
{context}

Question: {question}

If the answer is not in the context, clearly state that the information is not available.
"""

prompt = ChatPromptTemplate.from_template(template)

# --- 5. MODEL SETUP ---
# Using the 2026 LTS version of Flash for efficiency and reliability
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0
)

# --- 6. RAG CHAIN (LCEL) ---
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 7. EXECUTION ---
if __name__ == "__main__":
    query = "List the technical skills for Dominic Ian Bravo."
    print(f"\n--- AI RESPONSE ---\n")
    print(chain.invoke(query))