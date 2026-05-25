import uuid

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from pathlib import Path

from graph.workflow import app_workflow
from shared.document_storage import upload_document as upload_document_to_storage


router = APIRouter()

SUPPORTED_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
}

SUPPORTED_EXTENSIONS = {
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
}

SUPPORTED_FILE_ACCEPT = ".pdf,.png,.jpg,.jpeg,application/pdf,image/png,image/jpeg"


def is_supported_file(file: UploadFile) -> bool:

    content_type = (file.content_type or "").lower()
    suffix = Path(file.filename or "").suffix.lower()

    return content_type in SUPPORTED_TYPES or suffix in SUPPORTED_EXTENSIONS


@router.post("/document/upload")
async def upload_document(
    template_id: str,
    file: UploadFile = File(
        ...,
        description="Supported formats: PNG, JPG, JPEG, PDF",
        media_type=SUPPORTED_FILE_ACCEPT,
        json_schema_extra={
            "accept": SUPPORTED_FILE_ACCEPT,
            "contentMediaType": SUPPORTED_FILE_ACCEPT,
        },
    )
):
    
    if not is_supported_file(file):

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Supported formats: PNG, JPG, JPEG, PDF"
        )

    workflow_id = str(uuid.uuid4())

    temp_path = Path("tmp") / file.filename

    with open(temp_path, "wb") as buffer:

        content = await file.read()

        buffer.write(content)


    upload_document_to_storage(
        file.filename,
        str(temp_path)
    )

    initial_state = {
        "session_id": str(uuid.uuid4()),
        "workflow_id": workflow_id,

        "document_id": str(uuid.uuid4()),
        "document_path": str(temp_path),

        "template_id": template_id,
        "document_type": "unknown",

        "selected_model": "",

        "extracted_data": {},
        "validated_data": {},
        "corrected_data": {},

        "field_confidence_scores": {},
        "overall_confidence_score": 0.0,

        "retry_count": 0,
        "max_retries": 3,

        "requires_human_review": False,
        "workflow_status": "STARTED",

        "telemetry": {}
    }

    result = app_workflow.invoke(initial_state)

    return {
        "workflow_id": workflow_id,
        "status": result["workflow_status"],
        "confidence": result["overall_confidence_score"],
        "retry_count": result["retry_count"]
    }
