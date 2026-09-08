from backend.app.services.chunking.chunker import chunk_text


sample_text = """
Artificial Intelligence is a field of computer science.
Machine learning allows computers to learn from data.
Natural language processing helps computers understand human language.
Retrieval Augmented Generation combines information retrieval
with language generation.
A RAG system retrieves relevant information from documents
before generating an answer.
"""


chunks = chunk_text(
    text=sample_text,
    document_id="document_001",
    chunk_size=20,
    overlap=5,
    page=1,
    section="Introduction"
)


print("\n===== METADATA CHUNKING TEST =====")

for chunk in chunks:

    print(f"\n--- Chunk {chunk.chunk_index} ---")

    print(f"Chunk ID: {chunk.chunk_id}")
    print(f"Document ID: {chunk.document_id}")
    print(f"Page: {chunk.page}")
    print(f"Section: {chunk.section}")
    print(f"Token count: {chunk.token_count}")

    print(f"Text: {chunk.text}")


print("\n===== SUCCESS =====")
print(f"Total chunks: {len(chunks)}")