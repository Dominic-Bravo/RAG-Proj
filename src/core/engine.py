from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config import settings

class RAGEngine:
    def __init__(self, custom_template: str = None):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL, 
            temperature=0,
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        # Updated template to support history
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", custom_template or "Answer based on context: {context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])

    def get_chain(self, retriever):
        return (
            {
                # FIX: Use a lambda or itemgetter to pull just the "question" for the retriever
                "context": lambda x: retriever.invoke(x["question"]), 
                "question": lambda x: x["question"],
                "chat_history": lambda x: x.get("chat_history", [])
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )