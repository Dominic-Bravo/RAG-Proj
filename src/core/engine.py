from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from src.config import settings


def format_documents(documents) -> str:
    formatted = []
    for index, doc in enumerate(documents, start=1):
        metadata = doc.metadata or {}
        source = (
            metadata.get("relative_path")
            or metadata.get("source_name")
            or metadata.get("source")
            or "unknown source"
        )
        page = metadata.get("page")
        page_label = f", page {page + 1}" if isinstance(page, int) else ""
        formatted.append(f"[{index}] {source}{page_label}\n{doc.page_content}")

    return "\n\n".join(formatted)


class RAGEngine:
    def __init__(self, custom_template: str = None, llm=None):
        self.llm = llm or self._build_llm()

        system_prompt = custom_template or settings.SYSTEM_PROMPT
        if "{context}" not in system_prompt:
            system_prompt = f"{system_prompt}\n\nContext:\n{{context}}"

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

    def _build_llm(self):
        from langchain_google_genai import ChatGoogleGenerativeAI

        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required to create the chat model.")

        return ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL, 
            temperature=0,
            google_api_key=settings.GOOGLE_API_KEY
        )

    def get_chain(self, retriever):
        return (
            {
                "context": lambda x: format_documents(retriever.invoke(x["question"])),
                "question": lambda x: x["question"],
                "chat_history": lambda x: x.get("chat_history", [])
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
