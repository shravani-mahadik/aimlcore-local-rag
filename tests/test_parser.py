from backend.app.services.ingestion.document_parser import extract_text


file_path = r"data\sample.pdf"

try:
    text = extract_text(file_path)

    print("\n===== EXTRACTED TEXT =====\n")
    print(text)

    print("\n===== SUCCESS =====")
    print(f"Characters extracted: {len(text)}")

except Exception as e:
    print("\n===== ERROR =====")
    print(e)