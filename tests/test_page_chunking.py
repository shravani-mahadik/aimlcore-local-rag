from backend.app.services.ingestion.document_parser import extract_pdf_pages
from backend.app.services.chunking.chunker import chunk_text


PDF_PATH = r"data\sample.pdf"
DOCUMENT_ID = "sample_document_001"


try:
    pages = extract_pdf_pages(PDF_PATH)

    all_chunks = []

    for page_data in pages:

        page_number = page_data["page"]
        page_text = page_data["text"]

        page_chunks = chunk_text(
            text=page_text,
            document_id=DOCUMENT_ID,
            chunk_size=600,
            overlap=100,
            page=page_number
        )

        all_chunks.extend(page_chunks)

    print("\n===== PAGE-AWARE CHUNKING TEST =====")

    print(f"Pages processed: {len(pages)}")
    print(f"Total chunks: {len(all_chunks)}")

    for chunk in all_chunks:

        print("\n-------------------------")

        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Page: {chunk.page}")
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"Word count: {chunk.token_count}")
        print(f"Preview: {chunk.text[:150]}...")

    print("\n===== SUCCESS =====")


except Exception as e:

    print("\n===== ERROR =====")
    print(e)