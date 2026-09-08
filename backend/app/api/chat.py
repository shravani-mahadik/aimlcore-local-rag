from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.rag.rag_service import (
    RAGService
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):

    question: str

    top_k: int = 5


@router.post("")
def chat(
    request: ChatRequest
):

    # -----------------------------------------
    # Validate question
    # -----------------------------------------

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # -----------------------------------------
    # Run RAG
    # -----------------------------------------

    try:

        rag = RAGService()

        result = rag.ask(
            question=request.question,
            top_k=request.top_k
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    # -----------------------------------------
    # Format sources
    # -----------------------------------------

    sources = []

    for item in result["sources"]:

        metadata = item["metadata"]

        sources.append({
            "chunk_id": metadata.get(
                "chunk_id"
            ),
            "document_id": metadata.get(
                "document_id"
            ),
            "page": metadata.get(
                "page"
            ),
            "section": metadata.get(
                "section"
            ),
            "similarity": item["score"],
            "text": metadata.get(
                "text"
            )
        })

    # -----------------------------------------
    # Return response
    # -----------------------------------------

    return {
        "question": result["question"],
        "answer": result["answer"],
        "sources": sources,
        "source_count": len(sources)
    }