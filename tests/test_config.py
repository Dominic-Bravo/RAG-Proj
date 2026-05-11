from src.config import settings

# Testing load
def test_settings_load():
    assert settings.GOOGLE_API_KEY is not None
    assert settings.CHUNK_SIZE == 700
    assert "models/gemini" in settings.EMBEDDING_MODEL