from dataclasses import dataclass


@dataclass
class DocumentChunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    page: int | None = None
    section: str | None = None
    token_count: int = 0


def chunk_text(
    text: str,
    document_id: str,
    chunk_size: int = 600,
    overlap: int = 100,
    page: int | None = None,
    section: str | None = None
) -> list[DocumentChunk]:
    """
    Split document text into overlapping chunks
    and attach metadata to every chunk.
    """

    if not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    words = text.split()

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(words):

        end = start + chunk_size

        chunk_text_value = " ".join(words[start:end])

        if chunk_text_value.strip():

            chunk = DocumentChunk(
                chunk_id=f"{document_id}_chunk_{chunk_index}",
                document_id=document_id,
                chunk_index=chunk_index,
                text=chunk_text_value,
                page=page,
                section=section,
                token_count=len(chunk_text_value.split())
            )

            chunks.append(chunk)

            chunk_index += 1

        start += chunk_size - overlap

    return chunks