from typing import TypedDict


class WorkflowState(TypedDict):

    session_id: str
    workflow_id: str

    document_id: str
    document_path: str

    template_id: str
    document_type: str

    selected_model: str

    extracted_data: dict
    validated_data: dict
    corrected_data: dict

    field_confidence_scores: dict
    overall_confidence_score: float

    retry_count: int
    max_retries: int

    requires_human_review: bool
    workflow_status: str

    telemetry: dict
