from backend.app.services.retrieval.multi_document_retriever import (
    MultiDocumentRetriever
)

from backend.app.services.generation.llm_service import (
    LLMService,
    build_grounded_prompt
)


class RAGService:
    """
    Multi-document Retrieval Augmented Generation service.

    Question
        ↓
    Search ALL documents
        ↓
    Retrieve relevant chunks
        ↓
    Grounded prompt
        ↓
    Ollama
        ↓
    Answer + sources
    """

    def __init__(
        self,
        indexes_directory: str = "data/indexes"
    ):

        self.retriever = MultiDocumentRetriever(
            indexes_directory
        )

        self.llm_service = LLMService()

    def ask(
        self,
        question: str,
        top_k: int = 5
    ):

        # -----------------------------------------
        # 1. Retrieve from all documents
        # -----------------------------------------

        results = self.retriever.search(
            question=question,
            top_k=top_k
        )

        # -----------------------------------------
        # 2. Build context
        # -----------------------------------------

        context_parts = []

        for rank, result in enumerate(
            results,
            start=1
        ):

            metadata = result["metadata"]

            context_parts.append(
                f"""
SOURCE {rank}
Document: {metadata.get("document_id")}
Page: {metadata.get("page")}
Chunk: {metadata.get("chunk_id")}
Similarity: {result["score"]:.4f}

Content:
{metadata.get("text")}
""".strip()
            )

        context = "\n\n".join(
            context_parts
        )

        # -----------------------------------------
        # 3. Build grounded prompt
        # -----------------------------------------

        prompt = build_grounded_prompt(
            question=question,
            context=context
        )

        # -----------------------------------------
        # 4. Generate answer
        # -----------------------------------------

        answer = self.llm_service.generate(
            prompt
        )

        # -----------------------------------------
        # 5. Return answer + sources
        # -----------------------------------------

        return {
            "question": question,
            "answer": answer,
            "sources": results
        }