import os

from backend.app.services.indexing.indexing_service import (
    IndexingService
)


PDF_PATH = r"data\sample.pdf"

DOCUMENT_ID = "sample_document_001"


print("\n========================================")
print("       DOCUMENT INDEXING TEST")
print("========================================")


# -----------------------------------------
# Check PDF
# -----------------------------------------

if not os.path.exists(PDF_PATH):

    raise FileNotFoundError(
        f"PDF not found: {PDF_PATH}"
    )


# -----------------------------------------
# Create indexing service
# -----------------------------------------

service = IndexingService()


# -----------------------------------------
# Index document
# -----------------------------------------

result = service.index_pdf(
    file_path=PDF_PATH,
    document_id=DOCUMENT_ID
)


# -----------------------------------------
# Display result
# -----------------------------------------

print("\n===== INDEXING RESULT =====")

print(
    f"Document ID: {result['document_id']}"
)

print(
    f"Pages: {result['pages']}"
)

print(
    f"Chunks: {result['chunks']}"
)

print(
    f"Vectors: {result['vectors']}"
)

print(
    f"Index directory: "
    f"{result['index_directory']}"
)


# -----------------------------------------
# Verify files
# -----------------------------------------

index_file = os.path.join(
    result["index_directory"],
    "index.faiss"
)

metadata_file = os.path.join(
    result["index_directory"],
    "metadata.json"
)


assert os.path.exists(
    index_file
)

assert os.path.exists(
    metadata_file
)


print("\n===== SUCCESS =====")

print(
    "Document successfully processed and indexed."
)