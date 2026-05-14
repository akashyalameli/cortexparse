import uuid

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from graph.workflow import app_workflow


router = APIRouter()


@router.post("/document/upload")
async def upload_document(
    template_id: str,
    file: UploadFile = File(...)
):

    workflow_id = str(uuid.uuid4())

    initial_state = {
        "session_id": str(uuid.uuid4()),
        "workflow_id": workflow_id,

        "document_id": str(uuid.uuid4()),
        "document_path": file.filename,

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
        "status": result["workflow_status"]
    }
