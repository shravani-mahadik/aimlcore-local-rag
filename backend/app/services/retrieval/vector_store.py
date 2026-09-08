import faiss
import numpy as np
import json
import os


class FAISSVectorStore:
    """
    Local FAISS vector store for semantic search.
    """

    def __init__(self, dimension: int):
        self.dimension = dimension

        # Inner Product + normalized vectors
        # gives cosine similarity.
        self.index = faiss.IndexFlatIP(dimension)

        self.metadata = []

    def add(
        self,
        embeddings: np.ndarray,
        metadata: list[dict]
    ):
        """
        Add embeddings and their metadata to FAISS.
        """

        if len(embeddings) != len(metadata):
            raise ValueError(
                "Number of embeddings must match metadata."
            )

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

        self.metadata.extend(metadata)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5
    ):
        """
        Search for the most similar vectors.
        """

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, self.index.ntotal)
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            results.append({
                "score": float(score),
                "metadata": self.metadata[index]
            })

        return results

    def count(self) -> int:
        """
        Return number of stored vectors.
        """

        return self.index.ntotal
    def save(self, directory: str):
        """
        Save FAISS index and metadata to disk.
        """

        os.makedirs(
            directory,
            exist_ok=True
        )

        index_path = os.path.join(
            directory,
            "index.faiss"
        )

        metadata_path = os.path.join(
            directory,
            "metadata.json"
        )

        # Save FAISS index
        faiss.write_index(
            self.index,
            index_path
        )

        # Save chunk metadata
        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.metadata,
                file,
                ensure_ascii=False,
                indent=2
            )

        print(
            f"FAISS index saved to: {index_path}"
        )


    @classmethod
    def load(cls, directory: str):
        """
        Load FAISS index and metadata from disk.
        """

        index_path = os.path.join(
            directory,
            "index.faiss"
        )

        metadata_path = os.path.join(
            directory,
            "metadata.json"
        )

        # Load FAISS index
        index = faiss.read_index(
            index_path
        )

        # Load metadata
        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as file:

            metadata = json.load(file)

        # Create vector store
        store = cls(
            dimension=index.d
        )

        store.index = index
        store.metadata = metadata

        return store