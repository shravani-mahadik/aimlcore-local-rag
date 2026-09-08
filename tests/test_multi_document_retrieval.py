from backend.app.services.retrieval.multi_document_retriever import (
    MultiDocumentRetriever
)


print("\n========================================")
print("      MULTI-DOCUMENT RETRIEVAL TEST")
print("========================================")


retriever = MultiDocumentRetriever()


question = "What position was I offered?"


results = retriever.search(
    question=question,
    top_k=5
)


print("\n===== SEARCH RESULTS =====")


for rank, result in enumerate(
    results,
    start=1
):

    metadata = result["metadata"]

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
        f"{metadata.get('document_id')}"
    )

    print(
        f"Page: "
        f"{metadata.get('page')}"
    )

    print(
        f"Chunk: "
        f"{metadata.get('chunk_id')}"
    )

    print(
        f"Text: "
        f"{metadata.get('text')[:200]}..."
    )


print("\n===== SUCCESS =====")

print(
    f"Total results: {len(results)}"
)