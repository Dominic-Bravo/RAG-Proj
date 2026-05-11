from enum import StrEnum


class SourceType(StrEnum):
    PDF = "pdf"
    REPO = "repo"


COLLECTION_NAMES = {
    SourceType.PDF: "pdf_documents",
    SourceType.REPO: "repository_code",
}
