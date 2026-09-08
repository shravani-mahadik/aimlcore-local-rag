import os
import numpy as np

from backend.app.services.retrieval.vector_store import (
    FAISSVectorStore
)


INDEX_DIR = "indexes/test_index"


print("\n===== FAISS PERSISTENCE TEST =====")


# -----------------------------------------
# 1. Create sample embeddings
# -----------------------------------------

print("\n[1] Creating sample embeddings...")

embeddings = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
], dtype="float32")


metadata = [
    {
        "chunk_id": "chunk_0",
        "page": 1,
        "text": "Annual leave policy."
    },
    {
        "chunk_id": "chunk_1",
        "page": 2,
        "text": "Employee onboarding process."
    },
    {
        "chunk_id": "chunk_2",
        "page": 3,
        "text": "Invoice submission procedure."
    }
]


# -----------------------------------------
# 2. Create vector store
# -----------------------------------------

print("[2] Creating FAISS vector store...")

store = FAISSVectorStore(
    dimension=3
)


store.add(
    embeddings,
    metadata
)


print(
    f"Vectors before saving: {store.count()}"
)


# -----------------------------------------
# 3. Save index
# -----------------------------------------

print("\n[3] Saving FAISS index...")

store.save(
    INDEX_DIR
)


# -----------------------------------------
# 4. Check saved files
# -----------------------------------------

index_file = os.path.join(
    INDEX_DIR,
    "index.faiss"
)

metadata_file = os.path.join(
    INDEX_DIR,
    "metadata.json"
)


assert os.path.exists(index_file)

assert os.path.exists(metadata_file)


print("FAISS files saved successfully.")


# -----------------------------------------
# 5. Load index
# -----------------------------------------

print("\n[4] Loading FAISS index...")

loaded_store = FAISSVectorStore.load(
    INDEX_DIR
)


print(
    f"Vectors after loading: "
    f"{loaded_store.count()}"
)


# -----------------------------------------
# 6. Search loaded index
# -----------------------------------------

print("\n[5] Searching loaded index...")


query = np.array(
    [1.0, 0.0, 0.0],
    dtype="float32"
)


results = loaded_store.search(
    query,
    top_k=2
)


# -----------------------------------------
# 7. Display results
# -----------------------------------------

print("\n===== SEARCH RESULTS =====")


for rank, result in enumerate(
    results,
    start=1
):

    metadata_item = result["metadata"]

    print("\n-------------------------")

    print(
        f"Rank: {rank}"
    )

    print(
        f"Similarity: "
        f"{result['score']:.4f}"
    )

    print(
        f"Chunk: "
        f"{metadata_item['chunk_id']}"
    )

    print(
        f"Page: "
        f"{metadata_item['page']}"
    )

    print(
        f"Text: "
        f"{metadata_item['text']}"
    )


# -----------------------------------------
# 8. Verify results
# -----------------------------------------

assert loaded_store.count() == 3

assert len(results) == 2

assert (
    results[0]["metadata"]["chunk_id"]
    == "chunk_0"
)


print("\n===== SUCCESS =====")

print(
    "FAISS index was successfully "
    "saved, loaded and searched."
)