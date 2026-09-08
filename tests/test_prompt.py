from backend.app.services.generation.llm_service import (
    build_grounded_prompt
)


retrieved_chunks = [
    {
        "score": 0.3330,
        "metadata": {
            "document_id": "sample_document_001",
            "page": 1,
            "chunk_id": "sample_document_001_chunk_0",
            "text": (
                "We are delighted to offer you the "
                "position of AI/ML Engineer at AIMLCore."
            )
        }
    }
]


question = "What position was I offered?"


prompt = build_grounded_prompt(
    question,
    retrieved_chunks
)


print("\n===== GROUNDED PROMPT TEST =====")

print(prompt)

print("\n===== SUCCESS =====")
