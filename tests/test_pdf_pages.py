from backend.app.services.ingestion.document_parser import extract_pdf_pages


PDF_PATH = r"data\sample.pdf"


try:

    pages = extract_pdf_pages(PDF_PATH)

    print("\n===== PDF PAGE EXTRACTION TEST =====")

    print(f"Total pages with text: {len(pages)}")

    for page in pages:

        print("\n-------------------------")

        print(f"Page number: {page['page']}")

        print(
            f"Characters: {len(page['text'])}"
        )

        print(
            f"Preview: {page['text'][:150]}..."
        )

    print("\n===== SUCCESS =====")


except Exception as e:

    print("\n===== ERROR =====")
    print(e)