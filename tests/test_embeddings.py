from backend.app.services.embeddings.embedding_service import (
    EmbeddingService
)


try:

    print("\n===== EMBEDDING TEST =====")

    service = EmbeddingService()

    texts = [
        "Employees are eligible for paid leave.",
        "The company provides annual vacation days.",
        "The weather is sunny today."
    ]

    embeddings = service.embed_texts(texts)

    print(f"Model: {service.model_name}")
    print(f"Number of texts: {len(texts)}")
    print(f"Embedding shape: {embeddings.shape}")

    query = "How many vacation days do employees get?"

    query_embedding = service.embed_query(query)

    print(
        f"Query embedding shape: {query_embedding.shape}"
    )

    print("\n===== SUCCESS =====")


except Exception as e:

    print("\n===== ERROR =====")
    print(e)