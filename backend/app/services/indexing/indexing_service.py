import os

from backend.app.services.ingestion.document_parser import (
    extract_pdf_pages
)

from backend.app.services.chunking.chunker import (
    chunk_text
)

from backend.app.services.embeddings.embedding_service import (
    EmbeddingService
)

from backend.app.services.retrieval.vector_store import (
    FAISSVectorStore
)


class IndexingService:
    """
    Handles the complete document indexing pipeline:

    Document
        ↓
    Text extraction
        ↓
    Chunking
        ↓
    Embeddings
        ↓
    FAISS index
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def index_pdf(
        self,
        file_path: str,
        document_id: str
    ):

        # 1. Extract PDF pages
        pages = extract_pdf_pages(file_path)

        if not pages:
            raise ValueError(
                "No text could be extracted from PDF."
            )

        # 2. Create chunks
        all_chunks = []

        for page in pages:

            chunks = chunk_text(
                text=page["text"],
                document_id=document_id,
                chunk_size=600,
                overlap=100,
                page=page["page"]
            )

            all_chunks.extend(chunks)

        if not all_chunks:
            raise ValueError(
                "No chunks were created."
            )

        # 3. Create embeddings
        texts = [
            chunk.text
            for chunk in all_chunks
        ]

        embeddings = (
            self.embedding_service.embed_texts(texts)
        )

        # 4. Create FAISS vector store
        vector_store = FAISSVectorStore(
            dimension=embeddings.shape[1]
        )

        # 5. Create metadata
        metadata = []

        for chunk in all_chunks:

            metadata.append({
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "page": chunk.page,
                "section": chunk.section,
                "text": chunk.text,
                "token_count": chunk.token_count
            })

        # 6. Add embeddings to FAISS
        vector_store.add(
            embeddings,
            metadata
        )

        # 7. Save index
        index_directory = os.path.join(
            "data",
            "indexes",
            document_id
        )

        vector_store.save(
            index_directory
        )

        # 8. Return result
        return {
            "document_id": document_id,
            "pages": len(pages),
            "chunks": len(all_chunks),
            "vectors": vector_store.count(),
            "index_directory": index_directory
        }