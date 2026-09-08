import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.embeddings.embedding_service import (
    EmbeddingService
)

from backend.app.services.retrieval.vector_store import (
    FAISSVectorStore
)


router = APIRouter(
    prefix="/api",
    tags=["Search"]
)


class SearchRequest(BaseModel):

    question: str

    top_k: int = 5


INDEX_ROOT = os.path.join(
    "data",
    "indexes"
)


@router.post("/search")
def search_knowledge_base(
    request: SearchRequest
):

    # -----------------------------------------
    # 1. Validate question
    # -----------------------------------------

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    # -----------------------------------------
    # 2. Check index directory
    # -----------------------------------------

    if not os.path.exists(INDEX_ROOT):

        raise HTTPException(
            status_code=404,
            detail="Knowledge base index not found."
        )


    # -----------------------------------------
    # 3. Load embedding model
    # -----------------------------------------

    embedding_service = EmbeddingService()


    # -----------------------------------------
    # 4. Create query embedding
    # -----------------------------------------

    query_embedding = (
        embedding_service.embed_query(
            request.question
        )
    )


    # -----------------------------------------
    # 5. Find all document indexes
    # -----------------------------------------

    document_indexes = []

    for document_id in os.listdir(INDEX_ROOT):

        index_directory = os.path.join(
            INDEX_ROOT,
            document_id
        )

        if not os.path.isdir(
            index_directory
        ):
            continue

        index_file = os.path.join(
            index_directory,
            "index.faiss"
        )

        metadata_file = os.path.join(
            index_directory,
            "metadata.json"
        )

        if (
            os.path.exists(index_file)
            and
            os.path.exists(metadata_file)
        ):

            document_indexes.append(
                index_directory
            )


    if not document_indexes:

        raise HTTPException(
            status_code=404,
            detail="No document indexes found."
        )


    # -----------------------------------------
    # 6. Search every document index
    # -----------------------------------------

    all_results = []


    for index_directory in document_indexes:

        try:

            vector_store = (
                FAISSVectorStore.load(
                    index_directory
                )
            )

            results = vector_store.search(
                query_embedding,
                top_k=request.top_k
            )

            all_results.extend(
                results
            )

        except Exception as error:

            print(
                f"Skipping index "
                f"{index_directory}: {error}"
            )


    # -----------------------------------------
    # 7. Sort all results by similarity
    # -----------------------------------------

    all_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    # -----------------------------------------
    # 8. Keep top K overall results
    # -----------------------------------------

    all_results = all_results[
        :request.top_k
    ]


    # -----------------------------------------
    # 9. Prepare sources
    # -----------------------------------------

    sources = []


    for result in all_results:

        metadata = result[
            "metadata"
        ]

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

            "similarity": result[
                "score"
            ],

            "text": metadata.get(
                "text"
            )

        })


    # -----------------------------------------
    # 10. Return response
    # -----------------------------------------

    return {

        "question": request.question,

        "results": sources,

        "count": len(sources),

        "documents_searched": len(
            document_indexes
        )

    }