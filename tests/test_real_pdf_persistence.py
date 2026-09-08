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


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PDF_PATH = r"data\sample.pdf"

DOCUMENT_ID = "sample_document_001"

INDEX_DIR = r"indexes\sample_document_001"


print("\n========================================")
print("   REAL PDF FAISS PERSISTENCE TEST")
print("========================================")


# --------------------------------------------------
# 1. Extract PDF
# --------------------------------------------------

print("\n[1] Extracting PDF...")

pages = extract_pdf_pages(
    PDF_PATH
)

print(
    f"Pages extracted: {len(pages)}"
)


# --------------------------------------------------
# 2. Create page-aware chunks
# --------------------------------------------------

print("\n[2] Creating chunks...")

all_chunks = []

for page in pages:

    chunks = chunk_text(
        text=page["text"],
        document_id=DOCUMENT_ID,
        chunk_size=600,
        overlap=100,
        page=page["page"]
    )

    all_chunks.extend(chunks)


print(
    f"Total chunks: {len(all_chunks)}"
)


# --------------------------------------------------
# 3. Create embeddings
# --------------------------------------------------

print("\n[3] Creating embeddings...")

embedding_service = EmbeddingService()

texts = [
    chunk.text
    for chunk in all_chunks
]

embeddings = embedding_service.embed_texts(
    texts
)

print(
    f"Embedding shape: {embeddings.shape}"
)


# --------------------------------------------------
# 4. Create FAISS store
# --------------------------------------------------

print("\n[4] Creating FAISS vector store...")

store = FAISSVectorStore(
    dimension=embeddings.shape[1]
)


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


store.add(
    embeddings,
    metadata
)


print(
    f"Vectors stored: {store.count()}"
)


# --------------------------------------------------
# 5. Save FAISS index
# --------------------------------------------------

print("\n[5] Saving index...")

store.save(
    INDEX_DIR
)


# --------------------------------------------------
# 6. Verify files
# --------------------------------------------------

index_file = os.path.join(
    INDEX_DIR,
    "index.faiss"
)

metadata_file = os.path.join(
    INDEX_DIR,
    "metadata.json"
)


assert os.path.exists(index_file)

assert os.path.exists(metadata_file)


print("FAISS index file: OK")
print("Metadata file: OK")


# --------------------------------------------------
# 7. Load saved index
# --------------------------------------------------

print("\n[6] Loading saved index...")

loaded_store = FAISSVectorStore.load(
    INDEX_DIR
)


print(
    f"Vectors loaded: {loaded_store.count()}"
)


# --------------------------------------------------
# 8. Create query
# --------------------------------------------------

question = "What position was I offered?"

print(
    f"\nQuestion: {question}"
)


query_embedding = embedding_service.embed_query(
    question
)


# --------------------------------------------------
# 9. Search loaded FAISS index
# --------------------------------------------------

print("\n[7] Searching saved index...")

results = loaded_store.search(
    query_embedding,
    top_k=3
)


# --------------------------------------------------
# 10. Display results
# --------------------------------------------------

print("\n===== RETRIEVED SOURCES =====")


for rank, result in enumerate(
    results,
    start=1
):

    metadata_item = result["metadata"]

    print("\n-------------------------")

    print(
        f"Rank: {rank}"
    )

    print(
        f"Similarity: "
        f"{result['score']:.4f}"
    )

    print(
        f"Document: "
        f"{metadata_item['document_id']}"
    )

    print(
        f"Page: "
        f"{metadata_item['page']}"
    )

    print(
        f"Chunk: "
        f"{metadata_item['chunk_id']}"
    )

    print(
        f"Text:\n"
        f"{metadata_item['text']}"
    )


# --------------------------------------------------
# 11. Verify
# --------------------------------------------------

assert loaded_store.count() == len(all_chunks)

assert len(results) > 0

assert (
    results[0]["metadata"]["document_id"]
    == DOCUMENT_ID
)


print("\n========================================")
print("             ===== SUCCESS =====")
print("========================================")

print(
    "Real PDF was embedded, stored in FAISS, "
    "saved to disk, loaded again and searched."
)