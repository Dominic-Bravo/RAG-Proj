from src.config import settings

# Testing load
def test_settings_load():
    assert settings.CHUNK_SIZE == 700
    assert "models/gemini" in settings.EMBEDDING_MODEL
    assert ".py" in settings.SUPPORTED_CODE_EXTENSIONS
