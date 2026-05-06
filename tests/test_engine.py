from unittest.mock import MagicMock
from src.core.engine import RAGEngine
from langchain_core.runnables import RunnableSequence

def test_engine_initialization():
    engine = RAGEngine()
    assert engine.llm.model == "gemini-2.5-flash"
    
    # Create a "fake" retriever instead of None
    mock_retriever = MagicMock()
    
    # Now it won't crash!
    chain = engine.get_chain(retriever=mock_retriever)
    
    # Verify it created a valid LangChain sequence
    assert isinstance(chain, RunnableSequence)