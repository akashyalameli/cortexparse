import uuid

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import Query
from fastapi import UploadFile

from pathlib import Path
from typing import Literal

from graph.workflow import app_workflow
from shared.document_storage import upload_document as upload_document_to_storage
from shared.template_storage import SUPPORTED_TEMPLATE_NAMES
from shared.template_storage import TemplateNotFoundError


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
    template_name: Literal[
        "logo",
        "pan",
        "aadhaar",
        "form",
        "prescription",
        "receipt",
        "invoice",
    ] = Query("logo"),
    response_mode: Literal[
        "sync",
        "async",
    ] = Query("sync"),
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
    print("ENTERED /upload API ROUTE")

    if template_name not in SUPPORTED_TEMPLATE_NAMES:

        raise HTTPException(
            status_code=400,
            detail="Unsupported template_name"
        )
    
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

        "template_id": template_name,
        "template_name": template_name,
        "template_schema": {},
        "document_type": "unknown",
        "response_mode": response_mode,

        "selected_model": "",

        "extracted_data": {},
        "validated_data": {},
        "corrected_data": {},

        "field_confidence_scores": {},
        "overall_confidence_score": 0.0,
        "missing_required_fields": [],
        "low_confidence_fields": [],
        "response_payload": {},

        "retry_count": 0,
        "max_retries": 3,

        "requires_human_review": False,
        "workflow_status": "STARTED",

        "telemetry": {}
    }

    try:

        result = app_workflow.invoke(initial_state)

    except TemplateNotFoundError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        ) from ex

    response = {
        "workflow_id": workflow_id,
        "status": result["workflow_status"],
        "confidence": result["overall_confidence_score"],
        "retry_count": result["retry_count"],
        "document_type": result["document_type"],
        "template_name": result["template_name"],
        "response_mode": result["response_mode"],
        "missing_required_fields": result.get("missing_required_fields", []),
        "low_confidence_fields": result.get("low_confidence_fields", []),
        "requires_human_review": result.get("requires_human_review", False),
    }

    if response_mode == "async":
        return response

    return {
        **response,
        "extracted_data": result.get(
            "response_payload",
            {}
        ).get("extracted_data")
    }
