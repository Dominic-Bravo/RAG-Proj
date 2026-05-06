import pytest
from src.core.ingestion import load_and_split_pdf
import os

def test_load_and_split_pdf():
    # Use your existing PDF for the test
    path = r"C:\Users\63966\Documents\project\RAG-python\Dominic Ian bravo.pdf"
    
    if os.path.exists(path):
        chunks = load_and_split_pdf(path)
        assert len(chunks) > 0
        assert isinstance(chunks, list)
        # Check if chunks have page content
        assert hasattr(chunks[0], "page_content")
    else:
        pytest.skip("Test PDF not found at the specified path.")