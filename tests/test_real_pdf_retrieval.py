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


PDF_PATH = r"data\sample.pdf"
DOCUMENT_ID = "sample_document_001"


print("\n===== REAL PDF RAG RETRIEVAL TEST =====")


# --------------------------------------------------
# 1. Extract PDF pages
# --------------------------------------------------

pages = extract_pdf_pages(PDF_PATH)

print(f"Pages extracted: {len(pages)}")


# --------------------------------------------------
# 2. Create chunks
# --------------------------------------------------

all_chunks = []

for page_data in pages:

    page_chunks = chunk_text(
        text=page_data["text"],
        document_id=DOCUMENT_ID,
        chunk_size=600,
        overlap=100,
        page=page_data["page"]
    )

    all_chunks.extend(page_chunks)


print(f"Chunks created: {len(all_chunks)}")


# --------------------------------------------------
# 3. Create embeddings
# --------------------------------------------------

embedding_service = EmbeddingService()

texts = [
    chunk.text
    for chunk in all_chunks
]

embeddings = embedding_service.embed_texts(texts)


print(
    f"Embedding shape: {embeddings.shape}"
)


# --------------------------------------------------
# 4. Create FAISS index
# --------------------------------------------------

vector_store = FAISSVectorStore(
    dimension=embeddings.shape[1]
)


# --------------------------------------------------
# 5. Store metadata
# --------------------------------------------------

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


vector_store.add(
    embeddings,
    metadata
)


print(
    f"Vectors stored: {vector_store.count()}"
)


# --------------------------------------------------
# 6. Ask a question
# --------------------------------------------------

query = input(
    "\nAsk a question about the PDF: "
)


# --------------------------------------------------
# 7. Embed the question
# --------------------------------------------------

query_embedding = embedding_service.embed_query(
    query
)


# --------------------------------------------------
# 8. Search FAISS
# --------------------------------------------------

results = vector_store.search(
    query_embedding,
    top_k=3
)


# --------------------------------------------------
# 9. Display results
# --------------------------------------------------

print("\n===== RETRIEVED SOURCES =====")


for rank, result in enumerate(
    results,
    start=1
):

    metadata = result["metadata"]

    print("\n-------------------------")

    print(f"Rank: {rank}")

    print(
        f"Similarity: "
        f"{result['score']:.4f}"
    )

    print(
        f"Document: "
        f"{metadata['document_id']}"
    )

    print(
        f"Page: "
        f"{metadata['page']}"
    )

    print(
        f"Chunk: "
        f"{metadata['chunk_id']}"
    )

    print(
        f"Text:\n"
        f"{metadata['text']}"
    )


print("\n===== SUCCESS =====")