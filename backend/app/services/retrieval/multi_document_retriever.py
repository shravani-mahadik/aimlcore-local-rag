import os

from backend.app.services.embeddings.embedding_service import (
    EmbeddingService
)

from backend.app.services.retrieval.vector_store import (
    FAISSVectorStore
)


class MultiDocumentRetriever:
    """
    Searches across all indexed documents.
    """

    def __init__(
        self,
        indexes_directory: str = "data/indexes"
    ):

        self.indexes_directory = indexes_directory

        self.embedding_service = (
            EmbeddingService()
        )

    def _get_index_directories(self):

        if not os.path.exists(
            self.indexes_directory
        ):
            return []

        directories = []

        for name in os.listdir(
            self.indexes_directory
        ):

            path = os.path.join(
                self.indexes_directory,
                name
            )

            if not os.path.isdir(path):
                continue

            index_file = os.path.join(
                path,
                "index.faiss"
            )

            metadata_file = os.path.join(
                path,
                "metadata.json"
            )

            if (
                os.path.exists(index_file)
                and os.path.exists(metadata_file)
            ):
                directories.append(path)

        return directories

    def search(
        self,
        question: str,
        top_k: int = 5
    ):

        # -----------------------------------------
        # 1. Create query embedding
        # -----------------------------------------

        query_embedding = (
            self.embedding_service.embed_texts(
                [question]
            )
        )

        all_results = []

        # -----------------------------------------
        # 2. Search every document index
        # -----------------------------------------

        for index_directory in (
            self._get_index_directories()
        ):

            try:

                vector_store = (
                    FAISSVectorStore.load(
                        index_directory
                    )
                )

                results = vector_store.search(
                    query_embedding,
                    top_k=top_k
                )

                all_results.extend(
                    results
                )

            except Exception as error:

                print(
                    f"Could not load index "
                    f"{index_directory}: {error}"
                )

        # -----------------------------------------
        # 3. Sort by similarity
        # -----------------------------------------

        all_results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # -----------------------------------------
        # 4. Return global top-k
        # -----------------------------------------

        return all_results[:top_k]