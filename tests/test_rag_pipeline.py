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

from backend.app.services.generation.llm_service import (
    OllamaLLM,
    build_grounded_prompt
)


PDF_PATH = r"data\sample.pdf"

DOCUMENT_ID = "sample_document_001"


print("\n========================================")
print("       AIMLCORE LOCAL RAG TEST")
print("========================================")


# --------------------------------------------------
# 1. PDF EXTRACTION
# --------------------------------------------------

print("\n[1] Extracting PDF...")

pages = extract_pdf_pages(PDF_PATH)

print(
    f"Pages extracted: {len(pages)}"
)


# --------------------------------------------------
# 2. CHUNKING
# --------------------------------------------------

print("\n[2] Creating chunks...")

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


print(
    f"Chunks created: {len(all_chunks)}"
)


# --------------------------------------------------
# 3. EMBEDDINGS
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
# 4. FAISS VECTOR STORE
# --------------------------------------------------

print("\n[4] Building FAISS index...")

vector_store = FAISSVectorStore(
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


vector_store.add(
    embeddings,
    metadata
)


print(
    f"Vectors stored: {vector_store.count()}"
)


# --------------------------------------------------
# 5. USER QUESTION
# --------------------------------------------------

question = input(
    "\nAsk a question about the PDF: "
)


# --------------------------------------------------
# 6. QUERY EMBEDDING
# --------------------------------------------------

print("\n[5] Searching knowledge base...")

query_embedding = embedding_service.embed_query(
    question
)


# --------------------------------------------------
# 7. FAISS RETRIEVAL
# --------------------------------------------------

results = vector_store.search(
    query_embedding,
    top_k=3
)


print(
    f"Retrieved sources: {len(results)}"
)


# --------------------------------------------------
# 8. SHOW SOURCES
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


# --------------------------------------------------
# 9. BUILD GROUNDED PROMPT
# --------------------------------------------------

print("\n[6] Building grounded prompt...")

prompt = build_grounded_prompt(
    question,
    results
)


# --------------------------------------------------
# 10. CALL OLLAMA
# --------------------------------------------------

print("\n[7] Generating answer with Ollama...")

llm = OllamaLLM(
    model="llama3.2:3b"
)


answer = llm.generate(
    prompt
)


# --------------------------------------------------
# 11. FINAL ANSWER
# --------------------------------------------------

print("\n========================================")

print("             FINAL ANSWER")

print("========================================")

print(answer)


# --------------------------------------------------
# 12. SOURCES
# --------------------------------------------------

print("\n========================================")

print("               SOURCES")

print("========================================")


for rank, result in enumerate(
    results,
    start=1
):

    metadata = result["metadata"]

    print(
        f"{rank}. "
        f"{metadata['document_id']} | "
        f"Page {metadata['page']} | "
        f"{metadata['chunk_id']} | "
        f"Similarity "
        f"{result['score']:.4f}"
    )


print("\n===== RAG PIPELINE SUCCESS =====")