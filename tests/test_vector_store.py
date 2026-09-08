from backend.app.services.embeddings.embedding_service import (
    EmbeddingService
)

from backend.app.services.retrieval.vector_store import (
    FAISSVectorStore
)


print("\n===== FAISS VECTOR SEARCH TEST =====")


# Create embedding service
embedding_service = EmbeddingService()


# Example document chunks
documents = [
    "Employees receive paid annual leave according to company policy.",
    "The company provides technical support for its software products.",
    "Employees must complete onboarding training during their first week.",
    "Invoices must be submitted to the finance department.",
]


# Generate document embeddings
embeddings = embedding_service.embed_texts(
    documents
)


# Create FAISS store
vector_store = FAISSVectorStore(
    dimension=embeddings.shape[1]
)


# Add documents
metadata = []

for index, document in enumerate(documents):

    metadata.append({
        "chunk_id": f"chunk_{index}",
        "document_id": "demo_document",
        "page": index + 1,
        "text": document
    })


vector_store.add(
    embeddings,
    metadata
)


print(f"Vectors stored: {vector_store.count()}")


# User question
query = "How much annual leave do employees get?"


query_embedding = embedding_service.embed_query(
    query
)


# Search
results = vector_store.search(
    query_embedding,
    top_k=3
)


print("\n===== SEARCH RESULTS =====")


for rank, result in enumerate(results, start=1):

    print(f"\nResult {rank}")

    print(
        f"Similarity: {result['score']:.4f}"
    )

    print(
        f"Chunk ID: "
        f"{result['metadata']['chunk_id']}"
    )

    print(
        f"Page: "
        f"{result['metadata']['page']}"
    )

    print(
        f"Text: "
        f"{result['metadata']['text']}"
    )


print("\n===== SUCCESS =====")