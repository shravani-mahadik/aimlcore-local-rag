import os
import hashlib
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.services.indexing.indexing_service import (
    IndexingService
)


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


UPLOAD_DIR = "data/uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".csv"
}


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # -----------------------------------------
    # 1. Validate filename
    # -----------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    filename = os.path.basename(
        file.filename
    )

    extension = os.path.splitext(
        filename
    )[1].lower()

    # -----------------------------------------
    # 2. Validate file type
    # -----------------------------------------

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Allowed: PDF, DOCX, TXT, MD, CSV."
            )
        )

    # -----------------------------------------
    # 3. Read file
    # -----------------------------------------

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # -----------------------------------------
    # 4. Calculate file hash
    # -----------------------------------------

    file_hash = hashlib.sha256(
        contents
    ).hexdigest()

    # -----------------------------------------
    # 5. Create safe stored filename
    # -----------------------------------------

    safe_filename = (
        f"{file_hash[:12]}_{filename}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        safe_filename
    )

    # -----------------------------------------
    # 6. Duplicate detection
    # -----------------------------------------

    if os.path.exists(file_path):

        return {
            "status": "duplicate",
            "message": "This document already exists.",
            "filename": filename,
            "file_hash": file_hash,
            "document_id": f"doc_{file_hash[:12]}"
        }

    # -----------------------------------------
    # 7. Save document
    # -----------------------------------------

    with open(
        file_path,
        "wb"
    ) as output_file:

        output_file.write(
            contents
        )

    # -----------------------------------------
    # 8. Generate document ID
    # -----------------------------------------

    document_id = (
        f"doc_{file_hash[:12]}"
    )

    # -----------------------------------------
    # 9. Index PDF automatically
    # -----------------------------------------

    if extension == ".pdf":

        try:

            indexing_service = IndexingService()

            indexing_result = (
                indexing_service.index_pdf(
                    file_path=file_path,
                    document_id=document_id
                )
            )

        except Exception as error:

            return {
                "status": "uploaded",
                "indexing_status": "failed",
                "filename": filename,
                "document_id": document_id,
                "error": str(error)
            }

    else:

        return {
            "status": "uploaded",
            "indexing_status": "pending",
            "filename": filename,
            "document_id": document_id,
            "message": (
                "File uploaded successfully. "
                "Indexing for this file type "
                "will be added next."
            )
        }

    # -----------------------------------------
    # 10. Return indexing result
    # -----------------------------------------

    return {
        "status": "indexed",
        "filename": filename,
        "document_id": document_id,
        "file_hash": file_hash,
        "size": len(contents),
        "file_type": extension,
        "pages": indexing_result["pages"],
        "chunks": indexing_result["chunks"],
        "vectors": indexing_result["vectors"],
        "index_directory": indexing_result[
            "index_directory"
        ]
    }


# =========================================================
# LIST DOCUMENTS
# =========================================================

@router.get("")
def list_documents():

    documents = []

    if not os.path.exists(UPLOAD_DIR):

        return {
            "documents": [],
            "count": 0
        }

    for filename in os.listdir(
        UPLOAD_DIR
    ):

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        if not os.path.isfile(
            file_path
        ):
            continue

        # Stored filename:
        # hash12_originalfilename.pdf

        if "_" not in filename:
            continue

        hash_part = filename[:12]

        document_id = (
            f"doc_{hash_part}"
        )

        original_filename = filename[13:]

        documents.append({
            "document_id": document_id,
            "filename": original_filename,
            "stored_filename": filename,
            "size": os.path.getsize(
                file_path
            )
        })

    return {
        "documents": documents,
        "count": len(documents)
    }


# =========================================================
# DELETE DOCUMENT
# =========================================================

@router.delete("/{document_id}")
def delete_document(
    document_id: str
):

    # -----------------------------------------
    # 1. Validate document ID
    # -----------------------------------------

    if not document_id.startswith(
        "doc_"
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid document ID."
        )

    hash_part = document_id.replace(
        "doc_",
        "",
        1
    )

    # -----------------------------------------
    # 2. Find uploaded file
    # -----------------------------------------

    uploaded_file = None

    if os.path.exists(
        UPLOAD_DIR
    ):

        for filename in os.listdir(
            UPLOAD_DIR
        ):

            if filename.startswith(
                hash_part + "_"
            ):

                uploaded_file = os.path.join(
                    UPLOAD_DIR,
                    filename
                )

                break

    # -----------------------------------------
    # 3. Find FAISS index
    # -----------------------------------------

    index_directory = os.path.join(
        "data",
        "indexes",
        document_id
    )

    # -----------------------------------------
    # 4. Check document existence
    # -----------------------------------------

    if (
        uploaded_file is None
        and not os.path.exists(
            index_directory
        )
    ):

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # -----------------------------------------
    # 5. Delete uploaded file
    # -----------------------------------------

    if uploaded_file is not None:

        os.remove(
            uploaded_file
        )

    # -----------------------------------------
    # 6. Delete FAISS index
    # -----------------------------------------

    if os.path.exists(
        index_directory
    ):

        shutil.rmtree(
            index_directory
        )

    # -----------------------------------------
    # 7. Return success
    # -----------------------------------------

    return {
        "status": "deleted",
        "document_id": document_id
    }