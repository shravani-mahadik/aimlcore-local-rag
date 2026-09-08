from backend.app.services.ingestion.document_parser import extract_text
from backend.app.services.chunking.chunker import chunk_text


PDF_PATH = r"data\sample.pdf"
DOCUMENT_ID = "sample_document_001"


try:
    # Step 1: Extract text from PDF
    text = extract_text(PDF_PATH)

    # Step 2: Split extracted text into chunks
    chunks = chunk_text(
        text=text,
        document_id=DOCUMENT_ID,
        chunk_size=600,
        overlap=100
    )

    print("\n===== PDF → CHUNKING TEST =====")
    print(f"Document ID: {DOCUMENT_ID}")
    print(f"Total characters extracted: {len(text)}")
    print(f"Total chunks created: {len(chunks)}")

    print("\n===== FIRST FEW CHUNKS =====")

    for chunk in chunks[:5]:
        print(f"\nChunk ID: {chunk.chunk_id}")
        print(f"Page: {chunk.page}")
        print(f"Section: {chunk.section}")
        print(f"Word count: {chunk.token_count}")
        print(f"Text preview: {chunk.text[:150]}...")

    print("\n===== SUCCESS =====")

except Exception as e:
    print("\n===== ERROR =====")
    print(e)