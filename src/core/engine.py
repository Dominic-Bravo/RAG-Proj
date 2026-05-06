from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config import settings

class RAGEngine:
    def __init__(self, custom_template: str = None):
       # Inside RAGEngine.__init__
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL, 
            temperature=0,
            google_api_key=settings.GOOGLE_API_KEY # Ensure this is here
        )
        
        default_template = """Answer the question based strictly on the provided context:
{context}

Question: {question}

If the answer is not in the context, clearly state that the information is not available."""
        
        self.prompt = ChatPromptTemplate.from_template(custom_template or default_template)

    def get_chain(self, retriever):
        return (
            {"context": retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )