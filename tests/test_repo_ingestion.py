from pathlib import Path

from src.core.repo_ingestion import load_repo


def test_load_repo_tags_code_documents(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "app.py").write_text("print('hello')", encoding="utf-8")
    (repo / "image.png").write_bytes(b"not scanned")

    docs = load_repo(str(repo))

    assert len(docs) == 1
    assert docs[0].metadata["type"] == "repo"
    assert docs[0].metadata["relative_path"] == "app.py"
    assert docs[0].metadata["language"] == "py"
