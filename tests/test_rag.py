from backend.app.services.rag.rag_service import (
    RAGService
)


INDEX_DIRECTORY = (
    "data/indexes/sample_document_001"
)


print("\n========================================")
print("          REAL RAG TEST")
print("========================================")


rag = RAGService(
    INDEX_DIRECTORY
)


question = "What position was I offered?"


result = rag.ask(
    question,
    top_k=3
)


print("\n===== QUESTION =====")
print(result["question"])


print("\n===== ANSWER =====")
print(result["answer"])


print("\n===== SOURCES =====")

for source in result["sources"]:

    metadata = source["metadata"]

    print("\n-------------------------")

    print(
        f"Document: "
        f"{metadata.get('document_id')}"
    )

    print(
        f"Page: "
        f"{metadata.get('page')}"
    )

    print(
        f"Similarity: "
        f"{source['score']:.4f}"
    )

    print(
        f"Chunk: "
        f"{metadata.get('chunk_id')}"
    )


print("\n===== SUCCESS =====")