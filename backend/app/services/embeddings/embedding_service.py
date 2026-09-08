from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:
    """
    Creates embeddings for document chunks
    and user queries.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_texts(
        self,
        texts: list[str]
    ) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        """

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings

    def embed_query(
        self,
        query: str
    ) -> np.ndarray:
        """
        Generate an embedding for a user question.
        """

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding