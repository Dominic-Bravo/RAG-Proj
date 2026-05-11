from src.core.engine import RAGEngine
from langchain_core.runnables import RunnableLambda, RunnableSequence

def test_engine_initialization():
    fake_llm = RunnableLambda(lambda messages: "ok")
    engine = RAGEngine(llm=fake_llm)
    assert engine.llm is fake_llm
    
    fake_retriever = RunnableLambda(lambda question: [])
    
    chain = engine.get_chain(retriever=fake_retriever)
    
    assert isinstance(chain, RunnableSequence)
