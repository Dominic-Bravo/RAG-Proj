from langchain_core.messages import HumanMessage, AIMessage

from src.core import split_repo
from src.core.vectorstore import get_vectorstore
from src.core.engine import RAGEngine


def start_repo_chat(repo_path: str):

    chunks = split_repo(repo_path)

    vectorstore = get_vectorstore(chunks)

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 8}
    )

    engine = RAGEngine()

    chain = engine.get_chain(retriever)

    chat_history = []

    print("\n[AI Coding Assistant Ready]\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = chain.invoke({
            "question": user_input,
            "chat_history": chat_history
        })

        answer = response["answer"]

        print(f"\nAI: {answer}\n")

        print("\nSources:")

        for doc in response["source_documents"]:

            print(doc.metadata.get("source"))

        print()

        chat_history.extend([
            HumanMessage(content=user_input),
            AIMessage(content=answer)
        ])